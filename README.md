# ESG Monitor

> Upload ESG (Environmental, Social, Governance) reports and receive **explainable** E/S/G sub-scores, topic tags, branch/location summaries, and a JSON report — all via a clean FastAPI v1 backend and a minimal React UI.

---

## 1) Background

### What this is
ESG Monitor is a compact, end-to-end AI application that ingests PDF/text sustainability reports and produces:
- **Summaries** of the document (token-aware, chunked)
- **Topic tags** across ESG pillars via **zero-shot classification** (no custom training)
- **Explainable E/S/G sub-scores** with contribution breakdowns
- **Branch/location summaries** using NER-detected locations
- **Persisted artifacts** (documents + scores) in Postgres

It is a **skills demo** for AI engineering: ingestion → transformer pipelines (CPU/GPU safe) → scoring → API design → persistence → tests/CI → containerization → simple UI.

### What this is not
Not a ratings agency product. **Scores are heuristic and transparent** by design; see `backend/nlp/scoring.py`. Use it for prototyping, research demos, and engineering interviews.

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

## 3) Architecture
```mermaid
flowchart LR
  A[React Frontend] -->|HTTP| B[FastAPI /api/v1]
  B --> C[Transformers Pipelines (BART, BERT, MNLI, SST2)]
  B --> D[(Postgres)]
  C --> B
  B --> A

4) Prerequisites

Python 3.11+

Node 18+ (for the frontend)

Docker (optional, for compose)

PostgreSQL (optional locally; compose provides one)

5) Setup (Local, no Docker)
# 1) Create env & install deps
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt

# 2) Start a local Postgres (choose one):
# a) Docker ephemeral:
docker run --name esg-pg -e POSTGRES_USER=esg -e POSTGRES_PASSWORD=esg \
  -e POSTGRES_DB=esg_monitor -p 5432:5432 -d postgres:16
# b) Or use your local Postgres and create the DB manually

# 3) Configure env (creates tables on startup)
export DB_HOST=localhost DB_PORT=5432 DB_USER=esg DB_PASSWORD=esg DB_NAME=esg_monitor

# 4) Run API
uvicorn backend.app:app --reload --port 8000
# → http://127.0.0.1:8000/api/v1/docs

