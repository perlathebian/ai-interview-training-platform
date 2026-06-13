import { useEffect, useState } from "react";

import { apiClient } from "../api/client";

type Resume = {
  id: number;
  raw_text: string;
  parsed_summary: string | null;
  extracted_skills: string[] | null;
  extracted_projects: string[] | null;
  extracted_experience: string[] | null;
  extracted_education: string[] | null;
  is_active: boolean;
  is_deleted: boolean;
  created_at: string;
  updated_at: string;
};

export default function ResumePage() {
  const [rawText, setRawText] = useState("");
  const [resume, setResume] = useState<Resume | null>(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function loadResume() {
    try {
      const response = await apiClient.get("/resumes/me");
      setResume(response.data);
      setRawText(response.data.raw_text);
    } catch {
      setResume(null);
    }
  }

  useEffect(() => {
    loadResume();
  }, []);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setMessage("");
    setError("");
    setIsLoading(true);

    try {
      const response = await apiClient.post("/resumes", {
        raw_text: rawText,
      });

      setResume(response.data);
      setMessage("Resume saved successfully.");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to save resume.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleDelete() {
    if (!resume) return;

    setMessage("");
    setError("");

    try {
      await apiClient.delete(`/resumes/${resume.id}`);
      setResume(null);
      setRawText("");
      setMessage("Resume deleted.");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to delete resume.");
    }
  }

  return (
    <main>
      <h1>Resume</h1>

      <p>
        Paste your resume text below. This will be used to personalize interview
        questions and feedback.
      </p>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Resume Text</label>
          <br />
          <textarea
            value={rawText}
            onChange={(event) => setRawText(event.target.value)}
            rows={12}
            cols={80}
            required
          />
        </div>

        {error && <p>{error}</p>}
        {message && <p>{message}</p>}

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Saving..." : "Save Resume"}
        </button>
      </form>

      {resume && (
        <section>
          <h2>Parsed Resume</h2>

          <p>
            <strong>Summary:</strong>{" "}
            {resume.parsed_summary || "No summary extracted"}
          </p>

          <h3>Skills</h3>
          {resume.extracted_skills && resume.extracted_skills.length > 0 ? (
            <ul>
              {resume.extracted_skills.map((skill) => (
                <li key={skill}>{skill}</li>
              ))}
            </ul>
          ) : (
            <p>No skills extracted.</p>
          )}

          <h3>Projects</h3>
          {resume.extracted_projects && resume.extracted_projects.length > 0 ? (
            <ul>
              {resume.extracted_projects.map((project, index) => (
                <li key={index}>{project}</li>
              ))}
            </ul>
          ) : (
            <p>No projects extracted.</p>
          )}

          <h3>Education</h3>
          {resume.extracted_education &&
          resume.extracted_education.length > 0 ? (
            <ul>
              {resume.extracted_education.map((education, index) => (
                <li key={index}>{education}</li>
              ))}
            </ul>
          ) : (
            <p>No education extracted.</p>
          )}

          <button onClick={handleDelete}>Delete Resume</button>
        </section>
      )}
    </main>
  );
}
