"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import { askChat } from "@/lib/api";

interface Message {
    role: "user" | "assistant";
    text: string;
}

const SUGGESTIONS = [
    "Why did the service crash?",
    "What should I do to fix this?",
    "Which service is most affected?",
];

export function ChatPanel() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState("");
    const [busy, setBusy] = useState(false);

    async function send(question: string) {
        if (!question.trim() || busy) return;
        setBusy(true);
        setMessages((m) => [...m, { role: "user", text: question }]);
        setInput("");
        try {
            const res = await askChat(question);
            setMessages((m) => [...m, { role: "assistant", text: res.answer }]);
        } catch {
            setMessages((m) => [
                ...m,
                { role: "assistant", text: "Couldn't reach the backend." },
            ]);
        } finally {
            setBusy(false);
        }
    }

    return (
        <div className="glass rounded-2xl p-5 flex flex-col">
            <h3 className="text-sm font-semibold tracking-wide text-white/90 mb-3">
                CHAT WITH YOUR INFRA 🤖
            </h3>

            <div className="scroll-y h-56 overflow-y-auto space-y-2 mb-3 pr-1">
                {messages.length === 0 && (
                    <div className="text-xs text-white/50">
                        Ask a question about your logs. Try one:
                        <div className="flex flex-wrap gap-1 mt-2">
                            {SUGGESTIONS.map((s) => (
                                <button
                                    key={s}
                                    onClick={() => send(s)}
                                    className="text-[11px] px-2 py-1 rounded-full border border-border bg-panel2 hover:bg-panel hover:border-accent/40 transition"
                                >
                                    {s}
                                </button>
                            ))}
                        </div>
                    </div>
                )}
                {messages.map((m, i) => (
                    <motion.div
                        key={i}
                        initial={{ opacity: 0, y: 4 }}
                        animate={{ opacity: 1, y: 0 }}
                        className={`text-sm rounded-lg px-3 py-2 ${m.role === "user"
                                ? "bg-accent/15 border border-accent/30 ml-6"
                                : "bg-panel2 border border-border mr-6"
                            }`}
                    >
                        {m.text}
                    </motion.div>
                ))}
                {busy && (
                    <div className="text-xs text-white/50 italic mr-6">thinking…</div>
                )}
            </div>

            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    send(input);
                }}
                className="flex gap-2"
            >
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask about your infrastructure…"
                    className="flex-1 bg-panel2 border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-accent/60"
                />
                <button
                    type="submit"
                    disabled={busy}
                    className="px-3 py-2 rounded-lg bg-accent/20 border border-accent/40 hover:bg-accent/30 transition text-sm disabled:opacity-50"
                >
                    Send
                </button>
            </form>
        </div>
    );
}
