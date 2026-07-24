import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import AdminLayout from "../../components/AdminLayout";
import { getActiveResume, uploadResume } from "../../api/resources";

export default function AdminResume() {
  const [resume, setResume] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  function load() {
    getActiveResume().then((res) => setResume(res.data));
  }

  useEffect(() => {
    load();
  }, []);

  async function handleUpload(e) {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    try {
      await uploadResume(file);
      toast.success("Resume uploaded");
      setFile(null);
      load();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AdminLayout>
      <h1 className="font-display text-2xl mb-6">Resume</h1>

      <div className="bg-ink-alt border border-ink-border rounded-xl p-6 max-w-md">
        <p className="text-paper/70 mb-4">
          Current file: <span className="font-mono text-signal">{resume?.file_name || "none uploaded"}</span>
        </p>

        <form onSubmit={handleUpload} className="space-y-4">
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full text-sm"
          />
          <button
            type="submit"
            disabled={!file || loading}
            className="bg-signal text-ink font-mono px-5 py-2 rounded-lg disabled:opacity-50"
          >
            {loading ? "Uploading…" : "Upload new resume"}
          </button>
        </form>
        <p className="text-paper/40 text-xs mt-3 font-mono">PDF only, max 5MB.</p>
      </div>
    </AdminLayout>
  );
}
