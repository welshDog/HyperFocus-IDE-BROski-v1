# cagent Migration POC: QA Engineer

This directory contains a Proof of Concept (POC) for migrating the existing Python-based QA Engineer agent to Docker's `cagent` runtime.

## Files
- `qa-engineer.yaml`: Declarative configuration for the QA Engineer agent.

## Prerequisites
- Docker Desktop 4.49+ (includes `cagent`) or standalone `cagent` installation.
- An Anthropic API Key (or OpenAI/etc. if you change the model in `qa-engineer.yaml`).

## Running the POC

1. Set your API key:
   ```powershell
   $env:ANTHROPIC_API_KEY = "your-api-key-here"
   ```

2. Run the agent:
   ```powershell
   cagent run agents/cagent-poc/qa-engineer.yaml
   ```

3. Interact with the agent in the terminal.

## Migration Benefits
- **Simplified Architecture**: Replaces custom Python/FastAPI boilerplate with a single YAML file.
- **MCP Support**: Easy integration with external tools via Model Context Protocol.
- **Orchestration**: Built-in multi-agent support (though this POC is single-agent).
- **Maintainability**: Declarative configuration is easier to read and modify than Python code.

## Next Steps
To fully replace the existing `qa-engineer` service:
1. Update `docker-compose.yml` to use a `cagent` image or build a custom image with the YAML config.
2. Ensure the `cagent` runtime can communicate with the Core service (e.g., via MCP or HTTP tools).
3. Update the Orchestrator to interact with the new agent interface.
