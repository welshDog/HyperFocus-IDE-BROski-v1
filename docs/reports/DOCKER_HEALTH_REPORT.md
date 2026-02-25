# Docker Health Check Report
**Generated:** $(date)

---

## 📊 System Overview

| Metric | Value |
|--------|-------|
| **Docker Client Version** | 29.2.1 |
| **Docker Server Version** | 29.2.1 |
| **Total Containers** | 34 |
| **Running Containers** | 30 |
| **Stopped/Exited Containers** | 4 |
| **Total Images** | 34 |
| **Active Images** | 30 |
| **Total Volumes** | 25 |
| **Active Volumes** | 8 |
| **Total Networks** | 8 |

---

## ⚡ Resource Usage

### Disk Space Allocation
| Type | Total | Active | Size | Reclaimable |
|------|-------|--------|------|-------------|
| **Images** | 34 | 30 | 58.58 GB | 56.78 GB (96%) |
| **Containers** | 34 | 30 | 12.85 MB | 2.236 MB (17%) |
| **Volumes** | 25 | 8 | 5.517 GB | 5.306 GB (96%) |
| **Build Cache** | 284 | 0 | 34.02 GB | 11.42 GB |

**⚠️ Total Reclaimable Space: ~73.5 GB (96% potential cleanup)**

---

## 🟢 Healthy Containers (30)

| Container | Status | Ports | Health |
|-----------|--------|-------|--------|
| backend-specialist | Up 19m | 0.0.0.0:8003→8000 | ✅ Healthy |
| devops-engineer | Up 19m | 0.0.0.0:8006→8000 | ✅ Healthy |
| qa-engineer | Up 19m | 0.0.0.0:8005→8000 | ✅ Healthy |
| frontend-specialist | Up 19m | 0.0.0.0:8002→8000 | ✅ Healthy |
| hypercode-core | Up 13m | 0.0.0.0:8000→8000 | ✅ Healthy |
| loki | Up 19m | 0.0.0.0:3100→3100 | Running |
| cadvisor | Up 19m | 0.0.0.0:8081→8080 | ✅ Healthy |
| node-exporter | Up 19m | 0.0.0.0:9100→9100 | Running |
| hypercode-dashboard | Up 19m | 0.0.0.0:8088→80 | ✅ Healthy |
| celery-worker | Up 12m | 8000 | ✅ Healthy |
| broski-terminal | Up 12m | 0.0.0.0:3000→3000 | ✅ Healthy |
| grafana | Up 19m | 0.0.0.0:3001→3000 | Running |
| postgres | Up 13m | 0.0.0.0:5432→5432 | ✅ Healthy |
| redis | Up 13m | 0.0.0.0:6379→6379 | ✅ Healthy |
| jaeger | Up 19m | 0.0.0.0:5775→5775 (UDP), 0.0.0.0:5778→5778, etc. | Running |
| prometheus | Up 19m | 127.0.0.1:9090→9090 | Running |
| hypercode-ollama | Up 19m | 127.0.0.1:11434→11434 | ✅ Healthy |
| system-architect | Up 19m | 0.0.0.0:8008→8008 | ✅ Healthy |
| project-strategist | Up 19m | 0.0.0.0:8009→8009 | ✅ Healthy |
| security-engineer | Up 19m | 0.0.0.0:8007→8007 | ✅ Healthy |
| database-architect | Up 19m | 0.0.0.0:8004→8004 | ✅ Healthy |
| crew-orchestrator | Up 19m | 127.0.0.1:8080→8080 | ✅ Healthy |
| hyper-agents-box | Up 19m | 127.0.0.1:5000→5000 | ✅ Healthy |
| modest_hugle | Up 4m | — | Running |
| mcp-server | Up 11m | — | Running |
| jolly_sutherland | Exited (0) | — | ✅ Clean Exit |
| infallible_lamport | Exited (0) | — | ✅ Clean Exit |

---

## 🔴 Problem Containers (4)

### 1. **crazy_tharp** — UNHEALTHY
- **Status:** Running (8 minutes)
- **Health Check:** ⚠️ **UNHEALTHY**
- **Port:** 8003/tcp (internal)
- **Last Error:** Failing health checks
- **Root Cause:** Cannot reach `http://hypercode-core:8000` — DNS resolution failure
  ```
  ⚠️ Agent registration connection failed: [Errno -2] Name or service not known
  Health check returning 503 Service Unavailable
  ```
- **Recommendation:** 
  - Verify `hypercode-core` container is running and healthy
  - Check Docker network connectivity between containers
  - Run: `docker network inspect <network>` to verify container connectivity
  - Consider restarting the container: `docker restart crazy_tharp`

### 2. **frosty_hugle** — EXITED WITH ERROR
- **Status:** Exited (1) 3 minutes ago
- **Exit Code:** 1 (non-zero = error)
- **Recommendation:** Check logs: `docker logs frosty_hugle`

