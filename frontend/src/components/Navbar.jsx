import { useState } from "react";
import { Menu, X } from "lucide-react";

const LINKS = [
  { id: "experience", label: "Experience" },
  { id: "projects", label: "Projects" },
  { id: "education", label: "Education" },
  { id: "achievements", label: "Achievements" },
  { id: "resume", label: "Resume" },
  { id: "contact", label: "Contact" },
];

export default function Navbar() {
  const [open, setOpen] = useState(false);

  function scrollTo(id) {
    setOpen(false);
    document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-40 backdrop-blur bg-ink/70 dark:bg-ink/70 border-b border-ink-border">
      <nav className="max-w-6xl mx-auto flex items-center justify-between px-6 py-4">
        <button onClick={() => scrollTo("hero")} className="font-display text-lg text-signal">
          &#9673; portfolio
        </button>

        <div className="hidden md:flex items-center gap-8">
          {LINKS.map((link) => (
            <button
              key={link.id}
              onClick={() => scrollTo(link.id)}
              className="text-sm font-mono tracking-wide text-paper/80 hover:text-signal transition-colors"
            >
              {link.label}
            </button>
          ))}
        </div>

        <button className="md:hidden" onClick={() => setOpen((o) => !o)} aria-label="Toggle menu">
          {open ? <X /> : <Menu />}
        </button>
      </nav>

      {open && (
        <div className="md:hidden flex flex-col gap-4 px-6 pb-6">
          {LINKS.map((link) => (
            <button
              key={link.id}
              onClick={() => scrollTo(link.id)}
              className="text-left text-sm font-mono text-paper/80"
            >
              {link.label}
            </button>
          ))}
        </div>
      )}
    </header>
  );
}
