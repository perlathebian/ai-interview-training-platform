class ResearchAgent:
    def research_target(self, company: str | None, role: str, job_description: str | None) -> dict:
        return {
            "confidence": "low",
            "summary": "Mock research summary. Real company/job research will be added later.",
            "patterns": [
                "behavioral screening",
                "technical fundamentals",
                "role-specific questions",
            ],
            "sources": [],
        }


research_agent = ResearchAgent()