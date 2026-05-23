import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "IncidentIQ — AI Incident Analysis",
    description: "Live log streaming, root cause detection, and AI fixes.",
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body className="font-sans antialiased">{children}</body>
        </html>
    );
}
