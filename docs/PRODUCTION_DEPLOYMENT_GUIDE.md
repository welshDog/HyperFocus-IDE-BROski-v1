# HyperCode V3.0 - Production Deployment Guide

**Last Updated:** February 22, 2026
**Status:** Production Ready ✅
**Maintainer:** HyperCode DevOps Team

---

## 🎯 Overview

HyperCode V3.0 is a production-grade, AI-powered development platform featuring a distributed swarm of specialized agents, comprehensive monitoring, automated backups, and professional-grade resource management.

### Quick Stats
- **Services:** 10 AI agents + 7 infrastructure services
- **Uptime Target:** 99.9%+
- **Resource Headroom:** 90%+ (optimal for load spikes)
- **Backup Frequency:** Daily automated
- **Monitoring:** Prometheus + Grafana + Jaeger + **Custom Performance Gates**

---

## 🏗️ System Architecture

### Network Topology
```
┌─────────────────────────────────────────────┐
│          FRONTEND NETWORK (Public)          │
│  - broski-terminal (3000)                   │
│  - hyperflow-editor (5173)                  │
│  - dashboard (8088)                         │
│  - grafana (3001)                           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│       BACKEND NETWORK (Internal Only)       │
│  - hypercode-core (8000)                    │
│  - crew-orchestrator (8081)                 │
│  - 8 Specialized AI Agents                  │
│  - celery-worker                            │
│  - prometheus (9090)                        │
│  - jaeger (16686)                           │
│  - ollama (11434)                           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│         DATA NETWORK (Internal Only)        │
│  - redis (6379)                             │
│  - postgres (5432)                          │
└─────────────────────────────────────────────┘
```

### AI Agent Swarm
| Agent | Port | Role | Resource Limits |
|-------|------|------|-----------------|
| **project-strategist** | 8001 | Strategic planning | 1 CPU, 1GB RAM |
| **frontend-specialist** | 8002 | React/UI development | 1 CPU, 1GB RAM |
| **backend-specialist** | 8003 | Python/API development | 1 CPU, 1GB RAM |
| **database-architect** | 8004 | Schema design & optimization | 1 CPU, 1GB RAM |
| **qa-engineer** | 8005 | Testing & quality assurance | 1 CPU, 1GB RAM |
| **devops-engineer** | 8006 | Infrastructure & deployment | 1 CPU, 1GB RAM |
| **security-engineer** | 8007 | Security auditing | 1 CPU, 1GB RAM |
| **system-architect** | 8008 | System design | 1 CPU, 1GB RAM |
| **crew-orchestrator** | 8081 | Multi-agent coordination | 1.5 CPU, 1.5GB RAM |
| **hypercode-core** | 8000 | Central API & coordination | 1 CPU, 1GB RAM |

---

## 🚀 Deployment Options

### Option A: Docker Compose (Local / Single Node)

#### 1. Clone & Setup
```bash
git clone https://github.com/welshDog/HyperCode-V2.0.git
cd HyperCode-V2.0
cp .env.example .env
# Edit .env with your secrets
```

#### 2. Start Infrastructure
```bash
docker-compose up -d
```

### Option B: Kubernetes (Production / Multi-Node)

**New in V3.0:** Full Kubernetes support via Terraform and Helm.

#### 1. Provision Infrastructure (AWS EKS)
```bash
cd infra/terraform
terraform init
terraform apply
```

#### 2. Deploy Secrets
```bash
# Update secrets.yaml with real values first!
kubectl apply -f k8s/production/secrets-template.yaml
```

#### 3. Deploy Application
```bash
kubectl apply -f k8s/production/rbac.yaml
# Deploy other manifests as needed
```

---

## 📊 Monitoring & Observability

### Grafana Dashboards
**URL:** http://localhost:3001
**Login:** admin / admin (change on first login)

**New V3.0 Dashboards:**
- **HyperCode Production Overview**: Real-time RPS, P99 Latency, and Error Rates.
- **System Overview**: CPU, Memory, Network across all services.
- **Agent Performance**: Request rates, response times per agent.

### Performance Gates
We enforce strict performance metrics in CI/CD:
- **P99 Latency:** < 800ms
- **Error Rate:** < 0.1%
- **Throughput:** 100+ Concurrent Users

---

## 🔧 Maintenance

### Daily Automated Backups

**Script Location:** `scripts/backup_volumes.sh`

**What Gets Backed Up:**
- PostgreSQL database (full dump)
- Redis data (RDB snapshot)
- Grafana dashboards & configs

**Schedule (via cron):**
```bash
# Runs daily at 2 AM
0 2 * * * /path/to/HyperCode-V2.0/scripts/backup_volumes.sh
```

---

## 🩺 Health Checks & Resource Management

### Optimized Health Check Configuration

**Philosophy:** AI agents need generous timeouts to handle LLM inference spikes.

**Current Settings:**
```yaml
healthcheck:
  interval: 60s
  timeout: 10s
  retries: 5
  start_period: 90s
```

### Resource Limits

**Why Limits Matter:**
- Prevent single runaway agent from crashing host
- Ensure fair resource distribution
- Enable predictable scaling

**Current Allocation:**
| Service | CPU Limit | Memory Limit | Justification |
|---------|-----------|--------------|---------------|
| AI Agents (8×) | 1 CPU | 1GB | LLM inference + API handling |
| hypercode-core | 1 CPU | 1GB | Central API coordination |
| crew-orchestrator | 1.5 CPU | 1.5GB | Multi-agent task distribution |
| ollama | 1.5 CPU | 4GB | Local LLM model hosting |
| celery-worker | 1 CPU | 1GB | Background task processing |

---

## 🚨 Troubleshooting

### Agent Not Starting

**Symptoms:** Agent stuck in "health: starting" for >90s

**Diagnosis:**
```bash
# Check logs
docker logs <agent-name>
```

**Solutions:**
```bash
# Verify environment variables
docker exec <agent-name> env | grep ANTHROPIC_API_KEY

# Test Redis connectivity
docker exec <agent-name> redis-cli -h redis ping
```

---

## ✅ Pre-Deployment Checklist

```
□ All environment variables set in .env
□ PostgreSQL password is strong (min 16 chars)
□ API_KEY is unique and secure
□ HYPERCODE_JWT_SECRET is min 32 characters
□ Backup directory exists and is writable
□ Backup cron job is scheduled
□ Grafana admin password changed from default
□ Docker has sufficient resources (8GB RAM min)
□ Disk space >50GB available
□ All services start with "Up (healthy)" status
□ Health checks pass for all agents
□ Monitoring dashboards are accessible
□ Test mission completes successfully
```

---

**Deployment Status:** ✅ Production Ready
**Last Validated:** February 22, 2026
**Next Review:** March 22, 2026

---

*Built with ❤️ by the HyperCode Team*
*Optimized with expertise from Gordon AI & Trae (AI Architect)*