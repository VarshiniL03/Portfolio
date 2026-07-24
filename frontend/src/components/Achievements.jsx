import { motion } from "framer-motion";

export default function Achievements({ items = [] }) {
  return (
    <section id="achievements" className="relative py-24 px-6 max-w-4xl mx-auto">
      <div className="signal-line hidden md:block" aria-hidden="true" />
      <h2 className="font-display text-3xl md:text-4xl mb-12 text-center">Achievements</h2>

      {items.length === 0 && (
        <p className="text-center text-paper/50">No achievements yet — add some from the admin panel.</p>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        {items.map((item, i) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05 }}
            className="bg-ink-alt border border-ink-border rounded-xl p-6"
          >
            <span className="font-mono text-xs uppercase text-signal">{item.type}</span>
            <h3 className="font-display text-lg mt-2">{item.title}</h3>
            <p className="text-paper/70 text-sm mt-1">{item.issuer}</p>
            {item.description && <p className="text-paper/60 text-sm mt-2">{item.description}</p>}
            {item.credential_url && (
              <a href={item.credential_url} target="_blank" rel="noreferrer" className="text-pulse text-sm mt-2 inline-block">
                View credential →
              </a>
            )}
          </motion.div>
        ))}
      </div>
    </section>
  );
}
