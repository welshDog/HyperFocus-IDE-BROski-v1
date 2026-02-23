# backend-specialist - Optimized
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

# Install build dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

# ========================================
# Stage 2: Runtime
# ========================================
FROM python:3.11-slim-bookworm

WORKDIR /app

# Install runtime dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AGENT_NAME=backend-specialist \
    AGENT_ROLE="Backend Specialist" \
    AGENT_MODEL=claude-3-5-sonnet-20241022 \
    AGENT_PORT=8003

# Install wheels from builder
COPY --from=builder /wheels /wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY --chown=appuser:appuser agent.py .
COPY --chown=appuser:appuser config.json .
COPY --chown=appuser:appuser base_agent.py .
COPY --chown=appuser:appuser event_bus.py .

# Mount point for Hive Mind
# Note: When mounting volumes in Docker, permissions can be tricky for non-root users.
# We ensure the directory exists and is owned by appuser.
RUN mkdir -p /app/hive_mind && chown -R appuser:appuser /app/hive_mind
VOLUME ["/app/hive_mind"]

EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=20s \
    CMD curl -f http://localhost:8003/health || exit 1

# Switch to non-root user
USER appuser

CMD ["python", "agent.py"]
