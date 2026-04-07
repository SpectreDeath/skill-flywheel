---
name: spec-guardrail-enforcement
description: "Use when: enforcing specification compliance during implementation, validating code matches specs, catching spec violations early, or implementing automated spec gates. Triggers: 'enforce spec', 'spec compliance', 'validate implementation', 'spec gate', 'spec violation', 'compliance check'. NOT for: teams without spec discipline, early prototyping, or when specs aren't authoritative."
---

# Spec Guardrail Enforcement

Enforce specification compliance during implementation to catch violations early. This skill provides automated validation and enforcement mechanisms.

## When to Use This Skill

Use this skill when:
- Enforcing specification compliance during implementation
- Validating code matches specifications
- Catching spec violations early in development
- Implementing automated spec gates in CI/CD
- Establishing enforcement guardrails

Do NOT use this skill when:
- Teams lack spec discipline or buy-in
- Early prototyping phases
- Specifications aren't authoritative
- Enforcement overhead exceeds benefits

## Input Format

```yaml
enforcement_request:
  specification: string         # Specification to enforce
  implementation: string         # Implementation to validate
  rules: array                   # Enforcement rules
  strictness: string             # Enforcement level (strict, lenient)
```

## Output Format

```yaml
enforcement_result:
  violations: array              # Detected violations
  compliance_score: number       # Overall compliance percentage
  recommendations: array         # Remediation suggestions
  pass_status: boolean          # Whether spec passed enforcement
```

## Capabilities

### 1. Rule Definition (10 min)

- Define specification enforcement rules
- Map spec requirements to validation rules
- Configure severity levels
- Set up custom validation logic

### 2. Static Validation (15 min)

- Validate code structure against specs
- Check API signatures match contracts
- Verify data models align
- Validate naming conventions

### 3. Runtime Validation (15 min)

- Execute tests against specifications
- Validate behavior matches contracts
- Check error handling compliance
- Verify performance requirements

### 4. Compliance Reporting (10 min)

- Generate compliance reports
- Track compliance over time
- Identify recurring issues
- Create audit trails

### 5. Gate Integration (10 min)

- Integrate with CI/CD pipelines
- Configure pass/fail criteria
- Set up automated enforcement
- Define rollback triggers

## Usage Examples

### Basic Usage

"Enforce spec compliance on this implementation."

### Advanced Usage

"Run strict enforcement with custom rules and fail build on violations."

## Configuration Options

- `strictness`: Strict, standard, or lenient
- `auto_fix`: Attempt automatic fixes
- `rules`: Custom enforcement rules
- `blocking`: Block deployment on violations

## Constraints

- MUST detect spec violations accurately
- SHOULD provide clear remediation
- MUST avoid false positives
- SHOULD integrate with existing workflows

## Integration Examples

- CI/CD: Block builds on violations
- Linting: Add spec-aware lint rules
- Testing: Run spec compliance tests
- Pre-commit: Validate before commit

## Dependencies

- Python 3.10+
- Test frameworks
- Static analysis tools
- CI/CD integration
