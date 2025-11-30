# Bug Triage Agent - Input/Output Schemas

## Complete JSON Schema Specifications

This document provides the complete, production-ready JSON schemas for the Bug Triage AI Agent.

---

## Input Schema

The Supervisor sends task assignments in this format:

```json
{
  "message_id": "sup-msg-001",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "related_message_id": "uuid (optional)",
  "timestamp": "2025-11-20T12:00:00Z",
  "task": {
    "bugs": [
      {
        "bug_id": "BUG-1234",
        "title": "App crashes on login",
        "description": "The app throws a NullPointerException after entering credentials.",
        "steps_to_reproduce": [
          "Open app",
          "Enter username and password",
          "Click Login"
        ],
        "stack_trace": "java.lang.NullPointerException at AuthService.java:42",
        "logs": "2025-11-20 10:02:15 ERROR AuthService failed to load user",
        "code_context": {
          "file_path": "src/auth/AuthService.java",
          "line_start": 30,
          "line_end": 60,
          "snippet": "User user = db.findUser(email);\nreturn user.getName();"
        },
        "language": "java",
        "file_type": ".java",
        "metadata": {
          "reported_by": "ahmad",
          "environment": "production",
          "tags": ["crash", "auth", "nullpointer"]
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "dev-01",
        "name": "Hassan Raza",
        "skills": ["java", "authentication", "backend"],
        "modules_owned": ["auth", "session-management"],
        "current_load": 3
      },
      {
        "member_id": "dev-02",
        "name": "Sara Ahmed",
        "skills": ["frontend", "react", "css"],
        "modules_owned": ["ui", "dashboard"],
        "current_load": 1
      }
    ]
  }
}
```

### Input Schema Field Descriptions

#### Root Level
- `message_id` (string, required): Unique identifier for the message
- `sender` (string, required): Always "supervisor" for task assignments
- `recipient` (string, required): Always "bug_triage_agent"
- `type` (string, required): "task_assignment" for input messages
- `related_message_id` (string, optional): Reference to related message
- `timestamp` (string, required): ISO8601 timestamp

#### Task Object
- `bugs` (array, required): Array of bug objects to triage
- `team_profiles` (array, required): Array of team member profiles

#### Bug Object
- `bug_id` (string, required): Unique identifier for the bug
- `title` (string, required): Short description of the bug
- `description` (string, required): Detailed description
- `steps_to_reproduce` (array, optional): List of reproduction steps
- `stack_trace` (string, optional): Error stack trace
- `logs` (string, optional): Relevant log entries
- `code_context` (object, optional): Code snippet and location
  - `file_path` (string, required): Path to source file
  - `line_start` (number, optional): Starting line number
  - `line_end` (number, optional): Ending line number
  - `snippet` (string, optional): Code snippet
- `language` (string, optional): Programming language (e.g., "java", "python", "javascript", "typescript"). If not provided, will be auto-detected from file_path
- `file_type` (string, optional): File extension (e.g., ".java", ".py", ".js", ".tsx"). If not provided, will be auto-detected from file_path
- `metadata` (object, optional): Additional metadata
  - `reported_by` (string, optional): Username of reporter
  - `environment` (string, optional): Environment (dev/staging/production)
  - `tags` (array, optional): Array of tag strings

#### Team Profile Object
- `member_id` (string, required): Unique identifier for team member
- `name` (string, required): Full name
- `skills` (object, optional): Structured skills object
  - `languages` (array, optional): Array of programming languages (e.g., ["java", "python"])
  - `frameworks` (array, optional): Array of frameworks (e.g., ["spring", "django"])
  - `domains` (array, optional): Array of domain expertise (e.g., ["backend", "security"])
- `skills` (array, optional): Legacy format - array of skill strings (for backward compatibility)
- `modules_owned` (array, optional): Array of module names owned
- `current_load` (number, optional): Current number of assigned tasks

---

## Output Schema

The Bug Triage Agent returns results in this format:

