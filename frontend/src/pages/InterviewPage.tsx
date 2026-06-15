import { useLocation, useParams } from "react-router-dom";

export default function InterviewPage() {
  const { id } = useParams();
  const location = useLocation();

  const firstQuestion = location.state?.firstQuestion;

  return (
    <main>
      <h1>Interview Session</h1>

      <p>Session ID: {id}</p>

      <section>
        <h2>First Question</h2>

        {firstQuestion ? (
          <p>{firstQuestion}</p>
        ) : (
          <p>
            First question not available in page state. Later we will fetch the
            session from the backend directly.
          </p>
        )}
      </section>

      <section>
        <h2>Your Answer</h2>
        <textarea
          rows={8}
          cols={80}
          placeholder="Answer flow comes on Day 6..."
        />

        <br />

        <button disabled>Submit Answer Coming Next</button>
      </section>
    </main>
  );
}
