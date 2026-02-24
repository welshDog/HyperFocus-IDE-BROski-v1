import sys
import json
import subprocess
import urllib.request
import urllib.error
import time
from datetime import datetime

# Configuration
SERVICES = {
    "hypercode-core": {"port": 8000, "path": "/health"},
    "broski-terminal": {"port": 3000, "path": "/api/health"}, # Assuming this path based on docker-compose
    "coder-agent": {"port": 8001, "path": "/health"},
    "frontend-specialist": {"port": 8002, "path": "/health"},
    "backend-specialist": {"port": 8003, "path": "/health"},
    "database-architect": {"port": 8004, "path": "/health"},
    "qa-engineer": {"port": 8005, "path": "/", "expect_status": [200, 404]}, # cagent API root returns 404 currently
    "devops-engineer": {"port": 8006, "path": "/health"},
    "security-engineer": {"port": 8007, "path": "/health"},
    "system-architect": {"port": 8008, "path": "/health"},
    "project-strategist": {"port": 8009, "path": "/health"},
    "grafana": {"port": 3001, "path": "/api/health"},
    "prometheus": {"port": 9090, "path": "/-/healthy"},
    "jaeger": {"port": 16686, "path": "/"}, # Jaeger UI usually returns 200 on root
}

def check_docker_containers():
    print("🐳 Checking Docker Containers...")
    try:
        # Docker format string for json output
        cmd = ["docker", "ps", "--format", "{{json .}}"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        containers = [json.loads(line) for line in result.stdout.strip().split('\n') if line]
        
        status_map = {}
        for c in containers:
            names = c.get("Names", "unknown")
            state = c.get("State", "unknown")
            status = c.get("Status", "unknown")
            status_map[names] = {"state": state, "status": status}
            
            icon = "✅" if state == "running" else "❌"
            print(f"{icon} {names:<25} | {state:<10} | {status}")
            
        return status_map
    except Exception as e:
        print(f"❌ Failed to check Docker: {e}")
        return {}

def check_endpoint(name, config):
    url = f"http://localhost:{config['port']}{config['path']}"
    start_time = time.time()
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            latency = (time.time() - start_time) * 1000
            if response.status == 200 or response.status in config.get("expect_status", []):
                return True, latency, f"OK ({response.status})"
            else:
                return False, latency, f"Status {response.status}"
    except urllib.error.HTTPError as e:
        latency = (time.time() - start_time) * 1000
        if e.code in config.get("expect_status", []):
             return True, latency, f"OK ({e.code})"
        return False, latency, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, 0, f"Connection Failed: {e.reason}"
    except Exception as e:
        return False, 0, f"Error: {e}"

def main():
    print(f"🏥 HyperCode Health Check System - {datetime.now().isoformat()}")
    print("=" * 60)
    
    container_status = check_docker_containers()
    print("\n🌐 Checking Service Endpoints...")
    print(f"{'Service':<25} | {'Status':<8} | {'Latency':<10} | {'Message'}")
    print("-" * 60)
    
    overall_success = True
    
    for name, config in SERVICES.items():
        success, latency, msg = check_endpoint(name, config)
        if not success:
            overall_success = False
            
        icon = "✅" if success else "❌"
        latency_str = f"{latency:.2f}ms" if success else "-"
        print(f"{icon} {name:<23} | {'UP' if success else 'DOWN':<8} | {latency_str:<10} | {msg}")

    print("=" * 60)
    if overall_success:
        print("🎉 System is HEALTHY")
        sys.exit(0)
    else:
        print("⚠️ System has ISSUES")
        sys.exit(1)

if __name__ == "__main__":
    main()
