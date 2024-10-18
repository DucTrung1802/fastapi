from typing import Annotated
from fastapi import APIRouter, Depends, Body

from ..models.recommendModels import *

router = APIRouter()

TAG_NAME = "recommend"


@router.post("/recommend_single", tags=[TAG_NAME], response_model=RecommendSingleOutput)
async def recommend_single(request: RecommendSingleInput = Body(...)):
    pass


@router.post("/recommend_combo", tags=[TAG_NAME], response_model=RecommendComboOutput)
async def recommend_combo(request: RecommendComboInput = Body(...)):
    pass
