"use client";

import { useCallback, useEffect, useState } from "react";
import { AnomalyCard } from "@/components/AnomalyCard";
import { ChatPanel } from "@/components/ChatPanel";
import { Header } from "@/components/Header";
import { IncidentList } from "@/components/IncidentList";
import { LiveLogs } from "@/components/LiveLogs";
import { ServiceGrid } from "@/components/ServiceGrid";
import { SeverityChart } from "@/components/SeverityChart";
import { SeverityMeter } from "@/components/SeverityMeter";
import { Timeline } from "@/components/Timeline";
import {
    fetchAnalysis,
    fetchMetrics,
    type AnalysisReport,
    type MetricsResponse,
} from "@/lib/api";

export default function Dashboard() {
    const [report, setReport] = useState<AnalysisReport | null>(null);
    const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
    const [error, setError] = useState<string | null>(null);

    const refresh = useCallback(async () => {
        try {
            const [r, m] = await Promise.all([fetchAnalysis(), fetchMetrics()]);
            setReport(r);
            setMetrics(m);
            setError(null);
        } catch {
            setError("Backend offline — start FastAPI on port 8000.");
        }
    }, []);

    useEffect(() => {
        refresh();
        // Poll every 15s — keeps token usage low and respects free-tier rate limits.
        // Live log updates still arrive instantly via the WebSocket.
        const id = setInterval(refresh, 15000);
        return () => clearInterval(id);
    }, [refresh]);

    return (
        <main className="max-w-7xl mx-auto px-6 py-8">
            <Header onRefresh={refresh} />

            {error && (
                <div className="mb-4 rounded-lg border border-crit/40 bg-crit/10 px-4 py-2 text-sm text-crit">
                    {error}
                </div>
            )}

            {report && (
                <div className="mb-4 glass rounded-xl p-4">
                    <div className="flex items-center justify-between flex-wrap gap-2">
                        <p className="text-sm text-white/85">{report.summary}</p>
                        <span className="text-[10px] uppercase tracking-wider text-white/40">
                            engine: {report.engine}
                        </span>
                    </div>
                    {report.llm_error && (
                        <p className="mt-1 text-xs text-warn">
                            LLM unavailable, showing rule-based output ({report.llm_error})
                        </p>
                    )}
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
                {/* Left + center: live ops view */}
                <div className="lg:col-span-2 space-y-4">
                    <LiveLogs />
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <SeverityMeter level={report?.severity ?? "INFO"} />
                        <AnomalyCard
                            anomaly={report?.anomaly}
                            correlation={report?.deployment_correlation}
                        />
                    </div>
                    <ServiceGrid services={report?.services ?? []} />
                    <SeverityChart data={metrics} />
                    <IncidentList incidents={report?.incidents ?? []} />
                </div>

                {/* Right rail: timeline + AI chat */}
                <div className="space-y-4">
                    <Timeline events={report?.timeline ?? []} />
                    <ChatPanel />
                </div>
            </div>

            <footer className="mt-10 text-center text-xs text-white/30">
                IncidentIQ · AI infrastructure intelligence
            </footer>
        </main>
    );
}
