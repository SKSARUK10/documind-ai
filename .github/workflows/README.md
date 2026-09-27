# GitHub Actions Workflows

**Status: Phase 0 placeholder — no workflows configured yet.**

`.github/workflows/` is reserved for CI/CD configuration. Creating real workflow YAML before there is code to build, test, or lint would only produce failing or no-op runs, so none has been added.

## Planned workflows (later phases)

| Workflow | Trigger | Phase |
| --- | --- | --- |
| `ai-service-ci.yml` — ruff/black check + pytest | push/PR to `main` touching `ai-service/` | Phase 1+ |
| `backend-ci.yml` — lint + unit tests | push/PR to `main` touching `backend/` | Phase 5+ |
| `frontend-ci.yml` — lint + build + component tests | push/PR to `main` touching `frontend/` | Phase 7+ |
| `deploy.yml` | push to `main` / release tags | Phase 11 |

## Conventions when added

- Secrets (`LLM_API_KEY`, `MONGODB_URI`, etc.) go in GitHub Actions secrets, never in YAML.
- Paths filters keep each pipeline running only when its service changes.
- Deployment jobs are protected by GitHub environments with required reviewers.

No remote repository or GitHub account is connected at this stage — this directory is local-only preparation.
