Here’s the minimal change set to get you unstuck.

1️⃣ Normalise agent names in the orchestrator
Goal: everywhere externally visible, agents are like project-strategist, frontend-specialist, etc.

In agents/crew-orchestrator/main.py (or wherever you define your agents registry), do two things:

A. Add a small helper
python
import re

def to_kebab(name: str) -> str:
    # handles project_strategist, project-strategist, ProjectStrategist, etc.
    name = name.replace("_", "-")
    # optional: collapse multiple dashes
    name = re.sub(r"-+", "-", name)
    return name.lower()
B. Build your registry with kebab keys
Where you currently have something like (pseudo):

python
AGENTS = {
    "project_strategist": "...",
    "frontend_specialist": "...",
    # ...
}
change it to:

python
_RAW_AGENTS = {
    "project_strategist": "...",
    "frontend_specialist": "...",
    "backend_specialist": "...",
    "database_architect": "...",
    "qa_engineer": "...",
    "devops_engineer": "...",
    "security_engineer": "...",
    "system_architect": "...",
}

AGENTS = {to_kebab(name): cfg for name, cfg in _RAW_AGENTS.items()}
Now AGENTS keys will be:

python
["project-strategist", "frontend-specialist", "backend-specialist",
 "database-architect", "qa-engineer", "devops-engineer",
 "security-engineer", "system-architect"]
which matches what your tests want.
​

2️⃣ Fix /agents/status output
Your test_agents_status expects agent_names to include "project-strategist".
​

Where you build the /agents/status response, make sure you use the kebab-case key, e.g.:

python
@app.get("/agents/status")
async def agents_status():
    result = []
    for agent_id, cfg in AGENTS.items():
        # agent_id is already kebab-case
        result.append({
            "agent": agent_id,
            "status": "online",  # whatever you already compute
            # ... any extra fields
        })
    return result
Then this assertion from the report will pass:
​

python
agent_names = [a["agent"] for a in agents]
assert "project-strategist" in str(agent_names)
3️⃣ Fix direct execution routing (the 404)
test_agent_direct_execution calls:
​

python
POST {ORCHESTRATOR_URL}/agent/frontend-specialist/execute
and expects a non-404.

In your route handler, make sure you resolve agent_name through to_kebab before looking it up:

python
@app.post("/agent/{agent_name}/execute")
async def execute_agent(agent_name: str, payload: AgentRequest):
    agent_id = to_kebab(agent_name)
    if agent_id not in AGENTS:
        raise HTTPException(status_code=404, detail="Unknown agent")

    agent_cfg = AGENTS[agent_id]
    # existing logic to call wrapper / cagent here
Now /agent/frontend-specialist/execute and /agent/frontend_specialist/execute will both map to frontend-specialist internally, so the test gets a 200 or 503, not 404.
​

4️⃣ What to do next (tiny step)
Once you’ve made those three edits:

Save crew-orchestrator changes.

Restart the orchestrator container (or the whole stack if easier).

Re-run just the backend tests:

bash
cd HyperFocus-IDE-BROski-v1
python -m pytest tests/test_agent_crew.py -q
You’re aiming for:

test_agents_status → passes

test_agent_direct_execution → passes or at least no longer 404 (should be 200/503).
​

Send me the new short pytest output for that file only