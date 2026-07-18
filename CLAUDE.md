# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`ujmikamiapp` — Jozef Makiš's personal portfolio site. React/TypeScript frontend backed by a Django REST Framework API, deployed to Azure Container Apps with Azure Blob Storage for static/media files.

## Tech stack

| Layer | Details |
|---|---|
| Backend | Django 6.0.4, Django REST Framework 3.17.1, Python 3.12 (`python:3.12-slim`) |
| Backend libs | `django-environ` (env-driven settings), `django-cors-headers`, `django-storages[azure]`, `mysqlclient`, `gunicorn` (prod WSGI server) |
| Database | MySQL 8.0 (`env.db()` via `DATABASE_URL`; forced SSL CA in `settings.py`) |
| Frontend | React 19.2 + TypeScript 6, bootstrapped with `react-scripts` (CRA) 5.0.1 |
| Frontend serving | Multi-stage build: `node:20-alpine` builds the static bundle, `nginx:1.27-alpine` serves it |
| Reverse proxy | nginx (`frontend/nginx.conf`) serves the SPA at `/` and proxies `/api/`, `/admin/`, `/media/` to the `backend` service |
| Object storage | Azure Blob Storage for static/media in production (`ujmikamiapp/storage_backends.py`), local `FileSystemStorage` in dev |
| AI microservice | `fastapi-ai/` — FastAPI + Chroma Python client, talks to `chroma-db` over the Docker network by service name |
| Vector database | `chroma-db` service — official `chromadb/chroma` image, persisted via a named volume |
| Local orchestration | `docker-compose.yml`: `db` (MySQL), `backend` (Django), `frontend` (nginx), `chroma-db`, `fastapi-ai` — all on the compose-default network |
| Infra-as-code | Terraform (`terraform/`) — scaffolding only, `.tf` files currently empty |
| Testing/lint | Django test runner + `coverage.py` + `ruff` (backend); Jest + React Testing Library (frontend, via CRA's built-in setup); `pytest` + `pytest-asyncio` + `ruff` (fastapi-ai) |
| CI/CD | Single GitHub Actions workflow (`.github/workflows/azure-static-web-apps-*.yml`) — test/lint jobs gate the Azure deploy jobs via `needs:` |

## Commands

### Backend (`backend/ujmikamiapp/`)

```bash
cd backend/ujmikamiapp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver          # http://localhost:8000

python manage.py test                       # all backend tests
python manage.py test ml_models             # single app
python manage.py test projects.tests.SomeTestCase   # single test case
```

Lint + coverage (dev-only deps in `requirements-dev.txt`, same file used by CI):
```bash
pip install -r requirements-dev.txt
ruff check .                    # lint (config in pyproject.toml; migrations and seed-command
                                 # prose strings are exempted from line-length)
coverage run manage.py test && coverage report
```

Seed data (each app has its own seed command, run as needed):
```bash
python manage.py seed_ml_models
python manage.py seed_projects
python manage.py seed_experiences
python manage.py seed_publications
python manage.py seed_aboutme
```

After any model change:
```bash
python manage.py makemigrations <app_name>   # commit the migration file with the model change
```

### Frontend (`frontend/`)

```bash
cd frontend
npm install
REACT_APP_API_BASE_URL=http://localhost:8000 npm start   # http://localhost:3000
npm run build       # also runs CRA's built-in ESLint check
npm test             # watch mode
npm test -- --coverage --watchAll=false   # single run with coverage, matches CI
```

Markdown rendering in `ChatWidget` uses `markdown-to-jsx` pinned to `7.7.17`, not the current major —
`react-markdown`/newer `markdown-to-jsx` are ESM-only or use a package `exports` map that CRA's bundled
Jest (react-scripts 5, no eject) can't resolve. Don't casually bump this without re-verifying `npm test`.

### Full stack via Docker

```bash
docker compose up --build
```
Runs `db` (MySQL 8, gated by a healthcheck), `backend` (Django, port 8000), `frontend` (React build served by nginx, port 3000), `chroma-db` (vector DB, host port 8001 → container 8000), `fastapi-ai` (host port 8002 → container 8000). Frontend nginx proxies `/api/`, `/admin/`, `/media/` to the `backend` container. No explicit `networks:` block is declared, so all five services share the compose-default network and reach each other by service name (e.g. `fastapi-ai` talks to `chroma-db:8000`).

The backend's `entrypoint.sh` always runs `migrate --noinput` on container start, then, when `PRODUCTION != true`, also runs all five `seed_*` management commands automatically before starting the dev server — so `docker compose up` alone gives a fully-seeded local backend. When `PRODUCTION=true` it skips seeding and starts Gunicorn instead of `runserver`.

### fastapi-ai (`fastapi-ai/`)

`GET /health`, `GET /chroma/health` (round-trips a heartbeat through `chromadb.HttpClient` to `chroma-db`), and `POST /api/v1/chat` (streams the LangGraph agent's response token-by-token via `StreamingResponse` + `graph.astream(..., stream_mode="messages")`, filtered to the `synthesize_response` node). Reads `CHROMA_HOST`/`CHROMA_PORT`/`OLLAMA_BASE_URL`/`CORS_ALLOWED_ORIGINS` from the environment (set in `docker-compose.yml`).

```bash
pip install -r requirements-dev.txt
ruff check .
pytest -v
```

`agent.py` eagerly instantiates `HuggingFaceEmbeddings` (real model load) and `chromadb.HttpClient`
(live handshake) at module import time — `conftest.py` patches `HuggingFaceEmbeddings`, `ChatOllama`,
and `chromadb.HttpClient` at the module level *before* `agent`/`main` are ever imported, so `pytest`
never touches the network or downloads a model. Individual tests then monkeypatch `agent._llm` /
`agent._chroma_client` / `agent._embeddings` (or `main.graph`) per-test to control behavior.

**Local Ollama** (this dev machine only — not containerized, no root/systemd available): installed
user-locally to `~/ollama-local` (official install script needs passwordless sudo, which isn't set up
here; used the manual tarball method instead). Start it with:
```bash
OLLAMA_HOST=0.0.0.0:11434 ~/ollama-local/bin/ollama serve &
```
`OLLAMA_HOST` must bind `0.0.0.0`, not the default `127.0.0.1` — otherwise containers can't reach it
via `host.docker.internal` (confirmed: default binding accepts only same-machine loopback connections,
invisible from the Docker bridge network). GPU (RTX 5070 Ti, CUDA) is auto-detected and used. Model in
use: `qwen2.5-coder:7b` (`~/ollama-local/bin/ollama pull qwen2.5-coder:7b`).

## Architecture

```
ujmikamiapp/
  frontend/src/
    App.tsx           ← root component: fetches from all API endpoints, holds page-level data/state
    App.css            ← design tokens (CSS custom properties), hero, layout
    components/        ← one component per file, co-located .css (Card, Section, Navbar, Footer,
                          WorkExperience, MLShowcase, Item)
  backend/ujmikamiapp/
    ujmikamiapp/        ← Django settings, root URL conf, storage_backends.py (Azure Blob storage classes)
    api/                ← root API urls.py wiring; thin/generic endpoints
    projects/           ← Project, Tag, ProjectLink, WorkExperience, WorkExperienceTechnology,
                          Publication, AboutItem models + DRF serializers/views + seed commands
    ml_models/          ← MLModel, MLModelLink models (metrics/leaderboard as JSONField) + DRF API + seed command
  fastapi-ai/           ← FastAPI AI microservice (health + Chroma connectivity checks so far)
  terraform/            ← Azure infra-as-code (currently empty scaffolding — main.tf/variables.tf not yet written)
  docker-compose.yml    ← frontend + backend + MySQL db + chroma-db + fastapi-ai services
```

### Backend

- Django 6 + DRF. Root URL conf (`ujmikamiapp/urls.py`) only mounts `admin/` and includes `api.urls`; `api/urls.py` fans out to each app's `urls.py` plus a few directly-registered views (`publications/`, `experiences/`, `about/`).
- API paths: `/api/<resource>/`, trailing slash, plural noun. All endpoints are unauthenticated, read-only; content is managed exclusively through Django admin.
- Models are thin (no business logic in `save()`); every model has a `__str__`. Manual ordering uses `PositiveIntegerField(default=0)` + `Meta.ordering` (see `Project.order`), not view-level sorting.
- One `ModelSerializer` per model — never shared across apps.
- Storage is environment-driven: `PRODUCTION=true` (`USE_AZURE_STORAGE` in `settings.py`) switches static/media storage from local `FileSystemStorage` to Azure Blob (`ujmikamiapp/storage_backends.py`), requiring `AZURE_ACCOUNT_NAME`/`AZURE_ACCOUNT_KEY`.
- Database is MySQL via `django-environ`'s `env.db()` (`DATABASE_URL`), with a forced SSL CA path — this only works inside the container/deployed environment; local dev typically points at the `db` Docker service or a local MySQL instance.
- Env vars (see `.env.example`): `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`, plus `PRODUCTION`, `AZURE_ACCOUNT_NAME`, `AZURE_ACCOUNT_KEY` for prod storage.
- Running `manage.py test` against the docker-compose `db` service (or a fresh MySQL service container in CI) fails with `Access denied ... to database 'test_ujmikamiapp'` the first time — the app's DB user only has grants on `ujmikamiapp`, not on the `test_*` database Django creates for the test run. Fix once per database instance: `GRANT ALL PRIVILEGES ON` `` `test_%` `` `.* TO 'ujmikamiapp'@'%'; FLUSH PRIVILEGES;` as root (the CI workflow does this automatically before running tests).

### Frontend

- TypeScript strict mode. State via `useState`/`useEffect` only — no Redux/Zustand/Context.
- Data fetching is bare `fetch` inside `useEffect` with an `isMounted` guard, not a data-fetching library.
- Components stay small (~100 lines), one file per component, default export named after the file, co-located CSS using BEM-like class names (`.component-name`, `.component-name__part`).
- All colors/spacing reference the CSS custom properties defined in `App.css` (`--accent`, `--hero-bg`, `--text-strong`, `--font-display`, `--font-body`, etc.) — never hard-code colors.
- Page sections are numbered/ordered in the navbar: About → Experience → Research → Projects → ML Showcase, with Projects/ML Showcase fed by the Django API.

## Deployment notes

- Production runs on Azure Container Apps (`ujmikamiapp-env` / resource group `ujmikamiapp2`) with static/media served from Azure Blob Storage (`ujmikamiblob` account, `static`/`media` containers, public blob access).
- One-off management commands in prod are run via `az containerapp exec` (see `azure.txt` for the exact invocations: `collectstatic`, `seed_ml_models`, `seed_projects`).
- `terraform/` is intended to codify this Azure infrastructure but the `.tf` files are currently empty — treat any Azure infra changes as needing to be written from scratch there, not assumed to exist.
