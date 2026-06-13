from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.resume import ResumeCreate, ResumeResponse
from app.services.resume_service import resume_service


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"],
)


@router.post(
    "",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = resume_service.create_resume(
        db=db,
        user_id=current_user.id,
        resume_data=resume_data,
    )

    return resume


@router.get(
    "/me",
    response_model=ResumeResponse,
)
def get_my_resume(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = resume_service.get_active_resume_for_user(
        db=db,
        user_id=current_user.id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resume found",
        )

    return resume


@router.delete(
    "/{resume_id}",
    response_model=ResumeResponse,
)
def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = resume_service.get_resume_for_user(
        db=db,
        resume_id=resume_id,
        user_id=current_user.id,
    )

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    deleted_resume = resume_service.soft_delete_resume(
        db=db,
        resume=resume,
    )

    return deleted_resume