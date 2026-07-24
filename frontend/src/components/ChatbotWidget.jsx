import { useState, useRef, useEffect } from "react";
import { MessageCircle, X, Send, Download, Mail, Linkedin } from "lucide-react";
import { sendChatMessage } from "../api/resources";

function getSessionId() {
  let id = sessionStorage.getItem("chat_session_id");
  if (!id) {
    id = crypto.randomUUID();
    sessionStorage.setItem("chat_session_id", id);
  }
  return id;
}

const ACTION_ICONS = {
  resume: Download,
  email: Mail,
  linkedin: Linkedin,
};

function ActionButton({ action }) {
  const Icon = ACTION_ICONS[action.type] || Download;
  const isDownload = action.type === "resume";
  return (
    <a
      href={action.url}
      download={isDownload}
      target={action.type === "linkedin" || action.type === "email" ? "_blank" : undefined}
      rel={action.type === "linkedin" || action.type === "email" ? "noreferrer" : undefined}
      className="inline-flex items-center gap-2 bg-signal text-ink font-mono text-xs px-3 py-2 rounded-full mt-2 mr-2 hover:bg-signal-dim transition-colors"
    >
      <Icon size={14} />
      {action.label}
    </a>
  );
}

export default function ChatbotWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState([
    { role: "bot", text: "Hi! Ask me anything about my background, projects, or resume.", actions: [] },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  async function handleSend(e) {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending) return;

    setMessages((m) => [...m, { role: "user", text, actions: [] }]);
    setInput("");
    setSending(true);

    try {
      const res = await sendChatMessage(getSessionId(), text);
      setMessages((m) => [...m, { role: "bot", text: res.data.reply, actions: res.data.actions || [] }]);
    } catch {
      setMessages((m) => [
      ...m,
      { role: "bot", text: "Something went wrong on my end — please try again in a moment.", actions: [] },
    ]);
  } finally {
    setSending(false);
  }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {open && (
        <div className="mb-4 w-80 sm:w-96 h-[28rem] bg-ink-alt border border-ink-border rounded-2xl shadow-2xl flex flex-col overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-ink-border">
            <span className="font-mono text-sm text-signal">Ask me anything</span>
            <button onClick={() => setOpen(false)} aria-label="Close chat">
              <X size={18} />
            </button>
          </div>

          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-3 space-y-3">
            {messages.map((m, i) => (
              <div
                key={i}
                className={`max-w-[90%] text-sm rounded-lg px-3 py-2 ${
                  m.role === "user"
                    ? "bg-signal text-ink ml-auto"
                    : "bg-ink border border-ink-border text-paper/90"
                }`}
              >
                <div>{m.text}</div>
                {m.actions?.length > 0 && (
                  <div className="flex flex-wrap">
                    {m.actions.map((action, idx) => (
                      <ActionButton key={idx} action={action} />
                    ))}
                  </div>
                )}
              </div>
            ))}
            {sending && <div className="text-paper/40 text-xs font-mono">thinking…</div>}
          </div>

          <form onSubmit={handleSend} className="flex items-center gap-2 p-3 border-t border-ink-border">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a question…"
              className="flex-1 bg-ink border border-ink-border rounded-full px-4 py-2 text-sm focus:outline-none"
            />
            <button
              type="submit"
              disabled={sending}
              aria-label="Send message"
              className="bg-signal text-ink rounded-full p-2 disabled:opacity-50"
            >
              <Send size={16} />
            </button>
          </form>
        </div>
      )}

      <button
        onClick={() => setOpen((o) => !o)}
        aria-label="Toggle chat widget"
        className="bg-signal text-ink rounded-full p-4 shadow-xl hover:bg-signal-dim transition-colors animate-pulse-slow"
      >
        {open ? <X size={22} /> : <MessageCircle size={22} />}
      </button>
    </div>
  );
}
