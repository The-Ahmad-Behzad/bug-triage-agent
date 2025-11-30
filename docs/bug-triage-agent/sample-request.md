## Bug Triage AI Agent — Sample Execution Guide

This document shows how to interact with the Bug Triage AI Agent directly (no supervisor agent required). It includes a ready-to-use request payload, the expected response structure, and the end-to-end execution steps.

---

### 1. Prerequisites
- MongoDB running locally (e.g., Docker container using `docker run -d --name mongodb -p 27017:27017 mongo:latest`)
- Python 3.12+ with virtual environment created in `bug-triage-agent/venv`
- Dependencies installed via `pip install -r requirements.txt`

### 2. Start the API
```powershell
cd E:\spm-project\bug-triage-agent
.\venv\Scripts\Activate.ps1
uvicorn src.main.app:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` (interactive docs at `/docs`).

### 3. Sample Requests

Below are multiple payloads that cover diverse bug categories (backend runtime, UI glitch, security risk, performance issue). Use them individually or combine in the `bugs` array to stress-test the agent’s classification, priority, and assignment logic.

#### 3.1 Backend Runtime Error
Send this JSON to `/execute` to simulate a Java backend failure:

```json
{
  "message_id": "sample-001",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:00:00Z",
  "task": {
    "bugs": [
      {
        "bug_id": "BUG-101",
        "title": "NullPointerException when logging in",
        "description": "App crashes when user submits the login form.",
        "steps_to_reproduce": [
          "Open app",
          "Enter valid credentials",
          "Click Login"
        ],
        "stack_trace": "java.lang.NullPointerException at AuthService.java:42",
        "logs": "2025-01-01 10:02:15 ERROR AuthService failed to load user",
        "code_context": {
          "file_path": "src/auth/AuthService.java",
          "line_start": 30,
          "line_end": 60,
          "snippet": "User user = db.findUser(email);\nreturn user.getName();"
        },
        "language": "java",
        "file_type": ".java",
        "metadata": {
          "reported_by": "QA",
          "environment": "production",
          "tags": ["auth", "crash"]
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "dev-01",
        "name": "Hassan Raza",
        "skills": {
          "languages": ["java", "python"],
          "frameworks": ["spring"],
          "domains": ["backend", "authentication"]
        },
        "modules_owned": ["auth", "session-management"],
        "current_load": 2
      },
      {
        "member_id": "dev-02",
        "name": "Sara Ahmed",
        "skills": {
          "languages": ["javascript", "typescript"],
          "frameworks": ["react"],
          "domains": ["frontend", "ui"]
        },
        "modules_owned": ["ui"],
        "current_load": 1
      }
    ]
  }
}
```

#### 3.2 UI Glitch

```json
{
  "message_id": "sample-002",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:05:00Z",
  "task": {
    "bugs": [
      {
        "bug_id": "BUG-201",
        "title": "Dropdown misaligned on dashboard",
        "description": "Dropdown options overflow the card on smaller screens.",
        "steps_to_reproduce": [
          "Login as any user",
          "Open dashboard",
          "Resize browser to 1024x768",
          "Open the filter dropdown"
        ],
        "code_context": {
          "file_path": "web/src/components/FilterDropdown.vue",
          "line_start": 10,
          "line_end": 60,
          "snippet": "<div class=\"dropdown\" :class=\"{ open: isOpen }\">\n  <slot />\n</div>"
        },
        "language": "javascript",
        "file_type": ".vue",
        "metadata": {
          "environment": "staging",
          "tags": ["ui", "css", "responsive"],
          "reported_by": "UX"
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "dev-10",
        "name": "Ina Frontend",
        "skills": {
          "languages": ["javascript", "typescript"],
          "frameworks": ["vue", "react"],
          "domains": ["frontend", "design-systems"]
        },
        "modules_owned": ["dashboard-ui"],
        "current_load": 1
      }
    ]
  }
}
```

