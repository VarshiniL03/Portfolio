import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import { getSiteContent, updateSiteContent } from "../../api/resources";

export default function AdminSiteContent() {
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    getSiteContent().then((res) => setForm(res.data));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await updateSiteContent(form);
      toast.success("Homepage content updated");
    } catch {
      toast.error("Failed to save — please try again");
    } finally {
      setLoading(false);
    }
  }

  if (!form) return <AdminLayout><p>Loading…</p></AdminLayout>;

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-6">Homepage Content</h1>

      <form onSubmit={handleSubmit} className="bg-ink-alt border border-ink-border rounded-xl p-6 space-y-6 max-w-2xl">
        <div>
          <h2 className="font-mono text-signal text-sm uppercase mb-3">Hero</h2>
          <input
            placeholder="Full name"
            value={form.hero_name}
            onChange={(e) => setForm({ ...form, hero_name: e.target.value })}
            className="w-full mb-2 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
          <input
            placeholder="Title (e.g. Full-Stack Engineer)"
            value={form.hero_title}
            onChange={(e) => setForm({ ...form, hero_title: e.target.value })}
            className="w-full mb-2 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
          <textarea
            placeholder="Tagline"
            value={form.hero_tagline}
            onChange={(e) => setForm({ ...form, hero_tagline: e.target.value })}
            className="w-full bg-ink border border-ink-border rounded-lg px-3 py-2 h-20"
          />
        </div>

        <div>
          <h2 className="font-mono text-signal text-sm uppercase mb-3">About</h2>
          <textarea
            placeholder="About text (used by chatbot too)"
            value={form.about_text}
            onChange={(e) => setForm({ ...form, about_text: e.target.value })}
            className="w-full bg-ink border border-ink-border rounded-lg px-3 py-2 h-28"
          />
        </div>

        <div>
          <h2 className="font-mono text-signal text-sm uppercase mb-3">Contact</h2>
          <input
            placeholder="Contact email"
            value={form.contact_email}
            onChange={(e) => setForm({ ...form, contact_email: e.target.value })}
            className="w-full mb-2 bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
          <input
            placeholder="Location"
            value={form.contact_location || ""}
            onChange={(e) => setForm({ ...form, contact_location: e.target.value })}
            className="w-full bg-ink border border-ink-border rounded-lg px-3 py-2"
          />
        </div>

        <div>
          <h2 className="font-mono text-signal text-sm uppercase mb-3">Social Links</h2>
          {["github", "linkedin", "twitter"].map((platform) => (
            <input
              key={platform}
              placeholder={`${platform} URL`}
              value={form.social_links?.[platform] || ""}
              onChange={(e) =>
                setForm({ ...form, social_links: { ...form.social_links, [platform]: e.target.value } })
              }
              className="w-full mb-2 bg-ink border border-ink-border rounded-lg px-3 py-2"
            />
          ))}
        </div>

        <button type="submit" disabled={loading} className="bg-signal text-ink font-mono px-5 py-2 rounded-lg">
          {loading ? "Saving…" : "Save changes"}
        </button>
      </form>
    </AdminLayout>
  );
}
