# Comprehensive Test Report
**Date:** 2026-02-24T15:28:00.370514

## Summary Statistics
- **Total Test Suites/Files:** 14
- **Passed:** 7
- **Failed:** 7
- **Errors:** 0
- **Skipped:** 0
- **Total Duration:** 11.70s

## Module Details
### Backend Tests
Passed: 6/12

#### Failures/Errors:
- **test_agents_status** (tests.test_agent_crew)
  - Message: assert 'project-strategist' in "['project_strategist', 'frontend_specialist', 'backend_specialist', 'database_architect', 'qa_engineer', 'devops_engineer', 'security_engineer', 'system_architect']"
 +  where "['project_strategist', 'frontend_specialist', 'backend_specialist', 'database_architect', 'qa_engineer', 'devops_engineer', 'security_engineer', 'system_architect']" = str(['project_strategist', 'frontend_specialist', 'backend_specialist', 'database_architect', 'qa_engineer', 'devops_engineer', ...])
- **test_agent_direct_execution** (tests.test_agent_crew)
  - Message: assert 404 in [200, 503]
 +  where 404 = <Response [404 Not Found]>.status_code
- **test_coder_agent_hello_world** (tests.functional.test_coder_capabilities)
  - Message: SystemExit: 2
- **test_websocket_connection** (tests.integration.test_websocket_integration)
  - Message: Failed: WebSocket connection failed: server rejected WebSocket connection: HTTP 404
- **test_realtime_task_update** (tests.integration.test_websocket_integration)
  - Message: websockets.exceptions.InvalidStatus: server rejected WebSocket connection: HTTP 404
- **test_workflow_broadcast** (tests.integration.test_websocket_integration)
  - Message: websockets.exceptions.InvalidStatus: server rejected WebSocket connection: HTTP 404

<details><summary>Raw Output (Last 20 lines)</summary>

```
    
        Raises:
            InvalidHandshake: If the handshake response is invalid.
    
        """
    
        if response.status_code != 101:
>           raise InvalidStatus(response)
E           websockets.exceptions.InvalidStatus: server rejected WebSocket connection: HTTP 404

.venv\Lib\site-packages\websockets\client.py:144: InvalidStatus
- generated xml file: C:\Users\Lyndz\Downloads\HyperFocus-IDE-BROski-v1\test_reports\pytest_results_20260224_152800.xml -
=========================== short test summary info ===========================
FAILED tests/test_agent_crew.py::test_agents_status - assert 'project-strateg...
FAILED tests/test_agent_crew.py::test_agent_direct_execution - assert 404 in ...
FAILED tests/functional/test_coder_capabilities.py::test_coder_agent_hello_world
FAILED tests/integration/test_websocket_integration.py::test_websocket_connection
FAILED tests/integration/test_websocket_integration.py::test_realtime_task_update
FAILED tests/integration/test_websocket_integration.py::test_workflow_broadcast
======================== 6 failed, 6 passed in 11.89s =========================
```
</details>

### Frontend Tests
✅ **PASSED**

<details><summary>Output</summary>

```

> broski-terminal@0.1.0 test
> echo "Tests skipped: Vitest not configured" && exit 0 --run

"Tests skipped: Vitest not configured" 

```
</details>

### Smoke/E2E Tests
❌ **FAILED**

<details><summary>Output</summary>

```
Starting HyperCode DEV Smoke Tests...
[PASS] HyperCode Core Health is reachable at http://localhost:8000/health (0.239s)
[PASS] Broski Terminal API is reachable at http://localhost:3000/api/health (0.053s)
[FAIL] HyperFlow Editor at http://localhost:5173 unreachable: HTTPConnectionPool(host='localhost', port=5173): Max retries exceeded with url: / (Caused by NewConnectionError("HTTPConnection(host='localhost', port=5173): Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it"))

```
</details>
