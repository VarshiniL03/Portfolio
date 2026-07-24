import { createContext, useContext, useState, useEffect } from "react";
import { login as loginRequest, getMe } from "../api/resources";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("admin_token");
    if (!token) {
      setLoading(false);
      return;
    }
    getMe()
      .then((res) => setUser(res.data))
      .catch(() => localStorage.removeItem("admin_token"))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const res = await loginRequest(email, password);
    localStorage.setItem("admin_token", res.data.access_token);
    const me = await getMe();
    setUser(me.data);
    return me.data;
  }

  function logout() {
    localStorage.removeItem("admin_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// ← only this block is new, everything above is unchanged
export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}