# AI Interview Training Platform

## Overview

AI Interview Training Platform is an AI-powered interview coaching system designed to help software engineering, AI, machine learning, and backend candidates prepare for modern hiring processes.

The platform focuses on helping users succeed in:

- AI screening interviews
- Technical interviews
- Behavioral interviews
- Company-specific interview processes

Unlike traditional mock interview tools, the system aims to function as a personalized interview coach that identifies weaknesses, tracks progress, and adapts future interview sessions based on performance.

---

## Current Status

🚧 Active Development

### Day 1 Completed

- FastAPI backend initialized
- React + TypeScript frontend initialized
- PostgreSQL containerized setup
- Docker Compose local development environment
- API health endpoint
- Frontend routing foundation

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- React Router
- Axios

### Backend

- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

### Database

- PostgreSQL

### Infrastructure

- Docker
- Docker Compose

### AI

- Groq API (planned)
- Multi-agent interview architecture (planned)

---

## Architecture

```text
Frontend (React)

        ↓

Backend API (FastAPI)

        ↓

PostgreSQL

        ↓

AI Agent Layer
```

### Planned Agent Architecture

- Research Agent
- Interview Planner Agent
- Interviewer Agent
- Evaluator Agent
- Coach Agent
- Report Agent

---

## Planned Features

### Authentication

- User registration
- Login
- JWT authentication
- Account management

### Interview Engine

- Adaptive text interviews
- Voice interviews
- Video interview simulation
- Follow-up questioning
- Personalized difficulty adjustment

### Context Awareness

- Resume analysis
- Job description analysis
- Company-specific preparation
- Target role preparation

### Evaluation & Coaching

- Technical evaluation
- Behavioral evaluation
- STAR evaluation
- Communication feedback
- Progress tracking

### Reporting

- Session reports
- Interview history
- Performance analytics
- PDF export

### Monetization

- Credit system
- Lemon Squeezy integration
- Stripe migration

---

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 22+
- Docker Desktop

### Run with Docker

```bash
docker compose up --build
```

### Backend

Health Check:

```text
http://localhost:8000/health
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

### Frontend

```text
http://localhost:5173
```

---

## Project Roadmap

### Week 1

- Project setup
- Database design
- Authentication
- Resume management
- Training targets
- Interview session foundation

### Week 2

- Interview evaluation engine
- Coaching engine
- Session history
- Progress tracking
- Reporting

### Week 3

- Deployment
- Testing
- Monetization
- Launch preparation

---

## Development Philosophy

Prioritize:

- User value
- Reliability
- Personalization
- Adaptivity
- Resume value
- Real-world engineering practices

Avoid:

- Premature optimization
- Overengineering
- Unnecessary complexity
- Academic-only solutions

---
