# Hyper Dev Vibe Coder (HDVC) Technical Standards

This document defines the **law** for the HyperFocus-IDE-BROski-v1 project. All code must adhere to these conventions.

**All technical decisions are evaluated against one rule: does this make life easier for neurodivergent developers?**

## 1. Stack Enforcement

### Frontend
- **Framework**: React 18+ with Vite
- **Language**: TypeScript (Strict mode)
- **Styling**: Tailwind CSS
- **State/Logic**: 
  - React Hook Form + Zod for validation
  - Small, focused components in `components/`
  - Screen-level logic in `pages/` or `routes/`
  - Reusable logic in `hooks/`
- **Icons**: Lucide icons
- **Requirement**: Always include a usage example for new components.

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Concurrency**: Async-first (`async def`)
- **Validation**: Pydantic v2
- **Database**: PostgreSQL via Supabase (or local Docker container)
- **Auth**: JWT auth with expiry, bcrypt/Argon2 hashing
- **File Layout**:
  - `backend/app/main.py`
  - `backend/app/api/routes/*.py`
  - `backend/app/models/*.py`
  - `backend/app/core/config.py`
  - `backend/app/tests/*.py`

### Database
- **Primary Keys**: `uuid` or `bigserial`
- **Timestamps**: `created_at` / `updated_at` on all tables
- **Integrity**: Foreign Key constraints required
- **Security**: Row Level Security (RLS) on user tables
- **Performance**: Indices on frequently queried columns

### Docker
- **Images**: Multi-stage Dockerfiles (non-root, slim images like `python:3.11-slim` or `node:18-alpine`)
- **Orchestration**: `docker-compose.yml`
- **Services**: `postgres`, `backend`, `frontend`, `ollama` (optional)
- **Reliability**: Health checks required for all services

## 2. Security & Auth
- **JWT**: Short-lived access tokens, secure refresh tokens.
- **Cookies**: HTTP-only cookies for frontend auth storage.
- **Validation**: Strict Pydantic models for all incoming data.
- **Ownership**: Explicit checks that a resource belongs to the requesting user.

## 3. Testing
- **Python**: `pytest` with `pytest-asyncio` and fixtures.
- **JavaScript/TypeScript**: `Vitest` or `Jest` + React Testing Library.
- **Coverage**: At least 1-3 small tests per core feature.
- **Execution**: Must provide runnable test commands (e.g., `pytest`, `npm test`).

## 4. AI & LLM Integration
- **Client**: Thin, typed clients for Ollama (localhost:11434) or remote APIs (Perplexity, OpenAI).
- **Resilience**: Streaming support, timeouts, and retry logic.
- **Architecture**: Keep AI helpers composable and decoupled from business logic.

## 5. CI/CD & Version Control
- **Commits**: Conventional Commits (`feat:`, `fix:`, `chore:`).
- **Workflow**: GitHub Actions for testing and building.
- **Deployment**: Ready for Fly.io, Render, or VPS deployment via Docker.

## 6. Code Style
- **Python**: Black + Ruff
- **TypeScript**: Prettier + ESLint
- **Naming**: Descriptive and explicit (`userProfile` vs `up`, `createSessionToken` vs `cst`).
- **No Abbreviations**: Avoid cryptic variable names.
