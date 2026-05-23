"""In-memory ring buffer of recent log lines, shared across requests."""

from collections import deque
from threading import Lock
from typing import List

_MAX_LINES = 200
_buffer: deque = deque(maxlen=_MAX_LINES)
_lock = Lock()


def seed(lines: List[str]) -> None:
    with _lock:
        _buffer.clear()
        _buffer.extend(lines)


def append(line: str) -> None:
    with _lock:
        _buffer.append(line)


def extend(lines: List[str]) -> None:
    with _lock:
        _buffer.extend(lines)


def snapshot() -> List[str]:
    with _lock:
        return list(_buffer)


def clear() -> None:
    with _lock:
        _buffer.clear()
