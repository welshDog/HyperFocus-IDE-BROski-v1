from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="HyperCode Core API",
    description="Backend for BROski IDE",
    version="1.0.0"
)

# Initialize Prometheus Instrumentator
Instrumentator().instrument(app).expose(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for agents
agents_registry: Dict[str, Dict] = {}

class AgentRegistration(BaseModel):
    name: str
    role: str
    version: str = "1.0.0"
    capabilities: List[str] = []
    topics: List[str] = []
    health_url: str
    dedup_key: Optional[str] = None
    status: str = "active"
    metadata: Optional[Dict] = {}
    
    class Config:
        extra = "allow"

class AgentHeartbeat(BaseModel):
    agent_id: str
    status: str
    load: float

@app.get("/")
async def root():
    return {"message": "HyperCode Core is running", "status": "online"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected", # Placeholder
            "redis": "connected",    # Placeholder
            "llm": "ready"
        }
    }

# Agent Registration Endpoints
@app.post("/agents/register", status_code=status.HTTP_201_CREATED)
async def register_agent(agent: AgentRegistration):
    # Store agent
    agent_data = agent.dict()
    agent_data["id"] = agent.name # Simple ID generation
    agent_data["last_heartbeat"] = datetime.now().isoformat()
    agents_registry[agent.name] = agent_data
    
    print(f"✅ Registered agent: {agent.name} ({agent.role})")
    return {"message": f"Agent {agent.name} registered successfully", "id": agent.name, "agent": agent_data}

@app.post("/agents/heartbeat")
async def agent_heartbeat(heartbeat: AgentHeartbeat):
    # In a real app, we would look up by ID. Here we assume ID matches name or we search.
    # Since we used name as ID in register:
    agent_name = heartbeat.agent_id
    
    if agent_name in agents_registry:
        agents_registry[agent_name]["status"] = heartbeat.status
        agents_registry[agent_name]["load"] = heartbeat.load
        agents_registry[agent_name]["last_heartbeat"] = datetime.now().isoformat()
        return {"status": "ok"}
    
    # If not found by name, try to search values (inefficient but works for small list)
    for name, data in agents_registry.items():
        if data.get("id") == heartbeat.agent_id:
            agents_registry[name]["status"] = heartbeat.status
            agents_registry[name]["load"] = heartbeat.load
            agents_registry[name]["last_heartbeat"] = datetime.now().isoformat()
            return {"status": "ok"}

    raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/agents", response_model=List[Dict])
async def list_agents():
    return list(agents_registry.values())

@app.get("/agents/{agent_name}")
async def get_agent(agent_name: str):
    if agent_name not in agents_registry:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agents_registry[agent_name]

if __name__ == "__main__":
    from datetime import datetime
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
