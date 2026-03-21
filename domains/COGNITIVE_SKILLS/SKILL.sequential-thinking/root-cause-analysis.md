---
name: root-cause-analysis
description: Systematically trace problems to their fundamental causes using techniques like 5 Whys, fishbone diagrams, and causal chains
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "root-cause,rca,debugging,troubleshooting,5-whys"
---

# Root Cause Analysis

Find the fundamental reason behind a problem, not just symptoms.

## 5 Whys Method

```
Problem: API response time is 5 seconds

Why 1: Database query is slow
Why 2: Missing index on user_id column
Why 3: Schema was designed before user_id existed
Why 4: No code review for schema changes
Why 5: Database changes don't require review

ROOT CAUSE: Database changes bypass code review
```

## Fishbone (Ishikawa) Diagram

```
                    ┌─────────────┐
                    │   EFFECT    │
                    │   (Problem) │
                    └──────┬──────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐       ┌─────▼─────┐      ┌─────▼─────┐
   │ People  │       │ Process   │      │ Technology│
   ├─────────┤       ├───────────┤      ├───────────┤
   │ Training│       │ Procedure │      │ Tool      │
   │ Errors  │       │ Changes   │      │ Failures  │
   └─────────┘       └───────────┘      └───────────┘
```

## Causal Chain Tracing

```
Symptom: Users can't log in

Event Log:
├── 14:32 - User clicks login
├── 14:32 - Request sent to /auth
├── 14:32 - Auth service checks cache
├── 14:33 - Cache miss, query DB
├── 14:33 - DB connection timeout
└── 14:33 - Return 500 error

Chain:
1. Connection timeout → 
2. Pool exhausted (100 connections) →
3. Connections not released →
4. Code missing connection.close() →
5. Finally block not used

ROOT CAUSE: Missing finally block in retry logic
```

## Code Pattern: RCA Template

```python
class RootCauseAnalyzer:
    def __init__(self, problem: str):
        self.problem = problem
        self.symptoms = []
        self.causes = []
        self.root_cause = None
    
    def add_symptom(self, symptom: str):
        self.symptoms.append(symptom)
    
    def add_potential_cause(self, cause: str, evidence: str):
        self.causes.append({
            "cause": cause,
            "evidence": evidence,
            "verified": False
        })
    
    def verify_cause(self, cause_idx: int):
        self.causes[cause_idx]["verified"] = True
    
    def find_root_cause(self) -> str:
        # Root cause = verified cause with no deeper cause
        for cause in self.causes:
            if cause["verified"]:
                # Check if this cause has a parent
                if not self._has_parent(cause):
                    self.root_cause = cause["cause"]
                    return cause["cause"]
        return "Not found"
    
    def _has_parent(self, cause) -> bool:
        # Recursive check
        return any(c["cause"] in cause["evidence"] 
                   for c in self.causes if c != cause)
```

## Example: Production Incident

```
INCIDENT: Payment processing failed for 15% of users

Timeline Analysis:
14:00 - Deploy v2.1.0
14:05 - Alerts fire: high payment failure rate
14:15 - Rollback to v2.0.9
14:20 - Failure rate returns to normal

Investigation:
├── Code diff v2.0.9 → v2.1.0
│   └── Changed payment provider SDK
├── Logs analysis
│   └── New SDK returns different error format
├── Database check
│   └── No schema changes
└── Config check
    └── Environment variables unchanged

ROOT CAUSE: New SDK version has breaking change
            in error response parsing

Fix: Update error handling to match new SDK format
```

## Decision: Fix vs. Mitigate

| Situation | Action |
|-----------|--------|
| Root cause found | Fix |
| Root cause unknown | Investigate more |
| Fix too expensive | Mitigate + track |
| One-time issue | Monitor |
| Systemic problem | Add to tech debt |
