import type { Config } from "tailwindcss";

const config: Config = {
    content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
    theme: {
        extend: {
            colors: {
                bg: "#0b1020",
                panel: "#11172b",
                panel2: "#161d36",
                border: "#1f2747",
                accent: "#7c5cff",
                info: "#22c55e",
                warn: "#eab308",
                err: "#f97316",
                crit: "#ef4444",
            },
            boxShadow: {
                glow: "0 0 24px rgba(124, 92, 255, 0.35)",
                glowRed: "0 0 24px rgba(239, 68, 68, 0.45)",
            },
            animation: {
                pulseSlow: "pulse 2.5s cubic-bezier(0.4, 0, 0.6, 1) infinite",
            },
        },
    },
    plugins: [],
};

export default config;
