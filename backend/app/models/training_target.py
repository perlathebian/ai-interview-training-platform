from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class TrainingTarget(Base):
    __tablename__ = "training_targets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    target_type = Column(String(50), nullable=False)
    company = Column(String(255), nullable=True)
    role = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=True)

    desired_companies = Column(JSON, nullable=True)
    focus_areas = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="training_targets")
    interview_sessions = relationship(
        "InterviewSession",
        back_populates="training_target",
        cascade="all, delete-orphan",
    )