# Bug Triage AI Agent - Testing Guide

This guide provides step-by-step instructions for running all tests and test scripts for the Bug Triage AI Agent.

---

## Prerequisites

Before running tests, ensure you have:

1. **Python 3.11+** installed
2. **Virtual environment** (recommended)
3. **MongoDB** (optional, for database-dependent tests)

---

## Step 1: Set Up Environment

### Option A: Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd bug-triage-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Option B: Using System Python

```bash
# Navigate to project directory
cd bug-triage-agent
```

---

## Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 pydantic-2.5.0 ...
```

**If installation fails:**
- Ensure you have pip updated: `python -m pip install --upgrade pip`
- Check Python version: `python --version` (should be 3.11+)

---

## Step 3: Configure Environment Variables (Optional)

For tests that require MongoDB:

```bash
# Copy environment template
cp .env.template .env

# Edit .env file with your MongoDB connection string
# MONGODB_URI=mongodb://localhost:27017
# MONGODB_DB_NAME=bug_triage_agent_test
```

**Note:** Most tests work without MongoDB. Database is only needed for:
- Full integration tests
- Database operation tests
- Historical bug queries

---

## Step 4: Run Tests

### Option A: Run All Tests with pytest

```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run with detailed output and coverage
python -m pytest tests/ -v --tb=short --cov=src

# Run specific test file
python -m pytest tests/test_classification.py -v

# Run specific test function
python -m pytest tests/test_classification.py::test_classify_bug_runtime_error -v
```

**Expected output:**
```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-8.4.2
collected 15 items

tests/test_classification.py::test_classify_bug_runtime_error PASSED
tests/test_input_validation.py::test_validate_input_valid PASSED
...
============================= 15 passed in 2.34s ==============================
```

### Option B: Run Custom Test Script

```bash
# Run comprehensive test suite
python tests/run_tests.py
```

**Expected output:**
```
============================================================
Bug Triage AI Agent - Comprehensive Test Suite
============================================================

=== Testing Phase 2: Input/Output Schema and Validation ===
✅ Language detection: PASSED

=== Testing Phase 4: Bug Classification Engine ===
✅ Classification: PASSED

...

Test Summary
============================================================
Total Tests: 8
Passed: 8
Failed: 0
Success Rate: 100.0%

Results saved to test_results.json
```

### Option C: Run Individual Test Files

```bash
# Test input validation
python -m pytest tests/test_input_validation.py -v

# Test language detection
python -m pytest tests/test_language_detection.py -v

# Test classification
python -m pytest tests/test_classification.py -v

# Test database operations (requires MongoDB)
python -m pytest tests/test_database_operations.py -v

# Test integration
python -m pytest tests/test_integration.py -v

# Test all phases
python -m pytest tests/test_all_phases.py -v
```

---

## Step 5: Run Specific Test Scenarios

### Test Robustness (Missing Optional Fields)

```bash
# Run integration test for robust handling
python -m pytest tests/test_integration.py::test_triage_with_minimal_input -v
```

**What it tests:**
- Agent continues working with missing optional fields
- Warnings are generated
- Output is still valid

### Test Error Handling (Missing Required Fields)

```bash
# Run error handling test
python -m pytest tests/test_integration.py::test_triage_error_handling_missing_required -v
```

**What it tests:**
- Agent stops and returns error for missing required fields
- Clear error messages provided

### Test Batch Processing

```bash
# Run batch processing test
python -m pytest tests/test_integration.py::test_triage_batch_processing -v
```

**What it tests:**
- Multiple bugs processed in one request
- All results returned correctly

---

## Step 6: Run Manual API Tests

### Start the Agent Server

```bash
# Start FastAPI server
uvicorn src.main.app:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Test Health Check Endpoint

