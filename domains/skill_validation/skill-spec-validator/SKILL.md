---
name: skill-spec-validator
description: "Use when: validating AgentSkills directory structure, checking SKILL.md file compliance, verifying cross-reference integrity, or generating auto-fix scripts. Triggers: 'validate skills', 'skill spec', 'directory structure', 'validate structure', 'compliance check', 'auto fix'. NOT for: individual file content validation, format-specific validation, or dependency checking."
---

# Skill Spec Validator

Validates complete AgentSkills directory structure and SKILL.md file compliance. This tool ensures repository integrity and generates auto-fix scripts.

## When to Use This Skill

Use this skill when:
- Validating AgentSkills directory structure
- Checking SKILL.md file compliance
- Verifying cross-reference integrity
- Generating auto-fix scripts for common issues
- Performing repository health checks

Do NOT use this skill when:
- Validating individual file content (use frontmatter-validator)
- Checking format compliance (use format-compliance-tester)
- Analyzing dependencies (use dependency-analyzer)

## Input Format

```yaml
validation_request:
  root_path: string              # Path to skills directory
  check_cross_refs: boolean      # Validate cross-references
  generate_fixes: boolean       # Generate auto-fix scripts
  strict_mode: boolean          # Fail on warnings
```

## Output Format

```yaml
validation_result:
  status: "pass" | "fail"
  structure_valid: boolean
  files_checked: number
  issues: array
  auto_fix_script: string
  compliance_score: number
```

## Capabilities

### 1. Directory Structure Validation (5 min)

- Validate domain directories exist
- Check for required __init__.py files
- Verify skill subdirectory structure
- Check for duplicate skills

### 2. File Naming Validation (5 min)

- Verify SKILL.md filename convention
- Check domain directory naming
- Validate skill name consistency
- Detect naming violations

### 3. Cross-Reference Validation (10 min)

- Check internal skill references
- Verify external links
- Validate skill-to-skill dependencies
- Check documentation links

### 4. Metadata Completeness (5 min)

- Verify frontmatter exists
- Check required fields present
- Validate version formats
- Check complexity ratings

### 5. Auto-Fix Script Generation (10 min)

- Generate Python fix scripts
- Include common issue resolutions
- Make fixes reversible
- Document changes made

## Usage Examples

### Basic Usage

"Validate the skills directory structure."

### Advanced Usage

"Run full spec validation with cross-reference checking and auto-fix generation."

## Configuration Options

- `root_path`: Skills root directory
- `check_cross_refs`: Enable reference validation
- `generate_fixes`: Generate fix scripts
- `strict_mode`: Fail on warnings

## Constraints

- MUST validate directory structure
- SHOULD generate actionable fix scripts
- MUST report specific file issues
- SHOULD provide compliance score

## Integration Examples

- CI/CD: Run before commits
- Pre-commit hooks: Validate on push
- Repository health: Weekly checks

## Dependencies

- Python 3.10+
- pathlib for path handling
- yaml for frontmatter parsing
- re for pattern matching
