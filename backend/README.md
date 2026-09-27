# Backend (Node.js / Express) — DocuMind AI

**Status: Phase 0 placeholder — no application code yet.**

The main application backend and single entry point for the frontend.

## Planned responsibilities

- User registration, login, and JWT authentication.
- Authorization checks and protected routes.
- Document metadata (name, owner, size, upload date, indexing status) in MongoDB.
- File upload handling and forwarding files to the AI service.
- Chat/conversation history persistence.
- Proxying question-answering requests to the FastAPI AI service.
- Application-level APIs consumed by the React frontend.

## Explicitly NOT this service's job

- PDF text extraction, chunking, embeddings, FAISS, retrieval, LLM calls — all belong to `ai-service/`.

## Planned stack

- Node.js (LTS), Express.js
- MongoDB + Mongoose
- JWT auth, bcrypt for password hashing
- Multer (or similar) for uploads
- Deploy target: Render

## Directory (created from Phase 5 onward)

```
backend/
├── src/
│   ├── config/
│   ├── controllers/
│   ├── routes/
│   ├── middleware/
│   ├── models/
│   └── services/        # calls to ai-service
├── .env.example
├── package.json
└── server.js
```

## Environment

See [`.env.example`](./.env.example). Copy it to `.env` locally; `.env` is git-ignored.

## Development

Nothing to run yet. From Phase 5:

```bash
npm install
npm run dev
```
