class EvaluatorAgent:
    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> dict:
        return {
            "score": 7,
            "strengths": [
                "Clear communication"
            ],
            "weaknesses": [
                "Could provide more detail"
            ],
        }


evaluator_agent = EvaluatorAgent()