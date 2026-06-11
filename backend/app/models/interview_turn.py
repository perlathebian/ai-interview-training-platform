from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class InterviewTurn(Base):
    __tablename__ = "interview_turns"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("interview_sessions.id"),
        nullable=False,
        index=True,
    )

    turn_number = Column(Integer, nullable=False)

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)

    evaluation = Column(JSON, nullable=True)
    coaching = Column(JSON, nullable=True)

    score = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default="question_asked")

    turn_metadata = Column(JSON, nullable=True)

    answered_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    session = relationship("InterviewSession", back_populates="turns")