"""Read log files from the logs/ directory."""

from pathlib import Path
from typing import List

# logs/ folder lives one level up from backend/
LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
DEFAULT_LOG_FILE = LOGS_DIR / "sample.log"


def read_logs(log_file: Path = DEFAULT_LOG_FILE) -> List[str]:
    """Read a log file and return its lines (stripped, non-empty)."""
    if not log_file.exists():
        return []

    with open(log_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]
