# HyperCode Setup & Troubleshooting Guide

This guide provides detailed instructions for setting up the HyperCode ecosystem and resolving common issues.

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

1.  **Docker Desktop** (v4.0+)
    *   Windows/Mac: Install via Docker Desktop.
    *   Linux: Install `docker-ce` and `docker-compose-plugin`.
    *   *Verify*: `docker compose version` should return v2.x+.
2.  **Git**
    *   Required for cloning the repository.
3.  **Perplexity API Key**
    *   Required for agent intelligence (Sonar models).
    *   Get one at [docs.perplexity.ai](https://docs.perplexity.ai).

## 🚀 Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/welshDog/HyperCode-V2.0.git
cd HyperCode-V2.0
```

### 2. Configure Environment Variables
Copy the example configuration file:
```bash
cp .env.example .env
```
Open `.env` in a text editor and update the following:
*   `PERPLEXITY_API_KEY`: Paste your `pplx-...` key here.
*   `POSTGRES_PASSWORD`: (Optional) Change the default DB password.

### 3. Start the System
Run the Docker stack in detached mode:
```bash
docker compose up -d
```
*Wait about 30-60 seconds for all services to initialize.*

### 4. Verify Deployment
Check the status of your containers:
```bash
docker compose ps
```
You should see services like `crew-orchestrator`, `hypercode-core`, `broski-terminal`, and various agents listed as `Up (healthy)`.

---

## 🖥️ Access Points

| Service | URL | Description |
| :--- | :--- | :--- |
| **Mission Control** | `http://localhost:3000/dashboard` | Main interface for interacting with agents. |
| **Orchestrator API** | `http://localhost:8080/docs` | Swagger UI for the agent backend. |
| **Grafana** | `http://localhost:3001` | System monitoring dashboards (User/Pass: `admin`). |
| **Prometheus** | `http://localhost:9090` | Metrics collection endpoint. |

---

## 🔧 Troubleshooting

### 1. "Orchestrator Not Found" / Connection Refused
*   **Symptoms**: The frontend says "Failed to execute HyperRun" or you cannot reach `localhost:8080`.
*   **Fixes**:
    *   Check if the container is running: `docker compose ps crew-orchestrator`.
    *   Check logs: `docker compose logs crew-orchestrator`.
    *   **Port Conflict**: Ensure port 8080 is not used by another app (like another web server or Jenkins).

### 2. Agents Returning "Error" or "Timeout"
*   **Symptoms**: The dashboard shows a red status for agents.
*   **Fixes**:
    *   **API Key**: Verify your `PERPLEXITY_API_KEY` in `.env` is correct and has credits.
    *   **Internet Access**: Ensure Docker containers can reach the internet (to call Perplexity API).
    *   **Restart**: `docker compose restart crew-orchestrator`.

### 3. Frontend "Module Not Found"
*   **Symptoms**: Local development (`npm run dev`) fails.
*   **Fixes**:
    *   Run `npm install` in `src/broski-terminal` to ensure all dependencies are installed.
    *   Clear Next.js cache: Delete `.next` folder and restart.

### 4. Database Connection Issues
*   **Symptoms**: `hypercode-core` fails to start or logs DB errors.
*   **Fixes**:
    *   Ensure the `postgres` container is healthy.
    *   If you changed the password in `.env`, you may need to delete the existing volume to reset it:
        ```bash
        docker compose down -v
        docker compose up -d
        ```
        *(Warning: This deletes all database data!)*

### 5. Port Conflicts
If you see "Bind for 0.0.0.0:xxxx failed: port is already allocated":
1.  Identify the process using the port (e.g., `netstat -ano | findstr :3000` on Windows).
2.  Kill the process OR change the port mapping in `docker-compose.yml` (e.g., `"3005:3000"`).

## 🆘 Getting Help
If you are still stuck, please:
1.  Gather logs: `docker compose logs > system_logs.txt`
2.  Check the `docs/reports` directory for recent health checks.
3.  Open an issue on GitHub with the logs attached.
