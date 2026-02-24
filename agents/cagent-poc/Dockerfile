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

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Entrypoint script to handle dynamic agent selection
RUN echo '#!/bin/sh\n\
if [ -n "$AGENT_NAME" ]; then\n\
  # If AGENT_NAME is set, use it to find the config file\n\
  CONFIG_FILE="/app/configs/$AGENT_NAME.yaml"\n\
  echo "Starting cagent with config: $CONFIG_FILE"\n\
  exec cagent serve api -l 0.0.0.0:8000 "$CONFIG_FILE"\n\
else\n\
  echo "Error: AGENT_NAME environment variable not set"\n\
  exit 1\n\
fi' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Run cagent
CMD []

