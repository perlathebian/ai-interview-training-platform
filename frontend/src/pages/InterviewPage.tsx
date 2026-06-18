import { useLocation, useParams } from "react-router-dom";
import { useState } from "react";

import { apiClient } from "../api/client";

type Evaluation = {
  score: number;
  strengths: string[];
  weaknesses: string[];
  rubric: {
    clarity: number;
    specificity: number;
    technical_depth: number;
    communication: number;
  };
};

type Coaching = {
  main_advice: string;
  improved_answer: string;
  next_time_focus: string[];
};

export default function InterviewPage() {
  const { id } = useParams();
  const location = useLocation();

  const firstQuestion = location.state?.firstQuestion || "";

  const [currentQuestion, setCurrentQuestion] = useState(firstQuestion);
  const [answer, setAnswer] = useState("");

  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [coaching, setCoaching] = useState<Coaching | null>(null);
  const [nextQuestion, setNextQuestion] = useState("");

  const [turnCount, setTurnCount] = useState(1);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmitAnswer(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!id) {
      setError("Missing interview session ID.");
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const response = await apiClient.post(`/interviews/${id}/answer`, {
        answer,
      });

      setEvaluation(response.data.evaluation);
      setCoaching(response.data.coaching);
      setNextQuestion(response.data.next_question);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to submit answer.");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleContinue() {
    setCurrentQuestion(nextQuestion);
    setAnswer("");
    setEvaluation(null);
    setCoaching(null);
    setNextQuestion("");
    setTurnCount((count) => count + 1);
  }

  return (
    <main>
      <h1>Interview Session</h1>

      <p>Session ID: {id}</p>
      <p>Turn: {turnCount}</p>

      <section>
        <h2>Current Question</h2>

        {currentQuestion ? (
          <p>{currentQuestion}</p>
        ) : (
          <p>
            No question found. Go back and start a new interview. Later we will
            support loading sessions directly from the backend.
          </p>
        )}
      </section>

      <section>
        <h2>Your Answer</h2>

        <form onSubmit={handleSubmitAnswer}>
          <textarea
            rows={8}
            cols={80}
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            placeholder="Type your answer here..."
            required
            disabled={isSubmitting || Boolean(evaluation)}
          />

          <br />

          {error && <p>{error}</p>}

          <button
            type="submit"
            disabled={isSubmitting || !answer.trim() || Boolean(evaluation)}
          >
            {isSubmitting ? "Submitting..." : "Submit Answer"}
          </button>
        </form>
      </section>

      {evaluation && (
        <section>
          <h2>Evaluation</h2>

          <p>
            <strong>Score:</strong> {evaluation.score}/10
          </p>

          <h3>Rubric</h3>
          <ul>
            <li>Clarity: {evaluation.rubric.clarity}/10</li>
            <li>Specificity: {evaluation.rubric.specificity}/10</li>
            <li>Technical Depth: {evaluation.rubric.technical_depth}/10</li>
            <li>Communication: {evaluation.rubric.communication}/10</li>
          </ul>

          <h3>Strengths</h3>
          <ul>
            {evaluation.strengths.map((strength, index) => (
              <li key={index}>{strength}</li>
            ))}
          </ul>

          <h3>Weaknesses</h3>
          <ul>
            {evaluation.weaknesses.map((weakness, index) => (
              <li key={index}>{weakness}</li>
            ))}
          </ul>
        </section>
      )}

      {coaching && (
        <section>
          <h2>Coaching</h2>

          <p>
            <strong>Main advice:</strong> {coaching.main_advice}
          </p>

          <p>
            <strong>Improved answer guidance:</strong>{" "}
            {coaching.improved_answer}
          </p>

          <h3>Next Time Focus</h3>
          <ul>
            {coaching.next_time_focus.map((focus, index) => (
              <li key={index}>{focus}</li>
            ))}
          </ul>
        </section>
      )}

      {nextQuestion && (
        <section>
          <h2>Next Question</h2>

          <p>{nextQuestion}</p>

          <button onClick={handleContinue}>Continue to Next Question</button>
        </section>
      )}
    </main>
  );
}
