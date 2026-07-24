import { Mail, Github, Linkedin, Twitter } from "lucide-react";

const ICONS = { github: Github, linkedin: Linkedin, twitter: Twitter };

export default function Contact({ content }) {
  const links = content?.social_links || {};
  const gmailComposeUrl = content?.contact_email
    ? `https://mail.google.com/mail/?view=cm&fs=1&to=${content.contact_email}`
    : null;

  return (
    <section id="contact" className="relative py-24 px-6 max-w-2xl mx-auto text-center">
      <div
        className="absolute inset-y-0 left-1/2 -translate-x-1/2 w-screen -z-10 opacity-[0.18]"
        style={{
          backgroundImage: "radial-gradient(circle, #4FD1C5 1px, transparent 1px)",
          backgroundSize: "24px 24px",
        }}
      />
      <h2 className="font-display text-3xl md:text-4xl mb-6">Get in touch</h2>
      <p className="text-paper/70 mb-8">
        {content?.contact_location ? `Based in ${content.contact_location}. ` : ""}
        Feel free to reach out — I'd love to hear from you.
      </p>

      {gmailComposeUrl && (
        <a href={gmailComposeUrl} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 bg-signal text-ink font-mono px-6 py-3 rounded-full hover:bg-signal-dim transition-colors mb-8">
          <Mail size={18} />
          Email Me
        </a>
      )}

      <div className="flex justify-center gap-6">
        {Object.entries(links).map(([platform, url]) => {
          const Icon = ICONS[platform.toLowerCase()];
          if (!Icon || !url) return null;
          return (
            <a key={platform} href={url} target="_blank" rel="noreferrer" className="text-paper/60 hover:text-signal">
              <Icon size={22} />
            </a>
          );
        })}
      </div>
    </section>
  );
}