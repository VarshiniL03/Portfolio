import { motion } from "framer-motion";

function formatRange(start, end) {
  if (!start) return "";
  const fmt = (d) => new Date(d).toLocaleDateString(undefined, { month: "short", year: "numeric" });
  return `${fmt(start)} — ${end ? fmt(end) : "Present"}`;
}

export default function Education({ items = [] }) {
  return (
    <section id="education" className="relative py-24 px-6 max-w-4xl mx-auto">
      <div className="absolute inset-y-0 left-1/2 -translate-x-1/2 w-screen -z-10 opacity-[0.15]" style={{ backgroundImage: "radial-gradient(circle, #4FD1C5 1px, transparent 1px)", backgroundSize: "24px 24px" }} />

      <h2 className="font-display text-3xl md:text-4xl mb-12 text-center">Education</h2>

      {items.length === 0 && (
        <p className="text-center text-paper/50">No education entries yet — add some from the admin panel.</p>
      )}

      <div className="space-y-6">
        {items.map((item, i) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05 }}
            className="bg-ink-alt border border-ink-border rounded-xl p-6"
          >
            <div className="flex flex-wrap justify-between gap-2 mb-2">
              <h3 className="font-display text-lg">{item.degree}</h3>
              <span className="font-mono text-xs text-signal">{formatRange(item.start_date, item.end_date)}</span>
            </div>
            <p className="text-paper/70 text-sm mb-2">
              {item.institution}
              {item.location ? ` · ${item.location}` : ""}
              {item.grade ? ` · ${item.grade}` : ""}
            </p>
            {item.description && <p className="text-paper/80 leading-relaxed">{item.description}</p>}
          </motion.div>
        ))}
      </div>
    </section>
  );
}
