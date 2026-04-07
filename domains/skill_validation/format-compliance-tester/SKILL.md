---
name: format-compliance-tester
description: "Use when: testing format compliance against AgentSkills specification, validating section completeness, checking content quality, or generating compliance reports. Triggers: 'format compliance', 'test compliance', 'validate format', 'section completeness', 'compliance report', 'quality check'. NOT for: structure validation, frontmatter checking, or naming validation."
---

# Format Compliance Tester

Comprehensive format compliance testing against AgentSkills specification. This tool validates section completeness, content quality, and generates compliance reports.

## When to Use This Skill

Use this skill when:
- Testing format compliance against specifications
- Validating section completeness
- Checking content quality
- Generating compliance reports
- Performing quality assessments

Do NOT use this skill when:
- Validating directory structure (use skill-spec-validator)
- Checking frontmatter (use frontmatter-validator)
- Checking naming (use naming-convention-checker)

## Input Format

```yaml
test_request:
  root_path: string              # Path to skills directory
  domain: string                 # Specific domain (optional)
  strict: boolean               # Fail on warnings
  generate_report: boolean      # Generate detailed report
```

## Output Format

```yaml
test_result:
  status: "pass" | "fail" | "warning"
  compliance_score: number       # Overall score (0-100)
  sections_present: object      # Section status per file
  content_quality: object       # Quality metrics
  issues: array                 # List of issues
  report: string                # Detailed report
```

## Capabilities

### 1. Section Completeness Validation (10 min)

- Verify all required sections exist
- Check section order
- Validate section content
- Flag missing sections

### 2. Format Consistency Checking (10 min)

- Verify consistent heading levels
- Check code block formatting
- Validate list formatting
- Ensure proper YAML indentation

### 3. Content Quality Assessment (15 min)

- Check description quality
- Verify example completeness
- Validate constraint clarity
- Assess use case coverage

### 4. Cross-Reference Validation (10 min)

- Check internal skill references
- Verify external links
- Validate documentation links
- Detect broken references

### 5. Compliance Reporting (10 min)

- Generate detailed reports
- Create compliance scores
- Compare against thresholds
- Export to multiple formats

## Usage Examples

### Basic Usage

"Test format compliance of the skills repository."

### Advanced Usage

"Run full compliance test with detailed reporting."

## Configuration Options

- `strict`: Fail on warnings
- `generate_report`: Detailed output
- `min_score`: Minimum acceptable score
- `domains`: Specific domains to check

## Constraints

- MUST validate all required sections
- SHOULD provide quality scores
- MUST report specific issues
- SHOULD generate actionable reports

## Integration Examples

- CI/CD: Run in pipeline
- Pre-commit: Check before commit
- Quality gates: Enforce minimum scores

## Dependencies

- Python 3.10+
- PyYAML for parsing
- re for pattern matching
- json for output
