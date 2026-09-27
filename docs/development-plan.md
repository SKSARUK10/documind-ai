# DocuMind AI — Development Plan

**Current phase: Phase 2 — PDF Document Processing (next)**

Each phase has a single goal and a clear "done" signal.

---

## Phase 0 — Project setup and documentation ✅

**Goal:** A clean, GitHub-ready repository with structure, configuration placeholders, and documentation.

**Includes:**
- Repository folder structure (`frontend/`, `backend/`, `ai-service/`, `docs/`, `docker/`, `.github/workflows/`)
- `.gitignore`, `.env.example` placeholders, MIT `LICENSE`
- Root `README.md`, per-service READMEs, architecture doc, this plan
- Git initialization and one initial commit

**Done when:** The repo compiles nothing, runs nothing, and explains everything. ✅

---

## Phase 1 — Python + FastAPI foundation ✅

**Goal:** A minimal, runnable FastAPI service with health check, project layout, config loading from `.env`, CORS, logging, and a pytest smoke test.

**Delivered:**
- `app/main.py` application factory with CORS + structured logging
- `app/core/config.py` — pydantic-settings reading `.env` (safe defaults, no secrets required)
- `app/api/routes/health.py` — `GET /health`
- `tests/test_health.py` — 3 passing tests (health, 404, CORS preflight)
- `requirements.txt` (pinned), `pytest.ini`

**Done when:** `uvicorn app.main:app --reload` starts and `/health` returns OK; `pytest` passes. ✅

---

## Phase 2 — PDF document processing *(next)*

**Goal:** Accept a PDF, extract text page by page, and return structured text with page numbers.

**Done when:** A sample PDF can be processed and each page's text is retrievable.

---

## Phase 3 — Embeddings + FAISS

**Goal:** Chunk extracted text with overlap (carrying page metadata), generate embeddings, build a FAISS index, and run top-k similarity search.

**Done when:** Given a query, the service returns the most relevant chunks with their document/page references.

---

## Phase 4 — RAG + LLM

**Goal:** Assemble retrieved context into a prompt, call a paid LLM API through a provider-agnostic abstraction, and return an answer with sources.

**Done when:** A question about an indexed PDF returns a grounded answer plus page citations; no provider-specific code leaks outside the abstraction.

---

## Phase 5 — Node.js + MongoDB

**Goal:** Express backend with MongoDB models, user registration/login (JWT), document metadata endpoints, and protected routes.

**Done when:** A user can register, log in, and CRUD document metadata with a valid token.

---

## Phase 6 — Node.js ↔ FastAPI integration

**Goal:** Node.js forwards uploads and questions to FastAPI, maps responses, and updates indexing status in MongoDB.

**Done when:** Upload → index → ask works end-to-end via the Node.js API only.

---

## Phase 7 — React frontend

**Goal:** Vite + React UI: auth screens, document upload, document list, chat-style Q&A showing answers with sources.

**Done when:** A user can complete the full journey in the browser without curl.

---

## Phase 8 — Chat history and multiple documents

**Goal:** Persist conversations, support multiple documents and (optionally) cross-document questions.

**Done when:** Past conversations reload correctly and multi-document queries work.

---

## Phase 9 — Agentic capabilities

**Goal:** Introduce tool-calling patterns: the model can decide to retrieve, compare, or summarize on its behalf.

**Done when:** A multi-step question is solved through explicit tool calls with visible traces.

---

## Phase 10 — MCP integration

**Goal:** Expose selected capabilities as MCP tools and/or consume MCP tools from the AI service.

**Done when:** At least one DocuMind capability is usable through an MCP client.

---

## Phase 11 — Docker and deployment

**Goal:** Dockerize all three services, provide compose for local one-command startup, and deploy frontend/backend/AI service/database.

**Done when:** A fresh clone starts with `docker compose up`, and the deployed URL works end-to-end.

---

## Phase 12 — Production improvements and cost optimization

**Goal:** Hardening: rate limiting, monitoring, caching, embedding/index optimization, token-cost reduction, error budgets.

**Done when:** SLOs are defined and met; cost per query is measured and acceptable.

---

## Status legend

| Symbol | Meaning |
| --- | --- |
| ✅ | Completed |
| ⬜ | Planned, not started |
