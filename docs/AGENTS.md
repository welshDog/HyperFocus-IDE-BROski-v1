# HyperCode Agents - The Specialized Swarm

The HyperCode ecosystem is powered by a swarm of specialized AI agents, each designed for a specific phase of the software development lifecycle. These agents operate within the `hypercode-network` Docker network and communicate via the central Orchestrator.

**Each agent is designed to support neurodivergent workflows (chunked tasks, reduced context switching, visual control via the Mission Control dashboard).**

## 🦅 Tier 1: Strategic Agents (The "Brain")

These agents use **Perplexity Sonar Reasoning Pro** models for high-level planning and architectural decision-making.

### 1. Project Strategist
- **Role**: Mission Commander & Planner
- **Model**: `openai/sonar-reasoning-pro`
- **Responsibilities**:
  - Breaks down high-level user intents into actionable subtasks.
  - Delegates work to Tier 2 specialists.
  - Manages dependencies and execution order.
  - **Output**: Structured JSON mission plans.

### 2. System Architect
- **Role**: Technical Visionary
- **Model**: `openai/sonar-reasoning-pro`
- **Responsibilities**:
  - Defines system patterns (Microservices, Event-Driven, etc.).
  - Selects appropriate technologies and databases.
  - Ensures scalability, maintainability, and SOLID principles.
  - Reviews major architectural decisions.

---

## 🛠️ Tier 2: Specialist Agents (The "Hands")

These agents use **Perplexity Sonar** models for efficient, context-aware execution of specific tasks.

### 3. Frontend Specialist
- **Role**: UI/UX Implementer
- **Stack**: React 18, Next.js 14+, Tailwind CSS, Shadcn/ui.
- **Responsibilities**:
  - Builds responsive, accessible components.
  - Implements client-side state management (Zustand).
  - Ensures pixel-perfect design implementation.

### 4. Backend Specialist
- **Role**: API & Logic Developer
- **Stack**: FastAPI, Python 3.11+, Celery, Redis.
- **Responsibilities**:
  - Implements RESTful API endpoints.
  - Writes business logic and data processing services.
  - Handles authentication and authorization flows.

### 5. Database Architect
- **Role**: Data Modeler
- **Stack**: PostgreSQL, SQLAlchemy, Alembic.
- **Responsibilities**:
  - Designs normalized database schemas (3NF).
  - Optimizes SQL queries and indices.
  - Manages database migrations and data integrity.

### 6. QA Engineer
- **Role**: Quality Guardian
- **Stack**: Pytest, Playwright.
- **Responsibilities**:
  - Writes unit, integration, and E2E tests.
  - Validates acceptance criteria.
  - Ensures test coverage targets (>80%) are met.

### 7. DevOps Engineer (Phoenix)
- **Role**: System Guardian
- **Stack**: Docker, Kubernetes, CI/CD.
- **Responsibilities**:
  - **Self-Healing**: Detects and restarts failed services.
  - Manages container orchestration and deployment.
  - Monitors system health (Prometheus/Grafana).

### 8. Security Engineer
- **Role**: Security Auditor
- **Responsibilities**:
  - Conducts vulnerability scans (OWASP Top 10).
  - Reviews code for security flaws (Injection, XSS).
  - Ensures secure authentication and data encryption.

---

## 📡 Agent Communication

Agents do not communicate directly with the user. All interaction is mediated by the **Orchestrator**.

1. **Orchestrator** receives a task via HTTP POST.
2. It routes the request to the appropriate agent's Docker service (e.g., `http://frontend-specialist:8000`).
3. The agent processes the request using its `system_prompt` and context.
4. The agent returns a JSON response to the Orchestrator.

## 🧬 Configuration

Agent definitions are located in `agents/cagent-poc/*.yaml`. You can modify their system prompts or toolsets there.
