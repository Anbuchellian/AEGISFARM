from datetime import datetime
from pydantic import BaseModel, Field


class DetectionOut(BaseModel):
    id: int
    species: str
    confidence: float
    zone: str
    direction: str
    threat_state: str
    detected_at: datetime

    model_config = {"from_attributes": True}


class InterventionOut(BaseModel):
    id: int
    detection_id: int
    strategy: str
    outcome: str
    response_time_ms: int
    notes: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ValidationCreate(BaseModel):
    tester: str
    role: str
    task: str
    feedback: str
    change_made: str = ""


class ValidationOut(ValidationCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class EventScenario(BaseModel):
    species: str = "wild_boar"
    confidence: float = Field(default=0.94, ge=0, le=1)
    zone: str = "North-West"
    direction: str = "South-East"
    threat_state: str = "Approaching Crop"
    response_mode: str = "auto"
    simulate_no_response: bool = False
