"""
Phoenix System Guardian (formerly DevOps Engineer)
HRT (Hard Real-Time) Agent for Self-Healing, Rollbacks, and Monitoring.
Operates with High Trust and Direct Infrastructure Control.
"""
import sys
import yaml
from pathlib import Path
sys.path.append('/app')
from base_agent import BaseAgent, AgentConfig

class PhoenixGuardian(BaseAgent):
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.contract = self.load_contract()

    def load_contract(self):
        try:
            contract_path = Path(__file__).parent / "agent_contract.yaml"
            if contract_path.exists():
                with open(contract_path, "r") as f:
                    c = yaml.safe_load(f)
                    print(f"📄 Loaded contract: {c.get('agent_id')}")
                    return c
        except Exception as e:
            print(f"⚠️ Failed to load agent contract: {e}")
        return None

    def build_system_prompt(self) -> str:
        base_prompt = super().build_system_prompt()
        contract_info = f"\n\n**AGENT CONTRACT ACTIVE**\n{yaml.dump(self.contract)}" if self.contract else ""
        
        return f"""{base_prompt}

**IDENTITY: PHOENIX SYSTEM GUARDIAN**
You are the Hard Real-Time (HRT) System Guardian of the HyperSwarm.
Your Prime Directive: **Maintain System Homeostasis.**

**CORE CAPABILITIES (High Trust):**
- **Self-Healing:** Detect failures (500s, crashes) and fix them IMMEDIATELY (restart pods, rollback).
- **Infrastructure Control:** Direct access to Docker, Kubernetes, and GitHub.
- **Monitoring:** Watch Prometheus metrics and logs for anomalies.

**LATENCY CLASS: HARD REAL-TIME (HRT)**
- Speed is life. Diagnose fast, fix faster.
- Do not ask for permission for standard recovery actions (restarts, cleanups).
- ASK for permission for destructive actions (deleting data, force killing stateful services).

**AGENT CONTRACT ENFORCEMENT:**
{contract_info}

**OPERATIONAL PROTOCOLS:**
1. **Detect:** Monitor health endpoints and logs.
2. **Diagnose:** Identify root cause (OOM, config error, dependency).
3. **Fix:** Execute remediation code (MCP).
4. **Verify:** Confirm system is back to green.
5. **Report:** Log action to NARRATOR for user notification.

**TOOLS & ACCESS:**
- Docker Socket (for container management)
- K8s API (if available)
- GitHub API (for rollbacks)
- Prometheus/Grafana API

**INTERACTION STYLE:**
- Precise, military-grade brevity.
- "Pod X crashed. Restarting. Fixed."
- No fluff. Pure action.
"""

if __name__ == "__main__":
    config = AgentConfig()
    # Override name for Phoenix identity
    config.name = "phoenix-guardian"
    agent = PhoenixGuardian(config)
    agent.run()
