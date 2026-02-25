# HyperCode Agent Crew - Architecture

## System Overview

```mermaid
graph TD
    User[Client Applications] -->|HTTP/WS| API[Crew Orchestrator]
    API -->|Delegation| Strat[Project Strategist]
    API -->|Coordination| Arch[System Architect]
    
    subgraph "Data Layer"
        Redis[(Redis Cache & Queue)]
        DB[(PostgreSQL History)]
    end
    
    subgraph "Specialist Swarm (Tier 2)"
        FE[Frontend Specialist]
        BE[Backend Specialist]
        QA[QA Engineer]
        DevOps[DevOps Engineer]
        Sec[Security Engineer]
    end
    
    subgraph "Observability"
        Prom[Prometheus]
        Graf[Grafana]
        Jaeger[Jaeger Tracing]
    end

    subgraph "Background Processing"
        Celery[Celery Worker]
    end

    Strat -->|Task| Redis
    Arch -->|Standards| Redis
    Redis -->|Pub/Sub| Specialist Swarm
    Specialist Swarm -->|Results| Redis
    Redis -->|Aggregation| API
    
    API -->|Metrics| Prom
    Prom --> Graf
    
    Celery -->|Tasks| Redis
    Redis -->|Results| Celery
```

## Agent Hierarchy

### Tier 1: Strategic Agents (Orchestrators)
- **Project Strategist**: Plans, breaks down tasks, delegates
- **System Architect**: Defines architecture, patterns, standards

**Model**: Perplexity Sonar (Online Research & Reasoning)
**Responsibilities**: High-level planning, decision-making

### Tier 2: Specialist Agents (Executors)
- **Frontend Specialist**: UI/UX, React, Next.js
- **Backend Specialist**: APIs, business logic, Python
- **Database Architect**: Schema, queries, optimization
- **QA Engineer**: Testing, validation, quality assurance
- **DevOps Engineer**: CI/CD, Docker, Kubernetes
- **Security Engineer**: Security audits, vulnerability scanning

**Model**: Perplexity Sonar (Specialized Context)
**Responsibilities**: Specialized task execution

## Communication Flow

### 1. Task Submission
```
User → Mission Control (Dashboard) → Orchestrator (Port 8080) → Agents
```

### 2. Inter-Agent Communication
```
Orchestrator → HTTP (Internal Docker Network) → Specialist Agents
```

### 3. Result Aggregation
```
Specialists → JSON Response → Orchestrator → Client
```

## Data Flow

### Task Planning
1. User submits task to Orchestrator
2. Orchestrator creates a plan using `sonar-reasoning`
3. Subtasks are delegated to specific agents via their internal API endpoints

### Task Execution
1. Specialist receives payload
2. Executes task using its specific capabilities
3. Returns structured result to Orchestrator

### Result Collection
1. Orchestrator aggregates all results
2. Returns final workflow report to Dashboard

## Background Processing

### Docker Network
- **Agents** run on internal ports (e.g., 8001-8009).
- **Orchestrator** exposes port 8080 to the host.
- **Frontend** connects to Orchestrator via `localhost:8080` (browser-side).

### Auto-Restart Policy
- All services are configured with `restart: always` or `unless-stopped` to ensure high availability.
- `health_check.py` verifies the status of all containers and critical endpoints.

## Observability Stack
- **Prometheus**: Metrics collection
- **Grafana**: Visual dashboards (http://localhost:3001)
- **Jaeger**: Distributed tracing

### Logging
- Structured JSON logs
- Centralized via ELK/Loki (optional)
- Correlation IDs for tracing

## Hive Mind (Shared Knowledge)

### Team Memory Standards
- Coding conventions
- Best practices
- Project-specific rules
- Updated by all agents

### Skills Library
- Reusable functions
- Common patterns
- Tested solutions
- Version controlled

## Integration Points

### Trae Integration
```yaml
volumes:
  - ${TRAE_WORKSPACE}:/workspace:ro
environment:
  - TRAE_MCP_ENABLED=true
```

### GitHub Integration
- Webhooks for issues → tasks
- PR review by agents
- Commit on completion

## Future Enhancements
1. **Learning Loop**: Fine-tune on project-specific patterns
2. **Multi-project**: Separate workspaces per project
3. **Human-in-the-Loop**: Approval workflow for changes
