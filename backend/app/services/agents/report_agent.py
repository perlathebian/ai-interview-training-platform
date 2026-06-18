class ReportAgent:
    def generate_report(
        self,
        turns: list,
    ) -> dict:
        completed_turns = [
            turn
            for turn in turns
            if turn.evaluation is not None
        ]

        if not completed_turns:
            return {
                "overall_score": 0,
                "strengths": [],
                "weaknesses": [],
                "recommended_focus": [],
                "summary": "No completed interview turns found.",
            }

        scores = [
            turn.score
            for turn in completed_turns
            if turn.score is not None
        ]

        overall_score = round(sum(scores) / len(scores))

        strengths = []
        weaknesses = []

        for turn in completed_turns:
            strengths.extend(
                turn.evaluation.get("strengths", [])
            )

            weaknesses.extend(
                turn.evaluation.get("weaknesses", [])
            )

        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))

        recommended_focus = []

        for weakness in weaknesses:
            if "specific" in weakness.lower():
                recommended_focus.append(
                    "Use more concrete project examples"
                )

            if "technical" in weakness.lower():
                recommended_focus.append(
                    "Explain technical decisions and tradeoffs"
                )

            if "structure" in weakness.lower():
                recommended_focus.append(
                    "Use STAR-style answer structure"
                )

        recommended_focus = list(dict.fromkeys(recommended_focus))

        summary = (
            f"The interview completed with an overall score of "
            f"{overall_score}/10 across {len(completed_turns)} evaluated turns."
        )

        return {
            "overall_score": overall_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_focus": recommended_focus,
            "summary": summary,
        }


report_agent = ReportAgent()