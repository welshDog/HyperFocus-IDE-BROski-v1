import os
from pathlib import Path

AGENTS = ["researcher", "coder", "crew-orchestrator"]
PACKAGE = "prometheus-fastapi-instrumentator>=6.0.0"

for agent in AGENTS:
    req_file = Path(f"agents/{agent}/requirements.txt")
    
    if not req_file.exists():
        print(f"⚠️  {req_file} not found, skipping")
        continue
    
    content = req_file.read_text()
    
    # Check if already present
    if "prometheus-fastapi-instrumentator" in content:
        print(f"⏭️  {req_file} already updated")
        continue
    
    # Append package
    with req_file.open("a") as f:
        f.write(f"\n{PACKAGE}\n")
    
    print(f"✅ Updated {req_file}")
