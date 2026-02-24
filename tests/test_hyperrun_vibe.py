
import requests
import json
import sys

def test_hyperrun():
    url = "http://localhost:8080/hyperrun"
    payload = {"task": "Research the latest Agent Vibe coder"}
    headers = {"Content-Type": "application/json"}
    
    print(f"POST {url}")
    print(f"Payload: {json.dumps(payload)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hyperrun()
