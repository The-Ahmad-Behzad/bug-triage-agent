"""Simple CLI to simulate Supervisor → Bug Triage Agent handshake calls."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any

import httpx


SAMPLE_PAYLOADS: Dict[str, Dict[str, Any]] = {
    "backend": {
        "message_id": "mock-backend-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:00:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-BE-001",
                    "title": "NullPointerException during login",
                    "description": "NullPointerException when user submits credentials.",
                    "stack_trace": "NullPointerException at AuthService.java:42",
                    "code_context": {
                        "file_path": "src/auth/AuthService.java",
                        "line_start": 30,
                        "line_end": 55,
                        "snippet": "User user = db.findUser(email);\nreturn user.getName();",
                    },
                    "language": "java",
                    "file_type": ".java",
                    "metadata": {"environment": "production", "tags": ["auth", "runtime"]},
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-01",
                    "name": "Hassan Raza",
                    "skills": {
                        "languages": ["java", "python"],
                        "frameworks": ["spring"],
                        "domains": ["backend", "authentication"],
                    },
                    "modules_owned": ["auth"],
                    "current_load": 2,
                }
            ],
        },
    },
    "ui": {
        "message_id": "mock-ui-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:05:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-UI-201",
                    "title": "Dropdown misaligned on dashboard",
                    "description": "Dropdown overlaps buttons on tablets.",
                    "code_context": {
                        "file_path": "web/src/components/FilterDropdown.vue",
                        "line_start": 1,
                        "line_end": 40,
                        "snippet": "<div class=\"dropdown\" :class=\"{ open: isOpen }\">\n  <slot />\n</div>",
                    },
                    "language": "javascript",
                    "file_type": ".vue",
                    "metadata": {"environment": "staging", "tags": ["ui", "css"]},
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-10",
                    "name": "Ina Frontend",
                    "skills": {
                        "languages": ["javascript", "typescript"],
                        "frameworks": ["vue", "react"],
                        "domains": ["frontend", "design-systems"],
                    },
                    "modules_owned": ["dashboard-ui"],
                    "current_load": 1,
                }
            ],
        },
    },
    "security": {
        "message_id": "mock-sec-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:10:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-SEC-301",
                    "title": "SQL injection via search input",
                    "description": "Search endpoint concatenates query directly.",
                    "steps_to_reproduce": ["Enter ' OR 1=1 --", "All products return"],
                    "code_context": {
                        "file_path": "services/search_service.py",
                        "line_start": 50,
                        "line_end": 90,
                        "snippet": "query = f\"SELECT * FROM products WHERE name LIKE '%{search}%'\"",
                    },
                    "language": "python",
                    "file_type": ".py",
                    "metadata": {"environment": "production", "tags": ["security", "sql"]},
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-sec",
                    "name": "Nora Secure",
                    "skills": {
                        "languages": ["python", "go"],
                        "frameworks": ["fastapi"],
                        "domains": ["security", "backend"],
                    },
                    "modules_owned": ["search-service"],
                    "current_load": 3,
                }
            ],
        },
    },
    "performance": {
        "message_id": "mock-perf-001",
        "sender": "supervisor",
        "recipient": "bug_triage_agent",
        "type": "task_assignment",
        "timestamp": "2025-01-01T12:15:00Z",
        "task": {
            "bugs": [
                {
                    "bug_id": "BUG-PERF-401",
                    "title": "API throughput drops under load",
                    "description": "Latency spikes to 2s when QPS > 200.",
                    "logs": "WARN Timeout waiting for DB connection",
                    "code_context": {
                        "file_path": "src/api/order_controller.ts",
                        "line_start": 100,
                        "line_end": 170,
                        "snippet": "const client = await pool.connect();\nreturn await client.query(query);",
                    },
                    "language": "typescript",
                    "file_type": ".ts",
                    "metadata": {"environment": "production", "tags": ["performance"]},
                }
            ],
            "team_profiles": [
                {
                    "member_id": "dev-perf",
                    "name": "Liam Perf",
                    "skills": {
                        "languages": ["typescript", "rust"],
                        "frameworks": ["node", "nest"],
                        "domains": ["performance", "scalability"],
                    },
                    "modules_owned": ["order-api"],
                    "current_load": 4,
                }
            ],
        },
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Supervisor mock client for Bug Triage Agent.")
    parser.add_argument("--host", default="http://localhost:8000", help="Bug Triage Agent base URL.")
    parser.add_argument(
        "--scenario",
        choices=list(SAMPLE_PAYLOADS.keys()),
        default="backend",
        help="Sample bug scenario to submit.",
    )
    parser.add_argument("--save-response", type=Path, help="Optional path to save JSON response.")
    parser.add_argument("--timeout", type=float, default=30.0, help="Request timeout in seconds.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = SAMPLE_PAYLOADS[args.scenario]
    url = f"{args.host.rstrip('/')}/execute"

    try:
        with httpx.Client(timeout=args.timeout) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:  # pragma: no cover - CLI convenience
        print(f"[supervisor-mock] Request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    formatted = json.dumps(data, indent=2)
    print("[supervisor-mock] Response received:")
    print(formatted)

    if args.save_response:
        args.save_response.write_text(formatted, encoding="utf-8")
        print(f"[supervisor-mock] Response saved to {args.save_response}")


if __name__ == "__main__":
    main()


