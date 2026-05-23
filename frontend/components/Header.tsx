"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import {
    reportDownloadUrl,
    triggerDeployment,
    triggerSimulation,
} from "@/lib/api";

export function Header({ onRefresh }: { onRefresh: () => void }) {
    const [busy, setBusy] = useState(false);

    async function simulate() {
        setBusy(true);
        try {
            await triggerSimulation();
            onRefresh();
        } finally {
            setBusy(false);
        }
    }

    async function deploy() {
        setBusy(true);
        try {
            await triggerDeployment();
            onRefresh();
        } finally {
            setBusy(false);
        }
    }

    return (
        <header className="flex items-center justify-between mb-6 flex-wrap gap-3">
            <div className="flex items-center gap-3">
                <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="w-9 h-9 rounded-xl bg-accent/20 border border-accent/40 flex items-center justify-center shadow-glow"
                >
                    <span className="text-accent text-lg font-bold">⚡</span>
                </motion.div>
                <div>
                    <h1 className="text-xl font-bold tracking-tight">IncidentIQ</h1>
                    <p className="text-xs text-white/50">
                        AI-powered incident analysis · live log intelligence
                    </p>
                </div>
            </div>

            <div className="flex items-center gap-2">
                <button
                    onClick={deploy}
                    disabled={busy}
                    className="text-sm px-3 py-2 rounded-lg border border-border bg-panel2 hover:bg-panel transition disabled:opacity-50"
                    title="Record a fake deployment so the AI can correlate it with future incidents"
                >
                    🚀 Mark Deployment
                </button>
                <a
                    href={reportDownloadUrl()}
                    download="incident-report.md"
                    className="text-sm px-3 py-2 rounded-lg border border-border bg-panel2 hover:bg-panel transition"
                >
                    ⬇ Report
                </a>
                <button
                    onClick={simulate}
                    disabled={busy}
                    className="text-sm px-4 py-2 rounded-lg bg-accent/20 border border-accent/40 hover:bg-accent/30 transition shadow-glow disabled:opacity-50"
                >
                    {busy ? "Simulating…" : "🔥 Simulate Incident"}
                </button>
            </div>
        </header>
    );
}
