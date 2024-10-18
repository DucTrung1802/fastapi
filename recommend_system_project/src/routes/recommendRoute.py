from typing import Annotated
from fastapi import APIRouter, Depends, Body

from ..models.recommendModels import *

router = APIRouter()

TAG_NAME = "recommend"


@router.post("/recommend", tags=[TAG_NAME], response_model=RecommendResponse)
async def recommend(request: RecommendRequest = Body(...)):
    mock_response = RecommendResponse(
        lcv_id=request.lcv_id,
        result=[
            RecommendationResult(
                similarity_score=0.95,
                recommend=[
                    RegimenRecommendation(
                        regimen_id=regimen.regimen_id,
                        sku=regimen.sku,
                        shots=[
                            ShotRecommendation(
                                order=shot.order,
                                recommended_date=shot.prefer_date,  # Just reusing preferred date as mock
                            )
                            for shot in regimen.shots
                        ],
                    )
                    for regimen in request.requested
                ],
            )
        ],
    )

    # Return mock response to match expected structure
    return mock_response
