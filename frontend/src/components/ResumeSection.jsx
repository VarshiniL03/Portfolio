import { Download } from "lucide-react";
import cornerLeft from "../assets/corner-left.png";
import cornerRight from "../assets/corner-right.png";

export default function ResumeSection({ resume }) {
  return (
    <section id="resume" className="relative py-24 px-6 max-w-2xl mx-auto text-center overflow-hidden">
      <img src={cornerLeft} alt="" className="absolute inset-y-0 left-0 h-full w-32 md:w-48 object-cover opacity-25 pointer-events-none select-none" />
      <img src={cornerRight} alt="" className="absolute inset-y-0 right-0 h-full w-32 md:w-48 object-cover opacity-25 pointer-events-none select-none" />

      <h2 className="font-display text-3xl md:text-4xl mb-6">Resume</h2>
      <p className="text-paper/70 mb-8">
        Want the full picture? Grab a copy of my resume below.
      </p>

      {resume?.public_url ? (
        <a href={resume.public_url} download className="inline-flex items-center gap-2 bg-signal text-ink font-mono px-6 py-3 rounded-full hover:bg-signal-dim transition-colors">
          <Download size={18} />
          Download Resume
        </a>
      ) : (
        <p className="text-paper/40 font-mono text-sm">Resume not uploaded yet.</p>
      )}
    </section>
  );
}
