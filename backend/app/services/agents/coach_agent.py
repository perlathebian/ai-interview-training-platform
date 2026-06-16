class CoachAgent:
    def coach(
        self,
        answer: str,
        evaluation: dict,
    ) -> dict:
        score = evaluation.get("score", 0)

        if score < 5:
            main_advice = (
                "Your answer needs more detail. Use a structured format: situation, task, action, result."
            )
        elif score < 8:
            main_advice = (
                "Your answer is decent, but it would be stronger with measurable results and clearer tradeoffs."
            )
        else:
            main_advice = (
                "Strong answer. Focus on keeping it concise while preserving specific examples."
            )

        return {
            "main_advice": main_advice,
            "improved_answer_guidance": [
                "Start with brief context",
                "Explain your specific role",
                "Mention tools or decisions",
                "End with measurable outcome",
            ],
            "next_time_focus": evaluation.get("weaknesses", []),
        }


coach_agent = CoachAgent()