class CoachAgent:
    def coach(
        self,
        answer: str,
    ) -> dict:
        return {
            "improvements": [
                "Add measurable results",
                "Use STAR structure",
            ]
        }


coach_agent = CoachAgent()