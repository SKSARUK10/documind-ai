# AI Service (Python / FastAPI) — DocuMind AI

**Status: Phase 0 placeholder — no application code yet.**

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

## Directory (created from Phase 1 onward)

```
ai-service/
├── app/
│   ├── main.py
│   ├── api/
│   ├── core/
│   ├── services/        # extraction, chunking, embeddings, retrieval, llm
│   └── models/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

## Environment

See [`.env.example`](./.env.example). Copy it to `.env` locally; `.env` is git-ignored.

## Development

Nothing to run yet. From Phase 1:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate    # macOS / Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Conventions for later phases

- Python code style: `ruff` / `black` (configured in Phase 1).
- Tests: `pytest` under `tests/`.
