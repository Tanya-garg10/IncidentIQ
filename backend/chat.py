"""AI chat over recent logs ('Chat with your infrastructure').

Uses the active LLM provider (Groq / OpenAI / Gemini) when a key is set;
otherwise a deterministic keyword-based responder so the demo always works.

Includes rate-limit cooldown: on 429 we fall back to the rule-based
responder for COOLDOWN_SECONDS so the chat panel never stops working.
"""

import sys
import time
from pathlib import Path
from typing import List, Optional

# Reach into ai-engine/ for the unified LLM provider
_AI_DIR = Path(__file__).resolve().parent.parent / "ai-engine"
if str(_AI_DIR) not in sys.path:
    sys.path.insert(0, str(_AI_DIR))

from ai_engine_loader import detect_level
from llm_provider import active_provider, chat as llm_chat  # noqa: E402

SYSTEM = (
    "You are IncidentIQ, an SRE assistant. The user will ask about their "
    "infrastructure. Use ONLY the provided log lines to answer. Be concise "
    "(under 120 words). If the logs don't contain the answer, say so."
)

COOLDOWN_SECONDS = 300
_cooldown_until: float = 0.0
_last_error: Optional[str] = None


def _llm_answer(question: str, logs: List[str]) -> str:
    # Trim logs to last 40 lines to save tokens
    return llm_chat(
        [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Recent logs:\n" + "\n".join(logs[-40:])
                ),
            },
        ],
        temperature=0.2,
    ).strip()


def _fallback_answer(question: str, logs: List[str]) -> str:
    q = question.lower()
    relevant = [l for l in logs if detect_level(l) in ("ERROR", "CRITICAL")]
    if not relevant:
        return (
            "Looking at the recent logs, I see only INFO and WARNING events. "
            "There are no active errors or critical incidents to explain."
        )

    last = relevant[-1]
    if "crash" in q or "down" in q or "why" in q:
        return (
            f"The most recent severe event was: '{last}'. "
            "Likely cause: an upstream dependency timeout cascaded into the "
            "affected service. Check connection pools, downstream health, and "
            "the most recent deployment."
        )
    if "fix" in q or "do" in q or "how" in q:
        return (
            f"Based on the latest critical event ('{last}'), recommended steps: "
            "1) restart the affected service, 2) check downstream dependencies, "
            "3) consider rolling back the latest deployment if the issue began shortly after."
        )

    summary = "\n".join(relevant[-5:])
    return f"Recent severe events:\n{summary}"


def answer(question: str, logs: List[str]) -> dict:
    global _cooldown_until, _last_error

    provider = active_provider()
    if not provider:
        return {"answer": _fallback_answer(question, logs), "engine": "rule-based"}

    # Honour cooldown so we don't keep banging on a rate-limited provider
    if time.time() < _cooldown_until:
        return {
            "answer": _fallback_answer(question, logs),
            "engine": "rule-based",
            "llm_error": _last_error or "rate limit cooldown",
        }

    try:
        return {"answer": _llm_answer(question, logs), "engine": provider}
    except Exception as exc:
        msg = str(exc)
        if "429" in msg or "rate_limit" in msg.lower():
            _cooldown_until = time.time() + COOLDOWN_SECONDS
            _last_error = "rate limit"
        return {
            "answer": _fallback_answer(question, logs),
            "engine": "rule-based",
            "llm_error": msg,
        }
