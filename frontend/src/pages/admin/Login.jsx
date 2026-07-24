import { useState } from "react";
import { useNavigate } from "react-router-dom";
import toast from "react-hot-toast";
import { useAuth } from "../../context/AuthContext";

export default function AdminLogin() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      navigate("/admin");
    } catch {
      toast.error("Incorrect email or password");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-ink px-6">
      <form onSubmit={handleSubmit} className="w-full max-w-sm bg-ink-alt border border-ink-border rounded-xl p-8">
        <h1 className="font-display text-2xl mb-6 text-center">Admin Login</h1>

        <label className="block text-sm font-mono mb-1 text-paper/70">Email</label>
        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 bg-ink border border-ink-border rounded-lg px-3 py-2"
        />

        <label className="block text-sm font-mono mb-1 text-paper/70">Password</label>
        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-6 bg-ink border border-ink-border rounded-lg px-3 py-2"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-signal text-ink font-mono py-2 rounded-lg disabled:opacity-50"
        >
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
