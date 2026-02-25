# Health Check System Documentation

This document outlines the comprehensive health check system implemented for the HyperCode platform. The system ensures multi-layered verification of service health, including container status, dependencies, network connectivity, and resource utilization.

## Overview

The health check system consists of:
1.  **Docker Health Checks**: Built-in container health verification with strict timeout policies.
2.  **Application Health Endpoints**: `/health` endpoints in Core and Agents that validate internal state and downstream dependencies (Redis, Postgres, Core).
3.  **CLI Health Monitor**: A centralized Python script (`scripts/health_check_system.py`) for real-time system-wide health assessment.

## Success Criteria

-   **Response Time**: All services must respond to health checks within **5 seconds**.
-   **Status Code**: Healthy services return `200 OK`. Degraded or unhealthy services return `503 Service Unavailable`.
-   **Dependency Validation**: Services must successfully connect to their critical dependencies (e.g., Redis, Postgres) to be considered healthy.

## Docker Compose Configuration

All services are configured with `healthcheck` blocks in `docker-compose.yml` to support orchestration and automatic recovery.

Example Configuration (HyperCode Core):
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "--max-time", "5", "http://localhost:8000/health"]
  interval: 30s
  timeout: 5s
  retries: 3
```

-   **Interval**: Frequency of checks (30s - 60s).
-   **Timeout**: Strict 5s limit.
-   **Retries**: Number of consecutive failures before marking as unhealthy.

## Application Endpoints

### Core Service (`http://localhost:8000/health`)
Checks:
-   **Redis**: Verifies connection to Redis.
-   **Database**: Verifies connection to PostgreSQL.
-   **LLM**: Checks readiness of LLM integration.

### Agents (`http://localhost:800X/health`)
Checks:
-   **Redis**: Verifies connection to the shared Redis instance.
-   **Core**: Verifies connectivity to the HyperCode Core service.

## CLI Health Monitor

A centralized script is available at `scripts/health_check_system.py` to check the status of all services from the host machine.

### Usage

```bash
python scripts/health_check_system.py
```

### Features
-   **Parallel Checks**: Checks all configured services concurrently.
-   **Latency Reporting**: Reports response time for each service.
-   **Status Reporting**: Shows `OK`, `Status Code`, or error messages.
-   **Color-coded Output**: (If supported by terminal) Green for pass, Red for fail.

### Monitored Services
-   HyperCode Core
-   Broski Terminal
-   Redis (via Core)
-   Postgres (via Core)
-   Dashboard
-   All Agents (Frontend, Backend, Database, QA, DevOps, Security, System, Project)

## Integration with Orchestration (Kubernetes / Swarm)

The `healthcheck` definitions in `docker-compose.yml` are compatible with Docker Swarm. For Kubernetes, translate these into `livenessProbe` and `readinessProbe` in your Pod specs.

**Kubernetes Example:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 30
  timeoutSeconds: 5
```

## Alerting & Recovery

-   **Docker/Swarm**: Automatically restarts unhealthy containers based on the `healthcheck` status.
-   **Monitoring**: Prometheus and Grafana (running on ports 9090 and 3001) can be configured to scrape these `/health` endpoints and trigger alerts via Alertmanager if status != 200 or latency > 5s.
