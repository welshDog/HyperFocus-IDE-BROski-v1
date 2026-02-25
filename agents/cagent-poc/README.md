# Specialized Agent Configuration (cagent)

This directory contains the declarative configuration files for all specialized agents in the HyperCode ecosystem. These agents are now fully integrated into the Docker Compose stack and orchestrated via the central API.

## 📂 Agent Definitions

Each agent is defined in a YAML file:

*   `project-strategist.yaml`: High-level planning and delegation.
*   `system-architect.yaml`: Technical design and standards.
*   `frontend-specialist.yaml`: React/Next.js implementation.
*   `backend-specialist.yaml`: Python/FastAPI implementation.
*   `database-architect.yaml`: SQL/PostgreSQL schema design.
*   `qa-engineer.yaml`: Testing and validation.
*   `devops-engineer.yaml`: CI/CD and system health (Phoenix).
*   `security-engineer.yaml`: Vulnerability scanning and audits.

## 🚀 How It Works

1.  **Configuration**: Each YAML file defines the agent's:
    *   **Role & Description**: What it does.
    *   **Model**: Typically `openai/sonar` or `openai/sonar-reasoning-pro` (Perplexity).
    *   **System Prompt**: Detailed instructions on behavior and stack.
    *   **Tools**: Integration with MCP servers (like `infrastructure`).

2.  **Runtime**:
    *   The `agent_wrapper.py` script loads these YAML files at runtime.
    *   It exposes a FastAPI endpoint for each agent.
    *   The Orchestrator sends tasks to these endpoints.

3.  **Docker Integration**:
    *   In `docker-compose.yml`, each agent service mounts this directory.
    *   Example: `frontend-specialist` runs `python agent_wrapper.py --config frontend-specialist.yaml`.

## 🛠️ Modifying Agents

To change an agent's behavior (e.g., switch its model or update its instructions):

1.  Edit the corresponding `.yaml` file.
2.  Restart the specific agent container:
    ```bash
    docker compose restart frontend-specialist
    ```
    (Replace with the agent service name you modified).

## 🔑 Key Dependencies

*   **Perplexity API Key**: Required for the `sonar` models. Ensure `PERPLEXITY_API_KEY` is set in your root `.env` file.
*   **Infrastructure MCP**: Agents use the `infrastructure` MCP server to interact with Redis/Postgres.
