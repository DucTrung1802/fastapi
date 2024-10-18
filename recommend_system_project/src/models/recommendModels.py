from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RecommendSingleInput(BaseModel):
    regimen_id: str
    patient_id: str
    lcvid: str
    vaccine_id: str
    sku: str
    date: Optional[datetime] = None
    vaccine_shot: Optional[int] = None


class RecommendSingleOutput(BaseModel):
    regimen_name: str
    vaccine_name: str
    vaccine_shot_order: int
    days_between: int
    recommended_date: datetime
    similarity_score: float


class RecommendComboInput(BaseModel):
    regimen_id: str
    combo_id: str
    patient_id: str
    lcvid: str
    date: Optional[datetime] = None
    vaccine_shot_order: Optional[int] = None


class RecommendComboOutput(BaseModel):
    regimen_name: str
    combo_name: str
    vaccine_name: str
    vaccine_shot_order: int
    days_between: int
    recommended_date: datetime
    similarity_score: float
