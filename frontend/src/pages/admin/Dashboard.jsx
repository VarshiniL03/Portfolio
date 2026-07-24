import { useState } from "react";
import { Link } from "react-router-dom";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import { triggerReindex } from "../../api/resources";

const CARDS = [
  { to: "/admin/site-content", title: "Homepage Content", desc: "Edit hero text, about, contact info & social links." },
  { to: "/admin/experiences", title: "Experience", desc: "Add, edit or remove work history entries." },
  { to: "/admin/projects", title: "Projects", desc: "Manage the projects shown on your homepage." },
  { to: "/admin/education", title: "Education", desc: "Degrees, institutions, and coursework." },
  { to: "/admin/achievements", title: "Achievements", desc: "Certifications, awards, and publications." },
  { to: "/admin/resume", title: "Resume", desc: "Upload a new resume PDF." },
  { to: "/admin/faqs", title: "Chatbot FAQs", desc: "Curate what the chatbot knows." },
];

export default function AdminDashboard() {
  const [reindexing, setReindexing] = useState(false);

  async function handleReindex() {
    setReindexing(true);
    try {
      const res = await triggerReindex();
      toast.success(`Chatbot knowledge base updated (${res.data.chunks_indexed} chunks indexed)`);
    } catch {
      toast.error("Reindex failed — check the backend logs");
    } finally {
      setReindexing(false);
    }
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-2">Welcome back</h1>
      <p className="text-paper/60 mb-6">Everything here updates your live homepage immediately.</p>

      <div className="bg-ink-alt border border-ink-border rounded-xl p-6 mb-8 flex items-center justify-between flex-wrap gap-4">
        <div>
          <h3 className="font-display text-lg mb-1">Chatbot Knowledge Base</h3>
          <p className="text-paper/60 text-sm">
            Rebuild the chatbot's search index after adding or editing content, so it can find and reference your latest changes.
          </p>
        </div>
        <button
          onClick={handleReindex}
          disabled={reindexing}
          className="bg-signal text-ink font-mono px-5 py-2 rounded-lg disabled:opacity-50 shrink-0"
        >
          {reindexing ? "Reindexing…" : "Reindex Knowledge Base"}
        </button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {CARDS.map((c) => (
          <Link
            key={c.to}
            to={c.to}
            className="block bg-ink-alt border border-ink-border rounded-xl p-6 hover:border-signal transition-colors"
          >
            <h3 className="font-display text-lg mb-1">{c.title}</h3>
            <p className="text-paper/60 text-sm">{c.desc}</p>
          </Link>
        ))}
      </div>
    </AdminLayout>
  );
}
