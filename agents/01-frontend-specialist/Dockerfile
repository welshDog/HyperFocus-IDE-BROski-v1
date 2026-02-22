# frontend-specialist - Optimized
FROM python:3.11.8-slim AS builder

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
FROM python:3.11.8-slim

WORKDIR /app

# Install runtime dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    AGENT_NAME=frontend-specialist \
    AGENT_ROLE="Frontend Specialist" \
    AGENT_MODEL=claude-3-5-sonnet-20241022 \
    AGENT_PORT=8002

# Install wheels from builder
COPY --from=builder /wheels /wheels
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels

# Copy application code
COPY agent.py .
COPY config.json .
COPY base_agent.py .
COPY event_bus.py .

# Mount point for Hive Mind
VOLUME ["/app/hive_mind"]

EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=20s \
    CMD curl -f http://localhost:$8002/health || exit 1

CMD ["python", "agent.py"]
