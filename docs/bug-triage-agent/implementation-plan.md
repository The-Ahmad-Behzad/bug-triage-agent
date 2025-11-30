# Bug Triage AI Agent - Detailed Implementation Plan

This document provides a detailed, step-by-step implementation plan for the Bug Triage AI Agent with testing and verification at each phase.

---

## Phase 0: Documentation and Setup ✅

### Tasks Completed
1. ✅ Created agent specification documentation
2. ✅ Created input/output schema documentation  
3. ✅ Created agent interactions documentation
4. ✅ Created database schemas documentation
5. ✅ Created cloud deployment guide
6. ✅ Added Bug Triage Agent to SPM Agent Registry
7. ✅ Created progress tracker document
8. ✅ Created implementation plan document (this file)

### Verification
- ✅ Registry table is complete and properly formatted
- ✅ Progress tracker document exists with proper structure
- ✅ Implementation plan document exists with all phases

---

## Phase 1: Project Structure and Core Setup

### Tasks

1. **Initialize Project Structure**
   - Create main agent directory: `bug-triage-agent/`
   - Create subdirectories:
     - `src/` - Main source code
     - `src/main/` - Entry point and API routes
     - `src/handlers/` - Request handlers
     - `src/models/` - Data models (Pydantic, MongoDB)
     - `src/engines/` - Core engines (classification, priority, assignment, fix)
     - `src/database/` - Database operations
     - `src/utils/` - Utility functions
     - `tests/` - Test files
     - `config/` - Configuration files
   - Create `requirements.txt` with dependencies
   - Create `README.md` template
   - Create `.gitignore`

2. **Set Up Development Environment**
   - Create virtual environment: `python -m venv venv`
   - Install base dependencies:
     - FastAPI (web framework)
     - Uvicorn (ASGI server)
     - Pydantic (data validation)
     - pymongo (MongoDB driver)
     - python-dotenv (environment variables)
     - pytest (testing)
   - Set up logging configuration:
     - Create `config/logging.yaml` or `config/logging.json`
     - Configure structured logging
     - Set log levels (DEBUG, INFO, WARNING, ERROR)
   - Create `.env.template` with required variables:
     - `MONGODB_URI`
     - `MONGODB_DB_NAME`
     - `AGENT_NAME`
     - `AGENT_VERSION`
     - `LOG_LEVEL`

3. **Implement Basic Health Check Endpoint**
   - Create `src/main/app.py` with FastAPI app
   - Create `/health` endpoint:
     - Return agent status (healthy/unhealthy)
     - Return agent version
     - Return timestamp
   - Basic error handling middleware
   - CORS configuration (if needed)

### Testing/Verification
- [ ] Project structure follows best practices
- [ ] All directories created correctly
- [ ] Dependencies install without errors (`pip install -r requirements.txt`)
- [ ] Virtual environment activates correctly
- [ ] Health check endpoint responds correctly:
  ```bash
  curl http://localhost:8000/health
  ```
- [ ] Logging works properly (check log files)
- [ ] Environment variables load correctly

### Documentation
- Create `docs/bug-triage-agent/phase-1-setup.md` after completion

---

## Phase 2: Input/Output Schema and Validation

### Tasks

1. **Implement Input Schema Models**
   - Create `src/models/input_models.py`:
     - `HandshakeMessage` - Root message structure
     - `TaskAssignment` - Task object
     - `BugInput` - Bug object with language/file_type
     - `CodeContext` - Code context object
     - `Metadata` - Metadata object
     - `TeamProfile` - Team profile with structured skills
   - Validate handshake format (message_id, sender, recipient, type, timestamp)
   - Validate task structure (bugs array, team_profiles array)
   - Validate bug objects with required fields

2. **Implement Language/File Type Detection**
   - Create `src/utils/language_detector.py`:
     - `detect_language_from_path(file_path: str) -> str`
     - `detect_file_type_from_path(file_path: str) -> str`
     - `validate_language_file_type_consistency(language: str, file_type: str) -> bool`
   - Map file extensions to languages:
     - `.py` → `python`
     - `.java` → `java`
     - `.js` → `javascript`
     - `.ts` → `typescript`
     - `.tsx` → `typescript`
     - etc.
   - Auto-detect if not provided in input

3. **Implement Output Schema Models**
   - Create `src/models/output_models.py`:
     - `TriageResponse` - Root response structure
     - `TriageResult` - Individual triage result
     - `Classification` - Classification object
     - `Priority` - Priority object
     - `Assignment` - Assignment object
     - `SuggestedFix` - Fix suggestion object
     - `ConfidenceScores` - Confidence scores object

