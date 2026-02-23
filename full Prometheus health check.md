full Prometheus health check for 127.0.0.1:9090:

✅ Prometheus Core
Field	Value
Version	3.9.1 (built 2026-01-07)
​
Go Version	go1.25.5
Start Time	20:30:09 UTC today (running ~44 minutes)
​
Config reload	Success (last loaded 20:30:16 UTC)
Storage retention	15 days
Corruption count	0 — clean TSDB
Goroutines	58
GOMAXPROCS	4
🔴 Scrape Targets — 1 DOWN
agents — 8 / 9 UP
​
Instance	State	Last Scrape	Duration
coder-agent:8000	✅ UP	~21m ago	13ms
frontend-specialist:8002	✅ UP	~21m ago	16ms
backend-specialist:8003	✅ UP	~21m ago	6ms
database-architect:8004	✅ UP	~21m ago	5ms
qa-engineer:8005	✅ UP	~21m ago	15ms
devops-engineer:8006	✅ UP	~22m ago	33ms
security-engineer:8007	✅ UP	~21m ago	5ms
system-architect:8008	✅ UP	~21m ago	9ms
project-strategist:8001	❌ DOWN	~21m ago	—
Error: dial tcp 172.18.0.12:8001: connect: connection refused — the project-strategist container is not reachable.
​

hypercode-core — 1 / 1 UP ✅
prometheus (self-scrape) — 1 / 1 UP ✅
🚨 Firing Alerts — 1 CRITICAL
InstanceDown — FIRING since 20:30:26 UTC (firing for ~44 minutes)
​

Severity: critical

Instance: project-strategist:8001, job agents

Description: project-strategist:8001 has been down for more than 1 minute
​

✅ All Other Alert Rules — Inactive (Not Firing)
agent_registry_alerts — 6 rules, all INACTIVE
​
Rule	Threshold	Status
HighStreamLatencyP95	p95 > 500ms	Inactive
NoStreamClients	No SSE clients 10m	Inactive
StreamErrorsElevated	Error rate > 0.1/s	Inactive
SseConnectionDrops	No new clients but events flowing	Inactive
SseHighLatency	p99 > 2s	Inactive
Sse404RateHigh	>1% 404s on SSE endpoints	Inactive
hypercode_alerts — 2 inactive
​
Rule	Threshold	Status
HighCpuLoad	CPU > 80% for 5m	Inactive
HighMemoryUsage	Memory > 90% for 5m	Inactive
📊 Recording Rules — All Healthy
agent_registry_recording (5 rules) and hypercode_services_latency (3 rules) — all evaluating successfully, health: ok
​

Recording rules cover:

Agent stream latency histograms (p50/p95/p99)

Agent stream client rate

Agent registry error rate

Memory service latency p95

Key manager latency p95

Event bus latency p95

🗄️ TSDB Status
Metric	Value
Active series	2,060
Label pairs	601
Chunks	4,871
Unique metric names	334
Corruption count	0 ✅
Top series by metric name: http_request_duration_highr_seconds_bucket (198), prometheus_http_request_duration_seconds_bucket (190)
​

Summary of Issues
project-strategist:8001 is DOWN — container is refusing connections. This has been firing as a CRITICAL alert for ~44 minutes. You need to restart or investigate that agent container.

devops-engineer:8006 scrape duration is 33ms — higher than all other agents (5–16ms range), worth keeping an eye on but not critical.

Everything else is healthy — no TSDB corruption, config loads fine, all recording rules are working, and the other 8 agents are scraping cleanly.