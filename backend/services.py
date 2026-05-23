"""Per-service health scoring."""

import re
from collections import defaultdict
from typing import Dict, List

from ai_engine_loader import detect_level

SEVERITY_PENALTY = {"INFO": 0, "WARNING": 5, "ERROR": 15, "CRITICAL": 30}

SERVICE_RE = re.compile(r"\b([a-z-]+-service|api-gateway)\b", re.I)


def extract_service(line: str) -> str | None:
    m = SERVICE_RE.search(line)
    return m.group(1).lower() if m else None


def health_scores(logs: List[str]) -> List[Dict]:
    """Compute a 0–100 health score per service based on recent logs."""
    by_service: Dict[str, Dict[str, int]] = defaultdict(
        lambda: {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
    )

    for line in logs:
        svc = extract_service(line)
        if not svc:
            continue
        by_service[svc][detect_level(line)] += 1

    out: List[Dict] = []
    for svc, counts in sorted(by_service.items()):
        penalty = sum(SEVERITY_PENALTY[lvl] * n for lvl, n in counts.items())
        score = max(0, 100 - penalty)
        if counts["CRITICAL"] > 0:
            status = "down"
        elif counts["ERROR"] > 0:
            status = "degraded"
        elif counts["WARNING"] > 0:
            status = "warning"
        else:
            status = "healthy"
        out.append(
            {
                "service": svc,
                "score": score,
                "status": status,
                "counts": counts,
            }
        )
    return out
