# TaskFlow API - Session 02

Dockerized development environment with code review standards for the TaskFlow internal team work management backend.

## Overview

This session focuses on setting up a professional development workflow with:
- Docker containerization for consistent environments
- Pre-commit hooks for code quality enforcement
- Type checking with mypy
- Linting and formatting with ruff
- Automated testing with pytest

## Prerequisites

- Python 3.12 or higher
- Docker and Docker Compose
- PostgreSQL database (or use Docker)
- `uv` package manager

## Quick Start

### 1. Clone and Setup

```bash
cd session-02-dockerized-development-and-code-review-standards
```

### 2. Install Dependencies

Using uv:
```bash
uv sync
```

### 3. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Update `.env` with your PostgreSQL credentials:
```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=taskflow
APP_ENV=development
```

### 4. Run Database Migrations

```bash
uv run alembic upgrade head
```

### 5. Start the Development Server

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Access API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Common Commands

The following Make commands simplify common development tasks:

```bash
make install       # Install dependencies
make hooks         # Install pre-commit hooks
make lint          # Check lint issues
make lint-fix      # Fix lint issues automatically
make format        # Format code using Ruff
make typecheck     # Run MyPy type checking
make test          # Run pytest
make pre-commit    # Run all pre-commit hooks manually
make run           # Start FastAPI server
make migrate       # Run database migrations
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_users.py
```

## Code Quality Tools

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit to ensure code quality:

```bash
# Install pre-commit hooks (run once)
uv run pre-commit install

# Run hooks manually on all files
uv run pre-commit run --all-files
```

### Linting and Formatting

```bash
# Check code with ruff
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Format code
uv run ruff format .
```

### Type Checking

```bash
# Run mypy type checker
uv run mypy app
```

## Docker Setup

### Build and Run with Docker Compose

```bash
# Start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

### Database Migrations in Docker

```bash
# Run migrations
docker-compose exec api uv run alembic upgrade head

# Create new migration
docker-compose exec api uv run alembic revision --autogenerate -m "description"
```

## Project Structure

```
session-02-dockerized-development-and-code-review-standards/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   ├── dependencies/
│   │   │   └── deps.py           # Shared dependencies (DB session, pagination)
│   │   └── v1/
│   │       └── routes/
│   │           ├── users.py      # User endpoints
│   │           ├── tasks.py      # Task endpoints
│   │           └── projects.py   # Project endpoints
│   ├── core/
│   │   ├── config.py             # Application configuration
│   │   └── exceptions.py         # Custom exception classes
│   ├── db/
│   │   ├── base.py               # SQLAlchemy declarative base
│   │   └── database.py           # Database connection setup
│   ├── models/
│   │   ├── user.py               # User ORM model
│   │   ├── project.py            # Project ORM model
│   │   ├── task.py               # Task ORM model
│   │   └── project_member.py     # ProjectMember ORM model
│   ├── repositories/             # Data access layer
│   │   ├── user_repository.py
│   │   ├── project_repository.py
│   │   └── task_repository.py
│   ├── schemas/                  # Pydantic models (DTOs)
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   └── services/                 # Business logic layer
│       ├── user_service.py
│       ├── project_service.py
│       └── task_service.py
├── alembic/
│   ├── versions/                 # Database migration scripts
│   ├── env.py
│   └── script.py.mako
├── tests/
│   ├── test_users.py
│   ├── test_tasks.py
│   ├── test_projects.py
│   └── test_enum_values.py
├── .pre-commit-config.yaml       # Pre-commit hooks configuration
├── pyproject.toml                # Project metadata and dependencies
├── alembic.ini                   # Alembic configuration
├── .env.example                  # Environment variables template
└── Makefile                     # Common development commands
```

## API Endpoints

### Users
- `POST /users` - Create a new user
- `GET /users` - List users (paginated)
- `GET /users/{user_id}` - Get user by ID

### Projects
- `POST /projects` - Create a new project
- `GET /projects` - List projects (paginated, filterable)
- `GET /projects/{project_id}` - Get project by ID

### Tasks
- `POST /tasks` - Create a new task
- `GET /tasks` - List tasks (paginated, filterable)
- `GET /tasks/{task_id}` - Get task by ID
- `PATCH /tasks/{task_id}/status` - Update task status

### Health
- `GET /health` - Health check endpoint

## Code Review Standards

This project enforces the following code quality standards:

1. **Type Safety**: All code must pass mypy type checking
2. **Linting**: ruff enforces PEP 8 and best practices
3. **Formatting**: ruff ensures consistent code formatting
4. **Tests**: All new features must include tests
5. **Pre-commit Hooks**: Automated checks run before every commit

## Technology Stack

- **Framework**: FastAPI 0.140+
- **Database**: PostgreSQL with asyncpg
- **ORM**: SQLAlchemy 2.0 (async)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio + httpx
- **Type Checking**: mypy
- **Linting/Formatting**: ruff
- **Package Manager**: uv

## Development Workflow

1. Create a new branch for your feature
2. Make changes and write tests
3. Run tests:

```bash
make test
```

4. Run code quality checks:

```bash
make lint
make format
make typecheck
```
5. Commit (pre-commit hooks will run automatically)
6. Push and create a pull request

## Troubleshooting

### Database Connection Issues

Ensure PostgreSQL is running and credentials in `.env` are correct:
```bash
# Test connection
psql -h localhost -U your_user -d taskflow
```

### Migration Errors

If migrations fail, you may need to reset the database:
```bash
# WARNING: This will delete all data
uv run alembic downgrade base
uv run alembic upgrade head
```

### Port Already in Use

Change the port in the uvicorn command:
```bash
uv run uvicorn app.main:app --reload --port 8001
```

## License

This project is part of the Engineering Excellence curriculum.

## Contributing

Follow the code review standards and ensure all tests pass before submitting changes.