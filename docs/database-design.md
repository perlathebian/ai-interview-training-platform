# Database Design

## Overview

The application uses PostgreSQL as the primary database.

FastAPI remains stateless. All important application state is stored in PostgreSQL, including users, resumes, training targets, interview sessions, interview turns, and credit transactions.

The database is managed through SQLAlchemy models and Alembic migrations.

---

## Current Tables

### users

Stores account-level user information.

Fields include:

- id
- email
- password_hash
- specialty
- level
- is_verified
- is_active
- created_at
- updated_at

The users table should not store interview-specific data.

---

### resumes

Stores user resume data.

Fields include:

- id
- user_id
- raw_text
- parsed_summary
- extracted_skills
- extracted_projects
- extracted_experience
- extracted_education
- is_active
- is_deleted
- created_at
- updated_at

Resume records support soft deletion through `is_deleted`.

---

### training_targets

Stores the role, job, or company context the user wants to train for.

Fields include:

- id
- user_id
- target_type
- company
- role
- job_description
- desired_companies
- focus_areas
- created_at
- updated_at

Examples of target types:

- specific_job
- general_practice
- company_practice

---

### interview_sessions

Stores each interview session.

Fields include:

- id
- user_id
- training_target_id
- mode
- status
- resume_snapshot
- job_snapshot
- research_snapshot
- interview_plan_snapshot
- overall_score
- final_report
- started_at
- completed_at
- created_at
- updated_at

Sessions store snapshots so that historical interviews remain stable even if the user updates their resume or training target later.

---

### interview_turns

Stores one interview exchange per row.

A turn contains:

- question
- answer
- evaluation
- coaching
- score
- status
- turn_metadata

This keeps the interview flow simple:

```text
question → answer → evaluation → coaching → next question
```

---

### credit_transactions

Stores credit-related events.

Fields include:

- id
- user_id
- amount
- transaction_type
- status
- provider
- provider_reference
- created_at
- updated_at

Credit transactions provide an audit trail for future monetization.

Examples:

- purchased
- reserved
- consumed
- refunded

---

## Ownership Rule

Every protected user-owned resource must belong to a user.

The backend must never trust `user_id` from the frontend.

Instead:

```text
JWT → current_user → current_user.id
```

Then every protected query should enforce:

```python
resource.user_id == current_user.id
```

This prevents users from accessing each other's data.

---

## Relationships

```text
User
 ├── Resumes
 ├── Training Targets
 ├── Interview Sessions
 └── Credit Transactions

Training Target
 └── Interview Sessions

Interview Session
 └── Interview Turns
```

---

## Migration Strategy

Database schema changes are managed with Alembic.

Create a migration:

```bash
alembic revision --autogenerate -m "migration message"
```

Apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

View migration history:

```bash
alembic history
```

---

## Local Database

During local development, PostgreSQL runs in Docker.

The database is persisted in a Docker volume:

```text
postgres_data
```

Tables remain after:

```bash
docker compose down
```

Tables are deleted if the volume is removed:

```bash
docker compose down -v
```

---

## Current Verification Checklist

- Alembic initializes successfully
- Initial migration exists
- `alembic upgrade head` succeeds
- Tables exist in PostgreSQL
- Backend imports models successfully
- Backend starts cleanly
- `/health` returns `{ "status": "ok" }`

---

## Current Tables Created

- users
- resumes
- training_targets
- interview_sessions
- interview_turns
- credit_transactions
- alembic_version
