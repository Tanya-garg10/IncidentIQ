# IncidentIQ 🚨

**AI-powered incident analysis for production infrastructure.**
Stream live logs, detect root causes, predict failures, correlate with deployments, and chat with your infrastructure — all on a polished real-time dashboard.

## What it does

- **Live log streaming** over WebSockets, multi-service tagging
- **Root cause detection** with rule-based engine + OpenAI GPT (auto-fallback)
- **Anomaly detection** — rolling-window error-rate analysis with predictive alerts
- **Service health scoring** — 0–100 score per service (auth, payment, user, gateway)
- **Deployment correlation** — "issue began ~2 min after the payment-service v2.4.1 deploy"
- **Chat with your infra** — ask questions, get answers grounded in your logs
- **Downloadable reports** — incident summary as Markdown
- **History** — incidents persisted to SQLite

## Architecture

```
   App logs ─┐
             ▼
    ┌─────────────────┐    ┌────────────────────┐
    │ FastAPI backend │───▶│ AI Engine (rules + │
    │  /analyze       │    │   OpenAI GPT)      │
    │  /anomaly       │    └────────────────────┘
    │  /services      │              │
    │  /chat          │              ▼
    │  /report.md     │    ┌────────────────────┐
    │  WS /ws/logs    │───▶│ SQLite history     │
    └─────────────────┘    │ + deployments      │
             │             └────────────────────┘
             ▼
    ┌────────────────────────────────────┐
    │ Next.js dashboard (glassmorphism)  │
    │  • Live logs   • Anomaly card      │
    │  • Severity    • Service grid      │
    │  • Timeline    • AI chat panel     │
    └────────────────────────────────────┘
```

## Project Structure

```
IncidentIQ/
├── backend/        FastAPI + WebSockets + SQLite
├── frontend/       Next.js 14 + Tailwind + Framer Motion + Recharts
├── logs/           Sample log files
├── ai-engine/      Rule-based + OpenAI analyzers + severity utils
├── docker/         Dockerfiles + docker-compose
└── README.md
```

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
# optional, enables real AI responses everywhere:
cp .env.example .env  # then add OPENAI_API_KEY=...
uvicorn main:app --reload
```

API at http://127.0.0.1:8000 · Swagger UI at `/docs`.

### Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

Dashboard at http://localhost:3000.

### Docker (whole stack)

```bash
cd docker
docker compose up --build
```

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/` | health |
| GET | `/logs` | recent log buffer |
| GET | `/analyze` | full AI report (incidents, anomaly, services, correlation) |
| GET | `/anomaly` | error-rate trend + predictive alert |
| GET | `/services` | per-service health scores |
| GET | `/metrics` | severity counts for charts |
| GET | `/incidents` | persisted incident history |
| GET | `/deployments` | deployment history |
| POST | `/deployments` | record a real deployment |
| POST | `/chat` | ask a question about your logs |
| GET | `/report.md` | download incident report |
| POST | `/simulate` | inject a realistic outage burst |
| POST | `/simulate/deployment` | record a fake deployment (demo) |
| WS | `/ws/logs` | live log stream |

## Demo Flow 🎤

> "Imagine your production server crashes at 2 AM. Most teams find out from angry tweets."

1. Open http://localhost:3000 — logs are already streaming, services healthy
2. Click **🚀 Mark Deployment** — records that payment-service just shipped v2.4.1
3. Click **🔥 Simulate Incident** — watch:
   - Logs flood in, payment-service goes red
   - Severity meter jumps to **Critical**
   - Anomaly card shows error-rate spike + 🔮 predictive alert
   - Service grid: payment-service drops to ~30/100, status `DOWN`
   - **Deployment correlation** banner: "Issue began ~1 min after payment-service v2.4.1 deployment"
   - Timeline grows with new red dots
   - Active Incidents card lists root causes and recommended fixes
4. Open the chat panel and ask: *"Why did the service crash?"* — get a grounded answer
5. Click **⬇ Report** — downloads a clean Markdown incident report

## Roadmap

| Phase | Goal | Status |
|-------|------|--------|
| 1 | Backend + fake logs + rule-based analyzer | ✅ |
| 2 | Next.js + Tailwind dashboard | ✅ |
| 3 | OpenAI integration with rule-based fallback | ✅ |
| 4 | Charts, timeline, severity meter, animations | ✅ |
| 5 | Docker deployment | ✅ |
| 6 | Multi-service tagging + health scores | ✅ |
| 7 | Anomaly detection + predictive alerts | ✅ |
| 8 | Deployment tracking + AI correlation | ✅ |
| 9 | Chat with your infrastructure | ✅ |
| 10 | Markdown incident reports | ✅ |
| 11 | SQLite incident history | ✅ |
| 12 | Glassmorphism UI polish | ✅ |
| 13 | Notifications (Slack / Telegram) | ⏳ |
| 14 | Anomaly detection with sklearn IsolationForest | ⏳ |

## Tech Stack

- **Backend:** Python, FastAPI, WebSockets, SQLite, OpenAI
- **Frontend:** Next.js 14, Tailwind, Framer Motion, Recharts
- **AI:** OpenAI `gpt-4o-mini` (configurable) + rule-based fallback
- **Deploy:** Docker Compose · Vercel + Render compatible
