# AI Service (Python / FastAPI) — DocuMind AI

**Status: Phase 1 complete — FastAPI foundation (health check, config, CORS) + agent route skeleton (schemas, `/agent/chat`, `/agent/tools`). No agent loop yet.**

The AI/ML service. It owns everything related to turning documents into answers.

## Planned responsibilities

- Receive PDF files from the Node.js backend.
- Text extraction with page numbers preserved.
- Text chunking (overlapping windows, page-aware metadata).
- Embedding generation.
- Building and querying the FAISS index.
- Retrieval of relevant context for a question.
- Prompt assembly and paid LLM API calls.
- Returning answer text + source/page metadata to the backend.
- Future: agentic logic and MCP tool usage.

## Explicitly NOT this service's job

- Authentication, users, authorization, chat history, document metadata — all belong to `backend/`.

## Planned stack

- Python 3.11+, FastAPI, Uvicorn
- PDF extraction library (decision in Phase 2)
- Embedding model / provider (decision in Phase 3)
- FAISS (Phase 3)
- LLM SDK chosen in Phase 4 — **no provider is hard-coded now**
- Deploy target: Render

## Current directory (Phase 1)

```
ai-service/
├── app/
│   ├── __init__.py
│   ├── main.py            # app factory, CORS, logging, router mounting
│   ├── api/
│   │   └── routes/
│   │       ├── health.py   # GET /health
│   │       └── agent.py    # POST /agent/chat (501 skeleton), GET /agent/tools
│   ├── core/
│   │   └── config.py      # pydantic-settings, reads .env
│   └── models/
│       └── agent.py       # ChatRequest / ChatResponse / trace schemas
├── tests/
│   ├── test_health.py
│   └── test_agent.py
├── .env.example
├── requirements.txt
├── pytest.ini
└── README.md

# planned from Phase 2+
├── app/services/          # extraction, chunking, embeddings, retrieval, llm
├── app/models/            # request/response schemas
└── app/api/routes/        # documents, ask, index
```

## Environment

See [`.env.example`](./.env.example). Copy it to `.env` locally; `.env` is git-ignored. All values have defaults, so the service runs without a `.env` file.

## Development

```bash
cd ai-service
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # macOS / Linux
pip install -r requirements.txt

uvicorn app.main:app --reload     # http://127.0.0.1:8000  (docs at /docs)
pytest                            # smoke tests
```

**Implemented endpoints:** `GET /health` → `{"status":"ok","service":"documind-ai-service"}`; skeleton `POST /agent/chat` (501 until the agent loop lands) and `GET /agent/tools` (empty registry).

## Conventions for later phases

- Python code style: `ruff` (planned, not yet configured).
- Tests: `pytest` under `tests/`.
- No secrets in code — configuration only via `app/core/config.py` + environment variables.
