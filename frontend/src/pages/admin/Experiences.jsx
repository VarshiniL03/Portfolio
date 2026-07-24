import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import {
  listExperiences,
  createExperience,
  updateExperience,
  deleteExperience,
} from "../../api/resources";

const EMPTY = {
  company: "",
  role: "",
  location: "",
  start_date: "",
  end_date: "",
  description: "",
  order_index: 0,
  is_visible: true,
};

export default function AdminExperiences() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    const res = await listExperiences(true);
    setItems(res.data);
  }

  useEffect(() => {
    load();
  }, []);

  function startEdit(item) {
    setEditingId(item.id);
    setForm({ ...item, end_date: item.end_date || "" });
  }

  function resetForm() {
    setEditingId(null);
    setForm(EMPTY);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { ...form, end_date: form.end_date || null };
      if (editingId) {
        await updateExperience(editingId, payload);
        toast.success("Experience updated");
      } else {
        await createExperience(payload);
        toast.success("Experience added");
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
    if (!confirm("Delete this entry?")) return;
    await deleteExperience(id);
    toast.success("Deleted");
    load();
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-6">Experience</h1>

      <form onSubmit={handleSubmit} className="bg-ink-alt border border-ink-border rounded-xl p-6 mb-8 grid md:grid-cols-2 gap-4">
        <input
          placeholder="Company"
          required
          value={form.company}
          onChange={(e) => setForm({ ...form, company: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Role / Title"
          required
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          placeholder="Location"
          value={form.location || ""}
          onChange={(e) => setForm({ ...form, location: e.target.value })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <input
          type="number"
          placeholder="Order (lower = first)"
          value={form.order_index}
          onChange={(e) => setForm({ ...form, order_index: Number(e.target.value) })}
          className="bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <label className="text-sm font-mono text-paper/60">
          Start date
          <input
            type="date"
            required
            value={form.start_date}
            onChange={(e) => setForm({ ...form, start_date: e.target.value })}
            className="w-full mt-1 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
        </label>
        <label className="text-sm font-mono text-paper/60">
          End date (blank = current)
          <input
            type="date"
            value={form.end_date || ""}
            onChange={(e) => setForm({ ...form, end_date: e.target.value })}
            className="w-full mt-1 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
        </label>
        <textarea
          placeholder="Description"
          value={form.description || ""}
          onChange={(e) => setForm({ ...form, description: e.target.value })}
          className="md:col-span-2 bg-ink border border-ink-border rounded-lg px-3 py-2 h-24"
        />
        <label className="flex items-center gap-2 text-sm font-mono">
          <input
            type="checkbox"
            checked={form.is_visible}
            onChange={(e) => setForm({ ...form, is_visible: e.target.checked })}
          />
          Visible on homepage
        </label>

        <div className="md:col-span-2 flex gap-3">
          <button type="submit" disabled={loading} className="bg-signal text-ink font-mono px-5 py-2 rounded-lg">
            {editingId ? "Save changes" : "Add experience"}
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
              <p className="font-display">{item.role} · {item.company}</p>
              <p className="text-paper/50 text-sm font-mono">
                {item.start_date} — {item.end_date || "present"} {!item.is_visible && "(hidden)"}
              </p>
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
