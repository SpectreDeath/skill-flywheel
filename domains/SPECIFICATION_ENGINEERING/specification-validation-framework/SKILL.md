---
name: specification-validation-framework
description: "Use when: implementing automated testing and validation for specifications, validating spec completeness before implementation, ensuring spec quality meets defined thresholds, or running spec quality gates in CI/CD. Triggers: 'validate spec', 'spec validation', 'spec quality', 'test spec', 'validate specification', 'spec completeness'. NOT for: simple specs manually verifiable, early drafts with evolving requirements, or when validation overhead exceeds project needs."
---

# Specification Validation Framework

Implement comprehensive automated specification testing and validation to ensure specification quality, completeness, and alignment with implementation. This skill provides systematic validation with actionable feedback.

## When to Use This Skill

Use this skill when:
- Implementing automated spec testing and validation
- Validating spec completeness before implementation
- Ensuring spec quality meets defined thresholds
- Running spec quality gates in CI/CD pipelines
- Performing automated spec reviews

Do NOT use this skill when:
- Simple specifications that are manually verifiable
- Early drafts where requirements are still evolving
- Validation overhead exceeds project needs

## Input Format

```yaml
validation_request:
  spec_path: string              # Path to specification document
  validation_rules: array         # Custom validation rules to apply
  quality_thresholds: object     # Minimum quality scores required
  target_format: string          # Spec format (openapi, markdown, json)
```

## Output Format

```yaml
validation_result:
  status: "pass" | "fail" | "warning"
  score: number                  # Overall validation score (0-100)
  issues: array                 # List of issues found
  coverage: object              # Spec coverage metrics
  recommendations: array         # Suggested improvements
```

## Capabilities

### 1. Syntax Validation (5 min)

- Validate specification syntax and structure
- Check for required fields and proper formatting
- Verify schema correctness for structured specs (OpenAPI, JSON Schema)

### 2. Completeness Check (10 min)

- Identify missing sections or requirements
- Verify all acceptance criteria are defined
- Check for ambiguous or undefined terms

### 3. Consistency Analysis (10 min)

- Cross-reference related specifications
- Check for conflicting requirements
- Validate consistency across document sections

### 4. Test Coverage Mapping (15 min)

- Map specification requirements to test cases
- Identify gaps in test coverage
- Generate coverage reports

### 5. Quality Scoring (5 min)

- Calculate overall specification quality score
- Compare against defined thresholds
- Generate quality report with improvements

## Usage Examples

### Basic Usage

"Validate my API specification for completeness and consistency."

### Advanced Usage

"Run full validation on specification with custom rules for healthcare compliance."

## When to Use

- Before starting implementation to ensure spec is ready
- During spec reviews to catch issues early
- As part of CI/CD pipeline for spec quality gates
- When spec quality impacts downstream work

## When NOT to Use

- Simple specs that are manually verifiable
- Early drafts where requirements are still evolving
- When validation overhead exceeds project needs

## Configuration Options

- `strict_mode`: Fail on warnings (default: false)
- `custom_rules`: Add domain-specific validation rules
- `thresholds`: Customize minimum quality scores
- `auto_fix`: Attempt automatic fixes for common issues

## Constraints

- MUST validate all acceptance criteria are testable
- SHOULD report clear, actionable issues
- MUST include severity levels for each issue
- SHOULD suggest specific improvements

## Integration Examples

- CI/CD pipeline: Run validation before deployment
- Spec reviews: Use as automated reviewer
- Quality gates: Enforce minimum scores

## Dependencies

- Python 3.10+
- PyYAML for YAML parsing
- jsonschema for JSON schema validation
- Optional: OpenAPI validator libraries
