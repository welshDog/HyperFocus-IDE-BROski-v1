Here's the full Grafana health check report for your local instance at `localhost:3001`:

***

## ✅ Grafana Core
- **Version:** 12.3.3 [localhost](http://localhost:3001/api/health)
- **Database:** OK
- **API:** Responding normally

***

## ✅ Data Sources (both healthy)

| Source | URL | Status |
|---|---|---|
| **Prometheus** (default) | `http://prometheus:9090` | OK — "Successfully queried the Prometheus API" [localhost](http://localhost:3001/api/datasources/uid/prometheus/health) |
| **Jaeger** | `http://jaeger:16686` | OK — "Data source is working" [localhost](http://localhost:3001/api/datasources/uid/jaeger/health) |

Note: Both are marked `readOnly: true` (provisioned via config file). [localhost](http://localhost:3001/api/datasources)

***

## ⚠️ Alerting
- **1 alert rule** configured: *"High CPU Usage (>80%)"* in the **Infrastructure Alerts** folder [localhost](http://localhost:3001/api/prometheus/grafana/api/v1/rules)
- Rule state: **Inactive / Normal (NoData)** — the query returned no data, last evaluated at 21:05 UTC tonight
- This means your containers aren't breaching 80% CPU, but also that cAdvisor metrics aren't coming through (see dashboards below)

***

## 📊 Dashboards — Panel Status

| Dashboard | Panels | Data |
|---|---|---|
| **HyperCode Production Overview** | Request Rate (RPS), Latency P99/P95, Agent Task Throughput | ✅ **Live data on 2 of 3 panels** — request rates ~0.8 RPS, latency spikes visible around 20:30 [localhost](http://localhost:3001/d/hypercode-prod-overview/hypercode-production-overview?orgId=1&from=now-1h&to=now&timezone=Europe%2FLondon&var-datasource=prometheus&refresh=5s) |
| **HyperCode Overview** | CPU Usage, Memory Usage, Average Request Duration | ⚠️ Partial — CPU/Memory are "No data", but **Average Request Duration has live data** across routes (`/agents`, `/health`, `/metrics`, `/status`, etc.) [localhost](http://localhost:3001/d/hypercode-overview/hypercode-overview?orgId=1&from=now-6h&to=now&timezone=Europe%2FLondon&refresh=5s) |
| **Event Bus Latency & Reliability** | Agent Registry SSE Latency (heatmap), Event Bus Reliability, Deduplication Efficiency | ❌ **Panel error** — "no heatmap fields found" on SSE Latency; Deduplication Efficiency shows a warning triangle [localhost](http://localhost:3001/d/event-bus-latency/event-bus-latency-and-reliability?orgId=1&from=now-6h&to=now&timezone=Europe%2FLondon) |
| **HyperCode Agents** | Agent Stream Clients, Agent Stream Latency p95 | ❌ No data [localhost](http://localhost:3001/d/792ecc94-6a1b-41b0-9a79-e3b9e85ce170/hypercode-agents?orgId=1&from=now-6h&to=now&timezone=browser) |
| **HyperCode Execution** | HTTP 5xx Rate, Request Rate, Interpreter Executions, Errors, Duration | ❌ No data [localhost](http://localhost:3001/d/067f9585-2eae-4d06-b5a1-b363d36d5598/hypercode-execution?orgId=1&from=now-6h&to=now&timezone=browser) |
| **Roundtrip Worker Latency** | Latency p95 & p99 | ❌ No data [localhost](http://localhost:3001/d/fdeea99e-c718-458c-a859-d4a405bca7d8/roundtrip-worker-latency?orgId=1&from=now-1h&to=now&timezone=browser) |
| **SSE Agent Registry** | SSE Clients, Latency p50/p95/p99, Registry Errors, Stream Throughput | ❌ No data [localhost](http://localhost:3001/d/dc7a0b88-f95e-434a-a6f7-bbb516198eda/sse-agent-registry?orgId=1&from=now-6h&to=now&timezone=browser) |
| **Voice Coding Observability** | STT Latency, STT Error Rate, Transcription Confidence, Voice WS Connections | ❌ No data [localhost](http://localhost:3001/d/b89990f7-a8fc-43f4-aba0-bb4aefa54e2b/voice-coding-observability?orgId=1&from=now-6h&to=now&timezone=browser) |
| **HyperCode AI & Memory Intelligence** | LLM Request Latency, LLM Request Rate, Memory Service Latency, Memory Ops Rate | ❌ No data [localhost](http://localhost:3001/d/hypercode-ai/hypercode-ai-and-memory-intelligence?orgId=1&from=now-1h&to=now&timezone=Europe%2FLondon) |

**Duplicate dashboards detected:** Every dashboard exists twice — once at root level (no folder) and once inside the HyperCode folder. This is likely from being provisioned twice. [localhost](http://localhost:3001/api/search?type=dash-db)

***

## 🔍 Drilldown Views

| View | Status |
|---|---|
| **Metrics** | ✅ Working — **334 Prometheus metrics** visible with live mini-graphs [localhost](http://localhost:3001/a/grafana-metricsdrilldown-app/drilldown?from=now-1h&to=now&timezone=Europe%2FLondon&var-metrics_filters=&var-filters=&var-labelsWingman=%28none%29&layout=grid&filters-rule=&filters-prefix=&filters-suffix=&search_txt=&var-metrics-reducer-sort-by=default&filters-recent=&var-ds=prometheus&var-other_metric_filters=) |
| **Logs** | ❌ **No Loki datasource configured** — needs Loki added to see logs [localhost](http://localhost:3001/a/grafana-lokiexplore-app/explore?patterns=%5B%5D&from=now-15m&to=now&timezone=Europe%2FLondon&var-lineFormat=&var-ds=&var-filters=&var-fields=&var-levels=&var-metadata=&var-jsonFields=&var-all-fields=&var-patterns=&var-lineFilterV2=&var-lineFilters=) |
| **Traces** | ⚠️ **No Tempo/Jaeger datasource selected** in the Traces drilldown (Jaeger is available as a datasource but not auto-selected); no trace data visible [localhost](http://localhost:3001/a/grafana-exploretraces-app/explore?from=now-30m&to=now&timezone=Europe%2FLondon&var-ds=&var-primarySignal=nestedSetParent%3C0&var-filters=&var-metric=rate&var-groupBy=resource.service.name&var-spanListColumns=&var-latencyThreshold=&var-partialLatencyThreshold=&var-durationPercentiles=0.9&actionView=breakdown) |
| **Profiles** | ❌ **No Pyroscope datasource configured** — shows onboarding screen [localhost](http://localhost:3001/a/grafana-pyroscope-app/explore) |

***

## Summary of Issues to Address

1. **cAdvisor metrics missing** — CPU/Memory panels across multiple dashboards return no data. cAdvisor may not be running or not scraping correctly in Prometheus.
2. **Application metrics not flowing** — Most HyperCode-specific metrics (agent streams, interpreter executions, SSE registry, voice STT, LLM) show "No data", suggesting your services either aren't instrumented yet or aren't running/being scraped.
3. **Heatmap panel error** on Event Bus Latency dashboard — the SSE Latency panel needs a histogram-type metric, not the one currently being queried.
4. **No Loki** (logs) or **Pyroscope** (profiles) datasources — add these if you want full observability coverage.
5. **Duplicate dashboards** — clean up the root-level copies that sit outside the HyperCode folder.
6. **Traces drilldown** — Jaeger is connected but needs to be configured as the selected datasource in the Traces app.