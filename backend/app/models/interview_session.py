from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    training_target_id = Column(
        Integer,
        ForeignKey("training_targets.id"),
        nullable=False,
        index=True,
    )

    mode = Column(String(50), nullable=False, default="text")
    status = Column(String(50), nullable=False, default="in_progress")

    resume_snapshot = Column(JSON, nullable=True)
    job_snapshot = Column(JSON, nullable=True)
    research_snapshot = Column(JSON, nullable=True)
    interview_plan_snapshot = Column(JSON, nullable=True)

    overall_score = Column(Integer, nullable=True)
    final_report = Column(JSON, nullable=True)

    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="interview_sessions")
    training_target = relationship("TrainingTarget", back_populates="interview_sessions")
    turns = relationship(
        "InterviewTurn",
        back_populates="session",
        cascade="all, delete-orphan",
    )