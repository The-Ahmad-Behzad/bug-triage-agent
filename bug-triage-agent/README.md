# Bug Triage AI Agent

The Bug Triage AI Agent is an AI-driven module that automatically classifies, prioritizes, and assigns software bugs to the most suitable team members.

## Features

- **Automatic Classification**: Categorizes bugs by type, category, and root cause
- **Priority Assessment**: Determines bug priority based on severity, environment, and impact
- **Intelligent Assignment**: Matches bugs to team members based on language expertise, skills, and workload
- **Fix Suggestions**: Provides actionable fix recommendations with effort estimates
- **Batch Processing**: Handles multiple bugs in a single request
- **Language Support**: Auto-detects programming language and file type for accurate assignment

## Quick Start

### Prerequisites

- Python 3.11+
- MongoDB 6.0+ (or Docker for containerized MongoDB)
- Virtual environment (recommended)

### Installation

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up MongoDB (using Docker - recommended):
   ```bash
   docker run -d --name mongodb -p 27017:27017 mongo:latest
   ```
   Alternatively, install MongoDB locally and ensure it's running on port 27017.
5. Copy environment template:
   ```bash
   cp .env.template .env
   ```
6. Configure `.env` with your MongoDB connection string (default: `mongodb://localhost:27017/`)
7. Run the agent:
   ```bash
   uvicorn src.main.app:app --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Health Check
```
GET /health
```
Returns agent status, database connectivity, uptime, and request totals.

### Execute Triage
```
POST /execute
```
Accepts handshake format input and returns triage results. See [sample-request.md](docs/bug-triage-agent/sample-request.md) for example payloads.

### Metrics
```
GET /metrics
```
Returns runtime metrics including request counts, success rates, latency statistics, and health check information. Useful for observability dashboards.

See API documentation at `/docs` (Swagger UI) or `/redoc` when the server is running.

## Testing

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m pytest tests/ -v

# Or use custom test script
python tests/run_tests.py
```

### Detailed Testing Guide
See [TESTING.md](TESTING.md) for comprehensive testing instructions.

### Quick Test Guide
See [QUICK_TEST.md](QUICK_TEST.md) for fast testing commands.

### Testing with Supervisor Mock

The agent includes a supervisor mock script for testing handshake compatibility:

```bash
# Test with backend scenario
python scripts/supervisor_mock.py --scenario backend

# Test with security scenario
python scripts/supervisor_mock.py --scenario security

# Save response to file
python scripts/supervisor_mock.py --scenario ui --save-response response.json

# Use custom host
python scripts/supervisor_mock.py --scenario performance --host http://localhost:8000
```

Available scenarios: `backend`, `ui`, `security`, `performance`

## Configuration

See `.env.template` for all configuration options.

## Development

See `docs/bug-triage-agent/implementation-plan.md` for detailed development plan.

## Documentation

- [Agent Specification](docs/bug-triage-agent/agent-specification.md)
- [Input/Output Schemas](docs/bug-triage-agent/input-output-schemas.md)
- [Database Schemas](docs/bug-triage-agent/database-schemas.md)
- [Implementation Plan](docs/bug-triage-agent/implementation-plan.md)
- [Progress Tracker](docs/bug-triage-agent/progress-tracker.md)

## License

[To be determined]

