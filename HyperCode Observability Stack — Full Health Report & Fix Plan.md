HyperCode Observability Stack — Full Health Report & Fix Plan
Date: Monday 23 February 2026, ~21:00 GMT | Location: Llanelli, Wales

SYSTEM OVERVIEW
Component	Version	Status
Grafana	12.3.3	✅ Running
Prometheus	3.9.1	✅ Running
Prometheus DB	—	✅ No corruption
Jaeger	—	✅ Connected
Loki	—	❌ Not configured
Pyroscope	—	❌ Not configured
Tempo/Traces	—	❌ Not configured
CRITICAL ISSUE #1 — project-strategist Agent is DOWN
What's happening
Prometheus has had a CRITICAL InstanceDown alert firing since 20:30:26 UTC (~44 minutes at time of check). The project-strategist:8001 container is refusing TCP connections on 172.18.0.12:8001.
​

This is the single most urgent problem in the entire stack.

Impact
1 of your 9 BROski agents is completely offline

Prometheus scrape for this target fails every 15s

Any Grafana panels or recording rules that depend on project-strategist metrics will show gaps

The InstanceDown critical alert will continue firing indefinitely until resolved

Fix
bash
# 1. Check if the container is running at all
docker ps | grep project-strategist

# 2. If it's stopped, restart it
docker compose restart project-strategist

# 3. If it crashed, check why
docker logs project-strategist --tail=100

# 4. Verify it comes back up
curl http://project-strategist:8001/metrics
If the container keeps crashing, check for port conflicts, OOM kills, or misconfiguration in your compose file:

bash
docker inspect project-strategist | grep -A5 "ExitCode"
CRITICAL ISSUE #2 — cAdvisor Metrics Missing
What's happening
The HyperCode Overview and Infrastructure Alerts dashboards have CPU Usage and Memory Usage panels showing "No data". The alert rule High CPU Usage (>80%) in Grafana also returns NoData state. This is because cAdvisor is not a configured scrape target in Prometheus — there's no cadvisor job in the target list (only agents, hypercode-core, and prometheus).

Impact
You have zero container-level CPU/memory visibility right now

The HighCpuLoad and HighMemoryUsage Prometheus alert rules also rely on node_exporter metrics (node_cpu_seconds_total, node_memory_MemTotal_bytes) — none of those are being scraped either

The Infrastructure Alerts folder in Grafana is effectively non-functional

Fix — Add cAdvisor + node_exporter to your Docker Compose
text
# docker-compose.yml additions:
cadvisor:
  image: gcr.io/cadvisor/cadvisor:latest
  container_name: cadvisor
  ports:
    - "8081:8080"
  volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:rw
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
  restart: unless-stopped

node-exporter:
  image: prom/node-exporter:latest
  container_name: node-exporter
  ports:
    - "9100:9100"
  restart: unless-stopped
Then add scrape jobs to your prometheus.yml:

text
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
HIGH ISSUE #3 — Application Metrics Not Flowing to Most Dashboards
What's happening
The following dashboards all show "No data" across every panel:

HyperCode Agents (Agent Stream Clients, Agent Stream Latency p95)

HyperCode Execution (HTTP 5xx Rate, Request Rate, Interpreter Executions, etc.)

Roundtrip Worker Latency

SSE Agent Registry (SSE Clients, Latency, Errors, Stream Throughput)

Voice Coding Observability (STT Latency, STT Error Rate, etc.)

HyperCode AI & Memory Intelligence (LLM Request Latency, etc.)

Yet Prometheus does have 2,060 active series and 334 metric names being scraped. The live data is flowing for http_request_duration and request rates (visible in HyperCode Production Overview and HyperCode Overview). The gap is that the custom application metrics (agent stream metrics, interpreter metrics, voice STT metrics, LLM metrics) are not being emitted from your services.

Root cause possibilities
The HyperCode services haven't been instrumented yet with those specific Prometheus metrics (e.g. agent_stream_latency_ms_bucket, interpreter_executions_total, voice_stt_latency_seconds)

The services are running but the metrics endpoints aren't exposing those metric names

The metric names in the dashboards don't match what's actually being exported

Fix — Diagnose first
bash
# Check what metrics hypercode-core is actually exporting
curl http://hypercode-core:8000/metrics | grep -E "(agent|interpreter|voice|llm|stt)"

# Check what the agents are exporting
curl http://coder-agent:8000/metrics | grep -E "(agent|stream|latency)"
If those metrics don't exist yet, you need to add instrumentation to each service. Example for Python (using prometheus_client):

python
from prometheus_client import Histogram, Counter, Gauge

agent_stream_latency = Histogram(
    'agent_stream_latency_ms',
    'SSE agent stream latency in ms',
    buckets=[10, 50, 100, 250, 500, 1000, 2000, 5000]
)

agent_stream_clients = Counter(
    'agent_stream_clients_total',
    'Total SSE stream clients connected'
)
MEDIUM ISSUE #4 — Event Bus Latency Dashboard Panel Error
What's happening
The Agent Registry SSE Latency panel on the Event Bus Latency & Reliability dashboard shows "no heatmap fields found". The Deduplication Efficiency panel has a warning triangle.

Root cause
The panel is configured as a heatmap visualization, which requires a histogram-type metric (buckets, _bucket suffix). Either:

The metric doesn't exist yet (ties into Issue #3 above)

The metric exists but is not in the correct histogram format for heatmap rendering

Fix
Either instrument the metric as a proper Prometheus histogram:

