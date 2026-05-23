"""Rule-based incident analyzer.

Phase 1: pattern matching on log lines.
Phase 3: `llm_analyzer.py` wraps this with a real LLM (OpenAI / Ollama).
"""

import re
from typing import Dict, List

from severity import SEVERITY_LABEL, detect_level, highest

# Pattern → diagnosis. Order matters: most specific first.
RULES = [
    {
        "match": "database connection timeout",
        "issue": "Database Timeout",
        "cause": "DB overloaded, unreachable, or pool exhausted",
        "solution": "Increase DB pool size, check DB server health, verify network",
        "severity": "ERROR",
        "recommendations": [
            "Increase database connection pool size",
            "Check DB server CPU and memory",
            "Verify network connectivity to DB host",
        ],
    },
    {
        "match": "service crashed",
        "issue": "Service Crash",
        "cause": "Unhandled exception or resource exhaustion",
        "solution": "Inspect stack trace, restart the service, add health checks",
        "severity": "CRITICAL",
        "recommendations": [
            "Restart the affected service",
            "Roll back the latest deployment",
            "Inspect stack trace and add health checks",
        ],
    },
    {
        "match": "api response delayed",
        "issue": "API Latency",
        "cause": "Downstream slowness or thread pool starvation",
        "solution": "Profile slow endpoints, add caching, scale workers",
        "severity": "ERROR",
        "recommendations": [
            "Scale API pods horizontally",
            "Add caching to slow endpoints",
            "Profile and optimize hot paths",
        ],
    },
    {
        "match": "high cpu usage",
        "issue": "High CPU Usage",
        "cause": "Hot loop, traffic spike, or runaway process",
        "solution": "Identify top processes, enable autoscaling, optimize code",
        "severity": "WARNING",
        "recommendations": [
            "Enable horizontal autoscaling",
            "Identify top CPU-consuming processes",
            "Optimize hot loops in application code",
        ],
    },
]

# Optional ISO-ish timestamp prefix: `2024-05-23T12:01:05`
TS_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})")


def _extract_timestamp(line: str):
    m = TS_RE.match(line)
    return m.group(1) if m else None


def build_timeline(logs: List[str]) -> List[Dict]:
    """Return a chronological list of significant log events."""
    timeline = []
    for line in logs:
        level = detect_level(line)
        if level == "INFO":
            continue
        timeline.append(
            {
                "time": _extract_timestamp(line),
                "level": level,
                "message": line,
            }
        )
    return timeline


def analyze_logs(logs: List[str]) -> Dict:
    """Analyze logs and return a structured incident report."""
    if not logs:
        return {
            "status": "ok",
            "severity": "INFO",
            "severity_label": SEVERITY_LABEL["INFO"],
            "incidents": [],
            "timeline": [],
            "summary": "No logs available to analyze.",
            "engine": "rule-based",
        }

    joined = " ".join(logs).lower()
    incidents = []
    for rule in RULES:
        if rule["match"] in joined:
            incidents.append(
                {
                    "issue": rule["issue"],
                    "cause": rule["cause"],
                    "solution": rule["solution"],
                    "severity": rule["severity"],
                    "recommendations": rule["recommendations"],
                }
            )

    overall = highest(detect_level(line) for line in logs)
    timeline = build_timeline(logs)

    if not incidents:
        return {
            "status": "ok",
            "severity": overall,
            "severity_label": SEVERITY_LABEL[overall],
            "incidents": [],
            "timeline": timeline,
            "summary": "No known issue patterns detected.",
            "engine": "rule-based",
        }

    return {
        "status": "issues_found",
        "severity": overall,
        "severity_label": SEVERITY_LABEL[overall],
        "incidents": incidents,
        "timeline": timeline,
        "summary": (
            f"Detected {len(incidents)} incident(s). "
            f"Highest severity: {SEVERITY_LABEL[overall]}."
        ),
        "engine": "rule-based",
    }
