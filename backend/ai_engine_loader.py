"""Load the analyzer modules from the sibling `ai-engine/` folder.

The folder name uses a hyphen (per project spec), which isn't a valid
Python module name, so we put it on sys.path and import normally.
"""

import sys
from pathlib import Path

_AI_DIR = Path(__file__).resolve().parent.parent / "ai-engine"
if str(_AI_DIR) not in sys.path:
    sys.path.insert(0, str(_AI_DIR))

from analyzer import analyze_logs as rule_based_analyze  # noqa: E402
from llm_analyzer import analyze as smart_analyze  # noqa: E402
from severity import (  # noqa: E402
    SEVERITY_COLOR,
    SEVERITY_LABEL,
    SEVERITY_RANK,
    detect_level,
)

__all__ = [
    "rule_based_analyze",
    "smart_analyze",
    "SEVERITY_COLOR",
    "SEVERITY_LABEL",
    "SEVERITY_RANK",
    "detect_level",
]
