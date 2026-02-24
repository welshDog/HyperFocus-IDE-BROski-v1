"""
FastAPI Orchestration Layer for HyperCode Agent Crew
Manages communication between 8 specialized agents

Mission Brief:
You are the HyperFlow Orchestrator. Your goal is to coordinate 8 specialized AI agents 
to build software efficiently. You must enforce strict naming conventions (kebab-case), 
manage workflows via /hyperrun, and ensure robust error handling.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import redis.asyncio as redis
import httpx
import os
import json
import asyncio
from datetime import datetime
import re
import logging

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("orchestrator")

app = FastAPI(
    title="HyperCode Agent Crew Orchestrator",
    description="Coordinates 8 specialized AI agents for software development. Enforces kebab-case naming and manages /hyperrun workflows.",
    version="2.3"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection for agent communication
redis_client = None

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

manager = ConnectionManager()

# Agent service endpoints - STRICTLY KEBAB-CASE
# Corrected internal ports based on docker-compose.yml
AGENTS = {
    "project-strategist": "http://project-strategist:8009",
    "frontend-specialist": "http://frontend-specialist:8000",
    "backend-specialist": "http://backend-specialist:8000",
    "database-architect": "http://database-architect:8004",
    "qa-engineer": "http://qa-engineer:8000",
    "devops-engineer": "http://devops-engineer:8000",
    "security-engineer": "http://security-engineer:8007",
    "system-architect": "http://system-architect:8008",
}

def to_kebab(name: str) -> str:
    """Normalize agent names to kebab-case"""
    # Replace underscores with hyphens
    name = name.replace("_", "-")
    # Replace spaces with hyphens
    name = name.replace(" ", "-")
    # Collapse multiple hyphens
    name = re.sub(r"-+", "-", name)
    # Lowercase
    return name.lower().strip("-")

# Request Models
class HyperRunRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = {}

class TaskRequest(BaseModel):
    task: str
    context: Optional[Dict[str, Any]] = None
    priority: str = "normal"
    files: Optional[List[str]] = None

class AgentMessage(BaseModel):
    agent: str
    message: str
    context: Optional[Dict[str, Any]] = None

class WorkflowRequest(BaseModel):
    workflow_type: str  # "feature", "bugfix", "refactor"
    description: str
    requirements: Optional[Dict[str, Any]] = None

# Response Models
class TaskResponse(BaseModel):
    task_id: str
    status: str
    assigned_agents: List[str]
    estimated_time: str

class MockRedis:
    def __init__(self):
        self.data = {}
        self.pubsub_channels = {}

    async def hset(self, name, mapping=None, **kwargs):
        if name not in self.data:
            self.data[name] = {}
        if mapping:
            self.data[name].update(mapping)
        self.data[name].update(kwargs)
        return len(kwargs)

    async def hgetall(self, name):
        return self.data.get(name, {})

    async def publish(self, channel, message):
        if channel in self.pubsub_channels:
            for queue in self.pubsub_channels[channel]:
                await queue.put({"type": "message", "data": message})
        return 1

    def pubsub(self):
        return MockPubSub(self)

    async def close(self):
        pass

    async def ping(self):
        return True

class MockPubSub:
    def __init__(self, redis):
        self.redis = redis
        self.queue = asyncio.Queue()

    async def subscribe(self, channel):
        if channel not in self.redis.pubsub_channels:
            self.redis.pubsub_channels[channel] = []
        self.redis.pubsub_channels[channel].append(self.queue)

    async def listen(self):
        while True:
            yield await self.queue.get()

@app.on_event("startup")
async def startup():
    global redis_client
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    try:
        redis_client = await redis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info(f"✅ Connected to Redis at {redis_url}")
    except Exception as e:
        logger.warning(f"⚠️ Redis connection failed ({e}). Using In-Memory Mock Redis.")
        redis_client = MockRedis()

    asyncio.create_task(redis_listener())
    logger.info("✅ Agent Crew Orchestrator started")

async def redis_listener():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe("agent_events")
    async for message in pubsub.listen():
        if message["type"] == "message":
            await manager.broadcast(message["data"])

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.on_event("shutdown")
async def shutdown():
    if redis_client:
        await redis_client.close()

@app.get("/")
async def root():
    return {
        "service": "HyperCode Agent Crew Orchestrator",
        "version": "2.3",
        "agents": list(AGENTS.keys()),
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """System Health Check"""
    try:
        await redis_client.ping()
        return {"status": "healthy", "redis": "connected", "agents_configured": len(AGENTS)}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")

@app.get("/agents/status")
async def get_agents_status():
    """
    Get status of all agents.
    Returns 200 OK with list of agent statuses.
    """
    statuses = []
    async with httpx.AsyncClient() as client:
        for agent_name, endpoint in AGENTS.items():
            try:
                # Attempt to call the agent's health/status endpoint
                # Short timeout to avoid blocking
                response = await client.get(f"{endpoint}/health", timeout=2.0)
                if response.status_code == 200:
                    statuses.append({"agent": agent_name, "status": "online", "details": response.json()})
                else:
                    statuses.append({"agent": agent_name, "status": "degraded", "code": response.status_code})
            except Exception as e:
                statuses.append({
                    "agent": agent_name,
                    "status": "offline",
                    "error": str(e)
                })
    return {"agents": statuses}

@app.post("/hyperrun")
async def hyperrun_workflow(request: HyperRunRequest):
    """
    Primary workflow execution endpoint.
    Analyzes task, selects agents, and orchestrates execution.
    """
    workflow_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Simple heuristic for agent selection based on keywords
    selected_agents = []
    task_lower = request.task.lower()
    
    if "frontend" in task_lower or "ui" in task_lower or "react" in task_lower:
        selected_agents.append("frontend-specialist")
    if "backend" in task_lower or "api" in task_lower or "python" in task_lower:
        selected_agents.append("backend-specialist")
    if "database" in task_lower or "sql" in task_lower:
        selected_agents.append("database-architect")
    if "test" in task_lower or "qa" in task_lower:
        selected_agents.append("qa-engineer")
        
    # Default to project-strategist if no specific domain detected, or as the lead
    if not selected_agents:
        selected_agents.append("project-strategist")
    elif "project-strategist" not in selected_agents:
        selected_agents.insert(0, "project-strategist") # Always lead with strategist

    results = []
    
    # In a real scenario, this would likely be async/parallel or sequential depending on dependency
    # For this implementation, we will try to trigger them
    
    # Use execute_agent_task logic internally or duplicate robust logic here
    # Ideally, we call a helper function.
    
    for agent in selected_agents:
        try:
            # Construct message for the agent
            message = AgentMessage(
                agent=agent,
                message=request.task,
                context={
                    "task_id": workflow_id,
                    **request.context
                }
            )
            # Call the robust execution function
            # We need to await it
            response_data = await execute_agent_task_internal(agent, message)
            results.append({
                "agent": agent,
                "status": "success",
                "data": response_data
            })
        except Exception as e:
             logger.error(f"Workflow step failed for {agent}: {e}")
             results.append({
                "agent": agent,
                "status": "failed",
                "error": str(e)
            })

    return {
        "workflow_id": workflow_id,
        "status": "executed",
        "results": results
    }

async def execute_agent_task_internal(agent_name: str, message: AgentMessage) -> Dict:
    """
    Internal function to execute agent task with robust error handling and retries.
    """
    # 1. Normalize
    agent_id = to_kebab(agent_name)
    
    # 2. Validate
    if agent_id not in AGENTS:
        logger.error(f"Invalid agent name: {agent_name} (normalized: {agent_id})")
        raise HTTPException(status_code=404, detail=f"Agent '{agent_name}' (normalized: '{agent_id}') not found")
    
    endpoint_url = f"{AGENTS[agent_id]}/execute"
    
    # Construct Universal Payload to satisfy both BaseAgent and cagent-poc
    # BaseAgent expects: task_id, task, context
    # cagent-poc expects: message, context, (optional agent)
    
    # Extract context and ensure task_id is present
    context = message.context or {}
    task_id = context.get("task_id", "unknown_task_id")
    
    payload = {
        "agent": agent_id,
        "task_id": task_id,        # Required by BaseAgent
        "task": message.message,   # Required by BaseAgent
        "message": message.message, # Required by cagent-poc
        "context": context
    }
    
    # Retry configuration
    max_retries = 3
    base_delay = 1.0
    
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries + 1):
            try:
                logger.info(f"Invoking {agent_id} at {endpoint_url} (Attempt {attempt+1}/{max_retries+1})")
                
                response = await client.post(
                    endpoint_url,
                    json=payload,
                    timeout=60.0
                )
                
                # Check for HTTP errors
                if response.status_code >= 400:
                    # Log detailed error info
                    logger.error(
                        f"Agent {agent_id} returned error {response.status_code}\n"
                        f"URL: {endpoint_url}\n"
                        f"Response: {response.text}\n"
                        f"Headers: {response.headers}"
                    )
                    
                    # 4xx errors are likely permanent (bad request), so we might not want to retry unless it's 429 or 408
                    if response.status_code < 500 and response.status_code not in [408, 429]:
                        response.raise_for_status()
                    
                    # If 5xx or rate limit, raise to trigger retry logic
                    response.raise_for_status()
                
                # Success
                return response.json()
                
            except httpx.HTTPStatusError as e:
                # Decide whether to retry
                if e.response.status_code < 500 and e.response.status_code not in [408, 429]:
                    # Permanent error, re-raise immediately
                    raise HTTPException(status_code=e.response.status_code, detail=f"Agent error: {e.response.text}")
                
                if attempt == max_retries:
                    logger.error(f"Max retries reached for {agent_id}. Last error: {e}")
                    raise HTTPException(status_code=503, detail=f"Agent {agent_id} unavailable after retries: {str(e)}")
                
            except (httpx.RequestError, httpx.TimeoutException) as e:
                # Network level errors
                logger.warning(f"Connection attempt failed for {agent_id}: {e}")
                if attempt == max_retries:
                    logger.error(f"Max retries reached for {agent_id} (Network Error).")
                    raise HTTPException(status_code=503, detail=f"Agent {agent_id} unreachable: {str(e)}")
            
            # Exponential backoff
            delay = base_delay * (2 ** attempt)
            logger.info(f"Retrying in {delay}s...")
            await asyncio.sleep(delay)

@app.post("/agent/{agent_name}/execute")
async def execute_agent_task(agent_name: str, message: AgentMessage):
    """
    Direct execution of a specific agent task with normalization.
    """
    return await execute_agent_task_internal(agent_name, message)

# Keep existing endpoints for backward compatibility / other tests

@app.post("/plan", response_model=TaskResponse)
async def plan_task(request: TaskRequest, background_tasks: BackgroundTasks):
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    await redis_client.hset(
        f"task:{task_id}",
        mapping={
            "description": request.task,
            "status": "planning",
            "created_at": datetime.now().isoformat(),
            "context": json.dumps(request.context or {})
        }
    )
    background_tasks.add_task(delegate_to_strategist, task_id, request.task, request.context)
    return TaskResponse(
        task_id=task_id,
        status="planning",
        assigned_agents=["project-strategist"],
        estimated_time="Calculating..."
    )

async def delegate_to_strategist(task_id: str, task: str, context: Optional[Dict]):
    try:
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{AGENTS['project-strategist']}/plan",
                json={"task_id": task_id, "task": task, "context": context},
                timeout=120.0
            )
    except Exception as e:
        logger.error(f"Failed to delegate to strategist: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
