import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(cmd, cwd=None, capture_output=False):
    """Executes a shell command."""
    print(f"\n>>> {cmd}")
    try:
        if capture_output:
            return subprocess.check_output(cmd, shell=True, cwd=cwd or ROOT).decode().strip()
        else:
            subprocess.check_call(cmd, shell=True, cwd=cwd or ROOT)
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        return False

def check_docker():
    """Checks if Docker is running."""
    print("Checking Docker status...")
    if not run("docker info", capture_output=True):
        print("❌ Docker is not running. Please start Docker Desktop and try again.")
        sys.exit(1)
    print("✅ Docker is running.")

def main():
    print("\n🚀 Initializing HyperSwarm V3.0 Launch Sequence...\n")
    
    # 1. Check Pre-requisites
    check_docker()

    # 2. Start Docker Stack
    print("\n🐳 Starting Container Swarm...")
    if not run("docker compose up -d"):
        print("❌ Failed to start Docker containers.")
        sys.exit(1)

    # 3. Wait for critical services (Basic pause for spin-up)
    print("\n⏳ Waiting for services to stabilize (10s)...")
    time.sleep(10)

    # 4. Run Health Check
    health_script = ROOT / "scripts" / "comprehensive_health_check.py"
    if health_script.exists():
        print("\n🏥 Executing Health Diagnostics...")
        run(f"python {health_script}")
    else:
        print(f"\n⚠️ Health check script not found at {health_script}")

    # 5. Dashboard & Access Information
    print("\n" + "="*50)
    print("✅ HyperSwarm is ONLINE, BROski! 🚀")
    print("="*50)
    
    urls = {
        "Frontend Terminal": "http://localhost:3000",
        "Core API Docs": "http://localhost:8000/docs",
        "Grafana Dashboards": "http://localhost:3001",
        "Jaeger Tracing": "http://localhost:16686",
        "Prometheus": "http://localhost:9090"
    }

    for name, url in urls.items():
        print(f"{name:<20}: {url}")

    # 6. Optional: Open Frontend
    try:
        if input("\nOpen Frontend in browser? (y/n): ").lower().strip() == 'y':
            webbrowser.open(urls["Frontend Terminal"])
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
