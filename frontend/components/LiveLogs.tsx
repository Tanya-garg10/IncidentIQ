"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { WS_BASE, detectLevel, severityBadge, type Severity } from "@/lib/api";

interface LogEntry {
    id: number;
    line: string;
    level: Severity;
}

export function LiveLogs() {
    const [logs, setLogs] = useState<LogEntry[]>([]);
    const [connected, setConnected] = useState(false);
    const idRef = useRef(0);
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const ws = new WebSocket(`${WS_BASE}/ws/logs`);

        ws.onopen = () => setConnected(true);
        ws.onclose = () => setConnected(false);
        ws.onerror = () => setConnected(false);

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === "snapshot") {
                const seeded: LogEntry[] = data.logs.map((line: string) => ({
                    id: idRef.current++,
                    line,
                    level: detectLevel(line),
                }));
                setLogs(seeded.slice(-100));
            } else if (data.type === "log") {
                setLogs((prev) => {
                    const next = [
                        ...prev,
                        {
                            id: idRef.current++,
                            line: data.line,
                            level: detectLevel(data.line),
                        },
                    ];
                    return next.slice(-100);
                });
            }
        };

        return () => ws.close();
    }, []);

    useEffect(() => {
        const el = containerRef.current;
        if (el) el.scrollTop = el.scrollHeight;
    }, [logs]);

    return (
        <div className="glass rounded-2xl p-5 shadow-glow">
            <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold tracking-wide text-white/90">
                    LIVE LOG STREAM
                </h3>
                <span
                    className={`text-xs px-2 py-0.5 rounded-full border ${connected
                        ? "border-info/40 text-info bg-info/10"
                        : "border-crit/40 text-crit bg-crit/10"
                        }`}
                >
                    {connected ? "● connected" : "○ offline"}
                </span>
            </div>
            <div
                ref={containerRef}
                className="scroll-y h-80 overflow-y-auto font-mono text-xs space-y-1 pr-2"
            >
                <AnimatePresence initial={false}>
                    {logs.map((log) => (
                        <motion.div
                            key={log.id}
                            initial={{ opacity: 0, x: -8 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0 }}
                            className="flex items-start gap-2"
                        >
                            <span
                                className={`px-1.5 py-0.5 rounded text-[10px] font-bold ${severityBadge(
                                    log.level
                                )}`}
                            >
                                {log.level}
                            </span>
                            <span className="text-white/80 break-all">{log.line}</span>
                        </motion.div>
                    ))}
                </AnimatePresence>
            </div>
        </div>
    );
}
