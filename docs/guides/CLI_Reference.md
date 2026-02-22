# 💻 HyperSwarm CLI Reference

The HyperSwarm CLI (`cli/main.py`) provides a terminal-based interface for interacting with your agent swarm. This guide details the available commands and their expected outputs.

## 📋 Table of Contents

- [Listing Agents](#listing-agents)
- [Running Tasks](#running-tasks)
- [Checking Costs](#checking-costs)
- [Jira Integration](#jira-integration)

---

## Listing Agents

List all available agents in the swarm, their status, and capabilities.

**Command:**
```bash
python cli/main.py agents
```

**Output:**
```text
HyperCode Agents Swarm
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID       ┃ Name               ┃ Capabilities                                 ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 8001     │ Project Strategist │ planning, roadmap, task-breakdown            │
│ 8002     │ Frontend Spec.     │ react, nextjs, tailwind, ui-design           │
│ 8003     │ Backend Spec.      │ python, fastapi, database-schema, api-design │
│ 8004     │ Database Arch.     │ postgres, redis, optimization, migration     │
│ 8005     │ QA Engineer        │ unit-testing, integration-testing, cypress   │
│ 8006     │ DevOps Engineer    │ docker, kubernetes, ci-cd, monitoring        │
│ 8007     │ Security Engineer  │ audit, penetration-testing, compliance       │
│ 8008     │ System Architect   │ patterns, scalability, reliability           │
└──────────┴────────────────────┴──────────────────────────────────────────────┘
```

---

## Running Tasks

Submit a natural language task to the swarm. The system will automatically select the best agent (or team) for the job.

**Command:**
```bash
python cli/main.py run "Analyze the current database schema for the 'users' table and suggest performance improvements for high-volume reads."
```

**Output:**
```text
Submitting task: Analyze the current database schema for the 'users' table and suggest performance improvements for high-volume reads.

Response:
Based on the analysis of the `users` table schema, here are the recommended improvements:

1. **Add Index on `email`**: Currently, lookups by email are full-table scans. Adding a B-tree index will improve login performance by 100x.
   ```sql
   CREATE INDEX idx_users_email ON users(email);
   ```

2. **Partitioning**: If the table exceeds 10M rows, consider partitioning by `created_at` to keep recent data in hot storage.

3. **Denormalization**: The `last_login` timestamp is updated frequently. Move this to a separate `user_activity` table to reduce write lock contention on the main user record.

Would you like me to generate the migration script for these changes?
```

---

## Checking Costs

Monitor the token usage and estimated cost of your agent interactions.

**Command:**
```bash
python cli/main.py costs
```

**Output:**
```text
Total Cost: $4.12
Total Tokens: 1,245,890

Cost by Model
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Model             ┃ Cost      ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ gpt-4o            │ $3.45     │
│ gpt-3.5-turbo     │ $0.42     │
│ claude-3-opus     │ $0.25     │
└───────────────────┴───────────┘
```

---

## Jira Integration

Generate and validate Jira tickets directly from the CLI.

### Generate Ticket Payload

Create a JSON payload for a new Jira ticket based on a template.

**Command:**
```bash
python cli/main.py jira_generate --template bug_report --project-key HYPER --priority High --output json
```

**Output:**
```json
{
  "fields": {
    "project": { "key": "HYPER" },
    "summary": "[Bug] ",
    "description": "Steps to Reproduce:\n1. \n2. \n\nExpected Behavior:\n\nActual Behavior:\n",
    "issuetype": { "name": "Bug" },
    "priority": { "name": "High" }
  }
}
```

### Validate Ticket

Check if a ticket payload is valid before submitting.

**Command:**
```bash
python cli/main.py jira_validate --project-key HYPER --summary "Login fails on mobile" --description "Users cannot login." --issue-type Bug --priority High
```

**Output:**
```text
Valid
```
