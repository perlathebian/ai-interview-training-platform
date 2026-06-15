from abc import ABC
from typing import Any


class AIService(ABC):
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        """
        Temporary implementation.

        Week 1:
        Returns mock responses.

        Week 2:
        Real Groq integration.

        Future:
        Fallback model support.
        """

        return {
            "status": "mock_response"
        }


ai_service = AIService()