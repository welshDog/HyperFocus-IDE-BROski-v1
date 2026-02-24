import pytest
import asyncio
import json
import websockets
import httpx
from typing import Dict, Any

# Configuration
ORCHESTRATOR_URL = "http://127.0.0.1:8080"
WS_URL = "ws://127.0.0.1:8080/ws"

@pytest.mark.asyncio
async def test_websocket_connection():
    """
    Verify that we can establish a WebSocket connection
    and receive the initial connection success message/state.
    """
    try:
        async with websockets.connect(WS_URL) as websocket:
            # Send a ping to verify bidirectional communication
            await websocket.send("ping")
            response = await websocket.recv()
            assert response == "pong"
    except Exception as e:
        pytest.fail(f"WebSocket connection failed: {e}")

@pytest.mark.asyncio
async def test_realtime_task_update():
    """
    Verify that creating a task via REST API triggers a 
    real-time notification on the WebSocket.
    """
    task_payload = {
        "task": "Integration Test Task",
        "context": {"env": "test"},
        "priority": "high"
    }

    async with websockets.connect(WS_URL) as websocket:
        # Create task via REST API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/plan",
                json=task_payload
            )
            assert response.status_code == 200
            task_data = response.json()
            task_id = task_data["task_id"]

        # Wait for the broadcast message
        # We might receive other messages, so we look for the specific one
        received = False
        try:
            # Set a timeout to avoid hanging indefinitely
            message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(message)
            
            # Check if this is the task_created event
            if data.get("type") == "task_created" and data.get("task_id") == task_id:
                received = True
                assert data["description"] == task_payload["task"]
        except asyncio.TimeoutError:
            pytest.fail("Did not receive task_created event within timeout")
        
        assert received, "Failed to receive task_created event"

@pytest.mark.asyncio
async def test_workflow_broadcast():
    """
    Verify that starting a workflow broadcasts an event.
    """
    workflow_payload = {
        "workflow_type": "feature",
        "description": "Test Workflow Broadcast",
        "requirements": {}
    }

    async with websockets.connect(WS_URL) as websocket:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{ORCHESTRATOR_URL}/workflow/feature",
                json=workflow_payload
            )
            assert response.status_code == 200
            workflow_id = response.json()["workflow_id"]

        try:
            message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(message)
            
            if data.get("type") == "workflow_started" and data.get("workflow_id") == workflow_id:
                assert data["workflow_type"] == "feature"
            else:
                pytest.fail(f"Received unexpected message: {data}")
        except asyncio.TimeoutError:
            pytest.fail("Did not receive workflow_started event within timeout")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
