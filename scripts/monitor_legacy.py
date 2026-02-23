import os
import time
import json
import logging
from pathlib import Path
from datetime import datetime

# Configuration
LEGACY_DIR = Path("docs/archive/legacy")
REPORT_DIR = Path("docs/reports/monitoring")
THRESHOLD_SIZE_MB = 500
THRESHOLD_FILE_MB = 50
THRESHOLD_GROWTH_PERCENT = 25
HISTORY_FILE = REPORT_DIR / "legacy_growth_history.json"

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_size(path):
    total = 0
    try:
        if path.is_file():
            return path.stat().st_size
        for entry in os.scandir(path):
            try:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir(follow_symlinks=False):
                    total += get_size(Path(entry.path))
            except Exception:
                pass
    except Exception:
        pass
    return total

def analyze_legacy_folder():
    logger.info(f"Starting analysis of {LEGACY_DIR}...")
    
    if not LEGACY_DIR.exists():
        logger.warning(f"Legacy directory {LEGACY_DIR} does not exist.")
        return

    total_size = 0
    large_files = []
    file_count = 0

    for root, _, files in os.walk(LEGACY_DIR):
        for name in files:
            file_path = Path(root) / name
            try:
                size = file_path.stat().st_size
                total_size += size
                file_count += 1
                
                size_mb = size / (1024 * 1024)
                if size_mb > THRESHOLD_FILE_MB:
                    large_files.append({
                        "path": str(file_path),
                        "size_mb": round(size_mb, 2)
                    })
            except Exception as e:
                logger.error(f"Error accessing {file_path}: {e}")

    total_size_mb = total_size / (1024 * 1024)
    
    # Load History for Growth Calculation
    history = []
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except Exception:
            pass

    # Calculate Growth
    growth_percent = 0.0
    if history:
        last_entry = history[-1]
        last_size = last_entry.get("size_mb", 0)
        if last_size > 0:
            growth_percent = ((total_size_mb - last_size) / last_size) * 100

    # Generate Report Data
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_size_mb": round(total_size_mb, 2),
        "file_count": file_count,
        "large_files": large_files,
        "growth_percent": round(growth_percent, 2),
        "alerts": []
    }

    # Check Thresholds
    if total_size_mb > THRESHOLD_SIZE_MB:
        report_data["alerts"].append(f"CRITICAL: Legacy folder size ({total_size_mb:.2f} MB) exceeds limit ({THRESHOLD_SIZE_MB} MB)")
    
    if growth_percent > THRESHOLD_GROWTH_PERCENT:
        report_data["alerts"].append(f"WARNING: Weekly growth rate ({growth_percent:.2f}%) exceeds limit ({THRESHOLD_GROWTH_PERCENT}%)")

    if large_files:
        report_data["alerts"].append(f"WARNING: {len(large_files)} files exceed {THRESHOLD_FILE_MB} MB limit")

    # Save History
    history.append({
        "timestamp": report_data["timestamp"],
        "size_mb": report_data["total_size_mb"]
    })
    
    # Keep last 52 entries (1 year weekly)
    if len(history) > 52:
        history = history[-52:]
        
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    # Generate Markdown Report
    report_path = REPORT_DIR / f"LEGACY_MONITOR_REPORT_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 🛡️ Legacy Content Monitoring Report\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if report_data["alerts"]:
            f.write("## 🚨 Alerts Triggered\n")
            for alert in report_data["alerts"]:
                f.write(f"- 🔴 {alert}\n")
            f.write("\n")
        else:
            f.write("## ✅ Status: Healthy\n\n")

        f.write("## 📊 Statistics\n")
        f.write(f"- **Total Size:** {report_data['total_size_mb']} MB\n")
        f.write(f"- **File Count:** {report_data['file_count']}\n")
        f.write(f"- **Growth (vs last check):** {report_data['growth_percent']}%\n\n")

        if large_files:
            f.write("## 🐘 Large Files (> 50MB)\n")
            f.write("| File Path | Size (MB) |\n")
            f.write("|-----------|-----------|\n")
            for file in large_files:
                f.write(f"| `{file['path']}` | {file['size_mb']} |\n")
    
    logger.info(f"Report generated at {report_path}")
    
    # Output for Agent
    print(json.dumps(report_data, indent=2))

if __name__ == "__main__":
    analyze_legacy_folder()