#### 3.3 Security Risk

```json
{
  "message_id": "sample-003",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:10:00Z",
  "task": {
    "bugs": [
      {
        "bug_id": "BUG-301",
        "title": "SQL Injection via search box",
        "description": "Search endpoint executes unescaped input allowing injection.",
        "steps_to_reproduce": [
          "Enter ' OR 1=1 -- into the search input",
          "Observe full dataset returned"
        ],
        "logs": "WARN Potential SQL injection detected",
        "code_context": {
          "file_path": "services/search_service.py",
          "line_start": 50,
          "line_end": 85,
          "snippet": "query = f\"SELECT * FROM products WHERE name LIKE '%{search}%'\""
        },
        "language": "python",
        "file_type": ".py",
        "metadata": {
          "environment": "production",
          "tags": ["security", "sql", "critical"],
          "reported_by": "security-team"
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "dev-sec",
        "name": "Nora Secure",
        "skills": {
          "languages": ["python", "go"],
          "frameworks": ["fastapi"],
          "domains": ["security", "backend"]
        },
        "modules_owned": ["search-service"],
        "current_load": 3
      }
    ]
  }
}
```

#### 3.4 Performance / Infrastructure Issue

```json
{
  "message_id": "sample-004",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:15:00Z",
  "task": {
    "bugs": [
      {
        "bug_id": "BUG-401",
        "title": "API throughput drops under load",
        "description": "Latency > 2s when QPS exceeds 200.",
        "logs": "WARN Timeout waiting for DB connection",
        "code_context": {
          "file_path": "src/api/order_controller.ts",
          "line_start": 120,
          "line_end": 180,
          "snippet": "const client = await pool.connect();\n// reused without release\nreturn await client.query(query);"
        },
        "language": "typescript",
        "file_type": ".ts",
        "metadata": {
          "environment": "production",
          "tags": ["performance", "api", "db-connection"]
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "dev-perf",
        "name": "Liam Perf",
        "skills": {
          "languages": ["typescript", "rust"],
          "frameworks": ["node", "nest"],
          "domains": ["performance", "scalability"]
        },
        "modules_owned": ["order-api"],
        "current_load": 4
      }
    ]
  }
}
```

### 4. Expected Response (Structure)
The exact content will vary, but a successful response will follow this shape:

```json
{
  "message_id": "<server-generated>",
  "sender": "bug_triage_agent",
  "recipient": "supervisor",
  "type": "task_response",
  "related_message_id": "sample-001",
  "status": "completed",
  "timestamp": "<ISO8601 timestamp>",
  "results": {
    "triage": [
      {
        "bug_id": "BUG-101",
        "classification": {
          "category": "Runtime Error",
          "type": "NullPointerException",
          "root_cause": "Missing null check in code"
        },
        "priority": {
          "level": "high",
          "justification": "<text>"
        },
        "assignment": {
          "assigned_to_member_id": "dev-01",
          "assigned_to_name": "Hassan Raza",
          "confidence": 0.83
        },
        "suggested_fix": {
          "approach": "<text>",
          "estimated_effort": "2-4 hours"
        },
        "confidence_scores": {
          "classification_confidence": 0.9,
          "priority_confidence": 0.8,
          "assignee_confidence": 0.83,
          "overall_confidence": 0.84
        }
      }
    ]
  }
}
```

If the payload is malformed or missing required fields, the agent returns a `status: "failed"` response with validation details, as seen when posting `{}`.

### 5. Execution Steps Summary
1. Ensure MongoDB is running on `localhost:27017`.
2. Activate the Python virtual environment and start `uvicorn src.main.app:app`.
3. POST the sample JSON above to `http://localhost:8000/execute`.
4. Review the response for classification, priority, assignment, suggested fix, and confidence metrics.

Use this file as a quick reference whenever you need to demonstrate or manually test the Bug Triage AI Agent.


