class CoachAgent:
    def coach(
        self,
        question: str,
        answer: str,
        evaluation: dict,
    ) -> dict:
        score = evaluation.get("score", 0)
        weaknesses = evaluation.get("weaknesses", [])
        rubric = evaluation.get("rubric", {})

        main_advice = self._build_main_advice(
            score=score,
            weaknesses=weaknesses,
        )

        improved_answer = self._build_improved_answer(
            question=question,
            answer=answer,
            rubric=rubric,
        )

        next_time_focus = self._build_next_time_focus(
            weaknesses=weaknesses,
            rubric=rubric,
        )

        return {
            "main_advice": main_advice,
            "improved_answer": improved_answer,
            "next_time_focus": next_time_focus,
        }

    def _build_main_advice(
        self,
        score: int,
        weaknesses: list[str],
    ) -> str:
        if score < 5:
            return (
                "Your answer needs more detail and structure. Start with brief context, "
                "explain your specific actions, and end with the result or impact."
            )

        if score < 8:
            return (
                "Your answer is solid, but it would be stronger with clearer measurable impact, "
                "more specific technical decisions, and a tighter structure."
            )

        return (
            "Your answer is strong. To improve further, make it more concise while preserving "
            "the strongest technical and outcome-focused details."
        )

    def _build_improved_answer(
        self,
        question: str,
        answer: str,
        rubric: dict,
    ) -> str:
        technical_depth = rubric.get("technical_depth", 0)
        specificity = rubric.get("specificity", 0)

        additions = []

        if specificity < 8:
            additions.append(
                "include a concrete project example with your exact role and outcome"
            )

        if technical_depth < 8:
            additions.append(
                "mention technical decisions, tools, tradeoffs, or implementation details"
            )

        if not additions:
            additions.append(
                "keep the same structure but make the strongest points more concise"
            )

        return (
            "A stronger version of this answer would directly answer the question, "
            + ", ".join(additions)
            + ". Use this structure: background -> specific example -> your actions -> result -> connection to the role."
        )

    def _build_next_time_focus(
        self,
        weaknesses: list[str],
        rubric: dict,
    ) -> list[str]:
        focus = []

        if rubric.get("specificity", 0) < 8:
            focus.append("Add specific project examples and outcomes")

        if rubric.get("technical_depth", 0) < 8:
            focus.append("Explain technical decisions and tradeoffs")

        if rubric.get("communication", 0) < 8:
            focus.append("Use clearer structure such as STAR")

        if weaknesses:
            focus.extend(weaknesses[:2])

        if not focus:
            focus.append("Keep answers concise while preserving impact")

        return list(dict.fromkeys(focus))


coach_agent = CoachAgent()