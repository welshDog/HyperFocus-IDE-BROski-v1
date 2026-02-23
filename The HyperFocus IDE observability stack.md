BROski♾ — this is a solid observability reference. Here’s a cleaned-up, ready-to-drop-in “official guide” version with a few extra clarifications and future-proof hints.

1. High-Level Architecture
The HyperFocus IDE observability stack runs entirely inside Docker on the hypercode_backend_net network and uses a classic metrics + traces + dashboards pattern.

Prometheus scrapes metrics from hypercode-core and all AI agents over HTTP.

Jaeger receives OTLP traces (and Zipkin if you ever want it) from the app.

Grafana connects to Prometheus and Jaeger as data sources and provides dashboards.

Think: services emit metrics/traces → Prometheus/Jaeger collect → Grafana visualises.

2. Components & Endpoints
A. Grafana – Visualization
Local UI: http://localhost:3001

Internal URL (from other containers): http://grafana:3000

Provisioned datasources config: monitoring/grafana/provisioning/datasources/datasource.yml

Auth (local, dev):

Admin user: WelshDog (GF_SECURITY_ADMIN_USER)

Admin password: WelshDog123! (GF_SECURITY_ADMIN_PASSWORD)

An API key is defined in .env for optional Grafana Cloud use, but the current stack runs fully local.

Provisioned Data Sources:

Prometheus – http://prometheus:9090

Jaeger – http://jaeger:16686

This matches typical Docker observability stacks where Grafana talks to Prometheus and Jaeger by container name on the shared network.

B. Prometheus – Metrics
Local UI: http://localhost:9090 (bound to 127.0.0.1)

Internal URL: http://prometheus:9090

Config file: monitoring/prometheus/prometheus.yml

Scrape targets (internal services):

hypercode-core:8000

coder-agent:8000

frontend-specialist:8002

backend-specialist:8003

database-architect:8004

qa-engineer:8005

devops-engineer:8006

security-engineer:8007

system-architect:8008

project-strategist:8001

Each of these should expose a Prometheus-compatible /metrics endpoint or equivalent, which Prometheus scrapes on a schedule defined in prometheus.yml (e.g. global scrape_interval).

C. Jaeger – Distributed Tracing
Jaeger UI: http://localhost:16686

OTLP gRPC receiver (in Docker): http://jaeger:4317

Zipkin receiver: http://jaeger:9411

App integration:

OTLP_ENDPOINT=http://jaeger:4317

OTLP_EXPORTER_DISABLED=true (tracing currently OFF)

Jaeger’s native OTLP support over port 4317 matches standard Jaeger all‑in‑one setups where COLLECTOR_OTLP_ENABLED=true and port 4317 is exposed.

To actually see traces:

Set OTLP_EXPORTER_DISABLED=false

Ensure the app/agents are using an OTEL SDK or exporter configured to send traces to OTLP_ENDPOINT.

3. Grafana Cloud (Optional Extension)
You already have Grafana Cloud credentials in .env, but they are not wired into the current docker-compose.yml. The stack runs standalone with local Grafana + Prometheus + Jaeger.

Existing Cloud values:

Prometheus remote_write URL:
https://prometheus-prod-55-prod-gb-south-1.grafana.net/api/prom/push

Loki push URL:
https://logs-prod-035.grafana.net/loki/api/v1/push

Metrics instance ID (username): 2960668

Logs instance ID (username): 1476008

To enable metrics push to Grafana Cloud, add a remote_write block to monitoring/prometheus/prometheus.yml, like this pattern:

text
remote_write:
  - url: "https://prometheus-prod-55-prod-gb-south-1.grafana.net/api/prom/push"
    basic_auth:
      username: "2960668"        # your Metrics instance ID
      password: "<GRAFANA_CLOUD_API_KEY>"  # from .env or mounted file
Then restart Prometheus so it picks up the new config and begins sending all scraped samples to Grafana Cloud.

If you later want logs in Cloud, you’d typically:

Add Promtail or Grafana Agent as an extra Docker service.

Configure it to push to the Loki URL with the log instance ID.

4. Validation & Troubleshooting
Quick Validation Flow
Check services are running

bash
docker-compose ps
# grafana, prometheus, jaeger should be "Up"
Grafana login

Open http://localhost:3001

Login: WelshDog / WelshDog123!

Test data sources

In Grafana: Connections > Data sources

Click Prometheus → “Save & Test” → expect: “Data source is working”

Click Jaeger → “Save & Test” → expect: “Data source is working”

Check Prometheus targets

Open: http://localhost:9090/targets

All HyperCode/agent endpoints should be UP; otherwise, scraping is broken.

Common Issues Table
Issue	Likely Cause	Fix
Grafana login fails	Password mismatch vs .env or stale volume	Confirm GF_SECURITY_ADMIN_PASSWORD in .env. If changed, run docker-compose down -v to reset Grafana data and start fresh.
Prometheus targets DOWN	Containers not running, wrong ports, or different Docker network	Ensure all services are on hypercode_backend_net. Check individual service logs, e.g. docker logs coder-agent, and confirm each exposes metrics.
No traces in Jaeger	Tracing disabled or exporter not configured	Set OTLP_EXPORTER_DISABLED=false, confirm OTLP_ENDPOINT=http://jaeger:4317, and ensure the app uses OTEL exporter with traces enabled.
“Connection refused” to 4317	App using localhost instead of Docker service name	In .env, ensure OTLP_ENDPOINT=http://jaeger:4317 (not localhost:4317) so containers talk over the Docker network.
​
Empty dashboards	No requests, or Prometheus isn’t scraping	Generate traffic (use the IDE/agents), then re-check http://localhost:9090/targets and Grafana Prometheus datasource status.
5. Config Parameters Cheat Sheet
Variable	Current Value	Purpose
GF_SECURITY_ADMIN_USER	WelshDog	Grafana admin username
GF_SECURITY_ADMIN_PASSWORD	WelshDog123!	Grafana admin password
OTLP_ENDPOINT	http://jaeger:4317	OTLP endpoint for traces (Jaeger all‑in‑one)
OTLP_EXPORTER_DISABLED	true	Set to false to enable trace export
NEXT_PUBLIC_CORE_URL	http://localhost:8000	Frontend → Core API base URL
If you want, next step we can:

Flip tracing on together (OTLP exporter wiring + a simple “hello trace” test), or

Wire Prometheus → Grafana Cloud and design a first “HyperFocus Health” dashboard.