# DocuMind AI — Planned Architecture

**Status: documentation only (Phase 0). No service is implemented yet.**

## 1. High-level flow

```
React Frontend
       ↓
Node.js / Express API
       ↓
Python / FastAPI AI Service
       ↓
Document Processing
       ↓
Chunking
       ↓
Embeddings
       ↓
FAISS
       ↓
Relevant Context
       ↓
LLM
       ↓
Answer + Source/Page Information
```

## 2. Core architecture decision

**Node.js is the main application backend. FastAPI is the AI worker.**

The system is deliberately split this way because:

- The project owner is a MERN-stack developer — all application, auth, data, and API concerns stay in familiar territory (JavaScript/Express/MongoDB).
- Python ecosystem is the natural home for PDF parsing, embeddings, FAISS, and LLM tooling.
- The two services can be developed, tested, deployed, and scaled independently.
- The frontend only ever talks to one API (Node.js); it never needs to know the AI service exists.

Communication model: **frontend → Node.js → FastAPI**, synchronous HTTP for a single request/response, with a queue-based or background-job option considered later for long-running indexing.

## 3. Service responsibilities

### 3.1 React Frontend

- UI for uploading documents, asking questions, and viewing answers with sources.
- Talks exclusively to the Node.js API.
- Holds no secrets other than what is unavoidable in a browser context (none today).
- Deployment: Netlify.

### 3.2 Node.js / Express — main backend

Owns everything that is *application* logic:

- Authentication (JWT), password hashing, session/token handling.
- Users and authorization (whose documents, whose chats).
- Document metadata: filename, owner, size, upload time, indexing status.
- Chat history persistence (MongoDB).
- Application-level REST APIs for the frontend.
- Forwarding files and questions to the FastAPI service, and mapping its responses back.

Does **not** own: PDF parsing, chunking, embeddings, FAISS, retrieval, or LLM calls.

Deployment: Render. Database: MongoDB (Atlas in production).

### 3.3 Python / FastAPI — AI service

Owns everything that is *AI* logic:

- PDF processing and text extraction (page-aware).
- Text chunking with overlap and page tracking.
- Embedding generation.
- FAISS index creation, persistence, and similarity search.
- Retrieval of top-k relevant chunks.
- Prompt construction and paid LLM API interaction.
- Returning `{ answer, sources: [{ document, page, snippet }] }`.
- Future: agentic workflows, tool calling, MCP tool usage.

Does **not** own: users, auth, authorization, chat history, document metadata.

Deployment: Render. Internal only — not exposed to the public internet.

### 3.4 MongoDB

- Stores users, document metadata, chat sessions, and messages.
- Stores **no** vector data (FAISS owns that) and **no** file bytes (disk/Cloudinary owns that).

### 3.5 FAISS

- Local vector index files on disk (`faiss_index/`, git-ignored).
- One index (or index shard) per document initially; a consolidated index is a later optimization.
- Rebuilt from stored chunks when needed.

### 3.6 File storage

- Phase 0–10: local `uploads/` directory (git-ignored).
- Later: Cloudinary for durable object storage.

### 3.7 LLM

- Paid API, called only from the FastAPI service.
- Provider is **not** decided and **not** hard-coded — an abstraction layer is planned so the provider can be swapped (Phase 4).
- Keys are supplied only via environment variables.

## 4. Planned request flows

### 4.1 Upload and index

```
User → Frontend → Node.js (auth, metadata, store file)
                     → FastAPI (extract text → chunk → embed → FAISS)
                     ← status
       Node.js updates indexing status in MongoDB
       ← upload/indexing result
User ← Frontend
```

### 4.2 Ask a question

```
User → Frontend → Node.js (auth, load history)
                     → FastAPI (embed question → FAISS top-k → build prompt → LLM)
                     ← answer + sources
       Node.js saves Q/A to MongoDB
       ← response
User ← Frontend (answer + page citations)
```

## 5. Cross-cutting concerns (planned, not implemented)

- **Configuration** — all secrets via `.env`; `.env.example` committed, `.env` ignored.
- **Validation** — request validation at both service boundaries.
- **Errors** — consistent JSON error shape across services.
- **CORS** — FastAPI allows only Node.js; Node.js allows only the frontend origin.
- **Rate limiting** — on public Node.js endpoints.
- **Observability** — structured logs; retrieval/token metrics later.
- **Testing** — pytest for AI service, jest/vitest for backend, component tests for frontend.

## 6. Deployment topology (planned)

| Service | Platform | Notes |
| --- | --- | --- |
| React frontend | Netlify | Static build |
| Node.js backend | Render | Public entry point |
| FastAPI AI service | Render | Private/internal |
| MongoDB | MongoDB Atlas | M0 to start |
| Files | Local → Cloudinary | Migrate later |

## 7. Explicitly out of scope for now

Authentication, PDF processing, chunking, embeddings, FAISS, LLM integration, chat, agentic workflows, MCP, Docker, and deployment are **documented here but not implemented**.
