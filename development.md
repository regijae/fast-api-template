# Development

Setup and first run live in the [README](./README.md#quick-start).

## Requirements

[Docker](https://www.docker.com/).

## Daily Workflow

```bash
docker compose up -d                    # start
docker compose logs -f api              # follow logs
docker compose down                     # stop (--volumes also drops the database)
```

`docker compose run --rm api <command>` runs a one-off command in a throwaway
container.

```bash
docker compose run --rm api bash scripts/lint.sh
docker compose run --rm api bash          # interactive shell
docker compose exec db psql -U postgres -d app
```

## Authentication

`API_USERNAME` and `API_PASSWORD` are the only
dummy credentials the API accepts:

```bash
curl -X POST http://localhost:8000/api/v1/login/access-token \
  -d "username=$API_USERNAME&password=$API_PASSWORD"
```

## Migrations

Create a revision every time you change a model, then apply it:

```bash
docker compose run --rm api alembic revision --autogenerate -m "Add expires_at to DummyObject"
docker compose run --rm api alembic upgrade head
docker compose run --rm api alembic check    # confirms models and migrations agree
```

## Linting and Pre-commit Hooks

```bash
docker compose run --rm api bash scripts/lint.sh     # mypy, ty, ruff check, ruff format --check
docker compose run --rm api bash scripts/format.sh   # ruff check --fix, ruff format
```

```bash
uv sync                    # one-time host setup
uv run prek install -f     # install the git hook (-f replaces an existing one)
uv run prek run --all-files
```

## Agent Skills

FastAPI and SQLModel ship best-practice guidance for coding agents inside the
installed packages; `.agents/skills/` and `.claude/skills/` symlink to it. Rerun after any
dependency change:

```bash
uv sync
uvx library-skills --all --claude --copy --yes
```

## API Clients

Export the OpenAPI schema to generate a client in any language:

```bash
docker compose run --rm -T api bash scripts/generate-openapi.sh > openapi.json
```
