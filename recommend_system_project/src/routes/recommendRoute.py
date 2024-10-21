from fastapi import APIRouter, Body

from ..controller import recommendController
from ..models.recommendModels import RecommendationRequest, Recommendations
from ..validation import recommendValidation

router = APIRouter()

TAG_NAME = "recommend"


@router.post("/recommend", tags=[TAG_NAME], response_model=Recommendations)
async def recommend(request: RecommendationRequest = Body(...)):
    await recommendValidation.validate_recommend_request(request)

    return await recommendController.recommend(request)