python
sse_latency_hist = Histogram(
    'agent_registry_sse_latency_seconds',
    'SSE registry latency',
    buckets=[.001, .005, .01, .025, .05, .1, .25, .5, 1.0, 2.5]
)
Or, temporarily change the panel visualization from Heatmap to Time series in Grafana until the histogram data starts flowing.

MEDIUM ISSUE #5 — Duplicate Dashboards
What's happening
Every dashboard exists twice in Prometheus — once at root level and once inside the HyperCode folder. The API search returns 14 dashboard entries for what should be 7 unique dashboards.

Impact
Confusion about which dashboard is canonical

The root-level duplicates have no folder and may have outdated panel config

Grafana's Overview dashboard links to both copies of each dashboard (e.g. two "HyperCode Agents" buttons)

Fix
Delete the root-level orphan copies via the Grafana UI:

Go to Dashboards → switch to list view

Filter to show dashboards not in any folder

Select and delete: HyperCode Agents (id:4), HyperCode Execution (id:6), Roundtrip Worker Latency (id:8), SSE Agent Registry (id:9), Voice Coding Observability (id:2)

Or via API:

bash
# Delete root-level orphan dashboards (replace UIDs as needed)
curl -X DELETE http://admin:admin@localhost:3001/api/dashboards/uid/8a68cb30-d373-4b16-b6a2-c68b740e4bce
curl -X DELETE http://admin:admin@localhost:3001/api/dashboards/uid/3a3e7834-d926-4561-ba82-c30533cbc4b8
curl -X DELETE http://admin:admin@localhost:3001/api/dashboards/uid/7376ae1a-60d2-4222-bddd-4f244d201a02
curl -X DELETE http://admin:admin@localhost:3001/api/dashboards/uid/b0a5f911-769b-4f9f-bf8e-d34ae99b24b8
curl -X DELETE http://admin:admin@localhost:3001/api/dashboards/uid/6119f9fb-c778-455c-ae3a-2a95a66e5d9b
LOW ISSUE #6 — Logs, Traces & Profiles Not Configured
What's happening
Logs (Loki): No Loki datasource — the Logs Drilldown shows the onboarding screen

Traces: Jaeger is connected as a datasource but the Traces Drilldown app doesn't auto-select it — shows no data

Profiles (Pyroscope): No Pyroscope datasource configured

Fix — Logs (Loki)
Add Loki to your Docker Compose and provision it as a datasource:

text
# docker-compose.yml
loki:
  image: grafana/loki:latest
  container_name: loki
  ports:
    - "3100:3100"
  restart: unless-stopped
text
# grafana/provisioning/datasources/loki.yml
apiVersion: 1
datasources:
  - name: Loki
    type: loki
    url: http://loki:3100
    access: proxy
Fix — Traces (Jaeger already running)
The Jaeger datasource exists but isn't being selected in the Traces drilldown. In Grafana UI:

Go to Connections → Data Sources → Jaeger

Verify the URL is http://jaeger:16686

The Traces drilldown should then auto-detect it

Fix — Profiles (optional)
Only needed if you want profiling. Add Pyroscope to Docker Compose:

text
pyroscope:
  image: grafana/pyroscope:latest
  ports:
    - "4040:4040"
LOW ISSUE #7 — devops-engineer Scrape Duration Elevated
What's happening
devops-engineer:8006 takes 33ms to scrape vs 5–16ms for all other agents. Not critical, but worth watching — if it grows to hundreds of ms it may indicate that agent is doing expensive work on the /metrics endpoint.

Fix
No immediate action needed. Monitor it. If it exceeds ~200ms consistently, check if the /metrics handler is doing blocking operations and move metric collection to background.

PRIORITISED FIX CHECKLIST
Priority	Issue	Est. Time	Command/Action
🔴 P0	project-strategist container down	5 min	docker compose restart project-strategist
🔴 P1	cAdvisor + node_exporter missing	15 min	Add to compose + prometheus.yml
🟠 P2	Application metrics not instrumented	Hours	Add prometheus_client to each service
🟠 P3	Heatmap panel error (Event Bus)	10 min	Fix metric or change panel type to time series
🟡 P4	Duplicate dashboards	5 min	Delete root-level copies via API
🟡 P5	Loki (logs) not set up	20 min	Add Loki to compose + datasource provision
🟡 P6	Traces drilldown (Jaeger)	5 min	Select Jaeger datasource in Traces app
🟢 P7	devops-engineer scrape slow	Monitor	No action now
🟢 P8	Pyroscope profiles	Optional	Add to compose if profiling needed
WHAT'S WORKING WELL
Grafana 12.3.3 is fully healthy, DB clean, API responding

Prometheus 3.9.1 has zero TSDB corruption, 2,060 active series, 334 unique metrics

Jaeger datasource is live and returning OK

Prometheus config loaded cleanly, all recording rules evaluating correctly

HyperCode Production Overview is showing live Request Rate (~0.8 RPS) and real P99/P95 latency data

HyperCode Overview has live Average Request Duration data across /agents, /health, /metrics, /status routes

All Prometheus recording rules for latency histograms (p50/p95/p99) are evaluating with health: ok

8 of 9 agents are scraping successfully with low latency (5–33ms)

The core infrastructure is solid — it's mainly a case of getting project-strategist back online, adding cAdvisor/node_exporter for container visibility, and then progressively instrumenting your HyperCode services with the custom metrics your dashboards are expecting.