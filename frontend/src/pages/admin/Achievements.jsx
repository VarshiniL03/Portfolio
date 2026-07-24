import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import {
  listAchievements,
  createAchievement,
  updateAchievement,
  deleteAchievement,
} from "../../api/resources";

const EMPTY = {
  type: "certification",
  title: "",
  issuer: "",
  date: "",
  credential_url: "",
  description: "",
  order_index: 0,
  is_visible: true,
};

export default function AdminAchievements() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    const res = await listAchievements(true);
    setItems(res.data);
  }

  useEffect(() => {
    load();
  }, []);

  function startEdit(item) {
    setEditingId(item.id);
    setForm({ ...item, date: item.date || "" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(EMPTY);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...form, date: form.date || null };
      if (editingId) {
        await updateAchievement(editingId, payload);
        toast.success("Achievement updated");
      } else {
        await createAchievement(payload);
        toast.success("Achievement added");
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
    if (!confirm("Delete this achievement?")) return;
    await deleteAchievement(id);
    toast.success("Deleted");
    load();
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-6">Achievements</h1>

      <form onSubmit={handleSubmit} className="bg-ink-alt border border-ink-border rounded-xl p-6 mb-8 grid md:grid-cols-2 gap-4">
        <select
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        >
          <option value="certification">Certification</option>
          <option value="award">Award</option>
          <option value="publication">Publication</option>
          <option value="other">Other</option>
        </select>
        <input
          placeholder="Title"
          required
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Issuer / Organization"
          value={form.issuer || ""}
          onChange={(e) => setForm({ ...form, issuer: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Credential URL"
          value={form.credential_url || ""}
          onChange={(e) => setForm({ ...form, credential_url: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <label className="text-sm font-mono text-paper/60">
          Date
          <input
            type="date"
            value={form.date || ""}
            onChange={(e) => setForm({ ...form, date: e.target.value })}
            className="w-full mt-1 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
        </label>
        <textarea
          placeholder="Description"
          value={form.description || ""}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="md:col-span-2 bg-ink border border-ink-border rounded-lg px-3 py-2 h-20"
        />
        <label className="flex items-center gap-2 text-sm font-mono">
          <input type="checkbox" checked={form.is_visible} onChange={(e) => setForm({ ...form, is_visible: e.target.checked })} />
          Visible on homepage
        </label>

        <div className="md:col-span-2 flex gap-3">
          <button type="submit" disabled={loading} className="bg-signal text-ink font-mono px-5 py-2 rounded-lg">
            {editingId ? "Save changes" : "Add achievement"}
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
              <p className="text-paper/50 text-sm font-mono">{item.issuer} {!item.is_visible && "(hidden)"}</p>
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
