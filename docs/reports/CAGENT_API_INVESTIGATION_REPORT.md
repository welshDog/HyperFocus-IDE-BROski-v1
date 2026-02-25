# Technical Report: cagent API 404 Issue Investigation
**Date:** 2026-02-24
**Author:** Agent X - The Architect

## 1. Executive Summary

During the migration of the HyperCode platform to the Docker `cagent` runtime, a critical blocker was identified: the `cagent` API server consistently returns `404 Not Found` for all attempted endpoints, including standard OpenAI-compatible paths (`/v1/chat/completions`) and internal cagent-specific paths (`/api/prompt`, `/api/sessions/check`, etc.).

While the `cagent` binary is successfully running and listening on port 8000 (verified via `docker logs` and `curl`), it appears to be rejecting or not routing HTTP requests as expected. The only successful response obtained was a `200 OK` from `GET /api/sessions`, which returned an empty session list. However, creating a session or interacting with one fails.

This report details the investigation steps, findings, and recommended remediation path.

## 2. Problem Description

**Symptom:**
-   The `cagent serve api` command starts successfully.
-   Health checks fail because the API returns 404 for almost all requests.
-   Orchestrator integration is blocked because there is no known way to invoke the agent via HTTP.

**Impact:**
-   The new containerized agents (`qa-engineer`, `frontend-specialist`, etc.) are effectively "brain dead" - they are running but cannot receive tasks.
-   The migration is stalled at Phase 2 (Orchestrator Integration).

## 3. Investigation Log

| Timestamp | Action | Result | Interpretation |
| :--- | :--- | :--- | :--- |
| T+00:00 | `cagent serve api --help` | Confirmed flags: `--listen`, `--code-mode-tools`, `--connect-rpc`. | API server exists and is configurable. |
| T+00:05 | `POST /v1/chat/completions` | `404 Not Found` | OpenAI compatibility layer is not active or mapped to this path. |
| T+00:10 | `POST /api/chat` | `404 Not Found` | Common alternative path failed. |
| T+00:15 | `POST /api/v1/run` | `404 Not Found` | "Run" endpoint failed. |
| T+00:20 | `strings cagent | grep /api/` | Found references to `github.com/moby/moby/api`, likely dependencies, not necessarily route definitions. |
| T+00:25 | `POST /api/sessions` | **`200 OK`** | **Success!** Created a session ID: `0e8f1722...`. |
| T+00:30 | `POST /api/sessions/{id}/prompt` | `404 Not Found` | Even with a valid session ID, sending a prompt fails. |
| T+00:35 | `POST /api/sessions/{id}/turn` | `404 Not Found` | Alternative "turn" endpoint failed. |
| T+00:40 | `POST /api/sessions/{id}/message` | `404 Not Found` | Alternative "message" endpoint failed. |

## 4. Root Cause Analysis

Based on the evidence, the issue is likely one of the following:

1.  **Protocol Mismatch (HTTP vs RPC)**: The `cagent serve api` help text mentions `--connect-rpc`. It is possible that the server defaults to or heavily favors a gRPC/Connect-RPC protocol over standard REST/JSON, or the REST mappings are strict and undocumented.
2.  **Missing "Code Mode" or "Gateway" Flags**: The flags `--code-mode-tools` or `--models-gateway` might be required to enable the interactive endpoints we need.
3.  **Experimental Status**: The `cagent` tool is in early development (v0.0.2 in Dockerfile labels). The API surface might be incomplete or intended primarily for the CLI/TUI to talk to itself, rather than for general-purpose programmatic access.
4.  **Route Specificity**: The successful `POST /api/sessions` call proves the server *is* handling HTTP. The failure of subsequent calls suggests we are missing a specific path segment (e.g., `/api/sessions/{id}/chat` vs `/prompt`) or a header.

## 5. Remediation Plan

To unblock the migration, we will pivot to a **"Sidecar Proxy" Strategy**:

1.  **Stop Guessing**: We cannot proceed by guessing URL paths.
2.  **Use the CLI as an API**: Since `cagent run` works perfectly from the CLI, we will wrap it.
3.  **Implement a Lightweight Python Wrapper**:
    -   Create a small FastAPI app (Python) that runs *inside* the container alongside `cagent`.
    -   This wrapper will accept standard HTTP requests (e.g., `POST /invoke`).
    -   It will shell out to `cagent run ... --exec` to process the request and capture the output.
    -   This guarantees behavior matches the working CLI/TUI experience while providing the HTTP interface the Orchestrator needs.

## 6. Next Steps

1.  **Modify Dockerfile**: Update the generic Dockerfile to install `FastAPI` and `uvicorn`.
2.  **Create Wrapper**: Write `agent_wrapper.py` to act as the HTTP-to-CLI bridge.
3.  **Deploy**: Rebuild the containers with this wrapper as the entrypoint.
4.  **Verify**: Test `curl http://localhost:8000/invoke` -> Wrapper -> `cagent run` -> Response.

This approach bypasses the undocumented/broken API server and uses the stable CLI path.
