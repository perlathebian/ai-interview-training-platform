# Architecture

## System Overview

The application follows a clean full-stack architecture:

Frontend → Backend API → PostgreSQL → AI Services

## Frontend

The frontend is built with React, TypeScript, Vite, and Tailwind CSS.

It handles:

- authentication UI
- dashboard
- interview flow
- reports
- progress views

## Backend

The backend is built with FastAPI.

It handles:

- authentication
- authorization
- interview sessions
- AI agent orchestration
- database access
- credit logic
- reports

## Database

PostgreSQL stores all important application state.

FastAPI remains stateless.

## AI Services

The AI layer uses specialized agents:

- Research Agent
- Planner Agent
- Interviewer Agent
- Evaluator Agent
- Coach Agent
- Report Agent

Each agent should return structured JSON validated by Pydantic.

# Development Stage

Current Phase:

Week 1 - Foundation

Implemented:

- FastAPI backend
- React frontend
- PostgreSQL container
- Docker Compose environment

Next:

- Authentication
- Database models
- Interview engine
