import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { apiClient } from "../api/client";

type InterviewTurn = {
  id: number;
  turn_number: number;
  question: string;
  answer: string | null;
  evaluation: {
    score: number;
    strengths: string[];
    weaknesses: string[];
    rubric: Record<string, number>;
  } | null;
  coaching: {
    main_advice: string;
    improved_answer: string;
    next_time_focus: string[];
  } | null;
  score: number | null;
  status: string;
};

type InterviewSessionDetail = {
  id: number;
  mode: string;
  status: string;
  job_snapshot: {
    company?: string | null;
    role?: string | null;
  } | null;
  interview_plan_snapshot: {
    focus_areas?: string[];
    difficulty?: string;
  } | null;
  turns: InterviewTurn[];
};

export default function InterviewReportPage() {
  const { id } = useParams();

  const [session, setSession] = useState<InterviewSessionDetail | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadSession() {
      try {
        const response = await apiClient.get(`/interviews/${id}`);
        setSession(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || "Failed to load interview.");
      } finally {
        setIsLoading(false);
      }
    }

    loadSession();
  }, [id]);

  if (isLoading) {
    return <p>Loading interview report...</p>;
  }

  if (error) {
    return <p>{error}</p>;
  }

  if (!session) {
    return <p>Interview not found.</p>;
  }

  return (
    <main>
      <h1>Interview Report</h1>

      <Link to="/interviews/history">Back to History</Link>

      <section>
        <h2>Session Summary</h2>
        <p>Session ID: {session.id}</p>
        <p>Status: {session.status}</p>
        <p>Mode: {session.mode}</p>
        <p>Role: {session.job_snapshot?.role || "Unknown"}</p>
        <p>Company: {session.job_snapshot?.company || "Not specified"}</p>
        <p>
          Difficulty:{" "}
          {session.interview_plan_snapshot?.difficulty || "Not specified"}
        </p>
      </section>

      <section>
        <h2>Turns</h2>

        {session.turns.map((turn) => (
          <article key={turn.id}>
            <h3>Turn {turn.turn_number}</h3>

            <p>
              <strong>Question:</strong> {turn.question}
            </p>

            <p>
              <strong>Answer:</strong>{" "}
              {turn.answer || "No answer submitted yet."}
            </p>

            <p>
              <strong>Status:</strong> {turn.status}
            </p>

            {turn.evaluation && (
              <section>
                <h4>Evaluation</h4>
                <p>Score: {turn.evaluation.score}/10</p>

                <p>Strengths:</p>
                <ul>
                  {turn.evaluation.strengths.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>

                <p>Weaknesses:</p>
                <ul>
                  {turn.evaluation.weaknesses.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </section>
            )}

            {turn.coaching && (
              <section>
                <h4>Coaching</h4>
                <p>{turn.coaching.main_advice}</p>
                <p>{turn.coaching.improved_answer}</p>
              </section>
            )}

            <hr />
          </article>
        ))}
      </section>
    </main>
  );
}
