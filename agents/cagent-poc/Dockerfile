# Base on Python 3.11 (Debian Slim) for easy Python package installation
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install cagent binary from the official Docker image
COPY --from=docker/cagent:latest /cagent /usr/local/bin/cagent

# Install Python dependencies for MCP server
COPY cagent-poc/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP Server code
# Note: Context must be set correctly when building (from agents/ directory)
COPY mcp-servers /app/mcp-servers

# Copy Agent Configurations
# Using wildcard copy for all YAMLs
COPY cagent-poc/*.yaml /app/configs/

# Copy Agent Wrapper
COPY cagent-poc/agent_wrapper.py /app/agent_wrapper.py

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the wrapper
CMD ["python", "/app/agent_wrapper.py"]

