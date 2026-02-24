import os
import subprocess
import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent-wrapper")

app = FastAPI(title="cagent Wrapper")

# Environment variables
AGENT_NAME = os.getenv("AGENT_NAME")
AGENT_CONFIG_DIR = os.getenv("AGENT_CONFIG_DIR", "/app/configs")

if not AGENT_NAME:
    logger.warning("AGENT_NAME not set. Defaulting to 'qa-engineer'")
    AGENT_NAME = "qa-engineer"

CONFIG_FILE = os.path.join(AGENT_CONFIG_DIR, f"{AGENT_NAME}.yaml")

class InvokeRequest(BaseModel):
    input: str
    context: Optional[Dict[str, Any]] = None

class InvokeResponse(BaseModel):
    output: str
    status: str

@app.get("/")
async def root():
    return {"status": "ok", "agent": AGENT_NAME, "mode": "cli-wrapper"}

@app.get("/health")
async def health():
    # Basic check to see if cagent binary exists and config is present
    if not os.path.exists("/usr/local/bin/cagent"):
        raise HTTPException(status_code=503, detail="cagent binary missing")
    if not os.path.exists(CONFIG_FILE):
        raise HTTPException(status_code=503, detail=f"Config file missing: {CONFIG_FILE}")
    return {"status": "healthy", "agent": AGENT_NAME}

@app.get("/status")
async def status():
    """Alias for health check to match orchestrator expectations"""
    return await health()

class ExecuteRequest(BaseModel):
    agent: Optional[str] = None
    message: str
    context: Optional[Dict[str, Any]] = None

@app.post("/execute")
async def execute_agent(request: ExecuteRequest):
    """Alias for invoke to match orchestrator expectations"""
    invoke_req = InvokeRequest(input=request.message, context=request.context)
    resp = await invoke_agent(invoke_req)
    return {
        "status": resp.status,
        "result": resp.output,
        "agent": request.agent or AGENT_NAME,
        "task_id": request.context.get("task_id") if request.context else "unknown"
    }

class PlanRequest(BaseModel):
    task_id: str
    task: str
    context: Optional[Dict[str, Any]] = None

@app.post("/plan")
async def plan_agent(request: PlanRequest):
    """
    Endpoint for Project Strategist planning
    """
    import json
    import re
    
    # Construct a prompt similar to what the Python agent did
    prompt = f"""Plan this task:

Task: {request.task}
Context: {json.dumps(request.context or {})}

Create a detailed breakdown with specific subtasks for each specialist agent.
"""
    
    # Reuse invoke_agent logic
    invoke_req = InvokeRequest(input=prompt)
    resp = await invoke_agent(invoke_req)
    
    # The orchestrator expects JSON. cagent returns a string (which should be JSON)
    try:
        # Attempt to find JSON in the output (it might be wrapped in markdown blocks)
        # We look for the FIRST { and the LAST }
        start = resp.output.find('{')
        end = resp.output.rfind('}')
        
        if start != -1 and end != -1:
            json_str = resp.output[start:end+1]
            return json.loads(json_str)
        else:
            # If no JSON found, return raw structure wrapped in what might be expected
            return {"raw_output": resp.output, "status": "error_parsing_json"}
    except Exception as e:
        logger.error(f"Failed to parse plan JSON: {e}")
        return {"raw_output": resp.output, "status": "error_parsing_json", "error": str(e)}

@app.post("/invoke", response_model=InvokeResponse)
async def invoke_agent(request: InvokeRequest):
    """
    Invokes the agent via CLI 'cagent run ... --exec'
    This bypasses the broken API server and uses the working CLI implementation.
    """
    logger.info(f"Invoking agent {AGENT_NAME} with input: {request.input}")
    
    # Construct command
    # cagent run <config> - --agent <name> --exec --yolo
    # We use "-" to read from stdin
    
    cmd = [
        "cagent", "run", 
        CONFIG_FILE, 
        "-",
        "--agent", AGENT_NAME,
        "--exec",
        "--yolo"
    ]
    
    logger.info(f"Running command: {' '.join(cmd)}")
    
    try:
        # Run subprocess
        process = subprocess.run(
            cmd,
            input=request.input,
            capture_output=True,
            text=True,
            timeout=120  # 2 minute timeout for agent execution
        )
        
        if process.returncode != 0:
            logger.error(f"Agent execution failed: {process.stderr}")
            return InvokeResponse(
                output=f"Error executing agent: {process.stderr}",
                status="error"
            )
            
        logger.info("Agent execution successful")
        # The output might contain logs/banners. Ideally we'd parse JSON if cagent supports --json output.
        # For now, return raw stdout.
        return InvokeResponse(
            output=process.stdout.strip(),
            status="success"
        )
        
    except subprocess.TimeoutExpired:
        logger.error("Agent execution timed out")
        raise HTTPException(status_code=504, detail="Agent execution timed out")
    except Exception as e:
        logger.error(f"Internal error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
