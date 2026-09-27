# DocuMind AI

> **Status: Phase 0 — Project Setup / Initialization**
> Nothing in this repository is implemented yet. Everything below describes the *planned* system.

DocuMind AI is a full-stack AI document assistant that will allow users to upload documents and ask natural-language questions about their content. The system is designed around a React frontend, a Node.js/Express backend, a Python FastAPI AI service, a RAG (Retrieval-Augmented Generation) pipeline, and FAISS vector search.

---

## 1. Overview

DocuMind AI targets a single, clear job: turn a pile of PDF documents into something you can have a conversation with. A user uploads a document, the system extracts and indexes its content, and the user can then ask questions in plain language and receive answers grounded in the document — together with the page/slice information the answer came from.

The project is intentionally split into three deployable services so that each layer can be learned, tested, and scaled independently:

- **Frontend (React + Vite)** — user interface.
- **Main backend (Node.js + Express)** — application logic, users, auth, document metadata, chat history.
- **AI service (Python + FastAPI)** — document processing, chunking, embeddings, FAISS retrieval, LLM interaction.

## 2. Problem Statement

Working with long documents is slow and error-prone. Readers must scan hundreds of pages to answer a single question, and generic chatbots cannot cite where an answer came from, which makes their output untrustworthy for research, legal, technical, or academic material.

DocuMind AI addresses this by combining:

1. **Retrieval** — only the relevant slices of a document are considered.
2. **Grounding** — answers are produced from retrieved context, not from model memory alone.
3. **Attribution** — each answer carries source/page information so it can be verified.

## 3. Project Goals

- Build a clean, multi-service architecture that separates web application concerns from AI concerns.
- Implement a working RAG pipeline: PDF → text → chunks → embeddings → FAISS → context → LLM → answer.
- Return answers with source/page metadata, not just prose.
- Keep the codebase approachable for a MERN developer who is concurrently learning Python, FastAPI, and AI engineering.
- Progress in small, verifiable phases (see `docs/development-plan.md`) rather than one large build.
- Leave the system ready for later additions: chat history, multiple documents, tool calling, agents, MCP, and production deployment.

## 4. Planned Features

> All features below are **planned**. None are implemented in Phase 0.

| Feature | Status |
| --- | --- |
| Project structure and documentation | ✅ Phase 0 (this phase) |
| PDF upload and text extraction | ⬜ Planned |
| Text chunking with page tracking | ⬜ Planned |
| Embeddings generation | ⬜ Planned |
| FAISS vector index and similarity search | ⬜ Planned |
| LLM-powered answers with cited sources/pages | ⬜ Planned |
| User authentication (JWT) | ⬜ Planned |
| Document metadata storage (MongoDB) | ⬜ Planned |
| Chat interface | ⬜ Planned |
| Chat history persistence | ⬜ Planned |
| Multiple document support | ⬜ Planned |
| Tool calling / agentic workflows | ⬜ Planned |
| MCP tool integration | ⬜ Planned |
| Dockerized local environment | ⬜ Planned |
| Production deployment | ⬜ Planned |

## 5. Planned Architecture

```
React Frontend
       ↓
Node.js / Express API          ← auth, users, metadata, chat history, authorization
       ↓
Python / FastAPI AI Service    ← PDF processing, chunking, embeddings, FAISS, retrieval, LLM
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
FAISS Vector Search
       ↓
Relevant Document Context
       ↓
LLM (paid API, provider-agnostic)
       ↓
Answer + Source/Page Information
```

**Key decision:** Node.js remains the main application backend; FastAPI owns AI-related processing only. Rationale and per-service responsibilities are documented in [`docs/architecture.md`](docs/architecture.md).

## 6. Technology Stack

| Layer | Technology | Notes |
| --- | --- | --- |
| Frontend | React, Vite | Deploy target: Netlify (later) |
| Main backend | Node.js, Express.js | Deploy target: Render (later) |
| AI service | Python, FastAPI | Deploy target: Render (later) |
| Database | MongoDB | Atlas in production (later) |
| Vector search | FAISS | Local index files for now |
| Document storage | Local disk → Cloudinary (later) | Not configured yet |
| LLM | Paid LLM API (TBD) | No provider hard-coded; chosen in a later phase |
| Containerization | Docker | Later phase |
| Version control | Git / GitHub | Local repo only at this stage |

## 7. RAG Workflow (Planned)

1. User uploads a PDF through the React frontend.
2. Node.js validates the request, records document metadata in MongoDB, and forwards the file to the FastAPI AI service.
3. FastAPI extracts text, preserving page numbers.
4. Text is split into overlapping chunks; each chunk keeps a reference to its source document and page range.
5. Chunks are converted into embeddings and written into a FAISS index.
6. At question time, the user's question is embedded and the k most similar chunks are retrieved.
7. Retrieved context + question are sent to the LLM with a prompt that requires grounded answers.
8. The response is returned with answer text and source/page metadata.
9. Node.js persists the exchange as chat history and returns it to the frontend.

