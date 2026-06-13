import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiClient } from "../api/client";

export default function NewTrainingTargetPage() {
  const navigate = useNavigate();

  const [targetType, setTargetType] = useState("specific_job");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [focusAreas, setFocusAreas] = useState("");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setIsLoading(true);

    const focusAreaList = focusAreas
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);

    try {
      await apiClient.post("/training-targets", {
        target_type: targetType,
        company: company || null,
        role,
        job_description: jobDescription || null,
        desired_companies: null,
        focus_areas: focusAreaList.length > 0 ? focusAreaList : null,
      });

      navigate("/training-targets");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to save training target.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main>
      <h1>New Training Target</h1>

      <form onSubmit={handleSubmit}>
        <div>
          <label>Target Type</label>
          <br />
          <select
            value={targetType}
            onChange={(event) => setTargetType(event.target.value)}
          >
            <option value="specific_job">Specific Job</option>
            <option value="general_practice">General Practice</option>
            <option value="company_practice">Company Practice</option>
          </select>
        </div>

        <div>
          <label>Company</label>
          <br />
          <input
            type="text"
            value={company}
            onChange={(event) => setCompany(event.target.value)}
            placeholder="Datadog"
          />
        </div>

        <div>
          <label>Role</label>
          <br />
          <input
            type="text"
            value={role}
            onChange={(event) => setRole(event.target.value)}
            placeholder="Junior Backend Engineer"
            required
          />
        </div>

        <div>
          <label>Job Description</label>
          <br />
          <textarea
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            rows={10}
            cols={80}
            placeholder="Paste the job description here..."
          />
        </div>

        <div>
          <label>Focus Areas</label>
          <br />
          <input
            type="text"
            value={focusAreas}
            onChange={(event) => setFocusAreas(event.target.value)}
            placeholder="backend APIs, databases, system design"
          />
        </div>

        {error && <p>{error}</p>}

        <button type="submit" disabled={isLoading}>
          {isLoading ? "Saving..." : "Save Target"}
        </button>
      </form>
    </main>
  );
}
