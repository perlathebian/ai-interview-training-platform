import { useEffect, useState } from "react";

import { apiClient } from "../api/client";

export type AuthUser = {
  id: number;
  email: string;
  specialty: string | null;
  level: string | null;
  is_verified: boolean;
  is_active: boolean;
  created_at: string;
};

export function useAuth() {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    async function loadUser() {
      try {
        const response = await apiClient.get("/auth/me");

        setUser(response.data);
        setIsAuthenticated(true);
      } catch {
        setUser(null);
        setIsAuthenticated(false);
        localStorage.removeItem("access_token");
      } finally {
        setIsLoading(false);
      }
    }

    loadUser();
  }, []);

  return {
    user,
    isLoading,
    isAuthenticated,
  };
}