4. **Implement Validation Logic**
   - Create `src/utils/validators.py`:
     - `validate_input(data: dict) -> tuple[bool, str]`
     - `validate_output(data: dict) -> tuple[bool, str]`
     - `validate_bug_object(bug: dict) -> tuple[bool, str]`
     - `validate_team_profiles(profiles: list) -> tuple[bool, str]`
   - Error handling for invalid inputs
   - Return clear error messages

### Testing/Verification
- [ ] Input schema validates correct inputs
- [ ] Input schema rejects invalid inputs with clear errors:
  - Missing required fields
  - Invalid types
  - Invalid values
- [ ] Language/file type auto-detection works:
  - Test with various file paths
  - Test with missing language/file_type
- [ ] Language/file type consistency validation works
- [ ] Output schema generates valid JSON
- [ ] Unit tests for all validation functions:
  - `tests/test_input_validation.py`
  - `tests/test_output_validation.py`
  - `tests/test_language_detection.py`

### Documentation
- Create `docs/bug-triage-agent/phase-2-schemas.md` after completion

---

## Phase 3: MongoDB Database Setup and Team Member Management

### Tasks

1. **Set Up MongoDB Connection**
   - Create `src/database/connection.py`:
     - `get_mongodb_client() -> MongoClient`
     - `get_database() -> Database`
     - Connection pooling configuration
     - Error handling for connection failures
   - Install pymongo: `pip install pymongo`
   - Configure connection string from environment

2. **Implement Database Schema Models**
   - Create `src/database/models.py` with 8 collection schemas:
     - `team_members` - Developer profiles
     - `module_ownership` - Module ownership
     - `historical_bugs` - Resolved bugs
     - `severity_priority_rules` - Priority rules
     - `developer_load` - Workload tracking
     - `embeddings` - Vector embeddings
     - `routing_rules` - Assignment rules
     - `triage_history` - Decision audit trail
   - Create Pydantic models for each collection
   - Define indexes for performance

3. **Implement Database Operations**
   - Create `src/database/team_members.py`:
     - `create_team_member(member_data: dict) -> str`
     - `get_team_member(member_id: str) -> dict`
     - `update_team_member(member_id: str, updates: dict) -> bool`
     - `query_by_language(language: str) -> list[dict]`
     - `query_by_skills(skills: list) -> list[dict]`
     - `query_by_module(module: str) -> list[dict]`
   - Create `src/database/module_ownership.py`:
     - `get_module_owners(module: str) -> list[str]`
     - `get_modules_by_language(language: str) -> list[str]`
   - Create `src/database/developer_load.py`:
     - `get_developer_load(member_id: str) -> dict`
     - `update_developer_load(member_id: str, load_data: dict) -> bool`

4. **Implement Team Profile Loading**
   - Create `src/utils/team_profile_loader.py`:
     - `load_and_merge_profiles(input_profiles: list, db_profiles: list) -> list[dict]`
     - Handle missing profiles gracefully
     - Merge skills from input with database

5. **Database Initialization**
   - Create `src/database/init.py`:
     - `initialize_database() -> bool`
     - Create collections if they don't exist
     - Create all indexes
     - Seed initial data (routing rules, severity rules)

### Testing/Verification
- [ ] MongoDB connection works correctly
- [ ] All collections are created with proper indexes
- [ ] CRUD operations work as expected:
  - Create team member
  - Read team member
  - Update team member
  - Delete team member (if needed)
- [ ] Query functions return correct results:
  - Query by language
  - Query by skills
  - Query by module
- [ ] Team profile loading and merging works
- [ ] Database initialization is idempotent (can run multiple times)
- [ ] Unit tests for all database operations:
  - `tests/test_database_operations.py`
  - `tests/test_team_members.py`
  - `tests/test_module_ownership.py`
- [ ] Integration tests with MongoDB:
  - Use test database
  - Clean up after tests

### Documentation
- Create `docs/bug-triage-agent/phase-3-database.md` after completion

---

## Phase 4: Bug Classification Engine

### Tasks

1. **Implement Classification Logic**
   - Create `src/engines/classification.py`:
     - `classify_bug(bug: dict, code_context: dict) -> dict`
     - Category detection:
       - Runtime Error
       - Security Vulnerability
       - Performance Issue
       - UX/UI Issue
       - Logic Error
       - Configuration Error
     - Type detection (specific error types)
     - Root cause analysis using code context

2. **Implement Code Context Analysis**
   - Create `src/utils/code_analyzer.py`:
     - `parse_code_snippet(snippet: str) -> dict`
     - `extract_error_patterns(stack_trace: str) -> list[str]`
     - `match_patterns_in_code(patterns: list, code: str) -> bool`
     - Analyze file paths for module detection

3. **Implement Confidence Scoring**
   - Calculate classification confidence:
     - Higher if code context available
     - Higher if stack trace is clear
     - Lower if description is vague
   - Return confidence score (0.0-1.0)

