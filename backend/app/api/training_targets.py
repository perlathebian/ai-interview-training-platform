from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.training_target import TrainingTargetCreate, TrainingTargetResponse
from app.services.training_target_service import training_target_service


router = APIRouter(
    prefix="/training-targets",
    tags=["Training Targets"],
)


@router.post(
    "",
    response_model=TrainingTargetResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_training_target(
    target_data: TrainingTargetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    training_target = training_target_service.create_training_target(
        db=db,
        user_id=current_user.id,
        target_data=target_data,
    )

    return training_target


@router.get(
    "",
    response_model=list[TrainingTargetResponse],
)
def get_training_targets(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return training_target_service.get_training_targets_for_user(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/{training_target_id}",
    response_model=TrainingTargetResponse,
)
def get_training_target(
    training_target_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    training_target = training_target_service.get_training_target_for_user(
        db=db,
        training_target_id=training_target_id,
        user_id=current_user.id,
    )

    if training_target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training target not found",
        )

    return training_target