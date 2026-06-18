import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { apiClient } from "../api/client";

type InterviewSession = {
  id: number;
  training_target_id: number;
  mode: string;
  status: string;
  overall_score: number | null;
  started_at: string;
  completed_at: string | null;
};

export default function InterviewHistoryPage() {
  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadSessions() {
      try {
        const response = await apiClient.get("/interviews");
        setSessions(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load interviews.");
      } finally {
        setIsLoading(false);
      }
    }

    loadSessions();
  }, []);

  if (isLoading) {
    return <p>Loading interview history...</p>;
  }

  return (
    <main>
      <h1>Interview History</h1>

      <Link to="/interviews/new">Start New Interview</Link>

      {error && <p>{error}</p>}

      {sessions.length === 0 ? (
        <p>No interview sessions yet.</p>
      ) : (
        <ul>
          {sessions.map((session) => (
            <li key={session.id}>
              <h2>Interview #{session.id}</h2>
              <p>Mode: {session.mode}</p>
              <p>Status: {session.status}</p>
              <p>Started: {new Date(session.started_at).toLocaleString()}</p>
              <Link to={`/interviews/${session.id}/report`}>
                View Session Report
              </Link>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
