---
name: naming-convention-checker
description: "Use when: enforcing consistent naming conventions, validating SKILL.{Name}.md pattern, checking domain directory naming, or auto-correcting naming violations. Triggers: 'naming', 'convention', 'file name', 'validate naming', 'fix naming', 'naming violation'. NOT for: content validation, frontmatter checking, or structure validation."
---

# Naming Convention Checker

Enforces consistent naming conventions across the repository. This tool validates file names, directory names, and internal identifiers.

## When to Use This Skill

Use this skill when:
- Enforcing consistent naming conventions
- Validating SKILL.{Name}.md file pattern
- Checking domain directory naming (PascalCase)
- Auto-correcting naming violations
- Performing naming audits

Do NOT use this skill when:
- Validating directory structure (use skill-spec-validator)
- Checking frontmatter (use frontmatter-validator)
- Validating content sections (use format-compliance-tester)

## Input Format

```yaml
validation_request:
  root_path: string              # Path to skills directory
  auto_correct: boolean          # Auto-fix violations
  check_internal: boolean       # Check internal IDs
  pattern: string               # Custom naming pattern
```

## Output Format

```yaml
validation_result:
  status: "pass" | "fail"
  violations: array              # List of violations
  corrections: array             # Suggested corrections
  auto_fix_script: string        # Auto-fix if enabled
  compliance_score: number
```

## Capabilities

### 1. File Name Validation (5 min)

- Verify SKILL.{Name}.md pattern
- Check for proper PascalCase in Name
- Validate no invalid characters
- Check file extension

### 2. Directory Naming Validation (5 min)

- Verify domain directory names
- Check for PascalCase consistency
- Validate no spaces or special chars
- Check subdirectory names

### 3. Internal Identifier Checking (10 min)

- Check internal skill references
- Validate cross-reference syntax
- Check for broken links
- Verify anchor names

### 4. Cross-Reference Validation (10 min)

- Validate skill-to-skill references
- Check domain cross-references
- Verify documentation links
- Detect broken references

### 5. Auto-Correction (10 min)

- Rename files to correct pattern
- Fix directory names
- Update internal references
- Generate fix scripts

## Usage Examples

### Basic Usage

"Check naming conventions in the skills repository."

### Advanced Usage

"Run naming validation with auto-correction enabled."

## Configuration Options

- `auto_correct`: Auto-fix violations
- `check_internal`: Validate internal IDs
- `pattern`: Custom naming regex
- `domains`: Specific domains to check

## Constraints

- MUST validate file naming pattern
- SHOULD provide auto-correction
- MUST report specific violations
- SHOULD maintain cross-reference integrity

## Integration Examples

- Pre-commit: Check before commit
- CI/CD: Validate in pipeline
- Bulk rename: Fix multiple files

## Dependencies

- Python 3.10+
- pathlib for path handling
- re for pattern matching
- shutil for file operations
