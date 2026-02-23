# Performance Testing Harness

This directory contains the Locust load testing suite for the HyperCode Agent Orchestrator.

## Prerequisites

Ensure you have the required dependencies installed:

```bash
pip install -r ../requirements.txt
```

## Running the Load Test

### 1. Start the Orchestrator Service

Make sure the `agents/crew-orchestrator/main.py` service is running.

```bash
uvicorn agents.crew-orchestrator.main:app --host 0.0.0.0 --port 8081
```

### 2. Run Locust

You can run Locust in headless mode to automate the test and generate a CSV report.

```bash
locust -f locustfile.py --headless --host http://localhost:8081 --csv=load_test_results --run-time 140s
```

This will run the test for 140 seconds (matching the `StagesShape` duration) and output results to `load_test_results_stats.csv`.

### Metrics Captured

- **Requests per Second (RPS)**
- **Response Times (P50, P95, P99)**
- **Failure Rates**
- **WebSocket Connections** (custom event)

### Scenarios

1.  **Submit Task Intent** (`POST /plan`): Simulates high-priority task submission.
2.  **Initiate Workflow** (`POST /workflow/feature`): Simulates complex workflow initiation.
3.  **Health Check** (`GET /health`): Simulates keep-alive checks.
4.  **WebSocket Connection**: Simulates real-time updates (connection established on user start).

### Ramp-up / Ramp-down Strategy

The test uses a custom `LoadTestShape` to simulate:
- **Warmup**: 10 users (10s)
- **Normal Load**: 50 users (30s)
- **High Load**: 100 users (30s)
- **Steady State**: 100 users (60s)
- **Cooldown**: Ramp down to 0 (10s)
