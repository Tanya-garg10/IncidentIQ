"use client";

import { severityBadge, type TimelineEvent } from "@/lib/api";

export function Timeline({ events }: { events: TimelineEvent[] }) {
    return (
        <div className="glass rounded-2xl p-5">
            <h3 className="text-sm font-semibold tracking-wide text-white/90 mb-4">
                INCIDENT TIMELINE
            </h3>

            {events.length === 0 ? (
                <p className="text-sm text-white/60">All quiet.</p>
            ) : (
                <ol className="relative border-l border-border ml-2 space-y-3">
                    {events.map((ev, i) => (
                        <li key={i} className="ml-4">
                            <span
                                className={`absolute -left-1.5 mt-1.5 w-3 h-3 rounded-full ${ev.level === "CRITICAL"
                                    ? "bg-crit shadow-glowRed animate-pulseSlow"
                                    : ev.level === "ERROR"
                                        ? "bg-err"
                                        : ev.level === "WARNING"
                                            ? "bg-warn"
                                            : "bg-info"
                                    }`}
                            />
                            <div className="flex items-center gap-2 text-xs">
                                <span className="text-white/50 font-mono">
                                    {ev.time ?? "—"}
                                </span>
                                <span
                                    className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${severityBadge(
                                        ev.level
                                    )}`}
                                >
                                    {ev.level}
                                </span>
                            </div>
                            <p className="text-sm text-white/80 mt-1">{ev.message}</p>
                        </li>
                    ))}
                </ol>
            )}
        </div>
    );
}
