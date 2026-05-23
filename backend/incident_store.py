"""SQLite-backed incident history and deployment tracking.

Zero-config: file lives at backend/incidents.db. Stdlib only.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from typing import Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent / "incidents.db"
_lock = Lock()


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def _cursor():
    with _lock:
        conn = _connect()
        try:
            yield conn.cursor()
            conn.commit()
        finally:
            conn.close()


def init_db() -> None:
    with _cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                issue TEXT NOT NULL,
                cause TEXT,
                solution TEXT,
                severity TEXT,
                service TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS deployments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deployed_at TEXT DEFAULT CURRENT_TIMESTAMP,
                service TEXT NOT NULL,
                version TEXT,
                note TEXT
            )
            """
        )


def record_incident(inc: Dict, service: Optional[str] = None) -> int:
    with _cursor() as cur:
        cur.execute(
            """
            INSERT INTO incidents (issue, cause, solution, severity, service)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                inc.get("issue"),
                inc.get("cause"),
                inc.get("solution"),
                inc.get("severity"),
                service,
            ),
        )
        return cur.lastrowid


def list_incidents(limit: int = 50) -> List[Dict]:
    with _cursor() as cur:
        rows = cur.execute(
            "SELECT * FROM incidents ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def record_deployment(service: str, version: str, note: str = "") -> int:
    with _cursor() as cur:
        cur.execute(
            "INSERT INTO deployments (service, version, note) VALUES (?, ?, ?)",
            (service, version, note),
        )
        return cur.lastrowid


def latest_deployment() -> Optional[Dict]:
    with _cursor() as cur:
        row = cur.execute(
            "SELECT * FROM deployments ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def list_deployments(limit: int = 20) -> List[Dict]:
    with _cursor() as cur:
        rows = cur.execute(
            "SELECT * FROM deployments ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]
