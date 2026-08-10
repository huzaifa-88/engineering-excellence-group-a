# TaskFlow API - Session 02

This session packages the FastAPI backend and PostgreSQL database into a repeatable Docker-based development environment. The goal is to make local development consistent, reduce setup friction, and give the team a standard way to run the API, database, and migrations together.

## What this Docker setup does

The Docker workflow helps you run the application in a containerized environment with:

- a FastAPI service for the backend
- a PostgreSQL service for the database
- automatic database migrations on startup
- bind-mounted source code so changes are reflected while you develop
- a predictable local environment that matches the team’s setup

In short, Docker removes the need to install and configure PostgreSQL and Python dependencies manually on every machine.

## Prerequisites

- Docker Engine and Docker Compose
Python 3.12+ for local tooling with `uv`

## Quick start with Docker Compose

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Start the stack:

```bash

docker compose up --build
```

3. Open the API:

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

The `api` service waits for PostgreSQL to become healthy, then runs Alembic migrations before starting Uvicorn.

## Environment variables

The app reads PostgreSQL settings from environment variables. The defaults in `.env.example` are designed for local development. When running Docker Compose, the container uses the Compose service name `db` as the database host:


```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_HOST_DOCKER=db
POSTGRES_PORT=5432
POSTGRES_DB=taskflow
APP_ENV=development
```

If you want to use Docker Compose, the container will use `POSTGRES_HOST_DOCKER=db` automatically; you can override it if needed.

## Local development without Docker

If you prefer a non-container workflow, install dependencies and run the app directly:

```bash
uv sync
cp .env.example .env
uv run alembic upgrade head
uv run alembic upgrade head

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Common Commands

The following Make commands simplify common development tasks:

```bash
make install         # Install Python dependencies with uv
make lint            # Run Ruff checks
make lint-fix        # Auto-fix Ruff issues
make format          # Format code with Ruff
make typecheck       # Run mypy
make test            # Run pytest
make run             # Start the API locally
make migrate         # Run Alembic migrations locally
make docker-up       # Build and start Docker services
make docker-down     # Stop and remove Docker services
make docker-logs     # Follow API and database logs
make docker-migrate  # Run Alembic migrations inside the API container
make docker-test     # Run pytest inside the API container
```

## Useful Docker commands

```bash
# Rebuild the images
docker compose build

# Stop the stack
docker compose down

# View logs
docker compose logs -f api db

# Run migrations manually
docker compose exec api uv run alembic upgrade head
```

## Project Structure

```text
.
├── app/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── .env.example
└── README.md
```

## Code quality workflow

The repository already includes tooling for:

- Ruff for linting and formatting
- mypy for type checking
- pytest for tests
- pre-commit hooks for repeatable checks

Run them with:

```bash
make lint
make format
make typecheck
make test
```

## Troubleshooting

### Database connection errors

If the API cannot reach PostgreSQL, confirm that:

- the `db` service is healthy
- the credentials in `.env` match the Compose environment
- the app is using the correct host (`db` inside Docker, `localhost` outside Docker)

### Port conflicts

If port 8000 or 5432 is already in use, change the published ports in `docker-compose.yml`.

## Pull request note

The Docker setup is intended to make review and onboarding easier by giving the team a single, documented way to run the backend and database locally. It does not change the API contract; it only standardizes the runtime environment.