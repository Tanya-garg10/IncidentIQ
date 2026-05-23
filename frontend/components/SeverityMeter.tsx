"use client";

import { motion } from "framer-motion";
import type { Severity } from "@/lib/api";

const ORDER: Severity[] = ["INFO", "WARNING", "ERROR", "CRITICAL"];
const LABEL: Record<Severity, string> = {
    INFO: "Low",
    WARNING: "Medium",
    ERROR: "High",
    CRITICAL: "Critical",
};
const COLOR: Record<Severity, string> = {
    INFO: "bg-info",
    WARNING: "bg-warn",
    ERROR: "bg-err",
    CRITICAL: "bg-crit",
};

export function SeverityMeter({ level }: { level: Severity }) {
    const idx = ORDER.indexOf(level);
    const pct = ((idx + 1) / ORDER.length) * 100;

    return (
        <div className="glass rounded-2xl p-5">
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold tracking-wide text-white/90">
                    OVERALL SEVERITY
                </h3>
                <span className="text-xs text-white/50">{LABEL[level]}</span>
            </div>

            <div className="h-3 w-full bg-panel2 rounded-full overflow-hidden">
                <motion.div
                    className={`h-full ${COLOR[level]}`}
                    initial={{ width: 0 }}
                    animate={{ width: `${pct}%` }}
                    transition={{ duration: 0.6, ease: "easeOut" }}
                />
            </div>

            <div className="mt-2 grid grid-cols-4 text-[10px] text-white/40">
                {ORDER.map((l) => (
                    <span key={l} className={l === level ? "text-white/90" : ""}>
                        {LABEL[l]}
                    </span>
                ))}
            </div>
        </div>
    );
}
