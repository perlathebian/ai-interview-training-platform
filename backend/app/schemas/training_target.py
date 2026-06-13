from datetime import datetime

from pydantic import BaseModel, Field


class TrainingTargetCreate(BaseModel):
    target_type: str = Field(..., examples=["specific_job"])
    company: str | None = None
    role: str = Field(..., min_length=2)
    job_description: str | None = None
    desired_companies: list[str] | None = None
    focus_areas: list[str] | None = None


class TrainingTargetUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    job_description: str | None = None
    desired_companies: list[str] | None = None
    focus_areas: list[str] | None = None


class TrainingTargetResponse(BaseModel):
    id: int
    target_type: str
    company: str | None
    role: str
    job_description: str | None
    desired_companies: list[str] | None
    focus_areas: list[str] | None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }