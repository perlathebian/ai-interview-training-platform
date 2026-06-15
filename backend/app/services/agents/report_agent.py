class ReportAgent:
    def generate_report(self, session_data: dict) -> dict:
        return {
            "overall_summary": "Mock report. Real session reporting will be added later.",
            "strengths": [],
            "weaknesses": [],
            "recommended_focus": [],
            "overall_score": None,
        }


report_agent = ReportAgent()