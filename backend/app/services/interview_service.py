from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.interview_session import InterviewSession
from app.models.interview_turn import InterviewTurn
from app.models.training_target import TrainingTarget
from app.schemas.interview import InterviewSessionCreate


class InterviewService:
    def create_session(
        self,
        db: Session,
        user_id: int,
        session_data: InterviewSessionCreate,
        training_target: TrainingTarget,
        resume_snapshot: dict | None = None,
        job_snapshot: dict | None = None,
        research_snapshot: dict | None = None,
        interview_plan_snapshot: dict | None = None,
    ) -> InterviewSession:
        session = InterviewSession(
            user_id=user_id,
            training_target_id=session_data.training_target_id,
            mode=session_data.mode,
            status="in_progress",
            resume_snapshot=resume_snapshot,
            job_snapshot=job_snapshot,
            research_snapshot=research_snapshot,
            interview_plan_snapshot=interview_plan_snapshot,
        )

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    def create_turn(
        self,
        db: Session,
        session_id: int,
        turn_number: int,
        question: str,
        turn_metadata: dict | None = None,
    ) -> InterviewTurn:
        turn = InterviewTurn(
            session_id=session_id,
            turn_number=turn_number,
            question=question,
            status="question_asked",
            turn_metadata=turn_metadata,
        )

        db.add(turn)
        db.commit()
        db.refresh(turn)

        return turn

    def get_session_for_user(
        self,
        db: Session,
        session_id: int,
        user_id: int,
    ) -> InterviewSession | None:
        return (
            db.query(InterviewSession)
            .filter(
                InterviewSession.id == session_id,
                InterviewSession.user_id == user_id,
            )
            .first()
        )
    
    def get_latest_unanswered_turn(
        self,
        db: Session,
        session_id: int,
    ) -> InterviewTurn | None:
        return (
            db.query(InterviewTurn)
            .filter(
                InterviewTurn.session_id == session_id,
                InterviewTurn.answer.is_(None),
            )
            .order_by(InterviewTurn.turn_number.desc())
            .first()
        )

    def get_turns_for_session(
        self,
        db: Session,
        session_id: int,
    ) -> list[InterviewTurn]:
        return (
            db.query(InterviewTurn)
            .filter(InterviewTurn.session_id == session_id)
            .order_by(InterviewTurn.turn_number.asc())
            .all()
        )

    def save_answer_and_feedback(
        self,
        db: Session,
        turn: InterviewTurn,
        answer: str,
        evaluation: dict,
        coaching: dict,
    ) -> InterviewTurn:
        turn.answer = answer
        turn.evaluation = evaluation
        turn.coaching = coaching
        turn.score = evaluation.get("score")
        turn.status = "completed"
        turn.answered_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(turn)

        return turn

    def save_answer_as_pending(
        self,
        db: Session,
        turn: InterviewTurn,
        answer: str,
    ) -> InterviewTurn:
        turn.answer = answer
        turn.status = "pending_evaluation"
        turn.answered_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(turn)

        return turn
    
    def mark_turn_evaluation_failed(
        self,
        db: Session,
        turn: InterviewTurn,
    ) -> InterviewTurn:
        turn.status = "evaluation_failed"

        db.commit()
        db.refresh(turn)

        return turn
    
    def get_sessions_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[InterviewSession]:
        return (
            db.query(InterviewSession)
            .filter(InterviewSession.user_id == user_id)
            .order_by(InterviewSession.started_at.desc())
            .all()
        )

interview_service = InterviewService()