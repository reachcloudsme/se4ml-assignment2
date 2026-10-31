from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ScoreResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str
    anomaly_score: float
    threshold: float
    is_anomaly: bool
    points: int = Field(ge=5)


class ErrorResponse(BaseModel):
    detail: str


class ServiceStatus(BaseModel):
    service: str
    status: Literal["no_data", "insufficient_data", "error"]
    points: int | None = None
    error: str | None = None


class ScoreAllResponse(BaseModel):
    namespace: str
    results: list[ScoreResult | ServiceStatus]
