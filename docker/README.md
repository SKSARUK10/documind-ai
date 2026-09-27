# Docker — DocuMind AI

**Status: Phase 0 placeholder — no Docker files yet.**

This folder will hold container configuration for the three services once **Phase 11 (Docker and deployment)** begins.

## Planned contents

```
docker/
├── README.md                  # this file
├── frontend.Dockerfile
├── backend.Dockerfile
├── ai-service.Dockerfile
└── docker-compose.yml         # or a root-level compose file
```

## Planned services in compose

| Service | Image base | Port |
| --- | --- | --- |
| frontend | node (build) | 5173 / 80 |
| backend | node (build) | 4000 (example) |
| ai-service | python 3.11 | 8000 |
| mongo | mongo | 27017 |

Volumes are planned for `uploads/` and `faiss_index/` so indexed data survives restarts.

## Note

No `Dockerfile`, `compose` file, or image is committed in Phase 0 — intentionally. Containerization is deferred so that the services exist first.
