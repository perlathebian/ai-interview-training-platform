class PlannerAgent:
    def create_plan(
        self,
        resume_snapshot: dict | None,
        job_snapshot: dict,
        research_snapshot: dict | None = None,
    ) -> dict:
        role = job_snapshot.get("role", "the target role")

        return {
            "difficulty": "medium",
            "focus_areas": [
                "background",
                "role alignment",
                "technical fundamentals",
            ],
            "question_count": 10,
            "strategy": (
                f"Start by understanding the candidate's background, then assess fit for {role}."
            ),
            "research_confidence": research_snapshot.get("confidence") if research_snapshot else "low",
        }


planner_agent = PlannerAgent()