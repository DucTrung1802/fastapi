from pydantic import BaseModel, Field, RootModel
from typing import List, Optional
from datetime import date


# Request Models
class ShotRequest(BaseModel):
    order: int = Field(..., description="Shot order in the regimen")
    prefer_date: date = Field(..., description="Preferred date for the shot")


class RegimenRequest(BaseModel):
    regimen_id: str = Field(..., description="ID of the regimen")
    sku: str = Field(..., description="Vaccine ID")
    shots: Optional[List[ShotRequest]] = Field(
        None, description="List of requested shots"
    )


class RecommendationRequest(BaseModel):
    lcv_id: int = Field(..., description="Patient ID", example=8)
    requested: List[RegimenRequest] = Field(
        ...,
        description="List of requested regimens and shots",
        example=[
            {"regimen_id": "regimen 1", "sku": "HEXAXIM"},
            {"regimen_id": "regimen 2", "sku": "ROTATEQ 2ML"},
        ],
    )


# Response Models
class ShotRecommendation(BaseModel):
    order: int = Field(..., description="Recommended shot order")
    recommended_date: date = Field(..., description="Recommended date for the shot")


class RegimenRecommendation(BaseModel):
    regimen_id: str = Field(..., description="Recommended regimen ID")
    sku: str = Field(..., description="Recommended vaccine SKU")
    shots: List[ShotRecommendation] = Field(
        ..., description="Recommended shots with dates"
    )


class RecommendationResult(BaseModel):
    similarity_score: float = Field(
        ...,
        description="Score indicating similarity between request and recommendation",
    )
    recommend: List[RegimenRecommendation] = Field(
        ..., description="List of regimen recommendations"
    )


class RecommendationResponse(BaseModel):
    lcv_id: str = Field(..., description="Patient ID")
    result: List[RecommendationResult] = Field(
        ..., description="List of recommendation results"
    )


class Recommendations(RootModel[List[RecommendationResponse]]):
    pass
