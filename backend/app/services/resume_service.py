from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate


class ResumeService:
    def create_resume(self, db: Session, user_id: int, resume_data: ResumeCreate) -> Resume:
        resume = Resume(
            user_id=user_id,
            raw_text=resume_data.raw_text,
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume

    def get_active_resume_for_user(self, db: Session, user_id: int) -> Resume | None:
        return (
            db.query(Resume)
            .filter(
                Resume.user_id == user_id,
                Resume.is_active.is_(True),
                Resume.is_deleted.is_(False),
            )
            .order_by(Resume.created_at.desc())
            .first()
        )

    def update_resume(
        self,
        db: Session,
        resume: Resume,
        resume_data: ResumeUpdate,
    ) -> Resume:
        if resume_data.raw_text is not None:
            resume.raw_text = resume_data.raw_text

        db.commit()
        db.refresh(resume)

        return resume

    def soft_delete_resume(self, db: Session, resume: Resume) -> Resume:
        resume.is_active = False
        resume.is_deleted = True

        db.commit()
        db.refresh(resume)

        return resume


resume_service = ResumeService()