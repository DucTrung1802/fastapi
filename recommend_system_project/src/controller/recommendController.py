from ..services import recommendService
from ..models.recommendModels import RecommendationRequest


async def recommend(request: RecommendationRequest):
    return await recommendService.recommend(request)
