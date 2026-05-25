"""LLM-powered analyzer with caching, rate-limit cooldown, and graceful fallback.

If a provider key is set (GROQ_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY),
this calls the LLM. Otherwise it returns the rule-based analyzer's output.

Optimizations:
  - Result is cached and reused while the log fingerprint is unchanged.
  - On a rate-limit (429) error, the LLM is suspended for COOLDOWN_SECONDS
    and the rule-based engine takes over so the demo keeps working.
"""

import hashlib
import time
from typing import Dict, List, Optional, Tuple

from analyzer import analyze_logs as rule_based_analyze
from llm_provider import active_provider, chat_json
from severity import SEVERITY_LABEL, detect_level, highest

PROMPT = """You are an SRE assistant. Analyze the following log lines and respond
with STRICT JSON only (no markdown, no prose) matching this schema:

{
  "summary": "<one sentence>",
  "incidents": [
    {
      "issue": "<short title>",
      "cause": "<root cause>",
      "solution": "<concise fix>",
      "severity": "INFO|WARNING|ERROR|CRITICAL",
      "recommendations": ["<action 1>", "<action 2>"]
    }
  ]
}

Logs:
%s
"""

# Cache the last analysis so we don't re-call the LLM if logs haven't meaningfully changed
_cache: Dict[str, Dict] = {}
# Rate-limit cooldown — if we hit 429, suspend LLM calls for this many seconds.
# Short for hackathon demos so quota recovers fast; bump to 300+ in production.
COOLDOWN_SECONDS = 60
_cooldown_until: float = 0.0
_last_error: Optional[str] = None


def reset_cooldown() -> None:
    """Manually clear the rate-limit cooldown (useful right before a demo)."""
    global _cooldown_until, _last_error, _cache
    _cooldown_until = 0.0
    _last_error = None
    _cache.clear()


def _fingerprint(logs: List[str]) -> str:
    """Hash of the most recent log lines, used as a cache key."""
    sample = "\n".join(logs[-60:])
    return hashlib.sha1(sample.encode("utf-8")).hexdigest()


def _in_cooldown() -> Tuple[bool, float]:
    remaining = _cooldown_until - time.time()
    return remaining > 0, max(0.0, remaining)


def analyze(logs: List[str]) -> Dict:
    """Analyze logs using LLM if available, otherwise rules."""
    global _cooldown_until, _last_error

    if not logs:
        return rule_based_analyze(logs)

    provider = active_provider()
    if provider is None:
        return rule_based_analyze(logs)

    # If we recently hit a rate limit, stay on rules until cooldown ends
    cooling, remaining = _in_cooldown()
    if cooling:
        fallback = rule_based_analyze(logs)
        fallback["llm_error"] = (
            f"LLM rate-limited; using rule-based for {int(remaining)}s "
            f"({_last_error or 'rate limit'})"
        )
        return fallback

    # Cache hit: same logs as last time → reuse the previous LLM result
    fp = _fingerprint(logs)
    cached = _cache.get(fp)
    if cached:
        return {**cached, "cached": True}

    # Truncate to last 60 lines to keep prompt small (saves tokens)
    sample = logs[-60:]

    try:
        ai = chat_json([{"role": "user", "content": PROMPT % "\n".join(sample)}])
    except Exception as exc:
        msg = str(exc)
        # Detect rate-limit and start cooldown
        if "429" in msg or "rate_limit" in msg.lower():
            _cooldown_until = time.time() + COOLDOWN_SECONDS
            _last_error = "rate limit"
        fallback = rule_based_analyze(logs)
        fallback["llm_error"] = msg
        return fallback

    incidents = ai.get("incidents", []) or []
    overall = highest(
        [inc.get("severity", "INFO") for inc in incidents]
        + [detect_level(line) for line in logs]
    )

    rb = rule_based_analyze(logs)
    result = {
        "status": "issues_found" if incidents else "ok",
        "severity": overall,
        "severity_label": SEVERITY_LABEL[overall],
        "incidents": incidents,
        "timeline": rb["timeline"],
        "summary": ai.get("summary", rb["summary"]),
        "engine": provider,
    }

    # Keep cache small — only the most recent fingerprint
    _cache.clear()
    _cache[fp] = result
    return result
