# Bug Triage Agent - Agent Interactions

## Directly Interacting Agents

These agents either produce bug-relevant input or need bug classification output:

### ✅ Primary Interactions

#### 1. Code Reviewer Agent
- **Interaction Type:** Direct
- **Why:** Identifies bugs, vulnerabilities, and code smells
- **Flow:** Code Reviewer → Supervisor → Bug Triage Agent
- **Data:** Code review findings converted to bug reports

#### 2. Security Vulnerability Agent
- **Interaction Type:** Direct
- **Why:** Detects vulnerabilities and misconfigurations that need prioritization
- **Flow:** Security Vulnerability Agent → Supervisor → Bug Triage Agent
- **Data:** Vulnerability reports triaged by severity and priority

#### 3. Dependency Health Agent
- **Interaction Type:** Direct
- **Why:** Reports outdated/vulnerable dependencies that cause bugs
- **Flow:** Dependency Health Agent → Supervisor → Bug Triage Agent
- **Data:** Dependency issues assigned automatically

#### 4. API Contract Enforcer Agent
- **Interaction Type:** Direct
- **Why:** Contract mismatches produce real bugs that need classification
- **Flow:** API Contract Enforcer → Supervisor → Bug Triage Agent
- **Data:** Contract violations classified and assigned

#### 5. Architecture Compliance Agent
- **Interaction Type:** Direct
- **Why:** Structural violations are categorized as architecture bugs
- **Flow:** Architecture Compliance Agent → Supervisor → Bug Triage Agent
- **Data:** Architecture violations classified and prioritized

### ⚠️ Conditional Interactions

#### 6. Test Coverage Agent
- **Interaction Type:** Maybe (conditional)
- **Why:** Only when coverage gaps or test failures become issues
- **Flow:** Test Coverage Agent → Supervisor → Bug Triage Agent (if failures detected)
- **Condition:** Only triggers when test failures are reported

#### 7. Pair Programming Agent
- **Interaction Type:** Maybe (conditional)
- **Why:** Can send detected issues for triage
- **Flow:** Pair Programming Agent → Supervisor → Bug Triage Agent
- **Condition:** Optional integration for issue detection

#### 8. CI/CD Guardian Agent
- **Interaction Type:** Maybe (conditional)
- **Why:** Pipeline failures can be triaged as bugs
- **Flow:** CI/CD Guardian → Supervisor → Bug Triage Agent
- **Condition:** When pipeline failures need assignment

### ❌ No Direct Interaction

These agents do not produce bug reports:
- **Dev Onboarding Agent** - Not bug-related
- **Documentation Generator Agent** - Not bug-related
- **Knowledge Graph Builder Agent** - No bugs produced
- **Backend Test Cases Generator Agent** - Does not detect bugs
- **Supervisor Agent** - Only orchestrates workflow (does not produce bug data)

## Interaction Summary Table

| Agent | Interaction | Type | Reason |
|-------|------------|------|--------|
| Code Reviewer | ✅ Yes | Direct | Produces bug-like findings |
| Security Vulnerability Agent | ✅ Yes | Direct | Vulnerabilities need prioritization |
| Dependency Health Agent | ✅ Yes | Direct | Dependency issues → fixable bugs |
| API Contract Enforcer | ✅ Yes | Direct | Contract violations are bugs |
| Architecture Compliance Agent | ✅ Yes | Direct | Architecture violations categorized as bugs |
| Test Coverage Agent | ⚠️ Maybe | Conditional | Only when failures/gaps become issues |
| Pair Programming Agent | ⚠️ Maybe | Conditional | Produces small issues |
| CI/CD Guardian Agent | ⚠️ Maybe | Conditional | Pipeline failures can be triaged |
| Documentation Generator Agent | ❌ No | None | Not bug-related |
| Knowledge Graph Builder Agent | ❌ No | None | No bugs |
| Dev Onboarding Agent | ❌ No | None | Not relevant |
| Backend Test Cases Generator | ❌ No | None | Does not detect bugs |
| Supervisor Agent | ❌ No | None | Only orchestrates workflow |

## Communication Flow

```
[Source Agent] → [Supervisor] → [Bug Triage Agent] → [Supervisor] → [Target/Storage]
```

**Key Points:**
- All agent-to-agent communication goes through the Supervisor
- Supervisor handles format conversion and validation
- Bug Triage Agent only validates its own input requirements
- Supervisor maintains compatibility between agents



