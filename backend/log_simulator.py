"""Simulate a live stream of multi-service log events for the demo."""

import random
from datetime import datetime
from typing import List, Tuple

SERVICES = ["auth-service", "payment-service", "user-service", "api-gateway"]

# (level, message_template) — `{svc}` filled in at runtime
EVENT_POOL: List[Tuple[str, str]] = [
    ("INFO", "{svc}: request handled in 42ms"),
    ("INFO", "{svc}: cache hit"),
    ("INFO", "{svc}: health check passed"),
    ("INFO", "{svc}: db connection established"),
    ("WARNING", "{svc}: high CPU usage detected"),
    ("WARNING", "{svc}: memory usage at 82%"),
    ("WARNING", "{svc}: slow query detected (1.2s)"),
    ("ERROR", "{svc}: database connection timeout"),
    ("ERROR", "{svc}: API response delayed"),
    ("ERROR", "{svc}: failed to reach downstream"),
    ("CRITICAL", "{svc}: service crashed"),
    ("CRITICAL", "{svc}: out of memory"),
]
WEIGHTS = [9, 7, 6, 5, 3, 3, 2, 2, 2, 2, 1, 1]


def _now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def next_event(service: str | None = None) -> str:
    level, template = random.choices(EVENT_POOL, weights=WEIGHTS, k=1)[0]
    svc = service or random.choice(SERVICES)
    return f"{_now_iso()} {level}: " + template.format(svc=svc)


def burst_incident() -> List[str]:
    """Realistic cascading outage: one service fails, dependents follow."""
    primary = random.choice(["payment-service", "auth-service", "user-service"])
    scenarios = [
        [
            ("WARNING", f"{primary}: high CPU usage detected"),
            ("ERROR", f"{primary}: database connection timeout"),
            ("ERROR", "api-gateway: API response delayed"),
            ("CRITICAL", f"{primary}: service crashed"),
        ],
        [
            ("WARNING", f"{primary}: memory usage at 91%"),
            ("ERROR", f"{primary}: failed to reach downstream"),
            ("CRITICAL", f"{primary}: out of memory"),
        ],
    ]
    chosen = random.choice(scenarios)
    return [f"{_now_iso()} {lvl}: {msg}" for lvl, msg in chosen]
