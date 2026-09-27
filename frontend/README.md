# Frontend — DocuMind AI

**Status: Phase 0 placeholder — no application code yet.**

React + Vite single-page application for DocuMind AI.

## Planned responsibilities

- Upload documents (PDF) and show upload/processing status.
- Ask natural-language questions about indexed documents.
- Display answers together with source/page references.
- Manage the list of the user's documents.
- Handle authentication flows (login/register) against the Node.js backend.
- Present chat history (later phases).

## Planned stack

- React 18+ with Vite
- Routing (React Router)
- HTTP client (fetch/axios)
- Plain CSS / Tailwind (decision made in Phase 7)
- Deploy target: Netlify

## Directory (created in Phase 7)

```
frontend/
├── src/
├── public/
├── index.html
├── package.json
└── vite.config.js
```

## Development

Nothing to run yet. In Phase 7:

```bash
npm install
npm run dev
```

The frontend will call the Node.js backend (`backend/`), never the AI service directly.
