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

    def generate_next_question(
        self,
        resume_snapshot: dict | None,
        job_snapshot: dict,
        interview_plan: dict,
        previous_turns: list[dict],
    ) -> dict:
        role = job_snapshot.get("role", "this role")
        focus_areas = interview_plan.get("focus_areas") or ["background"]
        question_strategy = interview_plan.get("question_strategy") or []

        turn_count = len(previous_turns)
        next_turn_number = turn_count + 1

        last_turn = previous_turns[-1] if previous_turns else None

        if last_turn and self._answer_was_weak(last_turn):
            question = self._build_follow_up_question(last_turn)
            return {
                "question": question,
                "difficulty": "medium",
                "focus_area": last_turn.get("focus_area", "follow-up"),
                "question_type": "adaptive_follow_up",
                "reason": "Previous answer looked weak or too short.",
            }

        focus_area = focus_areas[turn_count % len(focus_areas)]
        strategy_stage = self._get_strategy_stage(
            question_strategy=question_strategy,
            turn_count=turn_count,
        )

        question = self._build_question_for_focus_area(
            role=role,
            focus_area=focus_area,
            strategy_stage=strategy_stage,
            next_turn_number=next_turn_number,
        )

        return {
            "question": question,
            "difficulty": interview_plan.get("difficulty", "mid"),
            "focus_area": focus_area,
            "question_type": strategy_stage.get("question_type", "role_specific"),
            "reason": "Generated from interview plan focus areas.",
        }

    def _answer_was_weak(self, turn: dict) -> bool:
        answer = turn.get("answer") or ""
        score = turn.get("score")

        if score is not None and score < 5:
            return True

        if len(answer.strip().split()) < 25:
            return True

        return False

    def _build_follow_up_question(self, last_turn: dict) -> str:
        focus_area = last_turn.get("focus_area", "that topic")

        return (
            f"Can you give a more specific example related to {focus_area}, "
            "including what you did, what tradeoffs you considered, and what the outcome was?"
        )

    def _get_strategy_stage(
        self,
        question_strategy: list[dict],
        turn_count: int,
    ) -> dict:
        if not question_strategy:
            return {
                "stage": "role_alignment",
                "question_type": "role_specific",
            }

        index = min(turn_count, len(question_strategy) - 1)
        return question_strategy[index]

    def _build_question_for_focus_area(
        self,
        role: str,
        focus_area: str,
        strategy_stage: dict,
        next_turn_number: int,
    ) -> str:
        question_type = strategy_stage.get("question_type", "role_specific")

        if question_type == "behavioral":
            return (
                f"Tell me about a time you demonstrated strong communication or problem-solving "
                f"while working on something related to {focus_area}."
            )

        if question_type == "technical_behavioral":
            return (
                f"Walk me through a project where you used or worked with {focus_area}. "
                "What was your role, what technical decisions did you make, and what was the result?"
            )

        if question_type == "adaptive_follow_up":
            return (
                f"Let's go deeper on {focus_area}. What is one challenge you faced there, "
                "and how did you approach it?"
            )

        return (
            f"For a {role} role, how would you explain your experience with {focus_area}, "
            "and what makes your experience relevant?"
        )


interviewer_agent = InterviewerAgent()