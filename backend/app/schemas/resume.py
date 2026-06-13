from datetime import datetime

from pydantic import BaseModel, Field


class ResumeCreate(BaseModel):
    raw_text: str = Field(..., min_length=50)


class ResumeUpdate(BaseModel):
    raw_text: str | None = Field(default=None, min_length=50)


class ResumeResponse(BaseModel):
    id: int

    raw_text: str
    parsed_summary: str | None

    extracted_skills: list | None
    extracted_projects: list | None
    extracted_experience: list | None
    extracted_education: list | None

    is_active: bool
    is_deleted: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }