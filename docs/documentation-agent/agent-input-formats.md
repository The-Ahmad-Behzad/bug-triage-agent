Agent Input Formats

API Documentation Generator Agent This document outlines the API
specification for the Documentation Generator Agent, including its
endpoints and all valid input formats.

Agent Endpoints Health Check ● URL:
https://api-documentation-agent.onrender.com/health ● Method: GET ●
Description: A simple endpoint to verify that the agent is running.

Documentation Generation ● URL:
https://api-documentation-agent.onrender.com/execute ● Method: POST ●
Content-Type: application/json ● Description: The main endpoint that
receives a task assignment and generates documentation.

Agent Inputs Our Agent accepts three types of inputs:

1.  Code files (one or more)
2.  Zip file (whole project in zip format)
3.  Github repository link (HTTPS .git link)
4.  

Note: For each input scenario, the user can optionally provide
existing_documentation as a valid JSON object. If provided, the agent
will add new endpoints to this object. If it is null, the agent will
create a new documentation object from scratch.

Part 1: Agent Inputs (Without Existing Documentation) These examples
show how to generate new documentation from scratch.

1.  Github Repository Example (New) {​ "message_id": "sup-msg-123",​
    "sender": "supervisor",​ "recipient":
    "documentation_generator_agent",​ "type": "task_assignment",​
    "timestamp": "2025-11-15T12:00:00Z",​ "results/task": {​ "language":
    "javascript",​ "git_repo_url":
    "https://github.com/Taimoor-Raza-Asif/event-planer.git",​
    "existing_documentation": null,​ "search_patterns": null,​
    "zip_file_base64": null,​ "code_files_base64": null​ }​ }​

2.  Zip File Example (New) {​ "message_id": "sup-msg-456",​ "sender":
    "supervisor",​ "recipient": "documentation_generator_agent",​ "type":
    "task_assignment",​ "timestamp": "2025-11-15T12:00:00Z",​
    "results/task": {​ "language": "java",​ "zip_file_base64":
    "UEsDBBQA...\[the giant Base64 string\]...kQAAAAA=",​
    "existing_documentation": null,​ "search_patterns": null,​
    "git_repo_url": null,​ "code_files_base64": null​ }​ }​

3.  Code Files Example (New) {​ "message_id": "sup-msg-789",​ "sender":
    "supervisor",​ "recipient": "documentation_generator_agent",​ "type":
    "task_assignment",​ "timestamp": "2025-11-15T12:00:00Z",​
    "results/task": {​ "language": "python",​ "code_files_base64": \[​ {​
    "file_path": "routes/users.py",​ "content_base64":
    "ZGVmIGdldF91c2VycygpOgogICAgcGFzcw=="​ },​ {​ "file_path":
    "routes/products.py",​ "content_base64":
    "ZGVmIGdldF9wcm9kdWN0cygpOgogICAgcGFzcw=="​ }​ \],​
    "existing_documentation": null,​ "search_patterns": null,​
    "git_repo_url": null,​ "zip_file_base64": null​ }​ }​

Part 2: Agent Inputs (With Existing Documentation) These examples show
how to update existing documentation. The existing_documentation field
is populated with a JSON object.

1.  Github Repository Example (Update) {​ "message_id": "sup-msg-124",​
    "sender": "supervisor",​ "recipient":
    "documentation_generator_agent",​ "type": "task_assignment",​
    "timestamp": "2025-11-15T12:05:00Z",​ "results/task": {​ "language":
    "javascript",​ "git_repo_url":
    "https://github.com/Taimoor-Raza-Asif/event-planer.git",​
    "existing_documentation": {​ "openapi": "3.0.0",​ "info": {​ "title":
    "My Existing API",​ "version": "1.0.0"​ },​ "paths": {​
    "/api/v1/health": {​ "get": {​ "summary": "Health Check",​ "responses":
    {​ "200": {​ "description": "Service is healthy"​ }​ }​ }​ }​ }​ },​
    "search_patterns": null,​ "zip_file_base64": null,​
    "code_files_base64": null​ }​ }​

2.  Zip File Example (Update) {​ "message_id": "sup-msg-457",​ "sender":
    "supervisor",​ "recipient": "documentation_generator_agent",​ "type":
    "task_assignment",​ "timestamp": "2025-11-15T12:06:00Z",​
    "results/task": {​ "language": "java",​ "zip_file_base64":
    "UEsDBBQA...\[the giant Base64 string\]...kQAAAAA=",​
    "existing_documentation": {​ "openapi": "3.0.0",​ "info": {​ "title":
    "My Existing Java API",​ "version": "2.1.0"​ },​ "paths": {​
    "/api/v2/admin/status": {​ "get": {​ "summary": "Admin Health Check",​
    "responses": {​ "200": {​ "description": "Admin service is healthy"​ }​
    }​ }​ }​ }​ },​ "search_patterns": null,​ "git_repo_url": null,​
    "code_files_base64": null​ }​ }​

3.  Code Files Example (Update) {​ "message_id": "sup-msg-790",​ "sender":
    "supervisor",​ "recipient": "documentation_generator_agent",​ "type":
    "task_assignment",​ "timestamp": "2025-11-15T12:07:00Z",​
    "results/task": {​ "language": "python",​ "code_files_base64": \[​ {​
    "file_path": "routes/new_feature.py",​ "content_base64":
    "ZGVmIGdldF9mZWF0dXJlKCk6CgkgICAgcGFzcw=="​ }​ \],​
    "existing_documentation": {​ "openapi": "3.0.0",​ "info": {​ "title":
    "My Existing Python API",​ "version": "1.0.3"​ },​ "paths": {​
    "/api/v1/users": {​ "get": {​ "summary": "Get all users",​ "responses":
    {​ "200": {​ "description": "A list of users"​ }​ }​ }​ }​ }​ },​
    "search_patterns": null,​ "git_repo_url": null,​ "zip_file_base64":
    null​ }​ }​
