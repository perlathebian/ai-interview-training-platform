from datetime import datetime

from pydantic import BaseModel


class ResumeCreate(BaseModel):
    raw_text: str


class ResumeUpdate(BaseModel):
    raw_text: str | None = None


class ResumeResponse(BaseModel):
    id: int

    raw_text: str
    parsed_summary: str | None

    extracted_skills: list | None
    extracted_projects: list | None

    is_active: bool
    is_deleted: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }