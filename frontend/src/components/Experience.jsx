import { motion } from "framer-motion";

function formatRange(start, end) {
  const fmt = (d) => new Date(d).toLocaleDateString(undefined, { month: "short", year: "numeric" });
  return `${fmt(start)} — ${end ? fmt(end) : "Present"}`;
}

export default function Experience({ items = [] }) {
  return (
    <section id="experience" className="relative py-24 px-6 max-w-4xl mx-auto">
      <div className="signal-line hidden md:block" aria-hidden="true" />
      <h2 className="font-display text-3xl md:text-4xl mb-12 text-center">Experience</h2>

      {items.length === 0 && (
        <p className="text-center text-paper/50">No experience entries yet — add some from the admin panel.</p>
      )}

      <div className="space-y-10">
        {items.map((exp, i) => (
          <motion.div
            key={exp.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05 }}
            className="relative bg-ink-alt border border-ink-border rounded-xl p-6"
          >
            <div className="flex flex-wrap justify-between gap-2 mb-2">
              <h3 className="font-display text-xl">{exp.role}</h3>
              <span className="font-mono text-xs text-signal">{formatRange(exp.start_date, exp.end_date)}</span>
            </div>
            <p className="text-paper/70 text-sm mb-3">
              {exp.company}
              {exp.location ? ` · ${exp.location}` : ""}
            </p>
            {exp.description && <p className="text-paper/80 leading-relaxed">{exp.description}</p>}
          </motion.div>
        ))}
      </div>
    </section>
  );
}
