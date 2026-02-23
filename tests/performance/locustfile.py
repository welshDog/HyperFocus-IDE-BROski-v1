import time
import uuid
import json
import logging
from locust import HttpUser, task, between, events, LoadTestShape
import websocket
import gevent
from gevent import Greenlet

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentOrchestratorUser(HttpUser):
    wait_time = between(1, 3)  # Think time between tasks
    
    def on_start(self):
        """
        Simulate user connecting to the platform.
        Establish WebSocket connection for real-time updates.
        """
        self.client.verify = False
        self.ws = None
        self.ws_greenlet = None
        # WebSocket Connection is optional but recommended for full simulation
        # In a real heavy load test, we might separate WS users from HTTP users
        # For now, let's try to connect and keep it open if the server supports it
        self.connect_websocket()

    def connect_websocket(self):
        try:
            # Construct WS URL from HTTP Base URL (e.g., http://localhost:8000 -> ws://localhost:8000/ws)
            ws_url = self.host.replace("http", "ws").replace("https", "wss") + "/ws"
            self.ws = websocket.create_connection(ws_url)
            self.ws_greenlet = gevent.spawn(self.receive_ws_messages)
            # Custom event for tracking WS connection success
            events.request.fire(
                request_type="WebSocket",
                name="Connect",
                response_time=0,
                response_length=0,
                exception=None,
            )
        except Exception as e:
            # Custom event for tracking WS connection failure
            events.request.fire(
                request_type="WebSocket",
                name="Connect",
                response_time=0,
                response_length=0,
                exception=e,
            )
            # logger.error(f"WebSocket connection failed: {e}") 
            # Suppress error log to avoid spamming console if WS is not up

    def receive_ws_messages(self):
        while True:
            try:
                if self.ws:
                    message = self.ws.recv()
                    # Just consume messages to simulate a real client
                    # We could parse and validate here if needed
            except Exception:
                break

    def on_stop(self):
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
        if self.ws_greenlet:
            self.ws_greenlet.kill()

    @task(3)
    def submit_task_intent(self):
        """
        Simulate a user submitting a new task intent.
        Critical Journey: Plan -> Execute
        """
        task_id = str(uuid.uuid4())
        payload = {
            "task": f"Generate a Python script for data processing {task_id}",
            "context": {"env": "production", "complexity": "medium"},
            "priority": "high"
        }
        
        with self.client.post("/plan", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to submit task: {response.status_code}")

    @task(1)
    def initiate_workflow(self):
        """
        Simulate a user starting a workflow.
        Critical Journey: Workflow Initiation
        """
        # We use 'feature' workflow as it involves multiple agents
        workflow_type = "feature"
        payload = {
            "workflow_type": workflow_type,
            "description": f"Implement user authentication {uuid.uuid4()}",
            "requirements": {"auth_provider": "oauth2"}
        }
        
        with self.client.post(f"/workflow/{workflow_type}", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                # 400 is expected if workflow type is invalid, but here we use valid one
                # 500 is failure
                response.failure(f"Failed to start workflow: {response.status_code}")

    @task(5)
    def health_check(self):
        """
        Simulate periodic health checks or keep-alives.
        """
        with self.client.get("/health", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")


class StagesShape(LoadTestShape):
    """
    A simple load test shape class that has different user counts and spawn rates
    at different times.
    
    Stages:
        - Ramp up to 10 users in 10 seconds (Warmup)
        - Ramp up to 50 users in 30 seconds (Normal Load)
        - Ramp up to 100 users in 30 seconds (High Load)
        - Sustain 100 users for 60 seconds (Steady State)
        - Ramp down to 0 in 10 seconds (Cooldown)
    """
    
    stages = [
        {"duration": 10, "users": 10, "spawn_rate": 1},
        {"duration": 40, "users": 50, "spawn_rate": 2},
        {"duration": 70, "users": 100, "spawn_rate": 5},
        {"duration": 130, "users": 100, "spawn_rate": 5}, # Sustain
        {"duration": 140, "users": 0, "spawn_rate": 10},
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
