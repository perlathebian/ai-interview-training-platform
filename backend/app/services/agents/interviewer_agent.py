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
        last_turn = previous_turns[-1] if previous_turns else None

        if last_turn:
            adaptive_question = self._try_generate_adaptive_follow_up(
                last_turn=last_turn,
                role=role,
            )

            if adaptive_question:
                return adaptive_question

        focus_area = self._select_next_focus_area(
            focus_areas=focus_areas,
            previous_turns=previous_turns,
        )

        strategy_stage = self._get_strategy_stage(
            question_strategy=question_strategy,
            turn_count=turn_count,
        )

        question = self._build_question_for_focus_area(
            role=role,
            focus_area=focus_area,
            strategy_stage=strategy_stage,
        )

        return {
            "question": question,
            "difficulty": interview_plan.get("difficulty", "mid"),
            "focus_area": focus_area,
            "question_type": strategy_stage.get("question_type", "role_specific"),
            "reason": "Generated from interview plan and uncovered focus areas.",
        }

    def _try_generate_adaptive_follow_up(
        self,
        last_turn: dict,
        role: str,
    ) -> dict | None:
        score = last_turn.get("score")
        weaknesses = last_turn.get("weaknesses") or []
        answer = last_turn.get("answer") or ""
        focus_area = last_turn.get("focus_area") or "that topic"

        if score is not None and score < 5:
            return {
                "question": (
                    f"Your previous answer needed more depth. Can you give a specific example related to "
                    f"{focus_area}, including your role, the technical decisions you made, and the outcome?"
                ),
                "difficulty": "medium",
                "focus_area": focus_area,
                "question_type": "adaptive_follow_up",
                "reason": "Previous answer received a low score.",
            }

        weakness_text = " ".join(weaknesses).lower()

        if "technical" in weakness_text or "tradeoff" in weakness_text:
            return {
                "question": (
                    f"Let's go deeper technically. For the {role} role, describe a technical decision "
                    f"you made related to {focus_area}. What alternatives did you consider and why?"
                ),
                "difficulty": "medium",
                "focus_area": focus_area,
                "question_type": "technical_follow_up",
                "reason": "Evaluation identified weak technical depth or missing tradeoffs.",
            }

        if "specific" in weakness_text or "examples" in weakness_text or "outcomes" in weakness_text:
            return {
                "question": (
                    f"Can you give a more concrete example related to {focus_area}? "
                    "Please include the situation, your actions, tools used, and measurable result."
                ),
                "difficulty": "medium",
                "focus_area": focus_area,
                "question_type": "specificity_follow_up",
                "reason": "Evaluation identified lack of specificity.",
            }

        if len(answer.strip().split()) < 25:
            return {
                "question": (
                    f"Can you expand your previous answer with a real example related to {focus_area}? "
                    "Focus on what you personally did and what changed because of your work."
                ),
                "difficulty": "easy",
                "focus_area": focus_area,
                "question_type": "clarification_follow_up",
                "reason": "Previous answer was too short.",
            }

        return None

    def _select_next_focus_area(
        self,
        focus_areas: list[str],
        previous_turns: list[dict],
    ) -> str:
        used_focus_areas = [
            turn.get("focus_area")
            for turn in previous_turns
            if turn.get("focus_area")
        ]

        for focus_area in focus_areas:
            if focus_area not in used_focus_areas:
                return focus_area

        return focus_areas[len(previous_turns) % len(focus_areas)]

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