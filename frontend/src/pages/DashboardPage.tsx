import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, isLoading } = useAuth();

  function handleLogout() {
    localStorage.removeItem("access_token");
    navigate("/login");
  }

  if (isLoading) {
    return <p>Loading dashboard...</p>;
  }

  return (
    <main>
      <h1>Dashboard</h1>

      {user && (
        <section>
          <p>Logged in as: {user.email}</p>
          <p>Specialty: {user.specialty || "Not set"}</p>
          <p>Level: {user.level || "Not set"}</p>
        </section>
      )}

      <nav>
        <Link to="/resume">Manage Resume</Link>
        {" | "}
        <Link to="/training-targets">Training Targets</Link>
        {" | "}
        <Link to="/interviews/new">Start Interview</Link>
        {" | "}
        <Link to="/interviews/history">Interview History</Link>
      </nav>

      <button onClick={handleLogout}>Logout</button>
    </main>
  );
}
