import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiClient } from "../api/client";

type TrainingTarget = {
  id: number;
  target_type: string;
  company: string | null;
  role: string;
};

export default function NewInterviewPage() {
  const navigate = useNavigate();

  const [targets, setTargets] = useState<TrainingTarget[]>([]);
  const [selectedTargetId, setSelectedTargetId] = useState("");
  const [mode, setMode] = useState("text");

  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingTargets, setIsLoadingTargets] = useState(true);

  useEffect(() => {
    async function loadTargets() {
      try {
        const response = await apiClient.get("/training-targets");
        setTargets(response.data);

        if (response.data.length > 0) {
          setSelectedTargetId(String(response.data[0].id));
        }
      } catch (err: any) {
        setError(
          err.response?.data?.detail || "Failed to load training targets.",
        );
      } finally {
        setIsLoadingTargets(false);
      }
    }

    loadTargets();
  }, []);

  async function handleStartInterview(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setIsLoading(true);

    try {
      const response = await apiClient.post("/interviews/start", {
        training_target_id: Number(selectedTargetId),
        mode,
      });

      navigate(`/interviews/${response.data.session_id}`, {
        state: {
          firstQuestion: response.data.first_question,
        },
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to start interview.");
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoadingTargets) {
    return <p>Loading training targets...</p>;
  }

  return (
    <main>
      <h1>Start Interview</h1>

      <p>
        Choose a training target. The interview will use your resume and target
        context to generate the first question.
      </p>

      {targets.length === 0 ? (
        <section>
          <p>
            You need to create a training target before starting an interview.
          </p>
          <button onClick={() => navigate("/training-targets/new")}>
            Create Training Target
          </button>
        </section>
      ) : (
        <form onSubmit={handleStartInterview}>
          <div>
            <label>Training Target</label>
            <br />
            <select
              value={selectedTargetId}
              onChange={(event) => setSelectedTargetId(event.target.value)}
              required
            >
              {targets.map((target) => (
                <option key={target.id} value={target.id}>
                  {target.role}
                  {target.company ? ` at ${target.company}` : ""}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label>Mode</label>
            <br />
            <select
              value={mode}
              onChange={(event) => setMode(event.target.value)}
            >
              <option value="text">Text</option>
            </select>
          </div>

          {error && <p>{error}</p>}

          <button type="submit" disabled={isLoading}>
            {isLoading ? "Starting..." : "Start Interview"}
          </button>
        </form>
      )}
    </main>
  );
}
