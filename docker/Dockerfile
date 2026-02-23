# Multi-stage build: dependencies and runtime separation
# Stage 1: Build - Install dependencies and prepare wheels
FROM python:3.11-bookworm AS builder

WORKDIR /build

# Install build dependencies (only needed for compilation)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip, setuptools, wheel in builder stage
RUN pip install --no-cache-dir --upgrade \
    pip>=26.0 \
    setuptools>=78.1.1 \
    wheel>=0.46.2

# Copy requirements and pre-build wheels
# COPY requirements.txt .
# RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# Stage 2: Runtime - Minimal production image
FROM python:3.11-slim-bookworm

# Install only runtime dependencies (security patches included)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Upgrade pip to latest patched version
RUN pip install --no-cache-dir --upgrade pip>=26.0

# Create non-root user for security
RUN useradd -m -u 1001 appuser

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/app/.venv/bin:$PATH"

# Copy wheels from builder and install dependencies
# COPY --from=builder /build/wheels /tmp/wheels
# RUN pip install --no-index --find-links /tmp/wheels /tmp/wheels/* && \
#     rm -rf /tmp/wheels

# Copy application code (create .dockerignore to exclude unnecessary files)
# COPY --chown=appuser:appuser app.py .
# COPY --chown=appuser:appuser config/ ./config/
# ... other app files ...

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8009

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8009/health || exit 1

# Run application
CMD ["python", "agent.py"]
