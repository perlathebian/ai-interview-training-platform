from datetime import datetime

from pydantic import BaseModel


class TrainingTargetCreate(BaseModel):
    target_type: str

    company: str | None = None
    role: str

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

    model_config = {
        "from_attributes": True
    }