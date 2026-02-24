import requests
import sys
import time
import os

CORE_URL = os.getenv("CORE_URL", "http://localhost:8000")
TERMINAL_URL = os.getenv("TERMINAL_URL", "http://localhost:3000")
EDITOR_URL = os.getenv("EDITOR_URL", "http://localhost:5173")

def check_url(url, name):
    try:
        start = time.time()
        # Disable SSL verification for self-signed certs
        response = requests.get(url, timeout=5, verify=False)
        duration = time.time() - start
        if response.status_code == 200:
            print(f"[PASS] {name} is reachable at {url} ({duration:.3f}s)")
            return True
        else:
            print(f"[FAIL] {name} at {url} returned {response.status_code}")
            return False
    except Exception as e:
        print(f"[FAIL] {name} at {url} unreachable: {e}")
        return False

def main():
    print("Starting HyperCode DEV Smoke Tests...")
    
    # 1. Core API Health
    core_ok = check_url(f"{CORE_URL}/health", "HyperCode Core Health")
    
    # 2. Core Metrics (if available, might be /metrics or /api/metrics)
    # Core usually has /health.
    
    # 3. Terminal Frontend
    term_ok = check_url(f"{TERMINAL_URL}/api/health", "Broski Terminal API")
    
    # 4. Editor Frontend
    editor_ok = check_url(EDITOR_URL, "HyperFlow Editor")

    if core_ok and term_ok: # Editor might be optional or not running
        print("\n✅ DEV SMOKE TESTS PASSED")
        sys.exit(0)
    else:
        print("\n❌ DEV SMOKE TESTS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
