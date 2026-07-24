import { motion } from "framer-motion";

export default function About({ content }) {
  if (!content?.about_text) return null;

  return (
    <section id="about" className="relative py-24 px-6 max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
      >
        <h2 className="font-display text-3xl md:text-4xl mb-8 text-center">About</h2>
        <p className="text-paper/80 text-lg leading-relaxed whitespace-pre-line text-center">
          {content.about_text}
        </p>
      </motion.div>
    </section>
  );
}