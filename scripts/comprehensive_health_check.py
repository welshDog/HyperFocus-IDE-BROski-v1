import subprocess
import json
import time
import sys
import os
from datetime import datetime
import urllib.request
import urllib.error

# Configuration
CORE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
OLLAMA_URL = "http://localhost:11434"
AGENTS = [
    {"name": "frontend-specialist", "port": 8002},
    {"name": "backend-specialist", "port": 8003},
    {"name": "database-architect", "port": 8004},
    {"name": "qa-engineer", "port": 8005},
    {"name": "devops-engineer", "port": 8006},
    {"name": "security-engineer", "port": 8007},
    {"name": "system-architect", "port": 8008},
    {"name": "project-strategist", "port": 8009},
    {"name": "coder-agent", "port": 8001},
]

REPORT_FILE = "COMPREHENSIVE_HEALTH_ASSESSMENT.md"

def run_command(command):
    try:
        # Using encoding='utf-8' and errors='replace' to handle potential encoding issues on Windows
        result = subprocess.run(
            command, 
            shell=True, 
            check=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except Exception as e:
        return "", str(e), -1

def check_http(url):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            return True, response.status, "OK"
    except urllib.error.HTTPError as e:
        return False, e.code, e.reason
    except urllib.error.URLError as e:
        return False, 0, str(e.reason)
    except Exception as e:
        return False, 0, str(e)

def get_docker_stats():
    # Get stats for all running containers
    # We use --no-stream to get a snapshot
    out, err, code = run_command("docker stats --no-stream --format \"{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}|{{.MemPerc}}\"")
    stats = {}
    if code == 0:
        for line in out.splitlines():
            parts = line.split("|")
            if len(parts) == 4:
                stats[parts[0]] = {
                    "cpu": parts[1],
                    "mem_usage": parts[2],
                    "mem_perc": parts[3]
                }
    return stats

def analyze_logs(container_name):
    out, err, code = run_command(f"docker logs --tail 50 {container_name}")
    errors = []
    if code == 0:
        combined = out + "\n" + err
        for line in combined.splitlines():
            if "ERROR" in line.upper() or "EXCEPTION" in line.upper() or "CRITICAL" in line.upper():
                # Filter out some common non-critical logs if needed
                errors.append(line.strip())
    return errors

def main():
    print("🚀 Starting Comprehensive Health Assessment...")
    report_lines = []
    report_lines.append(f"# 🏥 HyperCode Comprehensive Health Assessment")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # 1. System Resources & Container Status
    print("📊 Checking System Resources...")
    report_lines.append("## 1. System Resources & Container Status")
    
    out, err, code = run_command("docker ps -a --format \"{{.Names}}|{{.Status}}|{{.State}}\"")
    if code != 0:
        print("❌ Docker check failed.")
        sys.exit(1)
    
    container_stats = get_docker_stats()
    
    report_lines.append("| Container | Status | State | CPU | Memory | Errors Found |")
    report_lines.append("|---|---|---|---|---|---|")
    
    containers = [line.split("|") for line in out.splitlines()]
    containers.sort(key=lambda x: x[0])
    
    all_healthy = True
    
    for name, status, state in containers:
        stats = container_stats.get(name, {"cpu": "N/A", "mem_usage": "N/A", "mem_perc": "N/A"})
        
        # Log analysis
        errors = analyze_logs(name)
        error_status = f"⚠️ {len(errors)} issues" if errors else "✅ None"
        
        # Status icon
        icon = "✅" if state == "running" and ("healthy" in status or "Up" in status) else "❌"
        if "unhealthy" in status:
            icon = "❌"
            all_healthy = False
        elif state != "running":
            icon = "⚪" # Stopped
        
        report_lines.append(f"| {icon} {name} | {status} | {state} | {stats['cpu']} | {stats['mem_usage']} ({stats['mem_perc']}) | {error_status} |")
        
        if errors:
            report_lines.append(f"\n<details><summary>Recent Errors for {name}</summary>\n\n```")
            for e in errors[-5:]: # Show last 5
                report_lines.append(e)
            report_lines.append("```\n</details>\n")

    # 2. API Endpoint Validation
    print("🌐 Validating API Endpoints...")
    report_lines.append("\n## 2. API Endpoint Validation")
    report_lines.append("| Service | Endpoint | Status | Response |")
    report_lines.append("|---|---|---|---|")
    
    endpoints = [
        ("HyperCode Core", f"{CORE_URL}/health"),
        ("HyperCode Metrics", f"{CORE_URL}/metrics"),
        ("Broski Terminal", f"{FRONTEND_URL}/api/health"),
        ("Ollama", f"{OLLAMA_URL}/api/tags"), # Checks if model is loaded/ready
    ]
    
    for agent in AGENTS:
        endpoints.append((f"Agent: {agent['name']}", f"http://localhost:{agent['port']}/health"))
    
    for name, url in endpoints:
        success, code, msg = check_http(url)
        icon = "✅" if success and code == 200 else "❌"
        report_lines.append(f"| {icon} {name} | `{url}` | {code} | {msg} |")

    # 3. Database & Integration Checks
    print("🔗 Checking Connectivity...")
    report_lines.append("\n## 3. Infrastructure Connectivity")
    
    # Postgres
    out, err, code = run_command("docker exec postgres pg_isready -U postgres")
    pg_status = "✅ Connected" if code == 0 else f"❌ Failed: {out} {err}"
    report_lines.append(f"- **Postgres:** {pg_status}")
    
    # Redis
    out, err, code = run_command("docker exec redis redis-cli ping")
    redis_status = "✅ Connected (PONG)" if "PONG" in out else f"❌ Failed: {out} {err}"
    report_lines.append(f"- **Redis:** {redis_status}")
    
    # Core -> DB/Redis (via Health Endpoint)
    # We already checked Core /health, let's parse it if possible
    try:
        req = urllib.request.Request(f"{CORE_URL}/health")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            services = data.get("services", {})
            report_lines.append(f"- **Core Internal Checks:**")
            for k, v in services.items():
                icon = "✅" if v in ["connected", "ready"] else "⚠️"
                report_lines.append(f"  - {icon} {k}: {v}")
    except:
        report_lines.append("- **Core Internal Checks:** ⚠️ Could not parse /health response")

    # 4. Remediation Plan
    report_lines.append("\n## 🚀 Remediation Plan")
    if all_healthy:
        report_lines.append("✅ **System is fully operational.** No immediate actions required.")
    else:
        report_lines.append("⚠️ **Issues Detected:**")
        report_lines.append("1. **Check Logs:** Review the detailed error logs above for any failing containers.")
        report_lines.append("2. **Restart Services:** If services are unhealthy, try `docker-compose restart <service_name>`.")
        report_lines.append("3. **Resource Limits:** Ensure Docker Desktop has enough memory assigned (recommended: 4GB+).")
    
    # Write Report
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    
    print(f"✅ Assessment Complete. Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
