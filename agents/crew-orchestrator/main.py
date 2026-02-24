"""
FastAPI Orchestration Layer for HyperCode Agent Crew
Manages communication between 8 specialized agents
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

app = FastAPI(
    title="HyperCode Agent Crew Orchestrator",
    description="Coordinates 8 specialized AI agents for software development",
    version="2.1"
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
                # Handle disconnected clients gracefully
                pass

manager = ConnectionManager()

# Agent service endpoints
AGENTS = {
    "project-strategist": "http://project-strategist:8009",
    "frontend-specialist": "http://frontend-specialist:8002",
    "backend-specialist": "http://backend-specialist:8003",
    "database-architect": "http://database-architect:8004",
    "qa-engineer": "http://qa-engineer:8005",
    "devops-engineer": "http://devops-engineer:8006",
    "security-engineer": "http://security-engineer:8007",
    "system-architect": "http://system-architect:8008",
}

def to_kebab(name: str) -> str:
    name = name.replace("_", "-")
    name = re.sub(r"-+", "-", name)
    return name.lower()

# Request Models
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

class AgentStatus(BaseModel):
    agent: str
    status: str
    current_task: Optional[str]
    last_activity: str


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
        print(f"✅ Connected to Redis at {redis_url}")
    except Exception as e:
        print(f"⚠️ Redis connection failed ({e}). Using In-Memory Mock Redis.")
        redis_client = MockRedis()

    # Start Redis subscription listener in background
    asyncio.create_task(redis_listener())
    print("✅ Agent Crew Orchestrator started")
    for route in app.routes:
        print(f"Route: {route.path} {route.name}")

async def redis_listener():
    """Listens for Redis events and broadcasts to WebSockets"""
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
            # Keep connection alive, maybe receive commands
            data = await websocket.receive_text()
            # Simple echo or command processing
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
        "version": "2.1",
        "agents": list(AGENTS.keys()),
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        await redis_client.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")

@app.post("/plan", response_model=TaskResponse)
async def plan_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """
    Send task to Project Strategist for planning and delegation
    """
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store task in Redis
    await redis_client.hset(
        f"task:{task_id}",
        mapping={
            "description": request.task,
            "status": "planning",
            "created_at": datetime.now().isoformat(),
            "context": json.dumps(request.context or {})
        }
    )
    
    # Broadcast event
    await redis_client.publish("agent_events", json.dumps({
        "type": "task_created",
        "task_id": task_id,
        "description": request.task
    }))
    
    # Send to Project Strategist
    background_tasks.add_task(
        delegate_to_strategist,
        task_id,
        request.task,
        request.context
    )
    
    return TaskResponse(
        task_id=task_id,
        status="planning",
        assigned_agents=["project-strategist"],
        estimated_time="Calculating..."
    )

@app.post("/agent/{agent_name}/execute")
async def execute_agent_task(agent_name: str, message: AgentMessage):
    """
    Direct execution of a specific agent task
    """
    agent_id = to_kebab(agent_name)
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail=f"Agent {agent_name} not found")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AGENTS[agent_id]}/execute",
                json=message.dict(),
                timeout=120.0
            )
            return response.json()
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Agent {agent_name} unreachable: {str(e)}")

@app.post("/workflow/{workflow_type}")
async def start_workflow(workflow_type: str, request: WorkflowRequest):
    """
    Start a predefined workflow (feature, bugfix, refactor)
    """
    workflows = {
        "feature": ["project-strategist", "system-architect", "frontend-specialist", 
                   "backend-specialist", "database-architect", "qa-engineer", "devops-engineer"],
        "bugfix": ["project-strategist", "qa-engineer", "backend-specialist", "frontend-specialist"],
        "refactor": ["system-architect", "backend-specialist", "frontend-specialist", "qa-engineer"],
        "security_audit": ["security-engineer", "backend-specialist", "database-architect"]
    }
    
    if workflow_type not in workflows:
        raise HTTPException(status_code=400, detail=f"Unknown workflow: {workflow_type}")
    
    workflow_id = f"workflow_{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Store workflow
    await redis_client.hset(
        f"workflow:{workflow_id}",
        mapping={
            "type": workflow_type,
            "description": request.description,
            "agents": json.dumps(workflows[workflow_type]),
            "status": "initiated",
            "created_at": datetime.now().isoformat()
        }
    )
    
    # Broadcast event
    await redis_client.publish("agent_events", json.dumps({
        "type": "workflow_started",
        "workflow_id": workflow_id,
        "workflow_type": workflow_type
    }))
    
    return {
        "workflow_id": workflow_id,
        "type": workflow_type,
        "agents": workflows[workflow_type],
        "status": "initiated"
    }

@app.get("/agents/status")
async def get_agents_status():
    """
    Get status of all agents
    """
    statuses = []
    async with httpx.AsyncClient() as client:
        for agent_name, endpoint in AGENTS.items():
            try:
                response = await client.get(f"{endpoint}/status", timeout=5.0)
                statuses.append({
                    "agent": agent_name,
                    "status": "online",
                    "data": response.json()
                })
            except Exception as e:
                statuses.append({
                    "agent": agent_name,
                    "status": "offline",
                    "error": str(e)
                })
    return statuses

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """
    Get status of a specific task
    """
    task_data = await redis_client.hgetall(f"task:{task_id}")
    if not task_data:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task_id,
        **task_data
    }

@app.get("/memory/standards")
async def get_team_standards():
    """
    Retrieve shared Team Memory Standards (Hive Mind)
    """
    try:
        with open("/app/hive_mind/Team_Memory_Standards.md", "r") as f:
            standards = f.read()
        return {"standards": standards}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Team standards not found")

@app.get("/skills")
async def get_agent_skills():
    """
    Retrieve Agent Skills Library
    """
    try:
        with open("/app/hive_mind/Agent_Skills_Library.md", "r") as f:
            skills = f.read()
        return {"skills": skills}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Skills library not found")

# Background task functions
async def delegate_to_strategist(task_id: str, task: str, context: Optional[Dict]):
    """
    Send task to Project Strategist for breakdown and delegation
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{AGENTS['project-strategist']}/plan",
                json={
                    "task_id": task_id,
                    "task": task,
                    "context": context
                },
                timeout=120.0
            )
            
            # Update task status
            await redis_client.hset(
                f"task:{task_id}",
                "status",
                "delegated"
            )
            
            # Store planning result
            await redis_client.hset(
                f"task:{task_id}",
                "plan",
                json.dumps(response.json())
            )
    except Exception as e:
        await redis_client.hset(
            f"task:{task_id}",
            "status",
            f"error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
