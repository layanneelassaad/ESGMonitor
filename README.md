# ESG Monitor

> Upload ESG (Environmental, Social, Governance) reports and receive **explainable** sub-scores, topic tags, branch and location summaries, and a JSON report.

---

## 1) Background

### What this is
ESG Monitor is a compact, end-to-end AI application that ingests PDF/text sustainability reports and produces:
- **Summaries** of the document (token-aware, chunked)
- **Topic tags** across ESG pillars via **zero-shot classification** (no custom training)
- **Explainable E/S/G sub-scores** with contribution breakdowns
- **Branch/location summaries** using NER-detected locations
- **Persisted artifacts** (documents + scores) in Postgres

---

## 2) Features
- **FastAPI** (`/api/v1`) with typed Pydantic schemas & CORS
- **Transformers pipelines** (summarization, NER, zero-shot, sentiment) with **CPU/GPU fallback**
- **Token-aware chunking** with overlap + **offline fallback**
- **Explainable scoring**: E/S/G + sentiment weights → total score with contributions
- **Postgres** persistence; **auto-create tables** on startup (demo friendly)
- **Docker Compose** for one-command spin-up
- **Pytest + GitHub Actions** CI; Ruff for linting
- Minimal **React** frontend (Vite)

---

## 3) Prerequisites


- Python 3.11+

- Node 18+ (for the frontend)

- Docker (optional, for compose)

- PostgreSQL (optional locally; compose provides one)

---

## 4) Setup

Option 1: Local
```bash
# 1) Create env & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

# 2) Start a local Postgres
# a) Docker ephemeral:
docker run --name esg-pg -e POSTGRES_USER=esg -e POSTGRES_PASSWORD=esg \
  -e POSTGRES_DB=esg_monitor -p 5432:5432 -d postgres:16
# b) Or use your local Postgres and create the DB manually

# 3) Configure env (creates tables on startup)
export DB_HOST=localhost DB_PORT=5432 DB_USER=esg DB_PASSWORD=esg DB_NAME=esg_monitor

# 4) Run API
uvicorn backend.app:app --reload --port 8000
# → http://127.0.0.1:8000/api/v1/docs
```
Frontend:
```bash
cd frontend
npm install
npm run dev
# → http://127.0.0.1:5173
```

Option 2: Docker compose
```bash
docker compose up --build
# API: http://127.0.0.1:8000/api/v1/docs
```
> Note: On first API call, Hugging Face models download to cache. For offline/CI runs, set TRANSFORMERS_OFFLINE=1 (chunking falls back to character windows).
