from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    raw_text = Column(Text, nullable=False)
    parsed_summary = Column(Text, nullable=True)

    extracted_skills = Column(JSON, nullable=True)
    extracted_projects = Column(JSON, nullable=True)
    extracted_experience = Column(JSON, nullable=True)
    extracted_education = Column(JSON, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user = relationship("User", back_populates="resumes")