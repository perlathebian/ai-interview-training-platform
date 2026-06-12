import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <main>
      <h1>AI Interview Training Platform</h1>

      <p>
        Practice for AI screening interviews, technical interviews, and
        behavioral interviews with adaptive coaching.
      </p>

      <nav>
        <Link to="/register">Register</Link>
        {" | "}
        <Link to="/login">Login</Link>
        {" | "}
        <Link to="/dashboard">Dashboard</Link>
      </nav>
    </main>
  );
}
