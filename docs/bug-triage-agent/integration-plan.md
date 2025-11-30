# Bug Triage AI Agent - Integration Plan

## Overview

This document describes how the Bug Triage AI Agent integrates with the Supervisor agent, including communication protocols, error handling, and response processing.

## Supervisor Communication Protocol

### Handshake Format

The Bug Triage Agent communicates with the Supervisor using a standardized handshake message format. All requests and responses follow this structure:

#### Request Format (from Supervisor)

```json
{
  "message_id": "uuid",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "ISO8601",
  "task": {
    "bugs": [...],
    "team_profiles": [...]
  }
}
```

#### Response Format (to Supervisor)

```json
{
  "message_id": "uuid",
  "sender": "bug_triage_agent",
  "recipient": "supervisor",
  "type": "task_response",
  "related_message_id": "original-message-id",
  "status": "completed" | "failed",
  "timestamp": "ISO8601",
  "results": {
    "triage": [...]
  },
  "warnings": ["optional warning messages"]
}
```

### Message Flow

1. **Supervisor sends task assignment** → `/execute` endpoint
2. **Agent validates input** → Returns error response if validation fails
3. **Agent processes bugs** → Classification, priority, assignment, fix suggestion
4. **Agent returns results** → Handshake format response with triage results
5. **Supervisor processes response** → Uses triage results for bug management

## Endpoint: `/execute`

### Request Handling

The `/execute` endpoint (`src/main/app.py`) accepts POST requests with handshake format payloads:

```python
@app.post("/execute")
async def execute(request: dict):
    return process_triage_request(request)
```

### Processing Flow

The `process_triage_request` function (`src/handlers/triage_handler.py`) orchestrates the entire triage workflow:

1. **Input Validation** (`src/utils/validators.py`)
   - Validates handshake message structure
   - Validates bug objects and team profiles
   - Returns error response if validation fails

2. **Team Profile Loading** (`src/utils/team_profile_loader.py`)
   - Merges input team profiles with database profiles
   - Falls back to input-only if database unavailable
   - Logs warnings for database unavailability

3. **Bug Processing** (for each bug):
   - **Language Detection** (`src/utils/language_detector.py`)
     - Auto-detects language/file_type if not provided
     - Validates consistency
   - **Classification** (`src/engines/classification.py`)
     - Categorizes bug (runtime error, security, performance, etc.)
     - Identifies root cause
     - Calculates confidence score
   - **Priority Assessment** (`src/engines/priority.py`)
     - Determines priority level (critical, high, medium, low)
     - Generates justification
     - Considers environment, impact, severity rules
   - **Assignment** (`src/engines/assignment.py`)
     - Matches bug to team member by language, skills, module ownership
     - Considers workload and routing rules
     - Calculates assignment confidence
   - **Fix Suggestion** (`src/engines/fix_suggestion.py`)
     - Generates actionable fix approach
     - Estimates effort required

4. **Response Generation**
   - Creates handshake format response
   - Includes all triage results
   - Adds warnings for missing optional fields
   - Preserves `related_message_id` for supervisor tracking

### Error Handling

The agent handles errors gracefully:

- **Validation Errors**: Returns `status: "failed"` with error message
- **Processing Errors**: Returns `status: "failed"` with error details
- **Database Unavailability**: Continues with input-only profiles, logs warnings
- **Missing Optional Fields**: Includes warnings in response, continues processing

### Response Status Codes

- **200 OK**: Request processed successfully (status may be "completed" or "failed")
- **422 Unprocessable Entity**: Invalid request format (FastAPI validation)
- **500 Internal Server Error**: Unexpected server error

## Retry Logic

The Supervisor should implement retry logic for failed requests:

1. **Transient Errors** (database unavailable, network issues):
   - Retry with exponential backoff
   - Maximum 3 retries
   - Wait: 1s, 2s, 4s

2. **Validation Errors**:
   - Do not retry (fix request format first)
   - Log error for investigation

3. **Processing Errors**:
   - Retry once after short delay (1s)
   - If still failing, log and escalate

## Metrics and Monitoring

The agent exposes metrics for supervisor monitoring:

### `/metrics` Endpoint

Returns runtime metrics:
- Request counts (total, successful, failed, validation failures)
- Bugs processed
- Latency statistics (average, max)
- Success rates
- Health check statistics

### `/health` Endpoint

Returns agent health status:
- Agent status (healthy/degraded)
- Database connectivity
- Uptime
- Request totals

The Supervisor can poll these endpoints to monitor agent health and performance.

## Testing Integration

### Supervisor Mock Script

A mock supervisor client is provided (`scripts/supervisor_mock.py`) for testing:

```bash
python scripts/supervisor_mock.py --scenario backend
python scripts/supervisor_mock.py --scenario security --save-response out.json
```

### Integration Tests

Tests verify handshake format compatibility (`tests/test_supervisor_handshake.py`):
- Envelope structure validation
- Related message ID preservation
- Warning propagation
- Batch processing
- Error response format

## Configuration

### Environment Variables

The agent uses environment variables for configuration (`.env` file):

- `MONGODB_URI`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `MONGODB_DB_NAME`: Database name (default: `bug_triage_agent`)
- `AGENT_NAME`: Agent identifier (default: `bug_triage_agent`)
- `LOG_LEVEL`: Logging level (default: `INFO`)

### Supervisor Configuration

The Supervisor should configure:
- Agent endpoint URL: `http://bug-triage-agent:8000/execute`
- Timeout: 30 seconds (configurable)
- Retry policy: As described above

## Deployment Considerations

### Container Deployment

The agent is designed for containerized deployment:
- Exposes port 8000
- Health check endpoint for orchestration
- Graceful degradation if database unavailable
- Structured logging for log aggregation

### Supervisor Integration Points

1. **Service Discovery**: Supervisor should discover agent endpoint
2. **Health Monitoring**: Poll `/health` endpoint periodically
3. **Metrics Collection**: Poll `/metrics` for observability
4. **Error Handling**: Implement retry logic as described
5. **Response Processing**: Parse handshake format and extract triage results

## Example Integration Flow

```
1. Supervisor receives bug report
2. Supervisor formats handshake message with bug + team profiles
3. Supervisor POSTs to /execute endpoint
4. Agent validates and processes request
5. Agent returns handshake response with triage results
6. Supervisor extracts:
   - Classification (category, type, root cause)
   - Priority (level, justification)
   - Assignment (member_id, name, confidence)
   - Suggested fix (approach, effort)
7. Supervisor creates bug ticket with assignment
8. Supervisor updates team member workload
```

## References

- **Code Location**: `src/handlers/triage_handler.py` - Main request processing
- **Input Models**: `src/models/input_models.py` - HandshakeMessage, Task, BugInput
- **Output Models**: `src/models/output_models.py` - HandshakeResponse, TriageResult
- **Sample Requests**: `docs/bug-triage-agent/sample-request.md`
- **API Documentation**: `/docs` endpoint (Swagger UI) when agent is running

