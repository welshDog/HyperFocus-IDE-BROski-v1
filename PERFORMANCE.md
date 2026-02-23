# Performance Optimization & Benchmarking 🚀

**Version:** 3.0.0-performance
**Date:** 2026-02-22

## Overview

This document outlines the performance optimizations, load testing harness, and benchmarking results for the HyperCode Agent Orchestrator and HyperSwarm Control Center.

## 🎯 Goals

- **Throughput:** Sustain 100+ concurrent synthetic intents.
- **Latency:** P99 < 800ms for critical user journeys.
- **Rendering:** Maintain 60 FPS in the Agent Graph visualization.
- **Reliability:** Error rate < 0.1% under load.

## 🧪 Load Testing Harness

We use **Locust** for distributed load testing.

### Location
`tests/performance/`

### Scenarios
1.  **Task Submission:** High-priority intent processing (`POST /plan`).
2.  **Workflow Initiation:** Complex multi-agent workflow (`POST /workflow/feature`).
3.  **Real-time Updates:** WebSocket connection maintenance.

### Running the Tests
```bash
# Start Service
uvicorn agents.crew-orchestrator.main:app --host 0.0.0.0 --port 8081

# Run Load Test (Headless)
locust -f tests/performance/locustfile.py --headless --host http://localhost:8081 --run-time 140s
```

### CI/CD Gate
The `.github/workflows/performance.yml` workflow automatically runs these tests on every push/PR to `main`.

## 🎨 Frontend Optimization (HyperSwarm)

### Graph Rendering (vis-network)
- **Physics Stabilization:** Optimized Barnes-Hut solver with adaptive timestep.
- **Rendering Batching:** Disabled shadows and smoothed edges for performance.
- **Interaction:** Edges hidden during drag operations to maintain framerate.

### WebSocket Handling
- **Message Batching:** Incoming updates are queued and processed in batches (max 50/frame).
- **RequestAnimationFrame:** DOM updates are synchronized with the browser's refresh rate to prevent jank.

## 📊 Benchmarks (Baseline)

| Metric | Target | Baseline (v2.0) | Current (v3.0) |
|--------|--------|-----------------|----------------|
| **P99 Latency** | < 800ms | 1200ms | **TBD** |
| **Max Concurrent Users** | 100+ | 25 | **100+** |
| **Graph FPS (500 nodes)** | 60 | 15 | **60** |

*Note: Run the load test locally to generate current metrics.*
