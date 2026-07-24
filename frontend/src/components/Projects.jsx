import { motion } from "framer-motion";
import { Github, ExternalLink } from "lucide-react";

export default function Projects({ items = [] }) {
  return (
    <section id="projects" className="relative py-24 px-6 max-w-6xl mx-auto">
      <h2 className="font-display text-3xl md:text-4xl mb-12 text-center">Projects</h2>

      {items.length === 0 && (
        <p className="text-center text-paper/50">No projects yet — add some from the admin panel.</p>
      )}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {items.map((p, i) => (
          <motion.div
            key={p.id}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.05 }}
            whileHover={{ y: -6 }}
            className="group relative bg-ink-alt border border-ink-border rounded-xl overflow-hidden flex flex-col hover:border-signal/60 transition-colors"
          >
            {p.image_url && (
              <>
                <div
                  className="absolute inset-0 z-0 bg-cover bg-center blur-xl scale-110 opacity-30"
                  style={{ backgroundImage: `url(${p.image_url})` }}
                />
                <div className="absolute inset-0 z-0 bg-ink-alt/80" />
              </>
            )}

            <div className="relative z-10 flex flex-col flex-1">
              {p.image_url && (
                <div className="overflow-hidden h-40">
                  <img
                    src={p.image_url}
                    alt={p.title}
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-110"
                  />
                </div>
              )}
              <div className="p-6 flex flex-col flex-1">
                <h3 className="font-display text-lg mb-2 group-hover:text-signal transition-colors">{p.title}</h3>
                <p className="text-paper/70 text-sm flex-1">{p.summary}</p>

                {p.tech_stack?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mt-4">
                    {p.tech_stack.map((t) => (
                      <span key={t} className="font-mono text-xs px-2 py-1 rounded bg-ink border border-ink-border text-pulse">
                        {t}
                      </span>
                    ))}
                  </div>
                )}

                <div className="flex gap-4 mt-4">
                  {p.repo_url && (
                    <a href={p.repo_url} target="_blank" rel="noreferrer" className="text-paper/60 hover:text-signal transition-colors">
                      <Github size={18} />
                    </a>
                  )}
                  {p.live_url && (
                    <a href={p.live_url} target="_blank" rel="noreferrer" className="text-paper/60 hover:text-signal transition-colors">
                      <ExternalLink size={18} />
                    </a>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}