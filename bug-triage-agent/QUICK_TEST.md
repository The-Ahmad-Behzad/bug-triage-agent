# Quick Test Guide - Bug Triage AI Agent

## Fastest Way to Run Tests

### 1. Install Dependencies (One Time)

```bash
cd bug-triage-agent
pip install -r requirements.txt
```

### 2. Run All Tests

```bash
# Option 1: Using pytest (recommended)
python -m pytest tests/ -v

# Option 2: Using custom test script
python tests/run_tests.py
```

### 3. Run Specific Test

```bash
# Test classification only
python -m pytest tests/test_classification.py -v

# Test language detection only
python -m pytest tests/test_language_detection.py -v
```

### 4. Test Without Dependencies

If you don't have all dependencies installed, you can still test core functionality:

```bash
# These tests work without pydantic/pymongo
python -m pytest tests/test_language_detection.py -v
python -m pytest tests/test_classification.py -v
```

---

## Test Server Manually

### 1. Start Server

```bash
uvicorn src.main.app:app --reload
```

### 2. Test Health Check

Open browser: http://localhost:8000/health

Or use curl:
```bash
curl http://localhost:8000/health
```

### 3. Test Execute Endpoint

Create `test_request.json`:
```json
{
  "message_id": "test-001",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:00:00Z",
  "task": {
    "bugs": [{
      "bug_id": "BUG-001",
      "title": "Test bug",
      "description": "Test description"
    }],
    "team_profiles": [{
      "member_id": "dev-01",
      "name": "Developer",
      "skills": ["python"]
    }]
  }
}
```

Send request:
```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d @test_request.json
```

---

## Common Issues

**Problem:** `ModuleNotFoundError: No module named 'pydantic'`  
**Fix:** `pip install -r requirements.txt`

**Problem:** Tests fail with database errors  
**Fix:** Tests work without MongoDB. Database is optional.

**Problem:** Port 8000 already in use  
**Fix:** Use different port: `uvicorn src.main.app:app --reload --port 8001`

---

For detailed instructions, see `TESTING.md`



