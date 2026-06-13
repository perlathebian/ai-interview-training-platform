from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.schemas.resume import ResumeCreate, ResumeUpdate
from app.services.resume_parser import resume_parser

class ResumeService:
    def create_resume(self, db: Session, user_id: int, resume_data: ResumeCreate) -> Resume:
        existing_active_resume = self.get_active_resume_for_user(db, user_id)

        if existing_active_resume:
            existing_active_resume.is_active = False

        parsed_resume = resume_parser.parse(resume_data.raw_text)

        resume = Resume(
            user_id=user_id,
            raw_text=resume_data.raw_text,
            parsed_summary=parsed_resume["parsed_summary"],
            extracted_skills=parsed_resume["extracted_skills"],
            extracted_projects=parsed_resume["extracted_projects"],
            extracted_experience=parsed_resume["extracted_experience"],
            extracted_education=parsed_resume["extracted_education"],
            is_active=True,
            is_deleted=False,
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

    def get_resume_for_user(
        self,
        db: Session,
        resume_id: int,
        user_id: int,
    ) -> Resume | None:
        return (
            db.query(Resume)
            .filter(
                Resume.id == resume_id,
                Resume.user_id == user_id,
            )
            .first()
        )

    def update_resume(
        self,
        db: Session,
        resume: Resume,
        resume_data: ResumeUpdate,
    ) -> Resume:
        if resume_data.raw_text is not None:
            parsed_resume = resume_parser.parse(resume_data.raw_text)

            resume.raw_text = resume_data.raw_text
            resume.parsed_summary = parsed_resume["parsed_summary"]
            resume.extracted_skills = parsed_resume["extracted_skills"]
            resume.extracted_projects = parsed_resume["extracted_projects"]
            resume.extracted_experience = parsed_resume["extracted_experience"]
            resume.extracted_education = parsed_resume["extracted_education"]

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