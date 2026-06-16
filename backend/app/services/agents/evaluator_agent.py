class EvaluatorAgent:
    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> dict:
        word_count = len(answer.strip().split())

        if word_count < 25:
            score = 4
            weaknesses = [
                "Answer is too short",
                "Needs more specific examples",
                "Needs clearer structure",
            ]
        elif word_count < 80:
            score = 7
            weaknesses = [
                "Could include more measurable impact",
                "Could explain technical tradeoffs more clearly",
            ]
        else:
            score = 8
            weaknesses = [
                "Could be more concise",
            ]

        return {
            "score": score,
            "strengths": [
                "Answer addresses the question",
            ],
            "weaknesses": weaknesses,
            "rubric": {
                "clarity": min(score + 1, 10),
                "specificity": score,
                "structure": score,
                "technical_depth": max(score - 1, 1),
            },
        }


evaluator_agent = EvaluatorAgent()