## 8. Project Structure

```
documind-ai/
│
├── frontend/            # React + Vite application
├── backend/             # Node.js / Express main API
├── ai-service/          # Python / FastAPI AI service
├── docs/                # Architecture and planning documents
├── docker/              # Container configuration (later)
├── .github/
│   └── workflows/       # CI/CD (placeholder for now)
│
├── .gitignore
├── .env.example         # Placeholder environment variables
├── README.md
└── LICENSE
```

Each service folder contains its own `README.md` describing its intended responsibilities. `backend/.env.example` and `ai-service/.env.example` hold service-specific placeholder variables.

## 9. Development Roadmap

| Phase | Focus | Status |
| --- | --- | --- |
| 0 | Project setup and documentation | ✅ **Current** |
| 1 | Python + FastAPI foundation | ⬜ |
| 2 | PDF document processing | ⬜ |
| 3 | Embeddings + FAISS | ⬜ |
| 4 | RAG + LLM | ⬜ |
| 5 | Node.js + MongoDB | ⬜ |
| 6 | Node.js ↔ FastAPI integration | ⬜ |
| 7 | React frontend | ⬜ |
| 8 | Chat history and multiple documents | ⬜ |
| 9 | Agentic capabilities | ⬜ |
| 10 | MCP integration | ⬜ |
| 11 | Docker and deployment | ⬜ |
| 12 | Production improvements and cost optimization | ⬜ |

Full phase descriptions live in [`docs/development-plan.md`](docs/development-plan.md).

## 10. Environment Variables

Placeholder variables are listed in [`.env.example`](.env.example), with service-specific copies in `backend/.env.example` and `ai-service/.env.example`.

```
NODE_ENV=
PORT=
MONGODB_URI=
AI_SERVICE_URL=
LLM_API_KEY=
JWT_SECRET=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

- These are **examples/placeholders only** — no real values are committed.
- Real `.env` files are ignored by `.gitignore`.
- Never commit API keys, secrets, or connection strings.

## 11. Local Development

> Not runnable yet — no application code exists in Phase 0. This is the intended workflow once implementation begins.

```bash
# 1. Clone
git clone <your-repo-url>
cd documind-ai

# 2. Environment
copy .env.example .env          # Windows
# cp .env.example .env          # macOS / Linux
# then fill in values per service

# 3. AI service (Phase 1+)
cd ai-service
# python -m venv .venv && .venv\Scripts\activate
# pip install -r requirements.txt
# uvicorn app.main:app --reload

# 4. Backend (Phase 5+)
cd ../backend
# npm install
# npm run dev

# 5. Frontend (Phase 7+)
cd ../frontend
# npm install
# npm run dev
```

Prerequisites: Node.js (LTS), Python 3.11+, MongoDB (local or Atlas), Git.

## 12. Testing Strategy (Planned)

- **Python service** — `pytest` unit tests for extraction, chunking, retrieval helpers; later, evaluation sets for answer quality.
- **Node backend** — `jest`/`vitest` unit tests plus supertest-style API tests.
- **Frontend** — component tests with Vitest + React Testing Library; smoke tests for the upload/chat flows.
- **Integration** — end-to-end happy path: upload → index → ask → grounded answer.
- **RAG quality** — a small fixed question/answer dataset used to detect retrieval regressions.
- CI wiring is deferred to a later phase; `.github/workflows/` currently holds only a placeholder README.

## 13. Deployment Plan (Planned)

| Component | Target |
| --- | --- |
| React frontend | Netlify |
| Node.js backend | Render |
| FastAPI AI service | Render |
| MongoDB | MongoDB Atlas |
| Files | Local storage → Cloudinary |
| Secrets | Platform environment variables, never in Git |

Deployment, containerization, and CI/CD are Phase 11 work.

## 14. Security Considerations (Planned)

- Secrets live only in environment variables; `.env*` is git-ignored (`.env.example` is the sole exception).
- Authentication via JWT with short-lived access tokens and hashed passwords (Node.js side).
- Strict file-type and size validation on uploads; extracted text and uploaded files stored outside the web root.
- Rate limiting and request size limits on public endpoints.
- Prompt-injection awareness: retrieved document content is treated as untrusted data in LLM prompts.
- Least-privilege credentials for MongoDB, Cloudinary, and the LLM API key.
- Input validation on every API boundary; CORS restricted to the known frontend origin.
- Dependency and secret scanning once CI is introduced.

## 15. Future Improvements

- Streaming answers over SSE/WebSocket.
- Hybrid search (BM25 + vectors) and re-ranking.
- Multi-document and cross-document questions.
- Conversation memory and summarization of long chats.
- Tool calling, agentic workflows, and MCP tool integration.
- Cost/latency optimization: caching, smaller embedding models, index compression.
- Observability: tracing of retrieval quality, token usage, and latency.

## 16. License

MIT — see [LICENSE](LICENSE).
