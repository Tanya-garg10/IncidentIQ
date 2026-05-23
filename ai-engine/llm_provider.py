"""Unified LLM provider — supports Groq, OpenAI, and Gemini.

Reads `LLM_PROVIDER` env var ('groq', 'openai', or 'gemini'). If unset,
auto-detects from whichever API key is present.

All providers expose the same `chat()` interface so callers don't care
which backend is in use.
"""

import json
import os
from typing import Dict, List, Optional


def active_provider() -> Optional[str]:
    """Return the active LLM provider name, or None if no key is set."""
    explicit = os.getenv("LLM_PROVIDER", "").lower().strip()
    if explicit in ("groq", "openai", "gemini"):
        return explicit

    # Auto-detect by which key is set, in order of preference
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("OPENAI_API_KEY"):
        return "openai"
    if os.getenv("GEMINI_API_KEY"):
        return "gemini"
    return None


def _model_for(provider: str) -> str:
    """Pick a sensible default model per provider."""
    overrides = {
        "groq": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "gemini": os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
    }
    return overrides[provider]


def _openai_compat_client(api_key: str, base_url: Optional[str] = None):
    """Both OpenAI and Groq use the same SDK — Groq just needs a base_url."""
    from openai import OpenAI

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAI(**kwargs)


def _chat_openai_compat(
    provider: str,
    api_key: str,
    base_url: Optional[str],
    messages: List[Dict],
    *,
    json_mode: bool = False,
    temperature: float = 0.2,
) -> str:
    client = _openai_compat_client(api_key, base_url)
    kwargs: Dict = {
        "model": _model_for(provider),
        "messages": messages,
        "temperature": temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


def _chat_gemini(
    messages: List[Dict],
    *,
    json_mode: bool = False,
    temperature: float = 0.2,
) -> str:
    """Gemini uses a different SDK shape — convert messages to a single prompt."""
    import google.generativeai as genai

    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(_model_for("gemini"))

    # Flatten OpenAI-style messages into Gemini's expected format
    system = "\n".join(m["content"] for m in messages if m["role"] == "system")
    user = "\n\n".join(m["content"] for m in messages if m["role"] != "system")
    prompt = (system + "\n\n" + user).strip() if system else user

    config = {"temperature": temperature}
    if json_mode:
        config["response_mime_type"] = "application/json"

    resp = model.generate_content(prompt, generation_config=config)
    return resp.text


def chat(
    messages: List[Dict],
    *,
    json_mode: bool = False,
    temperature: float = 0.2,
) -> str:
    """Send chat messages to the active provider and return raw text."""
    provider = active_provider()
    if provider is None:
        raise RuntimeError("No LLM provider configured (set GROQ_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY)")

    if provider == "groq":
        return _chat_openai_compat(
            "groq",
            os.environ["GROQ_API_KEY"],
            "https://api.groq.com/openai/v1",
            messages,
            json_mode=json_mode,
            temperature=temperature,
        )
    if provider == "openai":
        return _chat_openai_compat(
            "openai",
            os.environ["OPENAI_API_KEY"],
            None,
            messages,
            json_mode=json_mode,
            temperature=temperature,
        )
    if provider == "gemini":
        return _chat_gemini(messages, json_mode=json_mode, temperature=temperature)

    raise RuntimeError(f"Unknown provider: {provider}")


def chat_json(messages: List[Dict], *, temperature: float = 0.2) -> Dict:
    """Send chat messages and parse the response as JSON."""
    raw = chat(messages, json_mode=True, temperature=temperature)
    return json.loads(raw)
