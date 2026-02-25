# Changelog

> **built with WelshDog + BROski 🚀🌙**

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.0.0-rc1] - 2026-02-25

### Added
- **Production Readiness:** Scaled `hypercode-core` to 2 replicas for high availability.
- **Load Testing:** Added `k6` smoke test script (`perf/load-test.js`) and validation report.
- **Documentation:** Created `docs/STORY.md` for the full manifesto and `docs/validation-report.md` for QA sign-off.
- **Root Cleanup:** Moved 50+ clutter files to `docs/reports/` and `archive/` for a cleaner repo root.

### Changed
- **README Refactor:** Streamlined `README.md` to be concise, visual, and neurodivergent-friendly.
- **Performance Docs:** Updated `PERFORMANCE.md` with latest load test results (P95: 2.56s).
- **Service Configuration:** Moved `coder-agent` port to `8011` to avoid conflict with scaled core services.

## [3.0.0-performance] - 2026-02-22

### Added
- **Load Testing Harness:** Locust suite for distributed load testing (`tests/performance/`).
- **Performance Gates:** CI workflow (`.github/workflows/performance.yml`) for P99 latency and error rate checks.
- **WebSocket Optimization:** Batch processing for real-time updates in HyperSwarm Control Center.
- **Graph Optimization:** Enhanced `vis-network` rendering with physics stabilization and shadow removal.

### Changed
- **HyperSwarm Rendering:** Reduced DOM thrashing with `requestAnimationFrame` and update batching.
- **Documentation:** Added `PERFORMANCE.md` with benchmarking details.

### Benchmarks
- **Throughput:** Sustained 100+ concurrent users.
- **Latency:** Targeted P99 < 800ms.
- **FPS:** Maintained 60 FPS under load.

### Added
- **MCP Integration:** Full support for Model Context Protocol to enable standardized agent tooling.
- **Autonomous Operations:** Agents can now deploy and manage Docker containers dynamically.
- **Observability Stack:** Integrated Prometheus, Grafana, and AlertManager for real-time monitoring.
- **Documentation:** Comprehensive architecture, security, and onboarding guides.
- **Traceability:** Matrix mapping requirements to code and tests.
- **New Quickstart:** Added `docs/QUICKSTART.md` and updated `.env.example`.

### Changed
- **Documentation Overhaul:** Synchronized all `docs/` files with Main `README.md` (Docker Compose syntax, ports, env setup).
- **Agent Architecture:** Refactored `Coder Agent` to use MCP clients instead of direct shell execution.
- **Docker Compose:** Updated service definitions to support new microservices structure.

### Fixed
- **Docker Socket Mounting:** Resolved permission issues on Windows/Linux cross-compatibility.
- **Database Migrations:** Fixed race conditions during initial startup.
- **Ollama Health Check:** Fixed health check failure by switching to TCP probe.

## [2.0.0] - 2026-01-15

### Initial Release
- Core microservices architecture.
- Basic Coder Agent capabilities.
- Next.js Frontend and FastAPI Backend.

---
> **built with WelshDog + BROski 🚀🌙**
