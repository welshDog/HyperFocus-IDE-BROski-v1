import os
import sys
import subprocess
import json
import time
from datetime import datetime
import glob
import xml.etree.ElementTree as ET

# Configuration
REPORT_DIR = "test_reports"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

def run_command(command, cwd=None, env=None):
    """Run a shell command and return output, return_code, duration"""
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        duration = time.time() - start_time
        return {
            "command": command,
            "cwd": cwd,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration
        }
    except Exception as e:
        duration = time.time() - start_time
        return {
            "command": command,
            "cwd": cwd,
            "return_code": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": duration
        }

def parse_junit_xml(xml_path):
    """Parse JUnit XML to get test stats"""
    if not os.path.exists(xml_path):
        return None
        
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        stats = {
            "tests": 0,
            "failures": 0,
            "errors": 0,
            "skipped": 0,
            "time": 0.0,
            "cases": []
        }
        
        # Handle different XML structures (testsuites vs testsuite)
        suites = root.findall('testsuite')
        if not suites and root.tag == 'testsuite':
            suites = [root]
            
        for suite in suites:
            stats["tests"] += int(suite.attrib.get("tests", 0))
            stats["failures"] += int(suite.attrib.get("failures", 0))
            stats["errors"] += int(suite.attrib.get("errors", 0))
            stats["skipped"] += int(suite.attrib.get("skipped", 0))
            stats["time"] += float(suite.attrib.get("time", 0))
            
            for case in suite.findall('testcase'):
                case_info = {
                    "name": case.attrib.get("name"),
                    "classname": case.attrib.get("classname"),
                    "time": float(case.attrib.get("time", 0)),
                    "status": "passed"
                }
                
                failure = case.find('failure')
                if failure is not None:
                    case_info["status"] = "failed"
                    case_info["message"] = failure.attrib.get("message")
                    case_info["text"] = failure.text
                
                error = case.find('error')
                if error is not None:
                    case_info["status"] = "error"
                    case_info["message"] = error.attrib.get("message")
                    case_info["text"] = error.text
                    
                skipped = case.find('skipped')
                if skipped is not None:
                    case_info["status"] = "skipped"
                    case_info["message"] = skipped.attrib.get("message")
                
                stats["cases"].append(case_info)
                
        return stats
    except Exception as e:
        print(f"Error parsing XML {xml_path}: {e}")
        return None

