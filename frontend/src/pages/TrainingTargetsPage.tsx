import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { apiClient } from "../api/client";

type TrainingTarget = {
  id: number;
  target_type: string;
  company: string | null;
  role: string;
  job_description: string | null;
  desired_companies: string[] | null;
  focus_areas: string[] | null;
  created_at: string;
  updated_at: string;
};

export default function TrainingTargetsPage() {
  const [targets, setTargets] = useState<TrainingTarget[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadTargets() {
      try {
        const response = await apiClient.get("/training-targets");
        setTargets(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load targets.");
      } finally {
        setIsLoading(false);
      }
    }

    loadTargets();
  }, []);

  if (isLoading) {
    return <p>Loading training targets...</p>;
  }

  return (
    <main>
      <h1>Training Targets</h1>

      <p>
        Training targets define the role, company, or job description you want
        to prepare for.
      </p>

      <Link to="/training-targets/new">Create New Target</Link>

      {error && <p>{error}</p>}

      {targets.length === 0 ? (
        <p>No training targets yet.</p>
      ) : (
        <ul>
          {targets.map((target) => (
            <li key={target.id}>
              <h2>
                {target.role}
                {target.company ? ` at ${target.company}` : ""}
              </h2>

              <p>Type: {target.target_type}</p>

              {target.focus_areas && target.focus_areas.length > 0 && (
                <p>Focus: {target.focus_areas.join(", ")}</p>
              )}

              {target.job_description && (
                <details>
                  <summary>Job Description</summary>
                  <p>{target.job_description}</p>
                </details>
              )}
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