```json
{
  "message_id": "triage-response-001",
  "sender": "bug_triage_agent",
  "recipient": "supervisor",
  "type": "task_response",
  "related_message_id": "sup-msg-001",
  "status": "completed",
  "timestamp": "2025-11-20T12:00:10Z",
  "results": {
    "triage": [
      {
        "bug_id": "BUG-1234",
        "classification": {
          "category": "Runtime Error",
          "type": "NullPointerException",
          "root_cause": "Missing null check on user object"
        },
        "priority": {
          "level": "critical",
          "justification": "Crash affecting authentication flow in production"
        },
        "assignment": {
          "assigned_to_member_id": "dev-01",
          "assigned_to_name": "Hassan Raza",
          "confidence": 0.91
        },
        "suggested_fix": {
          "approach": "Add a null check before calling getName() and ensure user object is retrieved properly.",
          "estimated_effort": "2-4 hours"
        },
        "confidence_scores": {
          "classification_confidence": 0.96,
          "priority_confidence": 0.88,
          "assignee_confidence": 0.91,
          "overall_confidence": 0.92
        }
      }
    ]
  }
}
```

### Output Schema Field Descriptions

#### Root Level
- `message_id` (string, required): Unique identifier for the response
- `sender` (string, required): Always "bug_triage_agent"
- `recipient` (string, required): Always "supervisor"
- `type` (string, required): "task_response" for output messages
- `related_message_id` (string, optional): Reference to original task message
- `status` (string, required): "completed", "failed", or "in_progress"
- `timestamp` (string, required): ISO8601 timestamp

#### Results Object
- `triage` (array, required): Array of triage results, one per input bug

#### Triage Result Object
- `bug_id` (string, required): Matches input bug_id
- `classification` (object, required): Bug classification
  - `category` (string, required): High-level category (e.g., "Runtime Error", "Security", "Performance")
  - `type` (string, required): Specific type (e.g., "NullPointerException", "SQL Injection")
  - `root_cause` (string, optional): AI-detected root cause
- `priority` (object, required): Priority assessment
  - `level` (string, required): "critical", "high", "medium", or "low"
  - `justification` (string, required): Explanation for priority level
- `assignment` (object, required): Team member assignment
  - `assigned_to_member_id` (string, required): ID from team_profiles
  - `assigned_to_name` (string, required): Name from team_profiles
  - `confidence` (number, required): Confidence score (0.0 to 1.0)
- `suggested_fix` (object, optional): Fix recommendation
  - `approach` (string, required): Description of suggested fix
  - `estimated_effort` (string, required): Time estimate (e.g., "2-4 hours", "1 day")
- `confidence_scores` (object, required): Detailed confidence metrics
  - `classification_confidence` (number, required): 0.0 to 1.0
  - `priority_confidence` (number, required): 0.0 to 1.0
  - `assignee_confidence` (number, required): 0.0 to 1.0
  - `overall_confidence` (number, required): 0.0 to 1.0

---

## Key Features

1. **Batch Processing**: Supports multiple bugs in a single request
2. **Code Context**: Includes source code snippets for better classification
3. **Team Profiles**: Uses team member data for intelligent assignment
4. **Confidence Scores**: Provides transparency in AI decisions
5. **Fix Suggestions**: Includes actionable fix recommendations
6. **Effort Estimation**: Helps with sprint planning

---

## Validation Rules

### Input Validation (Bug Triage Agent)
- Must validate: bug_id, title, description are present
- Must validate: code_context.file_path if code_context is provided
- Must validate: language/file_type if provided (must be valid)
- Must validate: language and file_type consistency (if both provided)
- Must validate: team_profiles array is not empty
- Should auto-detect: language and file_type from file_path if not provided
- Should NOT validate: Compatibility with other agents' outputs (Supervisor handles this)

### Output Validation (Supervisor)
- Must validate: All required fields are present
- Must validate: Confidence scores are between 0.0 and 1.0
- Must validate: Priority level is one of: critical, high, medium, low
- Must validate: assigned_to_member_id exists in input team_profiles

---

## Example Use Cases

### Single Bug Triage
Send one bug, receive one triage result.

### Batch Triage
Send multiple bugs, receive multiple triage results in same response.

### Code Context Required
When code_context is provided, classification accuracy improves significantly.

### Team Assignment
When team_profiles include skills and ownership, assignment confidence increases.

