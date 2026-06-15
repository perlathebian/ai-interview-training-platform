class InterviewerAgent:
    def generate_first_question(
        self,
        resume_snapshot: dict | None,
        job_snapshot: dict,
        interview_plan: dict,
    ) -> dict:
        role = job_snapshot.get("role", "this role")
        company = job_snapshot.get("company")

        if company:
            question = (
                f"Tell me about yourself and how your background makes you a strong fit "
                f"for the {role} role at {company}."
            )
        else:
            question = (
                f"Tell me about yourself and how your background connects to a {role} role."
            )

        return {
            "question": question,
            "difficulty": "easy",
            "focus_area": "background",
            "expected_signal": "Candidate can summarize experience and connect it to the target role.",
        }


interviewer_agent = InterviewerAgent()