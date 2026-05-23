"""Severity levels and helpers."""

SEVERITY_RANK = {
    "INFO": 1,
    "WARNING": 2,
    "ERROR": 3,
    "CRITICAL": 4,
}

SEVERITY_LABEL = {
    "INFO": "Low",
    "WARNING": "Medium",
    "ERROR": "High",
    "CRITICAL": "Critical",
}

SEVERITY_COLOR = {
    "INFO": "#22c55e",      # green
    "WARNING": "#eab308",   # yellow
    "ERROR": "#f97316",     # orange
    "CRITICAL": "#ef4444",  # red
}


def detect_level(line: str) -> str:
    """Return the highest severity level mentioned in a log line.

    Handles both `LEVEL: message` and `<timestamp> LEVEL: message` formats.
    """
    upper = line.upper()
    # Check most-severe first so a line tagged CRITICAL beats one mentioning INFO
    for level in ("CRITICAL", "ERROR", "WARNING", "INFO"):
        # match as a whole token followed by ':' to avoid accidental hits
        if f" {level}:" in f" {upper}" or f"{level}:" in upper:
            return level
    return "INFO"


def highest(levels):
    """Return the highest severity from an iterable of levels."""
    best = "INFO"
    for level in levels:
        if SEVERITY_RANK.get(level, 0) > SEVERITY_RANK[best]:
            best = level
    return best
