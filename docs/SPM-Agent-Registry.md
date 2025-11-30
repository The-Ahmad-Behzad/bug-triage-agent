# SPM Agent Registry

This document contains a comprehensive registry of all agents in the SPM (Software Project Management) system.

## Agent Registry Table

| Agent Name | Agent Description | Data Input | Data Output |
|------------|-------------------|------------|-------------|
| Supervisor Agent | Orchestrates and coordinates all worker agents, manages task distribution and workflow | - | - |
| Dev Onboarding Agent | Generates starter tasks for new developers | - | - |
| Dependency Health Agent | Dependency Health Agent is a system that tracks software dependencies, detects vulnerabilities, automates alerts, and integrates with development pipelines to help teams keep their software secure and up-to-date efficiently | whole projects or files | Health dependency report in json; includes dependency name, version, latest version, healthScore, riskLevel |
| Code Reviewer | The Code Reviewer Agent is an autonomous AI system that: Analyzes source code in Python, Java, and JavaScript; Identifies bugs, vulnerabilities, and quality issues; Provides actionable improvement suggestions; Learns from historical code review patterns; Integrates with version control and CI/CD pipelines | - | - |
| Test data Generator | It will generate test data for testing the system and ensuring quality | - | - |
| Test coverage agent | The Test Coverage Agent analyzes a project's source code to check how much of it is covered by tests. It finds untested or poorly tested parts of the code and suggests test cases to improve overall test coverage. | Source code files, existing test cases | Coverage report with missing steps and automatically suggested new test cases |
| CI/CD Guardian Agent | Adapts pipelines if frequent failures occur. | - | - |
| Documentation Generator Agent | The agent works automatically and can be integrated into CI/CD pipelines. It helps developers and project managers quickly see coverage gaps through easy-to-understand reports. | Whole project or repository | Documented Api Endpoints file by files and merged version of files too. |
| Knowledge Graph Builder Agent | Knowledge Graph Builder Agent that automatically parses Python repositories to extract modules, dependencies, and ownership, then constructs a visual knowledge graph in Neo4j. The system includes a natural language interface to answer impact-analysis queries for developers and architects. | - | - |
| API Contract Enforcer Agent | An API Contract Enforcer Agent ensures that API requests and responses strictly follow the defined contract. It prevents breaking changes by validating schemas and enforcing consistency during development, testing, and runtime. | OpenAPI 3.x or Swagger 2.0 contract (JSON format), API requests to validate (array of request objects), Mode selection: validate/train/report | Validation results with violation details, Compliance score and statistics, Action recommendations (allow/throttle/block), Alerts for critical violations, ML-based anomaly detection results |
| Security Vulnerability Agent | A tool that automatically scans systems, applications, or networks to detect and report potential security weaknesses, misconfigurations, or vulnerabilities that could be exploited by attackers | whole project / configurations file | Vulnerability report in JSON, it will include vulnerability name, severity level etc. |
| Architecture Compliance Agent | To ensure proper architecture structure, compatibilty and compliance is followed | whole project | report on the structure and architectural compliance of the project |
| Pair Programmiing Agent | It's an AI assistant for programmers that works with them like a partner ("pair programmer"). | Python or JavaScript code files (up to 500 lines) | JSON report including: detected errors with line numbers and severity levels (critical/warning/info), plain-language code explanations, debugging guidance with examples, and code quality metrics (0-100 score) |
| Bug Triage AI Agent | The Bug Triage Agent is an AI-driven module that automatically classifies, prioritizes, and assigns software bugs to the most suitable team members | Bug reports (title, description, steps to reproduce, stack traces, logs), code context (source files, snippets, file paths, line numbers), language/file type (programming language and file extension - auto-detected if not provided), team profiles (member skills including languages, frameworks, domains, ownership, current workload), metadata (environment, tags, reporter information) | JSON report with classification (category, type, root cause analysis), priority (level with justification), assignment (recommended team member with confidence score), suggested fix (approach and estimated effort), confidence scores (for classification, priority, assignment, and overall) |
| Backend Test Cases Generator Agent | an intelligent assistant designed to streamline the creation, maintenance, and execution of backend-focused test cases. | - | - |

## Notes

- This registry includes all agents in the SPM system
- Agents marked with "-" in Data Input or Data Output columns have specifications that are still being developed or are managed by other teams
- The Bug Triage AI Agent is the focus of current development efforts
- All agents communicate using the Supervisor handshake format



