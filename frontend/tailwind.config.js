/**
 * Design tokens for the "Signal Line" theme:
 * a dark, ink-toned portfolio with a warm amber accent that traces a
 * vertical "signal" through the page connecting each section — a nod to a
 * career timeline / transmission of a signal from experience to project.
 */
export default {
  darkMode: "class",
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#14161A",
          alt: "#1C1F26",
          border: "#2A2E37",
        },
        paper: {
          DEFAULT: "#FAF8F3",
          alt: "#F0EDE4",
          border: "#DED8C8",
        },
        signal: {
          DEFAULT: "#E8A33D", // warm amber — primary accent / signature signal color
          dim: "#B87F2E",
        },
        pulse: {
          DEFAULT: "#4FD1C5", // cool teal — secondary accent for links/highlights
        },
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "monospace"],
      },
      animation: {
        "fade-up": "fadeUp 0.6s ease-out forwards",
        "pulse-slow": "pulseSlow 3s ease-in-out infinite",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: 0, transform: "translateY(16px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        pulseSlow: {
          "0%, 100%": { opacity: 0.6 },
          "50%": { opacity: 1 },
        },
      },
    },
  },
  plugins: [],
};
