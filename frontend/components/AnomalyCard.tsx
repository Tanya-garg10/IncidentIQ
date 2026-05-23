"use client";

import { motion } from "framer-motion";
import type { AnomalyInfo } from "@/lib/api";

export function AnomalyCard({
    anomaly,
    correlation,
}: {
    anomaly?: AnomalyInfo;
    correlation?: string | null;
}) {
    if (!anomaly) return null;

    const trendUp = anomaly.trend > 0;
    const max = Math.max(...anomaly.windows, 0.01);

    return (
        <div
            className={`glass rounded-2xl p-5 ${anomaly.anomaly ? "shadow-glowRed" : ""
                }`}
        >
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold tracking-wide text-white/90">
                    ANOMALY DETECTION
                </h3>
                {anomaly.anomaly && (
                    <motion.span
                        initial={{ scale: 0.8, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        className="text-[10px] font-bold px-2 py-0.5 rounded bg-crit/15 text-crit border border-crit/40"
                    >
                        SPIKE
                    </motion.span>
                )}
            </div>

            <div className="flex items-end gap-1 h-16 mb-3">
                {anomaly.windows.map((v, i) => (
                    <motion.div
                        key={i}
                        initial={{ height: 0 }}
                        animate={{ height: `${(v / max) * 100}%` }}
                        transition={{ delay: i * 0.08, duration: 0.5 }}
                        className={`flex-1 rounded-t ${v > 0.5
                                ? "bg-crit"
                                : v > 0.25
                                    ? "bg-err"
                                    : v > 0.1
                                        ? "bg-warn"
                                        : "bg-accent/40"
                            }`}
                        style={{ minHeight: 2 }}
                    />
                ))}
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
                <div>
                    <div className="text-white/40">Current</div>
                    <div className="text-lg font-bold tabular-nums">
                        {(anomaly.current_error_rate * 100).toFixed(0)}%
                    </div>
                </div>
                <div>
                    <div className="text-white/40">Trend</div>
                    <div
                        className={`text-lg font-bold tabular-nums ${trendUp ? "text-crit" : "text-info"
                            }`}
                    >
                        {trendUp ? "▲" : "▼"} {Math.abs(anomaly.trend * 100).toFixed(0)}%
                    </div>
                </div>
            </div>

            {anomaly.prediction && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-3 rounded-lg border border-warn/40 bg-warn/10 p-3 text-xs text-warn"
                >
                    🔮 <span className="font-semibold">Predictive alert:</span>{" "}
                    {anomaly.prediction}
                </motion.div>
            )}

            {correlation && (
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="mt-2 rounded-lg border border-accent/40 bg-accent/10 p-3 text-xs"
                >
                    🚀 <span className="font-semibold text-accent">Deployment correlation:</span>{" "}
                    <span className="text-white/85">{correlation}</span>
                </motion.div>
            )}
        </div>
    );
}
