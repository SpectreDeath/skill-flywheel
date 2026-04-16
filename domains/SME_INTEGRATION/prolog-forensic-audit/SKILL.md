---
Domain: SME_INTEGRATION
Version: 1.0.0
Complexity: Advanced
Type: Tool
Category: Forensics
Estimated Execution Time: 100ms - 2 minutes
name: prolog-forensic-audit
---

## Description

Prolog-based forensic audit system for verifying logical consistency, detecting contradictions, and validating evidence chains in forensic analysis. Uses declarative logic rules to identify inconsistencies that might be missed by procedural approaches.

## Purpose

To provide rigorous logical verification of forensic findings using Prolog's inference capabilities. Particularly useful when dealing with complex multi-step reasoning chains where consistency is critical.

## When to Use

- Verifying forensic analysis before reporting
- Detecting contradictions in multi-source findings
- Validating evidence-to-conclusion chains
- Checking for logical fallacies in reasoning
- Audit trail verification for compliance

## When NOT to Use

- Simple single-source fact checks (use simpler tools)
- When human review is sufficient
- Real-time streaming analysis (use streaming version)

## Input Format

```yaml
audit_request:
  action: "verify|analyze|fallacy|chain|conflict"
  findings: array          # List of forensic findings/propositions
  evidence: object         # Evidence mapping
  rules: array             # Custom logic rules (optional)
```

## Output Format

```yaml
audit_result:
  status: "consistent" | "inconsistent" | "unknown"
  contradictions: array    # List of detected contradictions
  fallacies: array         # Detected logical fallacies
  confidence: number       # 0.0 to 1.0
  report: string          # Human-readable summary
```

## Capabilities

### 1. Prolog-Based Consistency Checking

```prolog
% Forensic finding consistency rules

% Contradiction detection
contradicts(finding(A), finding(not A)).
contradicts(finding(A), finding(B)) :- 
    mutually_exclusive(A, B).

% Evidence support chain
supports(evidence(E), finding(F)) :- 
    evidence_type(E, T),
    supports_type(T, F).

% Logical implication
implies(finding(A), finding(B)) :- 
    rule(A, B).

% Check overall consistency
consistent(Findings) :- 
    \+ (member(F1, Findings), 
        member(F2, Findings), 
        contradicts(F1, F2)).
```

### 2. Fallacy Detection

```prolog
% Common fallacy patterns
fallacy(straw_man, Argument) :- 
    misrepresents(Argument, Original),
    attack(Argument, Modified).

fallacy(ad_hominem, Argument) :- 
    attacks_person(Argument, Person),
    \+ attacks_argument(Argument, Position).

fallacy(false_dichotomy, Argument) :- 
    presents(Argument, [A, B]),
    \+ (A ; B),  % Excludes other possibilities
    implies(A ; B, false).

fallacy(circular_reasoning, Argument) :- 
    conclusion(Argument, C),
    premise(Argument, C).
```

### 3. Evidence Chain Validation

```python
def validate_evidence_chain(evidence_list, finding):
    """Validate that evidence properly supports finding."""
    rules = """
    supports(evidence(Source, Content), finding(Claim)) :-
        evidence_source(Source, trustworthiness(Trust)),
        Content contains Claim,
        Trust > 0.7.
    
    chain_valid(Evidence, Finding) :-
        supports(Evidence, Finding).
    chain_valid(Evidence, Finding) :-
        supports(Evidence, Intermediate),
        chain_valid(Intermediate, Finding).
    """
    return run_prolog_query(rules, f"chain_valid({evidence_list}, {finding})")
```

### 4. Contradiction Detection

```python
def find_contradictions(findings):
    """Find all contradictions in findings."""
    prolog_code = """
    find_contradictions(Findings, Contradictions) :-
        findall(C, (member(F1, Findings), 
                    member(F2, Findings), 
                    contradicts(F1, F2), 
                    C = f(F1, F2)), Contradictions).
    """
    return query_prolog(prolog_code)
```

### 5. Compliance Audit

```prolog
% Audit trail verification
verified_conclusion(Conclusion, AuditTrail) :-
    evidence(Conclusion, Evidence, Chain),
    complete_chain(Chain, AuditTrail),
    no_contradictions(Evidence).

complete_chain([], _).
complete_chain([E|Chain], Trail) :-
    member(E, Trail),
    complete_chain(Chain, Trail).
```

## Implementation Notes

- Use pyswip for Prolog integration
- Fall back to Python for simple cases
- Cache compiled rules for performance

## Dependencies

```python
# Required
pyswip  # Prolog interface

# Optional
# pandas  # For evidence analysis
```

## Best Practices

1. **Extensible Rules**: Allow custom rules per domain
2. **Audit Trail**: Record all verification steps
3. **Confidence Scoring**: Include confidence for each finding
4. **Explainability**: Provide reasoning for each conclusion

## Error Handling

- Prolog unavailable → Use Python fallback
- Invalid rule syntax → Log and skip
- Timeout → Return partial results

## Version History

- **1.0.0**: Initial Prolog forensic audit implementation

## Constraints

- MUST include audit trail for compliance
- ALWAYS provide confidence scores
- STOP if exceeds 1000 findings (batch processing needed)