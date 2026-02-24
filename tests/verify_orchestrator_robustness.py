
import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_hyperrun_success():
    print("Testing /hyperrun (Success Case)...")
    payload = {
        "task": "Research the latest Agent Vibe coder",
        "context": {"priority": "high"}
    }
    try:
        response = requests.post(f"{BASE_URL}/hyperrun", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Hyperrun Success")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Hyperrun Failed: {response.text}")
    except Exception as e:
        print(f"❌ Hyperrun Exception: {e}")

def test_direct_execution_success():
    print("\nTesting /agent/{name}/execute (Success Case)...")
    # project-strategist should be available
    agent_name = "project-strategist"
    payload = {
        "agent": "project-strategist",
        "message": "Hello",
        "context": {}
    }
    try:
        response = requests.post(f"{BASE_URL}/agent/{agent_name}/execute", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Direct Exec Success")
        else:
            print(f"❌ Direct Exec Failed: {response.text}")
    except Exception as e:
        print(f"❌ Direct Exec Exception: {e}")

def test_invalid_agent_name():
    print("\nTesting Invalid Agent Name...")
    agent_name = "invalid_agent_name"
    payload = {"agent": agent_name, "message": "test"}
    try:
        response = requests.post(f"{BASE_URL}/agent/{agent_name}/execute", json=payload)
        print(f"Status: {response.status_code}")
        if response.status_code == 404:
            print("✅ Correctly returned 404 for invalid agent")
        else:
            print(f"❌ Expected 404, got {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_hyperrun_success()
    test_direct_execution_success()
    test_invalid_agent_name()
