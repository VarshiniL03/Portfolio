import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import { listFaqs, createFaq, updateFaq, deleteFaq } from "../../api/resources";

const EMPTY = { question: "", answer: "", is_visible: true };

export default function AdminFaqs() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [editingId, setEditingId] = useState(null);

  async function load() {
    const res = await listFaqs();
    setItems(res.data);
  }

  useEffect(() => {
    load();
  }, []);

  function resetForm() {
    setEditingId(null);
    setForm(EMPTY);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (editingId) {
        await updateFaq(editingId, form);
        toast.success("FAQ updated");
      } else {
        await createFaq(form);
        toast.success("FAQ added");
      }
      resetForm();
      load();
    } catch {
      toast.error("Something went wrong");
    }
  }

  async function handleDelete(id) {
    if (!confirm("Delete this FAQ entry?")) return;
    await deleteFaq(id);
    load();
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-2">Chatbot FAQs</h1>
      <p className="text-paper/60 mb-6 text-sm">
        These Q&amp;A pairs are given to the chatbot as extra context, alongside your experience,
        projects, and qualifications. Use them for anything visitors commonly ask that isn't
        already covered elsewhere.
      </p>

      <form onSubmit={handleSubmit} className="bg-ink-alt border border-ink-border rounded-xl p-6 mb-8 space-y-3 max-w-2xl">
        <input
          placeholder="Question"
          required
          value={form.question}
          onChange={(e) => setForm({ ...form, question: e.target.value })}
          className="w-full bg-ink border border-ink-border rounded-lg px-3 py-2"
        />
        <textarea
          placeholder="Answer"
          required
          value={form.answer}
          onChange={(e) => setForm({ ...form, answer: e.target.value })}
          className="w-full bg-ink border border-ink-border rounded-lg px-3 py-2 h-24"
        />
        <div className="flex gap-3">
          <button type="submit" className="bg-signal text-ink font-mono px-5 py-2 rounded-lg">
            {editingId ? "Save changes" : "Add FAQ"}
          </button>
          {editingId && (
            <button type="button" onClick={resetForm} className="font-mono px-5 py-2 rounded-lg border border-ink-border">
              Cancel
            </button>
          )}
        </div>
      </form>

      <div className="space-y-3 max-w-2xl">
        {items.map((item) => (
          <div key={item.id} className="bg-ink-alt border border-ink-border rounded-lg p-4">
            <div className="flex justify-between items-start">
              <p className="font-display">{item.question}</p>
              <div className="flex gap-3 font-mono text-sm shrink-0 ml-4">
                <button onClick={() => { setEditingId(item.id); setForm(item); }} className="text-pulse">Edit</button>
                <button onClick={() => handleDelete(item.id)} className="text-red-400">Delete</button>
              </div>
            </div>
            <p className="text-paper/60 text-sm mt-1">{item.answer}</p>
          </div>
        ))}
      </div>
    </AdminLayout>
  );
}