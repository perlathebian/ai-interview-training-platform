from sqlalchemy.orm import Session

from app.models.training_target import TrainingTarget
from app.schemas.training_target import TrainingTargetCreate


class TrainingTargetService:
    def create_training_target(
        self,
        db: Session,
        user_id: int,
        target_data: TrainingTargetCreate,
    ) -> TrainingTarget:
        training_target = TrainingTarget(
            user_id=user_id,
            target_type=target_data.target_type,
            company=target_data.company,
            role=target_data.role,
            job_description=target_data.job_description,
            desired_companies=target_data.desired_companies,
            focus_areas=target_data.focus_areas,
        )

        db.add(training_target)
        db.commit()
        db.refresh(training_target)

        return training_target

    def get_training_targets_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[TrainingTarget]:
        return (
            db.query(TrainingTarget)
            .filter(TrainingTarget.user_id == user_id)
            .order_by(TrainingTarget.created_at.desc())
            .all()
        )

    def get_training_target_for_user(
        self,
        db: Session,
        training_target_id: int,
        user_id: int,
    ) -> TrainingTarget | None:
        return (
            db.query(TrainingTarget)
            .filter(
                TrainingTarget.id == training_target_id,
                TrainingTarget.user_id == user_id,
            )
            .first()
        )


training_target_service = TrainingTargetService()