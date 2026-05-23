"use client";

import { motion } from "framer-motion";
import { severityBadge, type Incident } from "@/lib/api";

export function IncidentList({ incidents }: { incidents: Incident[] }) {
    return (
        <div className="glass rounded-2xl p-5">
            <h3 className="text-sm font-semibold tracking-wide text-white/90 mb-4">
                ACTIVE INCIDENTS · {incidents.length}
            </h3>

            {incidents.length === 0 ? (
                <p className="text-sm text-white/60">No active incidents.</p>
            ) : (
                <div className="space-y-3">
                    {incidents.map((inc, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="rounded-xl border border-border bg-panel2 p-4"
                        >
                            <div className="flex items-center justify-between mb-2">
                                <h4 className="font-semibold text-white">{inc.issue}</h4>
                                <span
                                    className={`text-[10px] font-bold px-2 py-0.5 rounded ${severityBadge(
                                        inc.severity
                                    )}`}
                                >
                                    {inc.severity}
                                </span>
                            </div>
                            <p className="text-xs text-white/70 mb-1">
                                <span className="text-white/50">Root cause:</span> {inc.cause}
                            </p>
                            <p className="text-xs text-white/70 mb-2">
                                <span className="text-white/50">Suggested fix:</span>{" "}
                                {inc.solution}
                            </p>
                            {inc.recommendations && inc.recommendations.length > 0 && (
                                <ul className="mt-2 space-y-1">
                                    {inc.recommendations.map((rec, j) => (
                                        <li
                                            key={j}
                                            className="text-xs text-white/80 flex items-start gap-2"
                                        >
                                            <span className="text-accent">→</span>
                                            {rec}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    );
}
