from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.interview import InterviewSessionCreate, InterviewStartResponse
from app.services.agents import interviewer_agent, planner_agent, research_agent
from app.services.interview_service import interview_service
from app.services.resume_service import resume_service
from app.services.training_target_service import training_target_service


router = APIRouter(
    prefix="/interviews",
    tags=["Interviews"],
)


@router.post(
    "/start",
    response_model=InterviewStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_interview(
    session_data: InterviewSessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    training_target = training_target_service.get_training_target_for_user(
        db=db,
        training_target_id=session_data.training_target_id,
        user_id=current_user.id,
    )

    if training_target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Training target not found",
        )

    active_resume = resume_service.get_active_resume_for_user(
        db=db,
        user_id=current_user.id,
    )

    resume_snapshot = None

    if active_resume:
        resume_snapshot = {
            "resume_id": active_resume.id,
            "parsed_summary": active_resume.parsed_summary,
            "extracted_skills": active_resume.extracted_skills,
            "extracted_projects": active_resume.extracted_projects,
            "extracted_experience": active_resume.extracted_experience,
            "extracted_education": active_resume.extracted_education,
        }

    job_snapshot = {
        "training_target_id": training_target.id,
        "target_type": training_target.target_type,
        "company": training_target.company,
        "role": training_target.role,
        "job_description": training_target.job_description,
        "desired_companies": training_target.desired_companies,
        "focus_areas": training_target.focus_areas,
    }

    research_snapshot = research_agent.research_target(
        company=training_target.company,
        role=training_target.role,
        job_description=training_target.job_description,
    )

    interview_plan_snapshot = planner_agent.create_plan(
        resume_snapshot=resume_snapshot,
        job_snapshot=job_snapshot,
        research_snapshot=research_snapshot,
    )

    first_question_data = interviewer_agent.generate_first_question(
        resume_snapshot=resume_snapshot,
        job_snapshot=job_snapshot,
        interview_plan=interview_plan_snapshot,
    )

    session = interview_service.create_session(
        db=db,
        user_id=current_user.id,
        session_data=session_data,
        training_target=training_target,
        resume_snapshot=resume_snapshot,
        job_snapshot=job_snapshot,
        research_snapshot=research_snapshot,
        interview_plan_snapshot=interview_plan_snapshot,
    )

    interview_service.create_turn(
        db=db,
        session_id=session.id,
        turn_number=1,
        question=first_question_data["question"],
        turn_metadata={
            "difficulty": first_question_data["difficulty"],
            "focus_area": first_question_data["focus_area"],
            "expected_signal": first_question_data["expected_signal"],
        },
    )

    return InterviewStartResponse(
        session_id=session.id,
        first_question=first_question_data["question"],
    )