"use client";

import {
    Bar,
    BarChart,
    CartesianGrid,
    Cell,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import type { MetricsResponse } from "@/lib/api";

export function SeverityChart({ data }: { data: MetricsResponse | null }) {
    const chartData =
        data?.counts.map((c) => ({
            name: c.label,
            count: c.count,
            color: c.color,
        })) ?? [];

    return (
        <div className="glass rounded-2xl p-5">
            <h3 className="text-sm font-semibold tracking-wide text-white/90 mb-3">
                SEVERITY DISTRIBUTION
            </h3>
            <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1f2747" />
                        <XAxis dataKey="name" stroke="#8a91b4" fontSize={11} />
                        <YAxis stroke="#8a91b4" fontSize={11} allowDecimals={false} />
                        <Tooltip
                            contentStyle={{
                                background: "#161d36",
                                border: "1px solid #1f2747",
                                borderRadius: 8,
                                fontSize: 12,
                            }}
                        />
                        <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                            {chartData.map((entry, i) => (
                                <Cell key={i} fill={entry.color} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
