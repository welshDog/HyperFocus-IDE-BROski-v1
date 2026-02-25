# 🚀 HyperCode V2.0 Quickstart

**Goal:** Run the entire ecosystem (Agents, API, Dashboard, Observability) in under 2 minutes.

## 📋 Prerequisites

- **Docker & Docker Compose** (Desktop 4.0+)
- **Git**
- **Node.js 18+** (Optional, only for local frontend development)

## ⚡ Steps

### 1. Clone the Repository
```bash
git clone https://github.com/welshDog/HyperCode-V2.0.git
cd HyperCode-V2.0
```

### 2. Configure Environment
Set up your environment variables (API keys, Database credentials).
```bash
cp .env.example .env
# Edit .env and add your PERPLEXITY_API_KEY
```

### 3. Launch the Stack
Start all services including the Agent Swarm, Core API, and Observability stack.
```bash
docker compose up -d
```

### 4. Verify Services
Check that all containers are healthy.
```bash
docker compose ps
```

## 🖥️ Access Interfaces

| Service | URL | Credentials (Default) |
|---------|-----|-----------------------|
| **Mission Control** | [http://localhost:3000/dashboard](http://localhost:3000/dashboard) | N/A |
| **Orchestrator API** | [http://localhost:8080/docs](http://localhost:8080/docs) | N/A |
| **Grafana** | [http://localhost:3001](http://localhost:3001) | `admin` / `admin` |
| **Prometheus** | [http://localhost:9090](http://localhost:9090) | N/A |
| **Jaeger** | [http://localhost:16686](http://localhost:16686) | N/A |

## 🎮 Run Your First Mission

1. Open the **Mission Control** at `http://localhost:3000/dashboard`.
2. Enter your intent in the **Intent Box**.
3. Click **Execute Intent**.
4. Watch the agent graph light up as the swarm collaborates.

## 🛑 Stop Services
```bash
docker compose down
```

---
> *Need help? Check [DEPLOYMENT_SUMMARY_ONE_PAGE.md](../DEPLOYMENT_SUMMARY_ONE_PAGE.md) for quick troubleshooting.*
