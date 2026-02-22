import requests
import json
import time

def test_workflow():
    # 1. Health Check
    print("🏥 Checking Crew Orchestrator Health...")
    try:
        resp = requests.get("http://localhost:8080/health")
        print(f"Orchestrator Health: {resp.status_code} - {resp.json()}")
    except Exception as e:
        print(f"❌ Orchestrator not reachable: {e}")
        return

    # 2. Submit Task
    print("\n🚀 Submitting Test Task...")
    task_payload = {
        "task": "Draft a high-level project plan for a CLI tool that converts Markdown files to PDF.",
        "context": {
            "priority": "high",
            "constraints": ["Must be written in Python", "Use a library like WeasyPrint"]
        }
    }
    
    try:
        # Hitting the /plan endpoint which delegates to project-strategist
        resp = requests.post("http://localhost:8080/plan", json=task_payload)
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"✅ Task Submitted Successfully!")
            print(f"Task ID: {result.get('task_id')}")
            print(f"Assigned Agents: {result.get('assigned_agents')}")
            print(f"Status: {result.get('status')}")
        else:
            print(f"❌ Task Submission Failed: {resp.status_code}")
            print(resp.text)
            
    except Exception as e:
        print(f"❌ Error submitting task: {e}")

if __name__ == "__main__":
    test_workflow()
