"""Lightweight anomaly detection and predictive alerts.

Uses a rolling window over recent log lines. Pure stdlib — no sklearn
needed for a hackathon-grade demo.
"""

from collections import deque
from typing import Dict, List

from ai_engine_loader import detect_level


def _split_windows(logs: List[str], n: int = 4) -> List[List[str]]:
    """Split logs into `n` equal time windows (oldest → newest)."""
    if not logs:
        return [[] for _ in range(n)]
    size = max(1, len(logs) // n)
    chunks = [logs[i : i + size] for i in range(0, len(logs), size)]
    while len(chunks) < n:
        chunks.insert(0, [])
    return chunks[-n:]


def _error_rate(window: List[str]) -> float:
    if not window:
        return 0.0
    bad = sum(1 for l in window if detect_level(l) in ("ERROR", "CRITICAL"))
    return bad / len(window)


def detect(logs: List[str]) -> Dict:
    """Return anomaly + prediction info."""
    windows = _split_windows(logs, n=4)
    rates = [_error_rate(w) for w in windows]

    current = rates[-1]
    baseline = sum(rates[:-1]) / max(1, len(rates) - 1)

    spike = current > 0.3 and current > baseline * 1.5
    trend = current - baseline  # positive = getting worse

    prediction = None
    if trend > 0.15 and current >= 0.4:
        prediction = (
            "Error rate is climbing sharply. "
            "Likely service degradation within ~15 minutes."
        )
    elif trend > 0.08:
        prediction = (
            "Error rate trending up. Monitor closely; consider preemptive scale-out."
        )

    return {
        "anomaly": spike,
        "current_error_rate": round(current, 3),
        "baseline_error_rate": round(baseline, 3),
        "trend": round(trend, 3),
        "prediction": prediction,
        "windows": [round(r, 3) for r in rates],
    }
