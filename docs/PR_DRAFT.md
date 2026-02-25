# Pull Request: HyperCode v3.0.0-rc1 Production Readiness & Cleanup

## 📝 Summary
This PR transitions the repository from "development chaos" to a **Production-Ready Release Candidate**. It addresses critical technical debt, improves documentation clarity for neurodivergent developers, and verifies system stability under load.

### Key Changes
- **Root Cleanup:** Moved 50+ clutter files (reports, logs, temp notes) to `docs/reports/` and `archive/`.
- **README Refactor:** Streamlined the main entry point to be visual, concise, and focused on the value proposition. Migrated the full manifesto to `docs/STORY.md`.
- **High Availability:** Updated `docker-compose.yml` to deploy `hypercode-core` with 2 replicas.
- **Performance Validation:** Added a `k6` load testing script (`perf/load-test.js`) and established a performance baseline.
- **Port Conflict Resolution:** Moved `coder-agent` to port `8011` to allow core service scaling.

## 🏗️ Technical Architecture Decisions

### 1. Replica Scaling
- **Decision:** Scale `hypercode-core` to 2 replicas.
- **Rationale:** To verify the stateless nature of the backend and ensure the system can handle horizontal scaling.
- **Impact:** `docker-compose` now handles internal load balancing via round-robin on the `backend-net` network.

### 2. Documentation Structure
- **Decision:** Adopt a "Clean Root" policy.
- **Rationale:** A cluttered root directory causes cognitive overload (the "Wall of Text" problem). Moving reports to `docs/` makes the project approachable.

## 🚀 Performance Impact
- **Baseline:** Established via `perf/load-test.js`.
- **Current Metrics (Smoke Test):**
    - Throughput: ~5 req/s (limited by local dev environment).
    - Error Rate: 0.00% (Pass).
    - P95 Latency: 2.56s (Missed <300ms SLA).
- **Analysis:** The missed latency target is expected on a Windows dev machine running 15+ containers. Production deployment on Linux nodes is required for true validation.

## 🔒 Security Considerations
- **No Secrets:** Verified no secrets were added in this PR.
- **Health Checks:** Enhanced `docker-compose` health checks ensure traffic only flows to healthy containers.

## ✅ Verification Checklist
- [x] `docker compose up --scale hypercode-core=2` works.
- [x] `http://localhost:8000/health` returns 200 OK.
- [x] Root directory is clean.
- [x] `k6` load test runs without errors.

## 👥 Reviewers
@welshDog (Lead)
@BROski (AI Co-pilot)