### Testing/Verification
- [ ] Classification works for various bug types:
  - Runtime errors
  - Security issues
  - Performance problems
  - Logic errors
- [ ] Code context improves classification accuracy
- [ ] Confidence scores are reasonable (0.0-1.0)
- [ ] Handles edge cases:
  - Missing code context
  - Unclear descriptions
  - Ambiguous stack traces
- [ ] Unit tests with sample bugs:
  - `tests/test_classification.py`
- [ ] Integration tests with real-world examples

### Documentation
- Create `docs/bug-triage-agent/phase-4-classification.md` after completion

---

## Phase 5: Priority Assessment Engine

### Tasks

1. **Implement Priority Logic**
   - Create `src/engines/priority.py`:
     - `assess_priority(bug: dict, classification: dict) -> dict`
     - Define priority levels: critical, high, medium, low
     - Consider factors:
       - Environment (production = higher priority)
       - Impact (crash = critical)
       - Severity (from classification)
       - Metadata tags
     - Query `severity_priority_rules` collection

2. **Implement Justification Generation**
   - Generate clear justification text
   - Explain reasoning for priority level
   - Reference specific factors

3. **Implement Priority Confidence Scoring**
   - Calculate confidence in priority assessment
   - Consider available information quality

### Testing/Verification
- [ ] Priority levels assigned correctly:
  - Production bugs get higher priority
  - Critical errors identified correctly
  - Security issues prioritized appropriately
- [ ] Justifications are clear and accurate
- [ ] Confidence scores reflect uncertainty appropriately
- [ ] Unit tests for priority logic:
  - `tests/test_priority.py`

### Documentation
- Create `docs/bug-triage-agent/phase-5-priority.md` after completion

---

## Phase 6: Team Member Assignment Engine

### Tasks

1. **Implement Language-Based Matching**
   - Create `src/engines/assignment.py`:
     - `match_by_language(bug_language: str, team_members: list) -> list[dict]`
     - Query MongoDB by `skills.languages`
     - Prioritize developers with matching language expertise
     - Consider file_type for framework-specific matching

2. **Implement Assignment Algorithm**
   - `assign_bug(bug: dict, team_profiles: list, db: Database) -> dict`
   - Match bugs to team members by:
     - Language expertise (highest priority)
     - Skills (frameworks, domains)
     - Module ownership
     - Current workload
   - Calculate assignment confidence

3. **Implement Skill Matching**
   - `match_by_skills(bug: dict, team_members: list) -> list[dict]`
   - Parse bug requirements from description and code context
   - Match against team member skills
   - Weight language match higher than other skills

4. **Implement Workload Balancing**
   - `balance_workload(candidates: list, db: Database) -> dict`
   - Query `developer_load` collection
   - Consider `availability_score` from `team_members`
   - Distribute work evenly but prioritize expertise for critical bugs
   - Update `developer_load` after assignment

5. **Implement Routing Rules Application**
   - `apply_routing_rules(bug: dict, db: Database) -> dict | None`
   - Check `routing_rules` collection
   - Apply language-specific rules
   - Override normal assignment if routing rule applies

### Testing/Verification
- [ ] Language-based matching works correctly
- [ ] Assignments prioritize language expertise
- [ ] Module owners get relevant bugs
- [ ] Workload is considered appropriately
- [ ] Routing rules are applied correctly
- [ ] Assignment confidence reflects match quality
- [ ] Unit tests for assignment logic:
  - `tests/test_assignment.py`
- [ ] Integration tests with MongoDB queries

### Documentation
- Create `docs/bug-triage-agent/phase-6-assignment.md` after completion

---

## Phase 7: Fix Suggestion Engine

### Tasks

1. **Implement Fix Approach Generation**
   - Create `src/engines/fix_suggestion.py`:
     - `suggest_fix(bug: dict, classification: dict, code_context: dict) -> dict`
     - Analyze bug and code context
     - Generate actionable fix suggestions
     - Use pattern matching or AI/ML model

2. **Implement Effort Estimation**
   - `estimate_effort(bug: dict, classification: dict, fix_approach: str) -> str`
   - Estimate time required (hours/days)
   - Consider bug complexity
   - Factor in code context availability
   - Provide range estimates (e.g., "2-4 hours")

### Testing/Verification
- [ ] Fix suggestions are actionable
- [ ] Suggestions match bug type
- [ ] Effort estimates are reasonable
- [ ] Handles various bug categories
- [ ] Unit tests for fix generation:
  - `tests/test_fix_suggestion.py`

### Documentation
- Create `docs/bug-triage-agent/phase-7-fix-suggestions.md` after completion

---

## Phase 8: Main Agent Endpoint and Orchestration

### Tasks

1. **Implement Main Execute Endpoint**
   - Create `/execute` endpoint in `src/main/app.py`
   - Accept handshake format input
   - Orchestrate all engines:
     - Classification
     - Priority
     - Assignment
     - Fix suggestion
   - Generate complete output
   - Return in handshake format

