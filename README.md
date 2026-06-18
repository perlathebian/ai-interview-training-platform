# AI Interview Training Platform

## Overview

AI Interview Training Platform is a production-oriented interview preparation application that helps candidates practice interviews, receive structured AI feedback, improve their answers, and track progress over time.

The platform uses resume context, job target context, adaptive questioning, evaluation, coaching, reporting, and progress tracking to create a personalized interview preparation experience.

This project is being built as a full-stack software engineering and AI systems project with an emphasis on clean architecture, testing, database design, CI/CD, and production readiness.

---

## Current Status

Week 1 MVP Foundation Completed

### Implemented Features

- User registration and login
- JWT authentication
- Protected routes
- Resume management
- Training target management
- Interview session creation
- Adaptive interview flow
- Answer submission
- AI evaluation layer
- AI coaching layer
- Interview reports
- Session history
- User progress tracking
- PostgreSQL persistence
- Docker support
- GitHub Actions CI

---

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT Authentication
- Pydantic
- Pytest

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios

### Infrastructure

- Docker
- GitHub Actions

### AI Layer

- Groq (planned production integration)
- Multi-agent architecture

---

## Architecture

### Frontend

React application responsible for:

- Authentication
- Resume management
- Training targets
- Interview experience
- Reports
- Progress visualization

### Backend

FastAPI service responsible for:

- Authentication
- Business logic
- Interview orchestration
- Agent execution
- Reporting
- Progress tracking

### Database

PostgreSQL stores:

- Users
- Resumes
- Training targets
- Interview sessions
- Interview turns
- Progress data

### Agent Layer

The interview system is organized around specialized agents:

- Research Agent
- Planner Agent
- Interviewer Agent
- Evaluator Agent
- Coach Agent
- Report Agent

---

## Project Structure

```text
backend/
frontend/
docs/

backend/app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
│   └── agents/
├── tests/

frontend/src/
├── api/
├── pages/
├── components/
├── routes/
```

---

## Local Development Setup

### Backend

```bash
cd backend

python -m venv .venv

source .venv/Scripts/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

Backend available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

### Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend available at:

```text
http://localhost:5173
```

---

### Docker

```bash
docker compose up --build
```

---

## Testing

### Backend

```bash
pytest
```

### Frontend

```bash
npm run build

npm run test
```

---

## Continuous Integration

GitHub Actions automatically runs:

### Backend CI

- Dependency installation
- PostgreSQL service
- Database migrations
- Pytest

### Frontend CI

- Dependency installation
- Production build
- Test execution

---

## Roadmap

### Week 2

- Real Groq integration
- Resume-aware interviews
- Job-description-aware interviews
- Improved planner agent
- Improved evaluator agent
- Improved coach agent
- Improved interviewer agent
- Improved personalization

### Week 3

- Voice interviews
- Video interviews
- Payments
- Deployment
- Production monitoring
- Launch preparation

---

## Goals

This project is designed to demonstrate:

- Backend engineering
- Frontend engineering
- Database design
- API development
- AI system integration
- Software architecture
- CI/CD practices
- Production-oriented development

while delivering a real product that users can use to improve interview performance.
