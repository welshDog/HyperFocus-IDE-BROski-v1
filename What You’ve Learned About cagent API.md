Bro. This investigation is **spot on** and the sidecar plan is the right call. 🧠⚙️  

Here’s the minimal, actionable summary + what to build next.

***

## 1️⃣ What You’ve Learned About `cagent` API

From your report: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)

- `cagent serve api` starts, listens on port 8000, and responds to HTTP.  
- Standard OpenAI-style paths like `/v1/chat/completions`, `/api/chat`, `/api/v1/run` all return **404**.  
- The only working call you found is `POST /api/sessions` → **200 OK + session id**.  
- Any attempt to interact with that session (`/api/sessions/{id}/prompt`, `/turn`, `/message`) still returns **404**.  
- Help flags mention `--connect-rpc`, suggesting it’s built around **RPC/gRPC / Connect** and the HTTP mappings are either:
  - incomplete,  
  - undocumented, or  
  - meant only for an internal UI/CLI.  

Conclusion: **you cannot reliably treat `cagent serve api` as a public HTTP/REST API right now.** The CLI path (`cagent run ...`) is the stable, supported behavior. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)

***

## 2️⃣ Sidecar Proxy Strategy (the right pivot)

Your remediation plan is exactly what I’d recommend: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)

- **Stop guessing routes** – you already tried the obvious candidates and confirmed 404s.  
- **Use the CLI as the truth**: `cagent run` works, is battle-tested, and matches the intended UX.  
- Wrap it with a **tiny FastAPI HTTP service** inside each agent container:

High level flow:

1. Orchestrator → `POST /invoke` on the agent container.  
2. FastAPI handler receives JSON: messages, context, etc.  
3. Handler shells out to `cagent run ...` (with the right config/env) using `subprocess`.  
4. Captures stdout, parses if needed, returns a clean JSON response.  

This gives you:

- A stable **HTTP surface** for the orchestrator.  
- No dependency on undocumented `cagent serve api` routes.  
- Behavior that always matches what your CLI workflows already do.

***

## 3️⃣ Concrete Next Steps (build list)

From your own plan, turned into a to‑do checklist: [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)

1. **Dockerfile update**
   - In the generic agent Dockerfile, add:
     - `fastapi`, `uvicorn[standard]` (or similar) to the image.  
   - Set the container entrypoint to something like:
     ```bash
     uvicorn agent_wrapper:app --host 0.0.0.0 --port 8000
     ```
   - Ensure `cagent` binary + configs for that agent are still present in the image.

2. **`agent_wrapper.py` (FastAPI sidecar)**  
   Minimal skeleton:

   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel
   import subprocess
   import json

   app = FastAPI()

   class InvokeRequest(BaseModel):
       messages: list  # or your own schema
       # add fields like tools, system_prompt, etc.

   @app.post("/invoke")
   def invoke(req: InvokeRequest):
       # Build CLI command
       # Example: cagent run --config /agents/qa-engineer.yaml --exec ...
       cmd = [
           "cagent",
           "run",
           "--config", "/agents/agent.yaml",
           "--exec",  # if needed
       ]

       # You can pass the prompt via stdin or an env var/file
       proc = subprocess.run(
           cmd,
           input=json.dumps(req.dict()).encode("utf-8"),
           stdout=subprocess.PIPE,
           stderr=subprocess.PIPE,
       )

       if proc.returncode != 0:
           return {
               "status": "error",
               "stderr": proc.stderr.decode("utf-8"),
           }

       # Adjust this depending on cagent output format
       return {
           "status": "ok",
           "output": proc.stdout.decode("utf-8"),
       }
   ```

   You’ll refine:
   - How you pass the prompt (stdin vs file vs args).  
   - How you parse the output (JSON vs plain text).  

3. **Health endpoint in the wrapper**
   - Add a `/health` route that:
     - Optionally runs a very fast `cagent` sanity check OR  
     - Just returns 200 if the process is available and config is readable.  
   - Use this for your Docker + orchestrator healthchecks instead of hitting unknown `cagent` API paths.

4. **Rebuild & test one agent**
   - Start with `qa-engineer`:
     - Rebuild image.  
     - `curl http://qa-engineer:8000/health` → expect 200.  
     - `curl -X POST http://qa-engineer:8000/invoke -d '{...}'` → verify you get real answers via `cagent run`.  

5. **Wire orchestrator**
   - In `crew-orchestrator`, replace calls to the old FastAPI agents with:
     - `POST http://<agent-name>:8000/invoke` using your chosen JSON schema.  

***

## 4️⃣ TL;DR Answer to “Investigate cagent API”

- You’ve already done a **thorough investigation**: `cagent serve api` is not offering a usable, documented HTTP surface beyond `/api/sessions`, and attempts to use it to send prompts all 404. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)
- The safest, production-ready move is exactly what you outlined:
  - **Treat cagent as a CLI-only core**  
  - Add a **FastAPI sidecar** per agent that exposes `/invoke` and `/health` and shells out to `cagent run`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/107547080/b3547871-4ee1-46c2-b9a3-a50d343cbdab/CAGENT_API_INVESTIGATION_REPORT.md)

If you want, next step I can do is:

- Help you design the **exact JSON schema** for `/invoke` and  
- Sketch the **precise orchestrator call pattern** for one agent (e.g. `qa-engineer`) so you have a copy-paste template for the rest.