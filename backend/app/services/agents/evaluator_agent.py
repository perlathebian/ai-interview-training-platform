class EvaluatorAgent:
    def evaluate(
        self,
        question: str,
        answer: str,
    ) -> dict:
        word_count = len(answer.strip().split())

        clarity = self._score_clarity(answer)
        specificity = self._score_specificity(answer, word_count)
        technical_depth = self._score_technical_depth(answer)
        communication = self._score_communication(answer)

        score = round(
            (clarity + specificity + technical_depth + communication) / 4
        )

        strengths = self._build_strengths(
            clarity=clarity,
            specificity=specificity,
            technical_depth=technical_depth,
            communication=communication,
        )

        weaknesses = self._build_weaknesses(
            clarity=clarity,
            specificity=specificity,
            technical_depth=technical_depth,
            communication=communication,
            word_count=word_count,
        )

        return {
            "score": score,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "rubric": {
                "clarity": clarity,
                "specificity": specificity,
                "technical_depth": technical_depth,
                "communication": communication,
            },
        }

    def _score_clarity(self, answer: str) -> int:
        word_count = len(answer.strip().split())

        if word_count < 20:
            return 4

        if word_count < 60:
            return 7

        return 8

    def _score_specificity(self, answer: str, word_count: int) -> int:
        lowered_answer = answer.lower()

        specificity_signals = [
            "project",
            "built",
            "designed",
            "implemented",
            "improved",
            "reduced",
            "increased",
            "users",
            "requests",
            "database",
            "api",
            "pipeline",
        ]

        signal_count = sum(
            1 for signal in specificity_signals if signal in lowered_answer
        )

        if word_count < 25:
            return 4

        if signal_count >= 4:
            return 8

        if signal_count >= 2:
            return 6

        return 5

    def _score_technical_depth(self, answer: str) -> int:
        lowered_answer = answer.lower()

        technical_signals = [
            "python",
            "fastapi",
            "postgresql",
            "sql",
            "docker",
            "api",
            "database",
            "migration",
            "schema",
            "pipeline",
            "etl",
            "data modeling",
            "distributed",
            "cloud",
            "architecture",
        ]

        signal_count = sum(
            1 for signal in technical_signals if signal in lowered_answer
        )

        if signal_count >= 6:
            return 8

        if signal_count >= 3:
            return 6

        if signal_count >= 1:
            return 5

        return 3

    def _score_communication(self, answer: str) -> int:
        lowered_answer = answer.lower()

        structure_signals = [
            "because",
            "for example",
            "one project",
            "while",
            "which",
            "therefore",
            "as a result",
        ]

        signal_count = sum(
            1 for signal in structure_signals if signal in lowered_answer
        )

        if len(answer.strip().split()) < 20:
            return 4

        if signal_count >= 3:
            return 8

        if signal_count >= 1:
            return 6

        return 5

    def _build_strengths(
        self,
        clarity: int,
        specificity: int,
        technical_depth: int,
        communication: int,
    ) -> list[str]:
        strengths = []

        if clarity >= 7:
            strengths.append("Answer is clear and easy to follow")

        if specificity >= 7:
            strengths.append("Answer includes concrete examples and relevant details")

        if technical_depth >= 7:
            strengths.append("Answer demonstrates relevant technical background")

        if communication >= 7:
            strengths.append("Answer is structured and communicates fit effectively")

        if not strengths:
            strengths.append("Answer attempts to address the question")

        return strengths

    def _build_weaknesses(
        self,
        clarity: int,
        specificity: int,
        technical_depth: int,
        communication: int,
        word_count: int,
    ) -> list[str]:
        weaknesses = []

        if word_count < 25:
            weaknesses.append("Answer is too short and needs more detail")

        if clarity < 6:
            weaknesses.append("Answer could be clearer and more directly organized")

        if specificity < 7:
            weaknesses.append("Add more concrete examples, tools, projects, and outcomes")

        if technical_depth < 7:
            weaknesses.append("Explain technical decisions, tradeoffs, or implementation details more deeply")

        if communication < 7:
            weaknesses.append("Use a stronger structure to make the answer easier to evaluate")

        return weaknesses


evaluator_agent = EvaluatorAgent()