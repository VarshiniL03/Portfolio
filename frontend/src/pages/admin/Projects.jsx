import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import { listProjects, createProject, updateProject, deleteProject } from "../../api/resources";

const EMPTY = {
  title: "",
  summary: "",
  description: "",
  tech_stack: "",
  image_url: "",
  repo_url: "",
  live_url: "",
  featured: false,
  order_index: 0,
  is_visible: true,
};

export default function AdminProjects() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    const res = await listProjects(true);
    setItems(res.data);
  }

  useEffect(() => {
    load();
  }, []);

  function startEdit(item) {
    setEditingId(item.id);
    setForm({ ...item, tech_stack: (item.tech_stack || []).join(", ") });
  }

  function resetForm() {
    setEditingId(null);
    setForm(EMPTY);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        ...form,
        tech_stack: form.tech_stack
          ? form.tech_stack.split(",").map((t) => t.trim()).filter(Boolean)
          : [],
      };
      if (editingId) {
        await updateProject(editingId, payload);
        toast.success("Project updated");
      } else {
        await createProject(payload);
        toast.success("Project added");
      }
      resetForm();
      load();
    } catch {
      toast.error("Something went wrong — check the form and try again");
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this project?")) return;
    await deleteProject(id);
    toast.success("Deleted");
    load();
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-6">Projects</h1>

      <form onSubmit={handleSubmit} className="bg-ink-alt border border-ink-border rounded-xl p-6 mb-8 grid md:grid-cols-2 gap-4">
        <input
          placeholder="Title"
          required
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Short summary (shown on card)"
          value={form.summary || ""}
          onChange={(e) => setForm({ ...form, summary: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Image URL"
          value={form.image_url || ""}
          onChange={(e) => setForm({ ...form, image_url: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Tech stack (comma-separated)"
          value={form.tech_stack}
          onChange={(e) => setForm({ ...form, tech_stack: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Repo URL"
          value={form.repo_url || ""}
          onChange={(e) => setForm({ ...form, repo_url: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Live URL"
          value={form.live_url || ""}
          onChange={(e) => setForm({ ...form, live_url: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <textarea
          placeholder="Full description"
          value={form.description || ""}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="md:col-span-2 bg-ink border border-ink-border rounded-lg px-3 py-2 h-24"
        />
        <label className="flex items-center gap-2 text-sm font-mono">
          <input type="checkbox" checked={form.featured} onChange={(e) => setForm({ ...form, featured: e.target.checked })} />
          Featured
        </label>
        <label className="flex items-center gap-2 text-sm font-mono">
          <input type="checkbox" checked={form.is_visible} onChange={(e) => setForm({ ...form, is_visible: e.target.checked })} />
          Visible on homepage
        </label>

        <div className="md:col-span-2 flex gap-3">
          <button type="submit" disabled={loading} className="bg-signal text-ink font-mono px-5 py-2 rounded-lg">
            {editingId ? "Save changes" : "Add project"}
          </button>
          {editingId && (
            <button type="button" onClick={resetForm} className="font-mono px-5 py-2 rounded-lg border border-ink-border">
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item.id} className="flex justify-between items-center bg-ink-alt border border-ink-border rounded-lg p-4">
            <div>
              <p className="font-display">{item.title}</p>
              <p className="text-paper/50 text-sm font-mono">{!item.is_visible && "(hidden)"}</p>
            </div>
            <div className="flex gap-3 font-mono text-sm">
              <button onClick={() => startEdit(item)} className="text-pulse">Edit</button>
              <button onClick={() => handleDelete(item.id)} className="text-red-400">Delete</button>
            </div>
          </div>
        ))}
      </div>
    </AdminLayout>
  );
}
