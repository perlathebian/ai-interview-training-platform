import re


COMMON_TECH_SKILLS = [
    "python",
    "fastapi",
    "django",
    "flask",
    "javascript",
    "typescript",
    "react",
    "next.js",
    "node.js",
    "express",
    "html",
    "css",
    "tailwind",
    "sql",
    "postgresql",
    "mysql",
    "sqlite",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "linux",
    "git",
    "github",
    "ci/cd",
    "github actions",
    "machine learning",
    "deep learning",
    "nlp",
    "pytorch",
    "tensorflow",
    "scikit-learn",
    "pandas",
    "numpy",
    "langchain",
    "llm",
    "rag",
    "openai",
    "groq",
]


class ResumeParser:
    def parse(self, raw_text: str) -> dict:
        cleaned_text = self._normalize_text(raw_text)

        return {
            "parsed_summary": self._extract_summary(cleaned_text),
            "extracted_skills": self._extract_skills(cleaned_text),
            "extracted_projects": self._extract_section_lines(
                cleaned_text,
                section_keywords=["projects", "project experience"],
            ),
            "extracted_experience": self._extract_section_lines(
                cleaned_text,
                section_keywords=["experience", "work experience", "employment"],
            ),
            "extracted_education": self._extract_section_lines(
                cleaned_text,
                section_keywords=["education", "academic background"],
            ),
        }

    def _normalize_text(self, text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _extract_summary(self, text: str) -> str:
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        meaningful_lines = [
            line
            for line in lines
            if len(line) > 40 and not self._looks_like_section_heading(line)
        ]

        if not meaningful_lines:
            return "No clear summary detected."

        return " ".join(meaningful_lines[:3])

    def _extract_skills(self, text: str) -> list[str]:
        lowered_text = text.lower()

        found_skills = []

        for skill in COMMON_TECH_SKILLS:
            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, lowered_text):
                found_skills.append(skill)

        return sorted(set(found_skills))

    def _extract_section_lines(
        self,
        text: str,
        section_keywords: list[str],
        max_lines: int = 8,
    ) -> list[str]:
        lines = [line.strip() for line in text.split("\n")]

        section_start_index = None

        for index, line in enumerate(lines):
            normalized_line = line.lower().strip().rstrip(":")

            if normalized_line in section_keywords:
                section_start_index = index + 1
                break

        if section_start_index is None:
            return []

        section_lines = []

        for line in lines[section_start_index:]:
            if not line.strip():
                continue

            if self._looks_like_section_heading(line):
                break

            section_lines.append(line.strip())

            if len(section_lines) >= max_lines:
                break

        return section_lines

    def _looks_like_section_heading(self, line: str) -> bool:
        normalized_line = line.strip().lower().rstrip(":")

        common_headings = {
            "summary",
            "profile",
            "skills",
            "technical skills",
            "projects",
            "project experience",
            "experience",
            "work experience",
            "employment",
            "education",
            "academic background",
            "certifications",
            "languages",
        }

        if normalized_line in common_headings:
            return True

        if len(line.split()) <= 4 and line.isupper():
            return True

        return False


resume_parser = ResumeParser()