2. **Implement Batch Processing**
   - Handle multiple bugs in one request
   - Process in parallel or sequentially
   - Aggregate results
   - Handle partial failures gracefully

3. **Implement Error Handling**
   - Handle invalid inputs gracefully
   - Handle processing errors
   - Return appropriate error responses
   - Log errors properly

### Testing/Verification
- [ ] Endpoint accepts valid handshake format
- [ ] Processes single bug correctly
- [ ] Processes multiple bugs correctly
- [ ] Returns proper error messages
- [ ] All engines work together
- [ ] Integration tests with full workflow:
  - `tests/test_integration.py`
- [ ] Performance testing with batch requests

### Documentation
- Create `docs/bug-triage-agent/phase-8-orchestration.md` after completion

---

## Phase 9: Integration with Supervisor

### Tasks

1. **Implement Supervisor Communication**
   - Ensure handshake format compatibility
   - Test with supervisor mock
   - Handle supervisor responses

2. **Implement Message Handling**
   - Parse supervisor messages
   - Generate proper response format
   - Handle `related_message_id`

3. **Integration Testing**
   - Test with actual supervisor (if available)
   - Test with supervisor mock
   - Verify format compatibility

### Testing/Verification
- [ ] Handshake format matches supervisor expectations
- [ ] Messages are parsed correctly
- [ ] Responses are in correct format
- [ ] Integration tests pass
- [ ] Works with supervisor mock

### Documentation
- Create `docs/bug-triage-agent/phase-9-integration.md` after completion

---

## Phase 10: Logging, Monitoring, and Health Checks

### Tasks

1. **Implement Comprehensive Logging**
   - Log all requests and responses
   - Log processing steps
   - Log errors with context
   - Structured logging format (JSON)

2. **Implement Monitoring**
   - Track processing times
   - Track success/failure rates
   - Track confidence score distributions
   - Create `/metrics` endpoint

3. **Enhance Health Check**
   - Check database connectivity
   - Check model availability
   - Return detailed status

### Testing/Verification
- [ ] Logs are comprehensive and useful
- [ ] Monitoring metrics are accurate
- [ ] Health check reflects true status
- [ ] Logs help with debugging

### Documentation
- Create `docs/bug-triage-agent/phase-10-monitoring.md` after completion

---

## Phase 11: Testing and Quality Assurance

### Tasks

1. **Comprehensive Unit Testing**
   - Test all individual functions
   - Test edge cases
   - Achieve >80% code coverage
   - Use pytest

2. **Integration Testing**
   - Test full workflow
   - Test with various bug types
   - Test batch processing
   - Test error scenarios

3. **Performance Testing**
   - Test response times
   - Test batch processing performance
   - Optimize bottlenecks

4. **End-to-End Testing**
   - Test complete agent functionality
   - Test with realistic scenarios
   - Validate output quality

### Testing/Verification
- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] Performance meets requirements (<2s per bug)
- [ ] End-to-end tests pass
- [ ] Code coverage >80%

### Documentation
- Create `docs/bug-triage-agent/phase-11-testing.md` after completion

---

## Phase 12: Documentation and Deployment Preparation

### Tasks

1. **Create API Documentation**
   - Document all endpoints
   - Provide request/response examples
   - Use FastAPI auto-docs (Swagger/OpenAPI)

2. **Create README**
   - Setup instructions
   - Configuration guide
   - Usage examples
   - Troubleshooting

3. **Create Deployment Guide**
   - Local deployment steps
   - Docker setup
   - Environment variables
   - Health check configuration

4. **Finalize All Documentation**
   - Review all phase documentation
   - Update progress tracker
   - Create final summary

### Testing/Verification
- [ ] Documentation is complete
- [ ] README is clear and accurate
- [ ] Deployment guide works
- [ ] All examples are tested

### Documentation
- Create `docs/bug-triage-agent/phase-12-documentation.md` after completion

---

## Key Principles

- **Focus:** ONLY Bug Triage AI Agent
- **Testing:** Every phase includes verification
- **Documentation:** Phase docs after each milestone
- **Progress Tracking:** Updated continuously
- **Compatibility:** Works with supervisor handshake format
- **Language Support:** Explicit language/file_type fields for accurate assignment

---

## Technology Stack

- **Framework:** FastAPI
- **Database:** MongoDB (with pymongo)
- **Validation:** Pydantic
- **Testing:** pytest
- **Logging:** Python logging (structured)
- **Deployment:** Docker (recommended)

---

## Next Steps

1. Complete Phase 0 (Documentation) ✅
2. Begin Phase 1 (Project Structure)
3. Follow phases sequentially
4. Update progress tracker after each phase



