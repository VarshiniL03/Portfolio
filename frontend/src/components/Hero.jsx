import { motion } from "framer-motion";
import bgImage from "../assets/image.jpg";
import SectionDivider from "./SectionDivider";
export default function Hero({ content }) {
  const name = content?.hero_name || "Your Name";
  const title = content?.hero_title || "Software Engineer";
  const tagline = content?.hero_tagline || "I build things for the web.";
  const about = content?.about_text;

  return (
    <section id="hero" className="relative min-h-screen flex items-center px-6 pt-24">
      <div
        className="absolute inset-0 z-0 bg-cover bg-center blur-md scale-x-110 scale-y-95"
        style={{ backgroundImage: `url(${bgImage})` }}
      />
      <div className="absolute inset-0 z-0 bg-ink/50" />
      <div className="signal-line hidden md:block" aria-hidden="true" />

      <div className="max-w-4xl mx-auto text-center relative z-10">
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="font-mono text-signal text-sm tracking-widest uppercase mb-4"
        >
          {title}
        </motion.p>
        <motion.h1
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="font-display text-5xl md:text-7xl font-semibold leading-tight mb-6"
        >
          {name}
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-lg md:text-xl text-paper/70 max-w-2xl mx-auto"
        >
          {tagline}
        </motion.p>

        {about && (
          <motion.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-base text-paper/60 max-w-xl mx-auto mt-6 leading-relaxed whitespace-pre-line"
          >
            {about}
          </motion.p>
        )}
      <div className="absolute -bottom-12 left-0 right-0 z-10 px-6">
      <SectionDivider />
      </div>
    </div>
    </section>
  );
}