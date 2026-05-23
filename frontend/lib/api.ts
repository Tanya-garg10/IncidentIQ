export const API_BASE =
    process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";

export const WS_BASE =
    process.env.NEXT_PUBLIC_WS_BASE || "ws://127.0.0.1:8000";

export type Severity = "INFO" | "WARNING" | "ERROR" | "CRITICAL";

export interface Incident {
    issue: string;
    cause: string;
    solution: string;
    severity: Severity;
    recommendations?: string[];
}

export interface TimelineEvent {
    time: string | null;
    level: Severity;
    message: string;
}

export interface AnomalyInfo {
    anomaly: boolean;
    current_error_rate: number;
    baseline_error_rate: number;
    trend: number;
    prediction: string | null;
    windows: number[];
}

export interface ServiceHealth {
    service: string;
    score: number;
    status: "healthy" | "warning" | "degraded" | "down";
    counts: Record<Severity, number>;
}

export interface AnalysisReport {
    status: "ok" | "issues_found";
    severity: Severity;
    severity_label: string;
    incidents: Incident[];
    timeline: TimelineEvent[];
    summary: string;
    engine: string;
    llm_error?: string;
    anomaly?: AnomalyInfo;
    services?: ServiceHealth[];
    deployment_correlation?: string | null;
}

export interface MetricsResponse {
    counts: { level: Severity; label: string; count: number; color: string }[];
    total: number;
}

export interface ChatResponse {
    answer: string;
    engine: string;
    llm_error?: string;
}

export async function fetchAnalysis(): Promise<AnalysisReport> {
    const r = await fetch(`${API_BASE}/analyze`, { cache: "no-store" });
    if (!r.ok) throw new Error("analyze failed");
    return r.json();
}

export async function fetchMetrics(): Promise<MetricsResponse> {
    const r = await fetch(`${API_BASE}/metrics`, { cache: "no-store" });
    if (!r.ok) throw new Error("metrics failed");
    return r.json();
}

export async function triggerSimulation(): Promise<void> {
    await fetch(`${API_BASE}/simulate`, { method: "POST" });
}

export async function triggerDeployment(): Promise<void> {
    await fetch(`${API_BASE}/simulate/deployment`, { method: "POST" });
}

export async function askChat(question: string): Promise<ChatResponse> {
    const r = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
    });
    if (!r.ok) throw new Error("chat failed");
    return r.json();
}

export function reportDownloadUrl(): string {
    return `${API_BASE}/report.md`;
}

export function severityClass(level: Severity): string {
    switch (level) {
        case "INFO":
            return "text-info";
        case "WARNING":
            return "text-warn";
        case "ERROR":
            return "text-err";
        case "CRITICAL":
            return "text-crit";
    }
}

export function severityBadge(level: Severity): string {
    switch (level) {
        case "INFO":
            return "bg-info/15 text-info border border-info/30";
        case "WARNING":
            return "bg-warn/15 text-warn border border-warn/30";
        case "ERROR":
            return "bg-err/15 text-err border border-err/30";
        case "CRITICAL":
            return "bg-crit/15 text-crit border border-crit/40 shadow-glowRed";
    }
}

export function detectLevel(line: string): Severity {
    const upper = line.toUpperCase();
    if (upper.includes("CRITICAL")) return "CRITICAL";
    if (upper.includes("ERROR")) return "ERROR";
    if (upper.includes("WARNING")) return "WARNING";
    return "INFO";
}
