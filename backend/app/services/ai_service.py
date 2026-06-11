class AIService:
    def generate_first_question(self, role: str | None = None) -> str:
        if role:
            return f"Tell me about your background and why you are interested in a {role} role."

        return "Tell me about your background and the type of role you are preparing for."

    def evaluate_answer(self, question: str, answer: str) -> dict:
        return {
            "score": 7,
            "strengths": [
                "Clear attempt to answer the question",
            ],
            "weaknesses": [
                "Needs more specific examples and measurable impact",
            ],
            "rubric": {
                "clarity": 7,
                "specificity": 5,
                "structure": 6,
                "role_alignment": 6,
            },
        }

    def generate_coaching(self, answer: str, evaluation: dict) -> dict:
        return {
            "main_advice": "Use a more structured answer with specific examples, actions, and outcomes.",
            "improved_answer_example": "A stronger answer would briefly describe the situation, explain your specific contribution, and quantify the result where possible.",
            "next_time_focus": [
                "Add concrete project details",
                "Mention technical tradeoffs",
                "Explain measurable impact",
            ],
        }


ai_service = AIService()