def main():
    print(f"Starting Comprehensive Test Suite Execution at {datetime.now()}")
    os.makedirs(REPORT_DIR, exist_ok=True)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "skipped": 0,
            "duration": 0
        },
        "modules": {}
    }
    
    # Environment Setup
    env = os.environ.copy()
    # Add src/hypercode-core and cli to PYTHONPATH
    python_paths = [
        os.path.abspath(os.path.join(ROOT_DIR, "src", "hypercode-core")),
        os.path.abspath(os.path.join(ROOT_DIR, "cli")),
        env.get("PYTHONPATH", "")
    ]
    env["PYTHONPATH"] = os.path.pathsep.join(python_paths)
    
    # 1. Backend Tests (Pytest)
    print("\n[1/3] Running Backend Tests (Pytest)...")
    pytest_xml = os.path.join(REPORT_DIR, f"pytest_results_{TIMESTAMP}.xml")
    # Include tests/ and cli/tests/
    # Also ignore broken tests if necessary, but we want comprehensive report.
    backend_cmd = f"python -m pytest tests/ cli/tests/ --junitxml={pytest_xml} --continue-on-collection-errors"
    backend_res = run_command(backend_cmd, cwd=ROOT_DIR, env=env)
    
    results["modules"]["backend"] = {
        "command": backend_cmd,
        "output": backend_res["stdout"],
        "error": backend_res["stderr"],
        "return_code": backend_res["return_code"],
        "duration": backend_res["duration"],
        "stats": parse_junit_xml(pytest_xml)
    }
    
    if results["modules"]["backend"]["stats"]:
        s = results["modules"]["backend"]["stats"]
        results["summary"]["total_tests"] += s["tests"]
        results["summary"]["passed"] += (s["tests"] - s["failures"] - s["errors"] - s["skipped"])
        results["summary"]["failed"] += s["failures"]
        results["summary"]["errors"] += s["errors"]
        results["summary"]["skipped"] += s["skipped"]
        results["summary"]["duration"] += s["time"]

    # 2. Frontend Tests (Vitest/Jest)
    print("\n[2/3] Running Frontend Tests...")
    frontend_dir = os.path.join(ROOT_DIR, "src", "broski-terminal")
    if os.path.exists(frontend_dir):
        # Check package.json for test script
        pkg_json_path = os.path.join(frontend_dir, "package.json")
        has_test_script = False
        try:
            with open(pkg_json_path, "r", encoding="utf-8") as f:
                pkg_data = json.load(f)
                if "test" in pkg_data.get("scripts", {}):
                    has_test_script = True
        except Exception:
            pass

        if has_test_script:
            frontend_cmd = "npm test -- --run"
            frontend_res = run_command(frontend_cmd, cwd=frontend_dir)
            
            results["modules"]["frontend"] = {
                "command": frontend_cmd,
                "output": frontend_res["stdout"],
                "error": frontend_res["stderr"],
                "return_code": frontend_res["return_code"],
                "duration": frontend_res["duration"]
            }
            if frontend_res["return_code"] == 0:
                results["summary"]["passed"] += 1 # Count as 1 suite passed
            else:
                results["summary"]["failed"] += 1
            results["summary"]["total_tests"] += 1
        else:
            print("No 'test' script found in package.json, skipping.")
            results["modules"]["frontend"] = {"status": "skipped", "reason": "missing test script"}
            results["summary"]["skipped"] += 1
            results["summary"]["total_tests"] += 1
    else:
        print("Frontend directory not found, skipping.")
        results["modules"]["frontend"] = {"status": "skipped", "reason": "directory not found"}

    # 3. Smoke/E2E Tests
    print("\n[3/3] Running Smoke/E2E Tests...")
    # Use our DEV smoke test
    smoke_script = os.path.join(ROOT_DIR, "tests", "smoke_test_dev.py")
    if os.path.exists(smoke_script):
        smoke_cmd = f"python {smoke_script}"
        smoke_res = run_command(smoke_cmd, cwd=ROOT_DIR, env=env)
        
        results["modules"]["smoke"] = {
            "command": smoke_cmd,
            "output": smoke_res["stdout"],
            "error": smoke_res["stderr"],
            "return_code": smoke_res["return_code"],
            "duration": smoke_res["duration"]
        }
        # Count as 1 test
        results["summary"]["total_tests"] += 1
        if smoke_res["return_code"] == 0:
            results["summary"]["passed"] += 1
        else:
            results["summary"]["failed"] += 1
    else:
         results["modules"]["smoke"] = {"status": "skipped", "reason": "script not found"}

    # Generate JSON Report
    json_path = os.path.join(REPORT_DIR, "comprehensive_report.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\nJSON Report generated: {json_path}")

    # Generate Markdown Report
    md_path = os.path.join(REPORT_DIR, "comprehensive_report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Comprehensive Test Report\n")
        f.write(f"**Date:** {results['timestamp']}\n\n")
        
        f.write("## Summary Statistics\n")
        f.write(f"- **Total Test Suites/Files:** {results['summary']['total_tests']}\n")
        f.write(f"- **Passed:** {results['summary']['passed']}\n")
        f.write(f"- **Failed:** {results['summary']['failed']}\n")
        f.write(f"- **Errors:** {results['summary']['errors']}\n")
        f.write(f"- **Skipped:** {results['summary']['skipped']}\n")
        f.write(f"- **Total Duration:** {results['summary']['duration']:.2f}s\n\n")
        
        f.write("## Module Details\n")
        
        # Backend
        f.write("### Backend Tests\n")
        if "stats" in results["modules"]["backend"] and results["modules"]["backend"]["stats"]:
            stats = results["modules"]["backend"]["stats"]
            f.write(f"Passed: {stats['tests'] - stats['failures'] - stats['errors'] - stats['skipped']}/{stats['tests']}\n")
            if stats['failures'] > 0 or stats['errors'] > 0:
                f.write("\n#### Failures/Errors:\n")
                for case in stats['cases']:
                    if case['status'] in ['failed', 'error']:
                        f.write(f"- **{case['name']}** ({case['classname']})\n")
                        f.write(f"  - Message: {case.get('message', 'No message')}\n")
        else:
            f.write("No structured stats available. See raw output.\n")
        
        if results["modules"]["backend"]["return_code"] != 0:
             f.write("\n<details><summary>Raw Output (Last 20 lines)</summary>\n\n```\n")
             f.write("\n".join(results["modules"]["backend"]["output"].splitlines()[-20:]))
             f.write("\n```\n</details>\n")
        
        # Frontend
        f.write("\n### Frontend Tests\n")
        fe = results["modules"]["frontend"]
        if fe.get("status") == "skipped":
            f.write(f"⚠️ **SKIPPED**: {fe.get('reason')}\n")
        elif fe.get("return_code") == 0:
            f.write("✅ **PASSED**\n")
        else:
            f.write("❌ **FAILED**\n")
        
        if fe.get("output"):
             f.write("\n<details><summary>Output</summary>\n\n```\n")
             lines = fe["output"].splitlines()
             if len(lines) > 50:
                 f.write("\n".join(lines[:20]))
                 f.write("\n... (truncated) ...\n")
                 f.write("\n".join(lines[-20:]))
             else:
                 f.write(fe["output"])
             f.write("\n```\n</details>\n")

        # Smoke
        f.write("\n### Smoke/E2E Tests\n")
        smoke = results["modules"]["smoke"]
        if smoke.get("return_code") == 0:
            f.write("✅ **PASSED**\n")
        else:
            f.write("❌ **FAILED**\n")
        
        if smoke.get("output"):
             f.write("\n<details><summary>Output</summary>\n\n```\n")
             f.write(smoke["output"])
             f.write("\n```\n</details>\n")

    print(f"Markdown Report generated: {md_path}")

if __name__ == "__main__":
    main()
