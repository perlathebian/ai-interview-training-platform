import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { apiClient } from "../api/client";

type User = {
  id: number;
  email: string;
  specialty: string | null;
  level: string | null;
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
};

export default function DashboardPage() {
  const navigate = useNavigate();

  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadCurrentUser() {
      try {
        const response = await apiClient.get("/auth/me");
        setUser(response.data);
      } catch {
        localStorage.removeItem("access_token");
        setError("You must log in first.");
        navigate("/login");
      } finally {
        setIsLoading(false);
      }
    }

    loadCurrentUser();
  }, [navigate]);

  function handleLogout() {
    localStorage.removeItem("access_token");
    navigate("/login");
  }

  if (isLoading) {
    return <p>Loading dashboard...</p>;
  }

  if (error) {
    return <p>{error}</p>;
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

      <button onClick={handleLogout}>Logout</button>
    </main>
  );
}
