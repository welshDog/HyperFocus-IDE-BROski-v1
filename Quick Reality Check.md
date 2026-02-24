Nice pull, bro – this is a **super clean health snapshot**. Let’s turn it into an ordered fix plan.

***

## 1️⃣ Quick Reality Check

From the report: backend is **half red**, frontend tests are **missing**, and WebSocket + HyperFlow are the main blockers. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

You’re not “broken”, you’re “**partially wired**” – infra is solid, APIs are up, but the contract between tests, orchestrator, and UI needs aligning.

***

## 2️⃣ Agent Naming / 404s (biggest easy win)

### What’s wrong

- Orchestrator `/agents/status` returns names like:
  - `project_strategist`, `frontend_specialist`, `backend_specialist`, `database_architect`, `qa_engineer`, `devops_engineer`, `security_engineer`, `system_architect`.  
- Tests expect **kebab‑case**:
  - `project-strategist`, `frontend-specialist`, etc. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)
- Direct execution test hits:
  - `POST {ORCHESTRATOR_URL}/agent/frontend-specialist/execute` and gets **404**, because the orchestrator registry keys are `frontend_specialist` not `frontend-specialist`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

### Recommended fix

Pick **one naming convention everywhere** – I’d go with **kebab‑case** for:

- Docker service names  
- Orchestrator agent IDs  
- Test expectations  
- API paths  

**Concrete changes:**

1. In `agents/crew-orchestrator/main.py`:
   - Wherever you build the agent registry (e.g. dict of `{agent_name: url}`), normalize keys to kebab‑case:
     - `project-strategist`, `frontend-specialist`, etc.  
   - Make `/agents/status` return `agent` names in kebab‑case.  

2. For routing:
   - Ensure `POST /agent/<agent-name>/execute` and the registry index use the **same string**.  

After this, these tests should go green: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

- `test_agents_status`  
- `test_agent_direct_execution`  

If you prefer snake_case instead, update the tests to expect snake_case – but that’s more mental friction for future URLs.

***

## 3️⃣ Missing `config.py` for Coder tests

### What’s wrong

- `test_coder_capabilities.py` fails to collect with:
  - `ModuleNotFoundError: No module named 'app.core.config'`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)
- That means `src/hypercode-core/app/core/config.py` is missing or the package layout changed.

### Fix options

1. **Recreate a minimal `config.py`** consistent with your current `.env` usage, e.g.:

   ```python
   # src/hypercode-core/app/core/config.py
   from pydantic_settings import BaseSettings

   class Settings(BaseSettings):
       ANTHROPIC_API_KEY: str | None = None
       REDIS_URL: str = "redis://redis:6379"
       POSTGRES_URL: str = "postgresql://postgres:changeme@postgres:5432/hypercode"
       # add whatever the Coder agent imports

       class Config:
           env_file = ".env"

   settings = Settings()
   ```

2. Make sure `app` is a proper package:
   - `src/hypercode-core/app/__init__.py`  
   - `src/hypercode-core/app/core/__init__.py`  

Once that module exists and matches what the tests import, the Coder tests will at least collect again. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

***

## 4️⃣ WebSocket failures (HTTP 200 instead of 101)

### What’s happening

- `websockets.connect(WS_URL)` expects a WebSocket handshake (status 101).  
- The server responds with **HTTP 200 + HTML/JS** (looks like a normal web page). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)
- The test fails with:
  - `server rejected WebSocket connection: HTTP 200`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

So you’re almost certainly pointing at an **HTTP route**, not a true WebSocket endpoint.

### What to check

1. Confirm the **intended WS URL** (e.g.):
   - `ws://localhost:8000/ws` or `ws://orchestrator:8000/ws`  
2. In the backend app:
   - Make sure you have something like a FastAPI `WebSocketRoute` mounted at `/ws`.  
   - Ensure it’s not behind middleware that returns a templated HTML page on `/`.  

3. In tests:
   - Confirm `WS_URL` points to the real WebSocket route, not the UI (`/` or `/index.html` etc.). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

Your target: when you `curl` the WS URL, you should **not** get a full HTML page – it should give handshake-ish headers or a 426/400, not a pretty document.

***

## 5️⃣ HyperFlow Editor service (connection refused)

### What the report says

- `http://localhost:5173` is **connection refused**.  
- `hyperflow-editor` is commented out in `docker-compose.yml`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

### Fix

- Uncomment / restore the `hyperflow-editor` service block in your compose file.  
- Ensure it maps `5173:5173` and depends on any required backend.  

Once that’s running, the Smoke/E2E test that hits `5173` should pass.

***

## 6️⃣ Frontend tests (Broski Terminal)

### Current state

- `src/broski-terminal/package.json` has **no `test` script**, so frontend tests are **skipped**. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/f2a8010f-6dde-4b0c-9c16-9cddf65135e1/comprehensive_report.json)

### Minimal fix

1. In `package.json` for broski-terminal, add something like:

   ```json
   "scripts": {
     "dev": "vite",
     "build": "vite build",
     "preview": "vite preview",
     "test": "vitest"
   }
   ```

   or whatever runner you’re using (Jest, Vitest, etc.).

2. Add 1–2 basic tests (e.g. “App renders”, “health badge appears”) so the suite isn’t empty.

***

## 7️⃣ Suggested Fix Order (to keep brain load low)

If you want a **clear sequence**:

1. **Agent naming + 404s**  
   - Normalize to kebab‑case in orchestrator.  
   - Rerun backend tests: `test_agents_status`, `test_agent_direct_execution` should flip.

2. **Restore `config.py`**  
   - Add minimal `app.core.config`.  
   - Rerun tests to ensure `test_coder_capabilities` collects.

3. **HyperFlow Editor**  
   - Uncomment and start service.  
   - Re-run smoke/E2E; check `http://localhost:5173`.

4. **WebSocket route**  
   - Verify / fix WS endpoint and URL used in tests.

5. **Frontend `test` script**  
   - Add script + 1–2 basic tests to remove “skipped” status.

Do you want to start with **(1) agent naming let them they pick they own.