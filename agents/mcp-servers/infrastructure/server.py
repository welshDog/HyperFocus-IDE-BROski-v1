import os
import json
import logging
import asyncio
from typing import Any, Dict, List, Optional
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
from mcp.server import Server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    ToolInputSchema
)
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("infrastructure-mcp")

# Configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:changeme@localhost:5432/hypercode")

class RedisTools:
    def __init__(self):
        self.redis_client = redis.from_url(REDIS_URL, decode_responses=True)

    def get(self, key: str) -> str:
        """Get a value from Redis"""
        return self.redis_client.get(key) or ""

    def set(self, key: str, value: str) -> str:
        """Set a value in Redis"""
        self.redis_client.set(key, value)
        return "OK"
        
    def keys(self, pattern: str = "*") -> List[str]:
        """List keys matching pattern"""
        return self.redis_client.keys(pattern)

class PostgresTools:
    def __init__(self):
        self.conn_string = POSTGRES_URL

    def query(self, sql: str, params: Optional[List[Any]] = None) -> List[Dict[str, Any]]:
        """Execute a read-only SQL query"""
        if not sql.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed via this tool for safety.")
            
        try:
            with psycopg2.connect(self.conn_string) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql, params)
                    return cur.fetchall()
        except Exception as e:
            logger.error(f"Database error: {e}")
            return [{"error": str(e)}]

# Initialize Server
app = Server("hypercode-infrastructure")

redis_tools = RedisTools()
postgres_tools = PostgresTools()

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="redis_get",
            description="Get a value from Redis key-value store",
            inputSchema=ToolInputSchema(
                type="object",
                properties={
                    "key": {"type": "string", "description": "The key to retrieve"}
                },
                required=["key"]
            )
        ),
        Tool(
            name="redis_set",
            description="Set a value in Redis key-value store",
            inputSchema=ToolInputSchema(
                type="object",
                properties={
                    "key": {"type": "string", "description": "The key to set"},
                    "value": {"type": "string", "description": "The value to store"}
                },
                required=["key", "value"]
            )
        ),
        Tool(
            name="postgres_query",
            description="Execute a SELECT query on the PostgreSQL database",
            inputSchema=ToolInputSchema(
                type="object",
                properties={
                    "sql": {"type": "string", "description": "The SQL query to execute (SELECT only)"},
                    "params": {"type": "array", "description": "Optional parameters for the query", "items": {"type": "string"}}
                },
                required=["sql"]
            )
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent | ImageContent | EmbeddedResource]:
    try:
        if name == "redis_get":
            result = redis_tools.get(arguments["key"])
            return [TextContent(type="text", text=str(result))]
            
        elif name == "redis_set":
            result = redis_tools.set(arguments["key"], arguments["value"])
            return [TextContent(type="text", text=str(result))]
            
        elif name == "postgres_query":
            result = postgres_tools.query(arguments["sql"], arguments.get("params"))
            return [TextContent(type="text", text=json.dumps(result, default=str))]
            
        else:
            raise ValueError(f"Unknown tool: {name}")
            
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]

async def main():
    # Import stdio server transport
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
