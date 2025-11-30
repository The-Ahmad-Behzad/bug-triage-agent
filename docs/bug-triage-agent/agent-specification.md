# Bug Triage AI Agent - Complete Specification

## Agent Overview

**Agent Name:** Bug Triage AI Agent  
**Agent Description:** The Bug Triage Agent is an AI-driven module that automatically classifies, prioritizes, and assigns software bugs to the most suitable team members.

## Data Input

The Bug Triage Agent accepts:
- **Bug reports** (title, description, steps to reproduce, stack traces, logs)
- **Code context** (source files, snippets, file paths, line numbers)
- **Language/File type** (programming language and file extension - auto-detected if not provided)
- **Team profiles** (member skills including languages, frameworks, domains, ownership, current workload)
- **Metadata** (environment, tags, reporter information)

### Input Format Details

The agent receives data in the Supervisor handshake format with the following structure:

```json
{
  "message_id": "uuid",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "ISO8601",
  "task": {
    "bugs": [
      {
        "bug_id": "string",
        "title": "string",
        "description": "string",
        "steps_to_reproduce": ["string"],
        "stack_trace": "string",
        "logs": "string",
        "code_context": {
          "file_path": "string",
          "line_start": "number",
          "line_end": "number",
          "snippet": "string"
        },
        "language": "string (optional)",
        "file_type": "string (optional)",
        "metadata": {
          "reported_by": "string",
          "environment": "string",
          "tags": ["string"]
        }
      }
    ],
    "team_profiles": [
      {
        "member_id": "string",
        "name": "string",
        "skills": ["string"],
        "modules_owned": ["string"],
        "current_load": "number"
      }
    ]
  }
}
```

## Data Output

The Bug Triage Agent returns:
- **Classification** (category, type, root cause analysis)
- **Priority** (level with justification)
- **Assignment** (recommended team member with confidence score)
- **Suggested fix** (approach and estimated effort)
- **Confidence scores** (for classification, priority, assignment, and overall)

### Output Format Details

```json
{
  "message_id": "uuid",
  "sender": "bug_triage_agent",
  "recipient": "supervisor",
  "timestamp": "ISO8601",
  "results": {
    "triage": [
      {
        "bug_id": "string",
        "classification": {
          "category": "string",
          "type": "string",
          "root_cause": "string"
        },
        "priority": {
          "level": "critical|high|medium|low",
          "justification": "string"
        },
        "assignment": {
          "assigned_to_member_id": "string",
          "assigned_to_name": "string",
          "confidence": "number (0-1)"
        },
        "suggested_fix": {
          "approach": "string",
          "estimated_effort": "string"
        },
        "confidence_scores": {
          "classification_confidence": "number (0-1)",
          "priority_confidence": "number (0-1)",
          "assignee_confidence": "number (0-1)",
          "overall_confidence": "number (0-1)"
        }
      }
    ]
  }
}
```

## Key Design Decisions

1. **Input Format:** Both bug reports AND code context (option c) - provides best accuracy
2. **Output Format:** Classification + priority + assignee + suggested fix + estimated effort (option c) - industry standard
3. **Team Member Data:** Agent maintains its own database/knowledge (option b) - ensures reliable, fast assignment
4. **Compatibility:** Supervisor handles input/output compatibility between agents - Bug Triage Agent only validates its own required fields

## Features

- Supports multiple bug reports at once (batch processing)
- Includes code context for accurate classification
- Uses team profiles for intelligent assignment
- Provides confidence scores for all decisions
- Suggests fix approaches and effort estimates
- Fully compatible with multi-agent orchestration

