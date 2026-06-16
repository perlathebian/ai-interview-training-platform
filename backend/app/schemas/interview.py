from datetime import datetime

from pydantic import BaseModel


class InterviewSessionCreate(BaseModel):
    training_target_id: int
    mode: str = "text"


class InterviewStartResponse(BaseModel):
    session_id: int
    first_question: str


class InterviewSessionResponse(BaseModel):
    id: int
    training_target_id: int
    mode: str
    status: str
    overall_score: int | None
    started_at: datetime
    completed_at: datetime | None

    model_config = {
        "from_attributes": True
    }


class InterviewTurnCreate(BaseModel):
    answer: str


class InterviewTurnResponse(BaseModel):
    id: int
    turn_number: int
    question: str
    answer: str | None
    score: int | None
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class InterviewAnswerSubmit(BaseModel):
    answer: str

class InterviewAnswerResponse(BaseModel):
    evaluation: dict
    coaching: dict
    next_question: str