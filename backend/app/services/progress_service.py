from collections import Counter

from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession
from app.models.user_progress import UserProgress


class ProgressService:
    def update_progress_for_user(
        self,
        db: Session,
        user_id: int,
    ) -> UserProgress:
        completed_sessions = (
            db.query(InterviewSession)
            .filter(
                InterviewSession.user_id == user_id,
                InterviewSession.status == "completed",
            )
            .all()
        )

        scores = []
        strengths = []
        weaknesses = []

        for session in completed_sessions:
            report = session.final_report or {}

            if report.get("overall_score") is not None:
                scores.append(report["overall_score"])

            strengths.extend(report.get("strengths", []))
            weaknesses.extend(report.get("weaknesses", []))

        average_score = (
            round(sum(scores) / len(scores), 2)
            if scores
            else 0
        )

        top_strengths = [
            item
            for item, _ in Counter(strengths).most_common(5)
        ]

        top_weaknesses = [
            item
            for item, _ in Counter(weaknesses).most_common(5)
        ]

        last_session_at = (
            completed_sessions[0].completed_at.isoformat()
            if completed_sessions
            else None
        )

        progress_data = {
            "average_score": average_score,
            "sessions_completed": len(completed_sessions),
            "top_strengths": top_strengths,
            "top_weaknesses": top_weaknesses,
            "last_session_at": last_session_at,
        }

        progress = (
            db.query(UserProgress)
            .filter(UserProgress.user_id == user_id)
            .first()
        )

        if progress is None:
            progress = UserProgress(
                user_id=user_id,
                progress_data=progress_data,
            )

            db.add(progress)
        else:
            progress.progress_data = progress_data

        db.commit()
        db.refresh(progress)

        return progress


progress_service = ProgressService()