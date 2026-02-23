import requests
import os
import json
import time
from datetime import datetime

# Configuration
GRAFANA_URL = "http://localhost:3001"
PROMETHEUS_URL = "http://localhost:9090"
JAEGER_URL = "http://localhost:16686"
SERVICE_TOKEN = os.environ.get("SERVICE_ACCOUNT_TOKEN", "")  # Must be set in environment
if not SERVICE_TOKEN:
    print("⚠️  WARNING: SERVICE_ACCOUNT_TOKEN not set. Grafana checks may fail.")

REPORT_FILE = "docs/reports/OBSERVABILITY_VERIFICATION_REPORT.md"

def check_url(url, name):
    try:
        response = requests.get(url, timeout=5)
        status = "✅ ONLINE" if response.status_code == 200 else f"❌ ERROR ({response.status_code})"
        return {"name": name, "url": url, "status": status, "code": response.status_code}
    except Exception as e:
        return {"name": name, "url": url, "status": f"❌ UNREACHABLE ({str(e)})", "code": 0}

def check_prometheus_targets():
    url = f"{PROMETHEUS_URL}/api/v1/targets"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            targets = data.get("data", {}).get("activeTargets", [])
            return {
                "status": "✅ ONLINE",
                "count": len(targets),
                "details": [{"job": t["labels"]["job"], "health": t["health"], "url": t["scrapeUrl"]} for t in targets]
            }
        else:
            return {"status": f"❌ ERROR ({response.status_code})", "count": 0, "details": []}
    except Exception as e:
        return {"status": f"❌ UNREACHABLE ({str(e)})", "count": 0, "details": []}

def check_jaeger_services():
    url = f"{JAEGER_URL}/api/services"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            services = data.get("data", [])
            return {"status": "✅ ONLINE", "count": len(services), "services": services}
        else:
            return {"status": f"❌ ERROR ({response.status_code})", "count": 0, "services": []}
    except Exception as e:
        return {"status": f"❌ UNREACHABLE ({str(e)})", "count": 0, "services": []}

def check_grafana_datasources():
    url = f"{GRAFANA_URL}/api/datasources"
    headers = {"Authorization": f"Bearer {SERVICE_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            datasources = response.json()
            return {"status": "✅ ONLINE", "count": len(datasources), "details": [{"name": d["name"], "type": d["type"]} for d in datasources]}
        elif response.status_code == 401:
             return {"status": "❌ AUTH FAILED", "count": 0, "details": "Invalid Token"}
        else:
            return {"status": f"❌ ERROR ({response.status_code})", "count": 0, "details": []}
    except Exception as e:
        return {"status": f"❌ UNREACHABLE ({str(e)})", "count": 0, "details": []}

def main():
    print("🔍 Starting Observability Verification...")
    
    report_content = f"# 🔭 Observability Verification Report\n"
    report_content += f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # 1. Connectivity Check
    report_content += "## 1. Connectivity Check\n"
    report_content += "| Service | URL | Status |\n|---|---|---|\n"
    services = [
        ("Grafana", f"{GRAFANA_URL}/api/health"),
        ("Prometheus", f"{PROMETHEUS_URL}/-/healthy"),
        ("Jaeger", f"{JAEGER_URL}/")
    ]
    for name, url in services:
        res = check_url(url, name)
        report_content += f"| {res['name']} | `{res['url']}` | {res['status']} |\n"
        print(f"Checking {name}: {res['status']}")

    # 2. Prometheus Verification
    print("\nChecking Prometheus Targets...")
    prom_data = check_prometheus_targets()
    report_content += "\n## 2. Prometheus Data Collection\n"
    report_content += f"**Status:** {prom_data['status']}\n"
    report_content += f"**Active Targets:** {prom_data['count']}\n"
    if prom_data['count'] > 0:
        report_content += "| Job | Health | Scrape URL |\n|---|---|---|\n"
        for t in prom_data['details']:
            report_content += f"| `{t['job']}` | {t['health']} | `{t['url']}` |\n"
    
    # 3. Jaeger Verification
    print("\nChecking Jaeger Traces...")
    jaeger_data = check_jaeger_services()
    report_content += "\n## 3. Jaeger Trace Collection\n"
    report_content += f"**Status:** {jaeger_data['status']}\n"
    report_content += f"**Services Traced:** {jaeger_data['count']}\n"
    if jaeger_data['services']:
        report_content += "**Services List:** " + ", ".join([f"`{s}`" for s in jaeger_data['services']]) + "\n"

    # 4. Grafana Verification
    print("\nChecking Grafana Configuration...")
    grafana_data = check_grafana_datasources()
    report_content += "\n## 4. Grafana Configuration\n"
    report_content += f"**API Status:** {grafana_data['status']}\n"
    if grafana_data['status'] == "✅ ONLINE":
         report_content += f"**Data Sources:** {grafana_data['count']}\n"
         if grafana_data['count'] > 0:
             report_content += "| Name | Type |\n|---|---|\n"
             for d in grafana_data['details']:
                 report_content += f"| {d['name']} | {d['type']} |\n"
    elif grafana_data['status'] == "❌ AUTH FAILED":
        report_content += "**Error:** Service Account Token rejected. Check .env configuration.\n"

    # 5. Summary & Action Items
    report_content += "\n## 5. Summary & Action Items\n"
    issues = []
    if "❌" in prom_data['status'] or prom_data['count'] == 0:
        issues.append("- **Prometheus:** No active targets found or unreachable.")
    if "❌" in jaeger_data['status']:
        issues.append("- **Jaeger:** API unreachable.")
    if "❌" in grafana_data['status']:
        issues.append(f"- **Grafana:** {grafana_data['details'] if isinstance(grafana_data['details'], str) else 'Connection failed'}.")
    
    if not issues:
        report_content += "✅ **System is Fully Operational.** All monitoring components are connected and collecting data.\n"
    else:
        report_content += "⚠️ **Issues Detected:**\n"
        for issue in issues:
            report_content += f"{issue}\n"

    # Save Report
    os.makedirs("docs/reports", exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"\n✅ Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    main()
