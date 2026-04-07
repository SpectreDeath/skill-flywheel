---
name: frontmatter-validator
description: "Use when: validating YAML frontmatter in SKILL.md files, checking required fields, verifying version/complexity formats, or auto-fixing frontmatter issues. Triggers: 'frontmatter', 'validate yaml', 'validate metadata', 'fix frontmatter', 'required fields', 'metadata validation'. NOT for: directory structure validation, file naming, or content validation."
---

# Frontmatter Validator

Validates YAML frontmatter in SKILL.md files for completeness and correctness. This tool ensures metadata quality and generates fix scripts.

## When to Use This Skill

Use this skill when:
- Validating YAML frontmatter in SKILL.md files
- Checking required fields (name, description, Domain)
- Verifying version and complexity formats
- Auto-fixing common frontmatter issues
- Performing metadata completeness checks

Do NOT use this skill when:
- Validating directory structure (use skill-spec-validator)
- Checking file naming conventions (use naming-convention-checker)
- Validating content sections (use format-compliance-tester)

## Input Format

```yaml
validation_request:
  file_path: string              # Path to SKILL.md file
  domain: string                 # Domain to validate (optional)
  fix_issues: boolean            # Auto-fix common issues
  strict: boolean               # Fail on minor issues
```

## Output Format

```yaml
validation_result:
  status: "pass" | "fail" | "warning"
  field_status: object           # Status of each field
  issues: array                 # List of issues found
  fix_script: string            # Auto-fix if requested
  score: number                 # Overall score (0-100)
```

## Capabilities

### 1. Required Field Validation (5 min)

- Check for name field
- Verify description field exists
- Validate Domain field
- Check for version field

### 2. Format Validation (5 min)

- Validate version format (semver)
- Verify complexity value (Basic/Intermediate/Advanced)
- Check execution time format
- Validate type field

### 3. Semantic Validation (10 min)

- Check field value relationships
- Verify complexity matches domain
- Validate description triggers
- Check NOT for clauses

### 4. Cross-Field Checking (5 min)

- Verify name matches filename
- Check description matches triggers
- Validate consistency between fields
- Ensure no conflicting values

### 5. Auto-Fix Generation (10 min)

- Generate fixes for missing fields
- Add default values where appropriate
- Format version strings correctly
- Create reversible fix scripts

## Usage Examples

### Basic Usage

"Validate frontmatter in SKILL.md files."

### Advanced Usage

"Run frontmatter validation with auto-fix for common issues."

## Configuration Options

- `fix_issues`: Auto-fix common problems
- `strict`: Fail on warnings
- `required_fields`: Custom required fields list
- `version_format`: Custom version regex

## Constraints

- MUST validate all required fields
- SHOULD provide clear issue descriptions
- MUST generate fixable issues
- SHOULD validate semantic consistency

## Integration Examples

- Pre-commit: Validate on commit
- CI/CD: Check in pipeline
- Bulk validation: Run on all files

## Dependencies

- Python 3.10+
- PyYAML for parsing
- re for pattern matching
