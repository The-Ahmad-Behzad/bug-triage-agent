# Bug Triage AI Agent - MongoDB Database Schemas

## Overview

The Bug Triage AI Agent uses MongoDB for local memory storage. This document defines all collection schemas in Mongoose-style JSON format (compatible with raw MongoDB).

---

## 1. Collection: `team_members`

Stores all developer profiles with skills, ownership, and performance metrics.

```json
{
  "_id": "ObjectId",
  "member_id": "String",       // "dev-01"
  "name": "String",
  "email": "String",
  "skills": {
    "languages": ["String"],   // ["python", "java", "javascript"]
    "frameworks": ["String"],  // ["django", "spring", "react"]
    "domains": ["String"]      // ["backend", "frontend", "security"]
  },
  "modules_owned": ["String"],  // ["auth", "session"]
  "primary_stack": "String",    // "backend"
  "experience_years": "Number",
  "past_bugs_fixed": "Number",
  "workload": {
    "open_assigned_bugs": "Number",
    "current_sprint_tasks": "Number",
    "availability_score": "Number"   // 0–1
  },
  "performance_metrics": {
    "avg_fix_time_hours": "Number",
    "reopen_rate": "Number",
    "critical_issue_success_rate": "Number"
  },
  "preferences": {
    "prefers_security_tickets": "Boolean",
    "prefers_maintenance": "Boolean"
  },
  "last_active": "Date",
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `member_id` (unique)
- `skills.languages` (for language-based queries)
- `modules_owned` (for module-based queries)

---

## 2. Collection: `module_ownership`

Defines each module and its owners with tech stack information.

```json
{
  "_id": "ObjectId",
  "module_name": "String",      // "auth"
  "owners": ["String"],         // ["dev-01", "dev-02"]
  "tech_stack": ["String"],     // ["java", "spring", "postgresql"]
  "primary_language": "String", // "java" (for quick lookup)
  "risk_level": "String",       // "high", "medium", "low"
  "recent_bugs": "Number",
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `module_name` (unique)
- `primary_language` (for language-based routing)
- `owners` (for owner queries)

---

## 3. Collection: `historical_bugs`

Stores resolved bugs that help the model learn patterns and improve classification.

```json
{
  "_id": "ObjectId",
  "bug_id": "String",          // "HIST-001"
  "title": "String",
  "description": "String",
  "category": "String",        // "Runtime Error"
  "type": "String",            // "NullPointerException"
  "root_cause": "String",
  "module": "String",          // "auth"
  "language": "String",        // "java"
  "file_type": "String",       // ".java"
  "resolved_by": "String",     // member_id
  "resolution_time_hours": "Number",
  "date_resolved": "Date",
  "input_signature": {
    "embedding_id": "ObjectId"  // optional: hash of text for similarity search
  },
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `bug_id` (unique)
- `category`, `type` (for classification queries)
- `language` (for language-based matching)
- `module` (for module-based queries)
- `resolved_by` (for developer performance)

---

## 4. Collection: `severity_priority_rules`

Defines how severity maps to priority with conditions.

```json
{
  "_id": "ObjectId",
  "severity": "String",          // "crash", "security_vulnerability"
  "priority": "String",          // "critical", "high", etc.
  "conditions": ["String"],      // ["production", "public_exploit"]
  "auto_assign": "Boolean",
  "language_specific": "Boolean", // if true, applies only to specific languages
  "languages": ["String"],       // ["java", "python"] if language_specific
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `severity`, `priority` (for rule lookup)
- `language_specific`, `languages` (for language-based rules)

---

## 5. Collection: `developer_load`

Tracks dynamic developer workload and availability.

```json
{
  "_id": "ObjectId",
  "member_id": "String",
  "current_load_score": "Number",    // 0–1
  "recent_activity": "String",       // "active", "idle"
  "focus_area": ["String"],          // current focus areas
  "active_languages": ["String"],    // languages currently working on
  "burnout_risk_estimate": "Number", // 0–1
  "updated_at": "Date"
}
```

**Indexes:**
- `member_id` (unique)
- `current_load_score` (for workload balancing)
- `active_languages` (for language-based assignment)

---

## 6. Collection: `embeddings`

Stores vector embeddings for similarity search of historical bugs.

```json
{
  "_id": "ObjectId",
  "bug_id": "String",       // link to historical bug
  "vector": ["Number"],     // embedding array (e.g., 384 dimensions)
  "model": "String",        // "MiniLM-L6-v2" or "all-MiniLM-L6-v2"
  "text_content": "String", // original text used for embedding
  "last_trained": "Date",
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `bug_id` (unique)
- Vector index (for similarity search - requires MongoDB Atlas Vector Search or similar)

---

## 7. Collection: `routing_rules`

Assignment rules and policy overrides for specific scenarios.

```json
{
  "_id": "ObjectId",
  "rule_type": "String",             // "security", "database", "language"
  "assign_to": ["String"],           // ["dev-sec-01"]
  "auto_escalate": "Boolean",
  "conditions": {
    "severity": ["String"],
    "modules": ["String"],
    "tags": ["String"],
    "languages": ["String"],          // language-specific routing
    "file_types": ["String"]         // file type-specific routing
  },
  "priority": "Number",              // rule priority (higher = more important)
  "created_at": "Date",
  "updated_at": "Date"
}
```

**Indexes:**
- `rule_type` (for rule lookup)
- `conditions.languages` (for language-based routing)
- `priority` (for rule ordering)

---

## 8. Collection: `triage_history`

Stores all triage decisions made by the agent for audit, learning, and improvement.

```json
{
  "_id": "ObjectId",
  "bug_id": "String",
  "language": "String",              // detected/input language
  "file_type": "String",            // detected/input file type
  "classification": {
    "category": "String",
    "type": "String",
    "root_cause": "String"
  },
  "priority": {
    "level": "String",
    "justification": "String"
  },
  "assignment": {
    "member_id": "String",
    "confidence": "Number"
  },
  "suggested_fix": {
    "approach": "String",
    "estimated_effort": "String"
  },
  "confidence_scores": {
    "classification_confidence": "Number",
    "priority_confidence": "Number",
    "assignee_confidence": "Number",
    "overall_confidence": "Number"
  },
  "raw_input": "Object",        // what supervisor sent
  "raw_output": "Object",       // what agent returned
  "timestamp": "Date",
  "feedback": {                  // optional: human feedback
    "correct_assignment": "Boolean",
    "correct_priority": "Boolean",
    "notes": "String"
  }
}
```

**Indexes:**
- `bug_id` (unique)
- `timestamp` (for time-based queries)
- `assignment.member_id` (for developer performance)
- `language` (for language-based analytics)
- `classification.category` (for category analytics)

---

## Relationships Overview

| Collection | Relationship |
|------------|--------------|
| `team_members` | Member → owned modules (`module_ownership`) |
| `module_ownership` | Module → multiple owners, tech stack |
| `historical_bugs` | May link to `embeddings`, resolved by `team_members` |
| `developer_load` | Member load state (references `team_members.member_id`) |
| `routing_rules` | Global routing policies (may reference languages) |
| `triage_history` | Trace of all triage decisions (references bugs, members) |

---

## Key Design Decisions

1. **Language/File Type Support:**
   - Added `language` and `file_type` fields to `historical_bugs` and `triage_history`
   - Added `primary_language` to `module_ownership` for quick lookup
   - Added `active_languages` to `developer_load` for current work tracking
   - Added language conditions to `routing_rules` and `severity_priority_rules`

2. **Skills Structure:**
   - Separated `skills` into `languages`, `frameworks`, and `domains` for better matching
   - Allows precise matching of bug language to developer language expertise

3. **Performance Tracking:**
   - `team_members.performance_metrics` tracks developer effectiveness
   - `triage_history.feedback` allows learning from human corrections

4. **Similarity Search:**
   - `embeddings` collection enables finding similar historical bugs
   - Improves classification accuracy through pattern matching

---

## Database Initialization

The agent should:
1. Create all collections if they don't exist
2. Create indexes for performance
3. Seed initial data (routing rules, severity rules) if needed
4. Validate schema on startup



