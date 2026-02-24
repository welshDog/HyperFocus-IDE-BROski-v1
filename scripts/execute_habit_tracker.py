
import requests
import json
import time
import os
from datetime import datetime

BASE_URL = "http://localhost:8080"
REPORT_DIR = "docs/reports"
REPORT_FILE = os.path.join(REPORT_DIR, "Habit_Tracker_Execution_Report.md")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def execute_scenario():
    print("🚀 Initiating Habit Tracker Scenario Execution...")
    
    start_time = time.time()
    
    payload = {
        "task": "Build a full-stack Habit Tracker application. Frontend: React/Vite with Tailwind. Backend: FastAPI with PostgreSQL. Features: User auth, habit CRUD, streak tracking, daily progress analytics.",
        "context": {
            "priority": "high",
            "project_type": "mvp",
            "constraints": ["mobile-responsive", "dark-mode"]
        }
    }
    
    try:
        print(f"📡 Sending request to {BASE_URL}/hyperrun...")
        response = requests.post(f"{BASE_URL}/hyperrun", json=payload, timeout=120)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"⏱️ Execution completed in {duration:.2f} seconds")
        
        if response.status_code == 200:
            data = response.json()
            generate_report(data, duration, None)
            print(f"✅ Report generated at {REPORT_FILE}")
            print(json.dumps(data, indent=2))
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ Execution Failed: {error_msg}")
            generate_report(None, duration, error_msg)
            
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        generate_report(None, time.time() - start_time, str(e))

def generate_report(data, duration, error):
    ensure_dir(REPORT_DIR)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Habit Tracker Scenario Execution Report\n")
        f.write(f"**Date:** {timestamp}\n")
        f.write(f"**Duration:** {duration:.2f} seconds\n")
        f.write(f"**Status:** {'✅ Success' if not error else '❌ Failed'}\n\n")
        
        if error:
            f.write(f"## Error Details\n")
            f.write(f"```\n{error}\n```\n")
            return
            
        f.write(f"## Workflow Summary\n")
        f.write(f"- **Workflow ID:** `{data.get('workflow_id')}`\n")
        f.write(f"- **Status:** {data.get('status')}\n\n")
        
        f.write(f"## Agent Execution Details\n")
        
        results = data.get("results", [])
        if not results:
            f.write("*No results returned from agents.*\n")
        
        for res in results:
            agent = res.get("agent")
            status = res.get("status")
            result_data = res.get("data", {})
            
            f.write(f"### 🤖 Agent: {agent}\n")
            f.write(f"- **Status:** {status}\n")
            
            if status == "success":
                # Handle nested result structure if present
                content = result_data
                if isinstance(result_data, dict):
                    content = result_data.get("result", result_data)
                    
                f.write(f"\n**Output:**\n")
                f.write(f"```json\n{json.dumps(content, indent=2)}\n```\n")
            else:
                f.write(f"- **Error:** {res.get('error')}\n")
            
            f.write("\n---\n")

if __name__ == "__main__":
    execute_scenario()
