"""Generate downloadable incident reports in Markdown."""

from datetime import datetime
from typing import Dict


def render_markdown(report: Dict, anomaly: Dict, services) -> str:
    lines = []
    lines.append("# IncidentIQ — AI Incident Report")
    lines.append("")
    lines.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_")
    lines.append("")
    lines.append(f"**Status:** {report.get('status', 'unknown')}")
    lines.append(
        f"**Overall severity:** {report.get('severity_label', report.get('severity', 'INFO'))}"
    )
    lines.append(f"**Engine:** {report.get('engine', 'rule-based')}")
    lines.append("")
    lines.append("## Summary")
    lines.append(report.get("summary", "—"))
    lines.append("")

    lines.append("## Anomaly Detection")
    lines.append(f"- Current error rate: {anomaly['current_error_rate']}")
    lines.append(f"- Baseline error rate: {anomaly['baseline_error_rate']}")
    lines.append(f"- Trend: {anomaly['trend']:+.3f}")
    lines.append(f"- Spike detected: {anomaly['anomaly']}")
    if anomaly.get("prediction"):
        lines.append(f"- **Prediction:** {anomaly['prediction']}")
    lines.append("")

    lines.append("## Service Health")
    if services:
        for s in services:
            lines.append(
                f"- `{s['service']}` — {s['status'].upper()} "
                f"(score {s['score']}/100)"
            )
    else:
        lines.append("- No service data available.")
    lines.append("")

    lines.append("## Active Incidents")
    incidents = report.get("incidents", [])
    if not incidents:
        lines.append("_No active incidents._")
    for i, inc in enumerate(incidents, 1):
        lines.append(f"### {i}. {inc.get('issue', 'Unknown')} "
                     f"[{inc.get('severity', 'INFO')}]")
        lines.append(f"- **Root cause:** {inc.get('cause', '—')}")
        lines.append(f"- **Suggested fix:** {inc.get('solution', '—')}")
        for rec in inc.get("recommendations") or []:
            lines.append(f"  - {rec}")
        lines.append("")

    lines.append("## Timeline")
    timeline = report.get("timeline", [])
    if not timeline:
        lines.append("_No notable events._")
    for ev in timeline:
        lines.append(f"- `{ev.get('time') or '—'}` **{ev['level']}** — {ev['message']}")

    return "\n".join(lines)
