import os

dockerfile_template = """# {AGENT_NAME} - Optimized
FROM python:3.11.8-slim AS builder

WORKDIR /build

# Install build dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \\
    --mount=type=cache,target=/var/lib/apt,sharing=locked \\
    apt-get update && \\
    apt-get install -y --no-install-recommends \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \\
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ========================================
# Stage 2: Runtime
# ========================================
FROM python:3.11.8-slim

WORKDIR /app

# Install runtime dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \\
    --mount=type=cache,target=/var/lib/apt,sharing=locked \\
    apt-get update && \\
    apt-get install -y --no-install-recommends \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    AGENT_NAME={AGENT_NAME} \\
    AGENT_ROLE="{AGENT_ROLE}" \\
    AGENT_MODEL={AGENT_MODEL} \\
    AGENT_PORT={AGENT_PORT}

# Install wheels from builder
COPY --from=builder /wheels /wheels
RUN --mount=type=cache,target=/root/.cache/pip \\
    pip install --no-cache-dir /wheels/* && \\
    rm -rf /wheels

# Copy application code
COPY agent.py .
COPY config.json .
COPY base_agent.py .
COPY event_bus.py .

# Mount point for Hive Mind
VOLUME ["/app/hive_mind"]

EXPOSE {AGENT_PORT}

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=20s \\
    CMD curl -f http://localhost:${AGENT_PORT}/health || exit 1

CMD ["python", "agent.py"]
"""

coder_dockerfile = """# Coder Agent - Standardized
# Based on BaseAgent pattern (FastAPI)

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    docker.io \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install docker-mcp via pipx to avoid dependency conflicts (httpx version)
ENV PIPX_HOME=/opt/pipx
ENV PIPX_BIN_DIR=/usr/local/bin
RUN pip install pipx && \\
    pipx install git+https://github.com/QuantGeekDev/docker-mcp.git

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONPATH=/app

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "main.py"]
"""

agents = [
    ("01-frontend-specialist", "frontend-specialist", "Frontend Specialist", "claude-3-5-sonnet-20241022", 8002),
    ("02-backend-specialist", "backend-specialist", "Backend Specialist", "claude-3-5-sonnet-20241022", 8003),
    ("03-database-architect", "database-architect", "Database Architect", "claude-3-5-sonnet-20241022", 8004),
    ("04-qa-engineer", "qa-engineer", "QA Engineer", "claude-3-5-sonnet-20241022", 8005),
    ("05-devops-engineer", "devops-engineer", "DevOps Engineer", "claude-3-5-sonnet-20241022", 8006),
    ("06-security-engineer", "security-engineer", "Security Engineer", "claude-3-5-sonnet-20241022", 8007),
    ("07-system-architect", "system-architect", "System Architect", "claude-3-5-sonnet-20241022", 8008),
    ("08-project-strategist", "project-strategist", "Project Strategist", "claude-3-opus-20240229", 8009),
]

def restore():
    base_path = "agents"
    
    # Restore specialized agents
    for dir_name, name, role, model, port in agents:
        path = os.path.join(base_path, dir_name, "Dockerfile")
        content = dockerfile_template.format(
            AGENT_NAME=name,
            AGENT_ROLE=role,
            AGENT_MODEL=model,
            AGENT_PORT=port
        )
        with open(path, "w") as f:
            f.write(content)
        print(f"Restored {path}")

    # Restore coder agent
    coder_path = os.path.join(base_path, "coder", "Dockerfile")
    with open(coder_path, "w") as f:
        f.write(coder_dockerfile)
    print(f"Restored {coder_path}")

if __name__ == "__main__":
    restore()
