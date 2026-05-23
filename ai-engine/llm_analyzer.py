"""LLM-powered analyzer with graceful fallback to the rule-based engine.

If a provider key is set (GROQ_API_KEY / OPENAI_API_KEY / GEMINI_API_KEY),
this calls the LLM. Otherwise it returns the rule-based analyzer's output.
"""

from typing import Dict, List

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


def analyze(logs: List[str]) -> Dict:
    """Analyze logs using LLM if available, otherwise rules."""
    if not logs:
        return rule_based_analyze(logs)

    provider = active_provider()
    if provider is None:
        return rule_based_analyze(logs)

    try:
        ai = chat_json(
            [{"role": "user", "content": PROMPT % "\n".join(logs)}]
        )
    except Exception as exc:  # network errors, quota, malformed JSON, etc.
        fallback = rule_based_analyze(logs)
        fallback["llm_error"] = str(exc)
        return fallback

    incidents = ai.get("incidents", []) or []
    overall = highest(
        [inc.get("severity", "INFO") for inc in incidents]
        + [detect_level(line) for line in logs]
    )

    rb = rule_based_analyze(logs)
    return {
        "status": "issues_found" if incidents else "ok",
        "severity": overall,
        "severity_label": SEVERITY_LABEL[overall],
        "incidents": incidents,
        "timeline": rb["timeline"],
        "summary": ai.get("summary", rb["summary"]),
        "engine": provider,
    }
