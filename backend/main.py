"""IncidentIQ FastAPI backend."""

import asyncio
from collections import Counter
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Set

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

import anomaly
import chat
import incident_store
import log_store
import services as svc_health
from ai_engine_loader import (
    SEVERITY_COLOR,
    SEVERITY_LABEL,
    detect_level,
    rule_based_analyze,
    smart_analyze,
)
from log_reader import read_logs
from log_simulator import burst_incident, next_event
from report import render_markdown

load_dotenv()
incident_store.init_db()

# --- WebSocket connection manager -----------------------------------------

_clients: Set[WebSocket] = set()
_clients_lock = asyncio.Lock()


async def _broadcast(message: dict) -> None:
    async with _clients_lock:
        dead = []
        for ws in _clients:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            _clients.discard(ws)


async def _log_generator():
    while True:
        await asyncio.sleep(2)
        line = next_event()
        log_store.append(line)
        await _broadcast({"type": "log", "line": line})


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_store.seed(read_logs())
    task = asyncio.create_task(_log_generator())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(
    title="IncidentIQ",
    description="AI-powered incident analysis from log files.",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- helpers ---------------------------------------------------------------

def _full_report(logs):
    """Build the analysis report and persist any new incidents."""
    report = smart_analyze(logs)
    report["anomaly"] = anomaly.detect(logs)
    report["services"] = svc_health.health_scores(logs)

    # Correlate with the most recent deployment (Step 23)
    deploy = incident_store.latest_deployment()
    correlation = None
    if deploy and report["incidents"]:
        try:
            ts = datetime.fromisoformat(deploy["deployed_at"].replace(" ", "T"))
            mins = (datetime.utcnow() - ts).total_seconds() / 60
            if mins < 30:
                correlation = (
                    f"Issue began ~{mins:.0f} min after the {deploy['service']} "
                    f"v{deploy['version']} deployment. Consider rollback."
                )
        except Exception:
            pass
    report["deployment_correlation"] = correlation

    # Persist incidents (best effort, non-fatal)
    for inc in report.get("incidents", []):
        incident_store.record_incident(inc)
    return report


# --- HTTP routes -----------------------------------------------------------

@app.get("/")
def home():
    return {"message": "IncidentIQ Backend Running", "version": "0.3.0"}


@app.get("/logs")
def get_logs():
    logs = log_store.snapshot()
    return {"count": len(logs), "logs": logs}


@app.get("/analyze")
def analyze():
    return _full_report(log_store.snapshot())


@app.get("/analyze/rules")
def analyze_rules():
    return rule_based_analyze(log_store.snapshot())


@app.get("/metrics")
def metrics():
    counts = Counter(detect_level(line) for line in log_store.snapshot())
    return {
        "counts": [
            {
                "level": level,
                "label": SEVERITY_LABEL[level],
                "count": counts.get(level, 0),
                "color": SEVERITY_COLOR[level],
            }
            for level in ("INFO", "WARNING", "ERROR", "CRITICAL")
        ],
        "total": sum(counts.values()),
    }


@app.get("/services")
def services():
    return {"services": svc_health.health_scores(log_store.snapshot())}


@app.get("/anomaly")
def anomaly_endpoint():
    return anomaly.detect(log_store.snapshot())


@app.get("/incidents")
def incidents_history(limit: int = 50):
    return {"incidents": incident_store.list_incidents(limit)}


# --- Deployments (Step 23) ------------------------------------------------

class DeploymentBody(BaseModel):
    service: str
    version: str
    note: str = ""


@app.post("/deployments")
def add_deployment(body: DeploymentBody):
    incident_store.record_deployment(body.service, body.version, body.note)
    return {"ok": True, "latest": incident_store.latest_deployment()}


@app.get("/deployments")
def deployments():
    return {"deployments": incident_store.list_deployments()}


# --- Chat (Step 21) -------------------------------------------------------

class ChatBody(BaseModel):
    question: str


@app.post("/chat")
def chat_endpoint(body: ChatBody):
    return chat.answer(body.question, log_store.snapshot())


# --- Report download (Step 20) --------------------------------------------

@app.get("/report.md", response_class=PlainTextResponse)
def report_download():
    logs = log_store.snapshot()
    rep = smart_analyze(logs)
    return render_markdown(rep, anomaly.detect(logs), svc_health.health_scores(logs))


# --- Demo control ---------------------------------------------------------

@app.post("/simulate")
async def simulate():
    lines = burst_incident()
    log_store.extend(lines)
    for line in lines:
        await _broadcast({"type": "log", "line": line})
    return {"injected": lines}


@app.post("/simulate/deployment")
async def simulate_deployment():
    """Record a fake deployment so judges can see the correlation feature."""
    incident_store.record_deployment(
        service="payment-service", version="2.4.1", note="hotfix release"
    )
    return {"ok": True, "latest": incident_store.latest_deployment()}


# --- WebSocket -------------------------------------------------------------

@app.websocket("/ws/logs")
async def ws_logs(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({"type": "snapshot", "logs": log_store.snapshot()})

    async with _clients_lock:
        _clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        async with _clients_lock:
            _clients.discard(websocket)