### 3. **coder-agent** — EXITED WITH ERROR
- **Status:** Exited (255) 19 minutes ago
- **Exit Code:** 255 (critical error)
- **Port Mapping:** 0.0.0.0:8001→8000
- **Recommendation:** 
  - Check logs: `docker logs coder-agent`
  - Review startup configuration
  - Exit code 255 typically indicates a startup failure or signal termination

---

## 📦 Image Storage (34 Images)

### Largest Images
| Repository:Tag | Size | Age |
|---|---|---|
| ollama/ollama:latest | 9.01 GB | 34 days |
| hyperfocus-ide-broski-v1-hypercode-core:latest | 8.26 GB | 1 day |
| hyperfocus-ide-broski-v1-celery-worker:latest | 8.21 GB | 2 days |
| grafana/alloy:v1.0.0 | 1.01 GB | 319 days |
| hyperfocus-ide-broski-v1-project-strategist:v1-patched | 1.53 GB | 1 day |
| grafana/grafana:latest | 995 MB | 12 days |

**Note:** 56.78 GB (96%) of image storage is reclaimable — images are not in use.

### Unused Images (Candidates for Cleanup)
Most images are inactive. Run `docker image prune` to remove dangling images and unused images:
```bash
docker image prune -a  # Remove all unused images
```

---

## 💾 Volumes (25 Volumes)

### Active Volumes (8 in use)
- hyperfocus-ide-broski-v1_grafana-data
- hyperfocus-ide-broski-v1_postgres-data
- hyperfocus-ide-broski-v1_prometheus-data
- hyperfocus-ide-broski-v1_redis-data
- hypercode-v20_postgres-data
- hypercode-v20_redis-data
- hypercode-v20_ollama_data
- hypercode-v20_grafana-data

### Unused Volumes (17 not in use)
These consume 5.306 GB of reclaimable space. Run:
```bash
docker volume prune  # Remove unused volumes
```

---

## 🌐 Networks (8 Networks)

| Network Name | Driver | Scope |
|---|---|---|
| bridge (default) | bridge | local |
| host | host | local |
| none (null) | null | local |
| docker_labs-ai-tools-for-devs-desktop-extension_default | bridge | local |
| grafana_docker-desktop-extension-desktop-extension_extension | bridge | local |
| hypercode_backend_net | bridge | local |
| hypercode_data_net | bridge | local |
| hypercode_frontend_net | bridge | local |

**Network Status:** All networks operational. No connectivity issues detected except for DNS resolution in `crazy_tharp`.

---

## 🛠️ Recommendations & Actions

### Priority 1: IMMEDIATE (Operational Issues)
1. **Fix `crazy_tharp` unhealthy status:**
   ```bash
   docker restart crazy_tharp
   docker logs crazy_tharp  # Monitor for persistent issues
   ```
   - Verify hypercode-core is reachable from the container's network
   - Check if DNS resolution is working: `docker exec crazy_tharp nslookup hypercode-core`

2. **Investigate `coder-agent` exit (exit code 255):**
   ```bash
   docker logs coder-agent --tail 50
   ```

### Priority 2: CLEANUP (Free 73.5 GB)
1. **Remove unused images (56.78 GB):**
   ```bash
   docker image prune -a --force
   ```

2. **Remove unused volumes (5.306 GB):**
   ```bash
   docker volume prune --force
   ```

3. **Clean build cache (11.42 GB):**
   ```bash
   docker builder prune --all --force
   ```

4. **Full cleanup (use with caution):**
   ```bash
   docker system prune -a --volumes --force
   ```

### Priority 3: MONITORING
- Container `mcp-server` and `modest_hugle` are running but have no health checks configured. Consider adding health checks.
- `prometheus`, `grafana`, `loki`, `jaeger`, and `node-exporter` are running without health checks. These should ideally have monitoring endpoints configured.

---

## 📈 Summary

| Category | Status | Details |
|----------|--------|---------|
| **Overall Health** | ⚠️ **GOOD** | 30/34 containers healthy; 4 require attention |
| **Disk Space** | 🔴 **CRITICAL** | 73.5 GB reclaimable; recommend cleanup |
| **Network Connectivity** | ✅ **OK** | All networks operational; 1 DNS resolution issue |
| **Services** | ✅ **OK** | Core services running (DB, cache, logging, tracing) |
| **Configuration** | ⚠️ **WARNING** | Some containers lack health checks |

---

## 🔧 Quick Action Commands

```bash
# Restart unhealthy container
docker restart crazy_tharp

# Check specific container logs
docker logs coder-agent -n 100

# Clean up everything (use with caution)
docker system prune -a --volumes

# Check disk usage
docker system df

# Inspect specific container health
docker inspect crazy_tharp --format '{{.State.Health.Status}}'
```

---

**Report Complete.** Run `docker ps -a` to verify changes after any cleanup operations.
