# Session 3 — DB Transactions & Migrations

## Correctness SLO

Task assignment should not create partial writes. If assignment fails, task assignment, assignment history, status history, activity log, and notification record should roll back together.

### Scope & Execution Plan

- **Part A (Schema & Models)**: Define supporting SQLAlchemy models (`TaskAssignmentHistory`, `TaskStatusHistory`, `ActivityLog`, `Notification`), `Project.slug` unique constraint, and relationship mappings.
- **Part B (Transaction Service & Rollback)**: Implement 5-step atomic task assignment service (`/tasks/{id}/assign`), partial failure rollback handling, unit tests, and demo documentation.

