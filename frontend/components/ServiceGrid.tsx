"use client";

import { motion } from "framer-motion";
import type { ServiceHealth } from "@/lib/api";

const STATUS_STYLE: Record<ServiceHealth["status"], string> = {
    healthy: "border-info/40 bg-info/10 text-info",
    warning: "border-warn/40 bg-warn/10 text-warn",
    degraded: "border-err/40 bg-err/10 text-err",
    down: "border-crit/50 bg-crit/15 text-crit shadow-glowRed",
};

const DOT: Record<ServiceHealth["status"], string> = {
    healthy: "bg-info",
    warning: "bg-warn",
    degraded: "bg-err",
    down: "bg-crit animate-pulseSlow",
};

export function ServiceGrid({ services }: { services: ServiceHealth[] }) {
    return (
        <div className="glass rounded-2xl p-5">
            <h3 className="text-sm font-semibold tracking-wide text-white/90 mb-4">
                SERVICE HEALTH
            </h3>
            {services.length === 0 ? (
                <p className="text-sm text-white/60">No service data yet.</p>
            ) : (
                <div className="grid grid-cols-2 gap-3">
                    {services.map((s, i) => (
                        <motion.div
                            key={s.service}
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className={`rounded-xl border p-3 ${STATUS_STYLE[s.status]}`}
                        >
                            <div className="flex items-center justify-between mb-1">
                                <span className="font-mono text-xs text-white/85">
                                    {s.service}
                                </span>
                                <span
                                    className={`w-2 h-2 rounded-full ${DOT[s.status]}`}
                                />
                            </div>
                            <div className="text-2xl font-bold tabular-nums">
                                {s.score}
                                <span className="text-xs text-white/40 font-normal ml-1">
                                    /100
                                </span>
                            </div>
                            <div className="text-[10px] uppercase tracking-wider opacity-80">
                                {s.status}
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    );
}
