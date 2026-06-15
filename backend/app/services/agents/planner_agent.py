class PlannerAgent:
    def create_plan(
        self,
        resume_snapshot: dict | None,
        job_snapshot: dict,
        research_snapshot: dict | None = None,
    ) -> dict:
        role = job_snapshot.get("role", "target role")
        company = job_snapshot.get("company")
        focus_areas_from_target = job_snapshot.get("focus_areas") or []

        resume_skills = []
        resume_projects = []

        if resume_snapshot:
            resume_skills = resume_snapshot.get("extracted_skills") or []
            resume_projects = resume_snapshot.get("extracted_projects") or []

        focus_areas = self._build_focus_areas(
            role=role,
            resume_skills=resume_skills,
            target_focus_areas=focus_areas_from_target,
        )

        difficulty = self._infer_difficulty(role=role)

        return {
            "focus_areas": focus_areas,
            "difficulty": difficulty,
            "question_strategy": [
                {
                    "stage": "opening",
                    "goal": "Assess candidate background and communication clarity.",
                    "question_type": "behavioral",
                },
                {
                    "stage": "resume_deep_dive",
                    "goal": "Ask about projects, responsibilities, and technical decisions from the resume.",
                    "question_type": "technical_behavioral",
                },
                {
                    "stage": "role_alignment",
                    "goal": f"Evaluate fit for the {role} role.",
                    "question_type": "role_specific",
                },
                {
                    "stage": "weakness_probe",
                    "goal": "Ask follow-up questions based on weak or vague answers.",
                    "question_type": "adaptive_follow_up",
                },
            ],
            "evaluation_rubric": [
                {
                    "criterion": "clarity",
                    "description": "Answer is easy to follow and directly addresses the question.",
                    "max_score": 10,
                },
                {
                    "criterion": "specificity",
                    "description": "Answer includes concrete examples, project details, tools, and outcomes.",
                    "max_score": 10,
                },
                {
                    "criterion": "role_alignment",
                    "description": f"Answer connects experience to the {role} role.",
                    "max_score": 10,
                },
                {
                    "criterion": "technical_depth",
                    "description": "Answer demonstrates appropriate technical understanding for the target role.",
                    "max_score": 10,
                },
                {
                    "criterion": "structure",
                    "description": "Behavioral answers use a clear structure such as STAR when appropriate.",
                    "max_score": 10,
                },
            ],
            "metadata": {
                "role": role,
                "company": company,
                "resume_skill_count": len(resume_skills),
                "resume_project_count": len(resume_projects),
                "research_confidence": research_snapshot.get("confidence") if research_snapshot else "low",
            },
        }

    def _infer_difficulty(self, role: str) -> str:
        lowered_role = role.lower()

        if "senior" in lowered_role or "lead" in lowered_role or "staff" in lowered_role:
            return "senior"

        if "junior" in lowered_role or "entry" in lowered_role or "graduate" in lowered_role:
            return "junior"

        return "mid"

    def _build_focus_areas(
        self,
        role: str,
        resume_skills: list[str],
        target_focus_areas: list[str],
    ) -> list[str]:
        focus_areas = []

        focus_areas.extend(target_focus_areas)

        lowered_role = role.lower()
        lowered_skills = [skill.lower() for skill in resume_skills]

        if "backend" in lowered_role:
            focus_areas.extend(["APIs", "databases", "system design"])

        if "frontend" in lowered_role:
            focus_areas.extend(["React", "TypeScript", "UI architecture"])

        if "data" in lowered_role:
            focus_areas.extend(["SQL", "data pipelines", "data modeling"])

        if "ai" in lowered_role or "ml" in lowered_role or "machine learning" in lowered_role:
            focus_areas.extend(["machine learning", "model evaluation", "AI systems"])

        if "fastapi" in lowered_skills:
            focus_areas.append("FastAPI")

        if "postgresql" in lowered_skills:
            focus_areas.append("PostgreSQL")

        if "docker" in lowered_skills:
            focus_areas.append("Docker")

        if not focus_areas:
            focus_areas = ["background", "projects", "role alignment"]

        return sorted(set(focus_areas))


planner_agent = PlannerAgent()