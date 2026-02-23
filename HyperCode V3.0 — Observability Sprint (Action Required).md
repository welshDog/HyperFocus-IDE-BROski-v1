Here's the message, ready to send to your dev team / Agent X:

***

**Subject: HyperCode V3.0 — Observability Sprint (Action Required)**

Hey team,

Grafana's AI health check flagged three gaps in our observability stack. Everything else is green — 18 containers healthy, all services online, WebSocket live. This is the last thing standing between us and full production monitoring.

Here's exactly what needs doing, in order:

***

**1. Instrument the agents (do this first — everything else depends on it)**

Add to every agent's `requirements.txt`:
```
prometheus-fastapi-instrumentator>=6.1.0
```

Add these 3 lines to every agent's `main.py`, right after `app = FastAPI()`:
```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

That's it. Those two changes give us request count, latency, error rate, and in-progress requests for every agent automatically. No manual metric writing needed.

***

**2. Add Grafana Alloy to the stack (the collection pipeline)**

Add this to `docker-compose.yml`:
```yaml
alloy:
  image: grafana/alloy:latest
  container_name: hyperswarm-alloy
  ports:
    - "12345:12345"
    - "4317:4317"
    - "4318:4318"
  volumes:
    - ./config/alloy/config.alloy:/etc/alloy/config.alloy
    - /var/run/docker.sock:/var/run/docker.sock:ro
  command: run --server.http.listen-addr=0.0.0.0:12345 /etc/alloy/config.alloy
  networks:
    - hyperswarm-network
```

Create `config/alloy/config.alloy` — this tells Alloy which agents to scrape and where to send the data. Template is already written and ready to drop in. Just update the agent hostnames to match your compose service names.

Once that's running, check the Alloy debug UI at `http://localhost:12345` to confirm it's scraping successfully before moving on.

***

**3. Add alert rules to Prometheus (currently zero coverage)**

Create `config/prometheus/alert_rules.yml` with the following rules as a minimum:

- `AgentDown` — any agent unreachable for more than 1 minute → **critical**
- `CoreAPIDown` — orchestrator unreachable for 30 seconds → **critical**
- `MultipleAgentsDown` — more than 2 agents down simultaneously → **critical**
- `HighErrorRate` — error rate above 1% for 2 minutes → **warning**
- `SlowAPIResponse` — p95 latency above 800ms for 5 minutes → **warning**

Then add this line to `prometheus.yml`:
```yaml
rule_files:
  - /etc/prometheus/alert_rules.yml
```

Restart Prometheus:
```bash
docker compose restart prometheus
```

Verify the rules loaded at `http://localhost:9090/rules`.

***

**4. Import the dashboards (5 minutes once data is flowing)**

In Grafana → Dashboards → New → Import:

- ID `22676` — FastAPI Observability (tailored for our agents)
- ID `193` — Docker container monitoring (all 18 containers)
- Agent Command Centre JSON — custom HyperSwarm dashboard (already written, ready to import)

Set datasource to `prometheus-1` on import for each one.

***

**Estimated time: 50 minutes end to end.**

Do steps 1 → 2 → 3 → 4 in that exact order. Step 1 must be done before anything shows up in dashboards or triggers alerts, so don't skip ahead.

Once complete, re-run the Grafana AI health check. All three warnings should be gone.

All the code for every step above is written and ready. Just ask if you need any of it.

Let's close this out.

***
