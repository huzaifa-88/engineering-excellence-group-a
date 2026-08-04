clea.PHONY: install hooks lint lint-fix format typecheck test pre-commit run migrate

install:
	uv sync

hooks:
	uv run pre-commit install

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

format:
	uv run ruff format .

typecheck:
	uv run mypy app

test:
	uv run pytest -v

pre-commit:
	uv run pre-commit run --all-files

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	uv run alembic upgrade head