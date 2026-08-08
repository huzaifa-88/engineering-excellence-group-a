#!/usr/bin/env sh
set -e

# Run database migrations on container startup
uv run alembic upgrade head

# Replace process with main command (e.g. uvicorn) as PID 1 for graceful shutdown
exec "$@"
