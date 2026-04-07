---
name: executable-spec-harness
description: "Use when: converting specifications into automated tests, generating test cases from spec documents, creating executable validation for specs, or implementing contract-driven testing. Triggers: 'spec to test', 'executable spec', 'contract testing', 'spec test', 'generate tests from spec', 'test from specification'. NOT for: simple specs manually verifiable, rapidly changing specs, or when test maintenance overhead is too high."
---

# Executable Spec Harness

Build frameworks that run specifications as automated tests, generating test cases directly from specification documents. This skill bridges spec authoring and test automation.

## When to Use This Skill

Use this skill when:
- Converting specifications into automated tests
- Generating test cases from spec documents
- Creating executable validation for specs
- Implementing contract-driven testing
- Building spec-driven test harnesses

Do NOT use this skill when:
- Simple specifications easily verified manually
- Rapidly changing specifications (tests become obsolete)
- Test maintenance overhead exceeds benefits

## Input Format

```yaml
harness_request:
  spec_path: string              # Path to specification
  framework: string              # Target test framework (pytest, jest, junit)
  output_path: string            # Where to generate test files
  test_types: array             # Types of tests to generate (unit, integration, e2e)
```

## Output Format

```yaml
harness_result:
  generated_tests: array        # Generated test files
  coverage: object             # Test coverage metrics
  mappings: object              # Spec-to-test mappings
  execution_results: object    # Test execution results
```

## Capabilities

### 1. Spec Parsing (10 min)

- Parse specification documents
- Extract testable requirements
- Identify acceptance criteria

### 2. Test Generation (20 min)

- Generate unit tests from requirements
- Create integration test templates
- Build E2E test scenarios

### 3. Test Synchronization (10 min)

- Track spec-test correspondence
- Detect drift between spec and tests
- Auto-update tests when spec changes

### 4. Execution Framework (15 min)

- Set up test execution environment
- Configure test runners
- Define quality gates

### 5. Coverage Analysis (10 min)

- Measure spec-to-test coverage
- Identify untested requirements
- Generate coverage reports

## Usage Examples

### Basic Usage

"Generate pytest tests from my API specification."

### Advanced Usage

"Create full test harness with unit, integration, and E2E tests from OpenAPI spec."

## When to Use

- API specifications that need executable validation
- Complex requirements requiring test coverage
- Contract-driven development
- Automated acceptance testing

## When NOT to Use

- Simple specifications easily verified manually
- Rapidly changing specs (tests become obsolete)
- When test maintenance overhead is too high

## Configuration Options

- `framework`: Test framework target
- `test_types`: Types of tests to generate
- `auto_sync`: Auto-update tests on spec changes
- `coverage_target`: Minimum coverage percentage

## Constraints

- MUST generate executable, runnable tests
- SHOULD maintain spec-test alignment
- MUST provide clear test failure messages
- SHOULD minimize test maintenance burden

## Integration Examples

- CI/CD: Run tests on spec changes
- Contract testing: Validate implementations against specs
- Regression: Ensure spec changes don't break tests

## Dependencies

- Python 3.10+
- Test framework (pytest, unittest, jest, etc.)
- Spec parsers (OpenAPI, JSON Schema)
- Optional: Code generation libraries