```bash
# Using curl (Linux/Mac/Git Bash)
curl http://localhost:8000/health

# Using PowerShell (Windows)
Invoke-RestMethod -Uri http://localhost:8000/health -Method Get

# Using Python
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

**Expected response:**
```json
{
  "status": "healthy",
  "agent_name": "bug_triage_agent",
  "version": "1.0.0",
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### Test Execute Endpoint

```bash
# Create test request file (test_request.json)
cat > test_request.json << 'EOF'
{
  "message_id": "test-001",
  "sender": "supervisor",
  "recipient": "bug_triage_agent",
  "type": "task_assignment",
  "timestamp": "2025-01-01T12:00:00Z",
  "task": {
    "bugs": [{
      "bug_id": "BUG-001",
      "title": "NullPointerException",
      "description": "App crashes with NullPointerException",
      "code_context": {
        "file_path": "src/auth/AuthService.java",
        "snippet": "User user = db.findUser(email);\nreturn user.getName();"
      },
      "language": "java"
    }],
    "team_profiles": [{
      "member_id": "dev-01",
      "name": "Hassan Raza",
      "skills": {
        "languages": ["java"]
      },
      "modules_owned": ["auth"]
    }]
  }
}
EOF

# Send request using curl
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d @test_request.json

# Or using PowerShell
$body = Get-Content test_request.json -Raw
Invoke-RestMethod -Uri http://localhost:8000/execute -Method Post -Body $body -ContentType "application/json"
```

**Expected response:**
```json
{
  "status": "completed",
  "results": {
    "triage": [{
      "bug_id": "BUG-001",
      "classification": {...},
      "priority": {...},
      "assignment": {...},
      "suggested_fix": {...}
    }]
  }
}
```

---

## Step 7: View Test Results

### View JSON Test Results

```bash
# View test results file
cat test_results.json

# Or on Windows
type test_results.json

# Pretty print JSON
python -m json.tool test_results.json
```

### View Test Coverage Report

```bash
# Generate HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html

# Open coverage report
# On Windows:
start htmlcov/index.html
# On Linux/Mac:
open htmlcov/index.html
```

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'pydantic'
```

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt
```

### Issue: MongoDB Connection Error

**Error:**
```
pymongo.errors.ServerSelectionTimeoutError
```

**Solution:**
- Start MongoDB: `mongod` (or use MongoDB service)
- Or set `MONGODB_URI` in `.env` file
- Or run tests without database (most tests work without it)

### Issue: Import Errors

**Error:**
```
ImportError: cannot import name 'X' from 'src.Y'
```

**Solution:**
```bash
# Ensure you're in the correct directory
cd bug-triage-agent

# Check Python path
python -c "import sys; print(sys.path)"

# Install package in development mode
pip install -e .
```

### Issue: Port Already in Use

**Error:**
```
ERROR: [Errno 48] Address already in use
```

**Solution:**
```bash
# Use different port
uvicorn src.main.app:app --reload --port 8001

# Or kill existing process
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
# On Linux/Mac:
lsof -ti:8000 | xargs kill
```

---

## Test Files Overview

| File | Purpose | Dependencies |
|------|---------|--------------|
| `tests/test_input_validation.py` | Input schema validation | pydantic |
| `tests/test_language_detection.py` | Language/file type detection | None |
| `tests/test_classification.py` | Bug classification engine | None |
| `tests/test_database_operations.py` | Database operations | pymongo, MongoDB |
| `tests/test_integration.py` | Full workflow integration | pydantic |
| `tests/test_all_phases.py` | All phases comprehensive | pydantic, pymongo |
| `tests/run_tests.py` | Custom test runner | pydantic, pymongo |

---

## Quick Start Commands

```bash
# 1. Setup (one time)
cd bug-triage-agent
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Run all tests
python -m pytest tests/ -v

# 3. Run custom test script
python tests/run_tests.py

# 4. Start server and test manually
uvicorn src.main.app:app --reload
# Then test endpoints in another terminal
```

---

## Expected Test Results

### Successful Test Run

- **Total Tests:** 15-20 tests
- **Passed:** 15-20 (100%)
- **Failed:** 0
- **Duration:** 2-5 seconds

### With Missing Dependencies

- **Total Tests:** 15-20 tests
- **Passed:** 8-10 (core functionality)
- **Failed:** 5-7 (database-dependent)
- **Note:** Code structure verified, functionality implemented

---

## Next Steps

After running tests:

1. **Review test results:** Check `test_results.json` and `docs/bug-triage-agent/test-results.md`
2. **Fix any failures:** Address issues in failed tests
3. **Improve coverage:** Add tests for edge cases
4. **Integration testing:** Test with actual supervisor when available
5. **Performance testing:** Run load tests with multiple requests

---

## Additional Resources

- **Test Results Documentation:** `docs/bug-triage-agent/test-results.md`
- **Implementation Plan:** `docs/bug-triage-agent/implementation-plan.md`
- **Progress Tracker:** `docs/bug-triage-agent/progress-tracker.md`

---

**Last Updated:** 2025-01-XX  
**Test Suite Version:** 1.0.0



