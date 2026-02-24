import requests
import json
import sys

def test_invoke(port=8005, agent_name="qa-engineer"):
    base_url = f"http://localhost:{port}"
    
    print(f"\n--- Testing {agent_name} on port {port} ---")
    
    # Test /status
    try:
        url = f"{base_url}/status"
        print(f"GET {url}")
        response = requests.get(url, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error checking status: {e}")

    # Test /execute
    try:
        url = f"{base_url}/execute"
        payload = {
            "message": "Hello, are you operational?",
            "agent": agent_name
        }
        print(f"\nPOST {url}")
        print(f"Payload: {json.dumps(payload)}")
        
        response = requests.post(url, json=payload, timeout=125)
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print("Response JSON:")
            print(json.dumps(data, indent=2))
        except:
            print("Response Text:")
            print(response.text)
            
    except Exception as e:
        print(f"Error executing agent: {e}")

if __name__ == "__main__":
    agents = [
        {"port": 8002, "name": "frontend-specialist"},
        {"port": 8003, "name": "backend-specialist"},
        {"port": 8005, "name": "qa-engineer"},
        {"port": 8006, "name": "devops-engineer"}
    ]
    
    for agent in agents:
        test_invoke(agent["port"], agent["name"])
        print("-" * 50)
