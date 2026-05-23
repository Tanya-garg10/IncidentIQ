"""AI chat over recent logs ('Chat with your infrastructure').

Uses the active LLM provider (Groq / OpenAI / Gemini) when a key is set;
otherwise a deterministic keyword-based responder so the demo always works.
"""

import sys
from pathlib import Path
from typing import List

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


def _llm_answer(question: str, logs: List[str]) -> str:
    return llm_chat(
        [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Recent logs:\n" + "\n".join(logs[-80:])
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
    provider = active_provider()
    if provider:
        try:
            return {"answer": _llm_answer(question, logs), "engine": provider}
        except Exception as exc:
            return {
                "answer": _fallback_answer(question, logs),
                "engine": "rule-based",
                "llm_error": str(exc),
            }
    return {"answer": _fallback_answer(question, logs), "engine": "rule-based"}
