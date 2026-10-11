# FastAPI Template

A production-shaped starting point for APIs: **FastAPI + SQLModel + PostgreSQL**,
organized by domain, and run entirely in Docker.

- **Stack** — FastAPI · SQLModel · SQLAlchemy 2 · PostgreSQL 18 · Alembic
- **Tooling** — uv · ruff · mypy · ty · prek
- **Requirements** — Docker. Nothing else on the host.

## Quick Start

**1. Create `.env`** in the project root — it is not tracked in git. The minimum is:

```bash
# [app]
PROJECT_NAME="FastAPI Template"

# [auth]
SECRET_KEY=...            # python -c "import secrets; print(secrets.token_urlsafe(32))"
API_USERNAME=admin
API_PASSWORD=change-me

# [database]
POSTGRES_SERVER=db        # the compose service name
POSTGRES_PORT=5432
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PSW=change-me
```

**2. Build, migrate, start:**

```bash
docker compose build
docker compose run --rm api alembic upgrade head
docker compose up -d
```

**3. Open:**

- API — <http://localhost:8000>
- Swagger UI — <http://localhost:8000/docs>
- ReDoc — <http://localhost:8000/redoc>
- Health checks — <http://localhost:8000/api/v1/health/live> (liveness), <http://localhost:8000/api/v1/health/ready> (readiness)

`API_USERNAME` and `API_PASSWORD` are the only credentials the API accepts. Post them to
`POST /api/v1/login/access-token` for a JWT, then send it as a bearer token on every
protected route — or click **Authorize** in Swagger UI.

## Commands

Every project command runs in the container, so the host needs no Python, uv or psql:

| Task | Command |
| --- | --- |
| Start / stop | `docker compose up -d` / `docker compose down` |
| Follow logs | `docker compose logs -f api` |
| Apply migrations | `docker compose run --rm api alembic upgrade head` |
| New migration | `docker compose run --rm api alembic revision --autogenerate -m "..."` |
| Check for drift | `docker compose run --rm api alembic check` |
| Lint | `docker compose run --rm api bash scripts/lint.sh` |
| Format | `docker compose run --rm api bash scripts/format.sh` |
| Shell | `docker compose run --rm api bash` |
| psql | `docker compose exec db psql -U postgres -d app` |
| Export OpenAPI | `docker compose run --rm -T api bash scripts/generate-openapi.sh > openapi.json` |

## Project Structure

Code is organized **by domain**, not by file type: everything one bounded context needs
sits in one package.

```text
app/
├── auth/                  # Domain: login and token validation
├── objects/               # Domain: the reference CRUD slice — copy this one
│   ├── router.py          # Endpoints (/dummy-objects)
│   ├── schemas.py         # Create / Update / Public (plain Pydantic)
│   ├── models.py          # SQLModel table
│   ├── service.py         # CRUD
│   ├── dependencies.py    # valid_object_id, the single 404 site
│   ├── constants.py       # Error codes
│   └── exceptions.py      # ObjectNotFound
├── alembic/               # Database migrations
├── config.py              # Global settings (auth/config.py holds the auth ones)
├── database.py            # Engine and the get_db session dependency
├── models.py              # Metadata naming convention, table model helpers
├── schemas.py             # Shared API schemas (Message, ErrorResponse)
├── exceptions.py          # Shared HTTPException base classes
├── health.py              # Liveness and readiness probes
└── main.py                # FastAPI app, lifespan, router registration
scripts/                   # lint, format, generate-openapi
```

## Next Steps

- [development.md](./development.md) — daily workflow, migrations, linting, agent skills, API clients.
