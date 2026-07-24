import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const NAV = [
  { to: "/admin", label: "Overview" },
  { to: "/admin/site-content", label: "Homepage Content" },
  { to: "/admin/experiences", label: "Experience" },
  { to: "/admin/projects", label: "Projects" },
  { to: "/admin/education", label: "Education" },
  { to: "/admin/achievements", label: "Achievements" },
  { to: "/admin/resume", label: "Resume" },
  { to: "/admin/faqs", label: "Chatbot FAQs" },
];

export default function AdminLayout({ children }) {
  const { user, logout } = useAuth();
  const location = useLocation();

  return (
    <div className="min-h-screen flex bg-ink text-paper">
      <aside className="w-60 border-r border-ink-border p-6 flex flex-col">
        <h2 className="font-display text-lg text-signal mb-8">Admin</h2>
        <nav className="flex-1 space-y-2">
          {NAV.map((item) => (
            <Link
              key={item.to}
              to={item.to}
              className={`block px-3 py-2 rounded-lg text-sm font-mono ${
                location.pathname === item.to ? "bg-ink-alt text-signal" : "text-paper/70 hover:bg-ink-alt"
              }`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
        <div className="border-t border-ink-border pt-4 text-sm">
          <p className="text-paper/60 mb-2">{user?.email}</p>
          <button onClick={logout} className="text-signal font-mono text-sm">
            Log out
          </button>
        </div>
      </aside>
      <main className="flex-1 p-8 overflow-y-auto">{children}</main>
    </div>
  );
}
