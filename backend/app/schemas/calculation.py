from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# Pydantic models for calculation requests and responses
class EvaluateRequest(BaseModel):
    expression: str


class EvaluateResponse(BaseModel):
    expression: str
    result: float


class CalculationHistoryResponse(BaseModel):
    id: UUID
    expression: str
    result: str
    created_at: datetime

    class Config:
        from_attributes = True
