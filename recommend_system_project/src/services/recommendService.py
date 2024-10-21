from datetime import datetime
from neo4j import GraphDatabase
from collections import defaultdict

from ..utils.exceptions import BadRequestException

from ..config import configuration, environment
from ..models.recommendModels import *


target_database = "neo4j"


class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def query(self, query, parameters=None, db=None):
        with (
            self.driver.session(database=db)
            if db is not None
            else self.driver.session()
        ) as session:
            try:
                result = session.run(query, parameters)
                # Immediately collect all records to prevent ResultConsumedError
                return [dict(record) for record in result]
            except Exception as e:
                print(f"Query failed: {e}")
                return []

    def close(self):
        self.driver.close()


def convert_neo4j_date(neo4j_date):
    if isinstance(neo4j_date, dict):
        year = neo4j_date["_Date__year"]
        month = neo4j_date["_Date__month"]
        day = neo4j_date["_Date__day"]
    else:
        year = neo4j_date.year
        month = neo4j_date.month
        day = neo4j_date.day

    return date(year, month, day).isoformat()


def transform_data(input_data):
    # Initialize a nested dictionary to store the results
    result_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    # Process the input data
    for entry in input_data:
        lcv_id = entry["lcv_id"]
        similarity_score = entry["similarityScore"]

        # Create a new entry for the similarity score if it doesn't exist
        if similarity_score not in result_dict[lcv_id]:
            result_dict[lcv_id][similarity_score] = {
                "similarity_score": similarity_score,
                "recommend": [],
            }

        # Append the regimen information
        regimen_info = {
            "regimen_id": entry["regimen_id"],
            "sku": entry["vaccine_sku"],
            "shots": [
                {
                    "order": entry["vaccine_shot_injection_order"],
                    "recommended_date": convert_neo4j_date(entry["recommended_date"]),
                }
            ],
        }

        # Check if the regimen already exists in the recommend list
        existing_regimen = next(
            (
                reg
                for reg in result_dict[lcv_id][similarity_score]["recommend"]
                if reg["regimen_id"] == regimen_info["regimen_id"]
            ),
            None,
        )
        if existing_regimen:
            existing_regimen["shots"].append(
                {
                    "order": entry["vaccine_shot_injection_order"],
                    "recommended_date": convert_neo4j_date(entry["recommended_date"]),
                }
            )
        else:
            result_dict[lcv_id][similarity_score]["recommend"].append(regimen_info)

    # Convert the result_dict to the desired output format
    output_list = []
    for lcv_id, scores in result_dict.items():
        lcv_result = {"lcv_id": str(lcv_id), "result": []}

        for score, data in scores.items():
            lcv_result["result"].append(data)

        output_list.append(lcv_result)

    return output_list


def transform_to_models(data: List[dict]) -> List[RecommendationResponse]:
    response = []
    for item in data:
        lcv_id = item["lcv_id"]
        result = []

        for res in item["result"]:
            similarity_score = res["similarity_score"]
            recommendations = []

            for rec in res["recommend"]:
                regimen_id = rec["regimen_id"]
                sku = rec["sku"]
                shots = [
                    ShotRecommendation(
                        order=shot["order"], recommended_date=shot["recommended_date"]
                    )
                    for shot in rec["shots"]
                ]
                recommendations.append(
                    RegimenRecommendation(regimen_id=regimen_id, sku=sku, shots=shots)
                )

            result.append(
                RecommendationResult(
                    similarity_score=similarity_score, recommend=recommendations
                )
            )

        response.append(RecommendationResponse(lcv_id=lcv_id, result=result))

    return response


async def recommend(request: RecommendationRequest):
    neo4j_conn = Neo4jConnection(
        configuration.NEO4J_DB_URI,
        environment.NEO4J_DB_USERNAME,
        environment.NEO4J_DB_PASSWORD,
    )

    new_lcv_id = request.lcv_id

    if len(request.requested) == 0:
        raise BadRequestException

    regimenids = []
    vaccineskus = []
    start_dates = []

    for req in request.requested:
        regimenids.append(req.regimen_id)
        vaccineskus.append(req.sku)

        start_dates.append(datetime.today().date().isoformat())

    query = ""
    with open("query.txt", "r") as file:
        query = file.read()

    parameters = {
        "vaccineskus": vaccineskus,
        "regimenids": regimenids,
        "new_lcv_id": new_lcv_id,
        "start_dates": start_dates,
    }

    result = neo4j_conn.query(query, parameters, db=target_database)

    response = transform_to_models(transform_data(result))

    return response
