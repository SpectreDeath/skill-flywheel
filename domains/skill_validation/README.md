# Skill Validation Suite

Domain containing validation tools for ensuring AgentSkills adhere to specifications and maintain high quality standards.

## Skills

| Skill | Description |
|-------|-------------|
| [skill-spec-validator](skill-spec-validator/) | Validates directory structure and SKILL.md file compliance |
| [frontmatter-validator](frontmatter-validator/) | Validates YAML frontmatter in SKILL.md files |
| [naming-convention-checker](naming-convention-checker/) | Enforces consistent naming conventions |
| [dependency-analyzer](dependency-analyzer/) | Analyzes skill dependencies and detects circular refs |
| [format-compliance-tester](format-compliance-tester/) | Tests format compliance against AgentSkills spec |

## Usage

Load these skills when validating the AgentSkills repository:

- **skill-spec-validator**: Check directory structure and file organization
- **frontmatter-validator**: Validate YAML metadata in skill files
- **naming-convention-checker**: Ensure consistent file/directory naming
- **dependency-analyzer**: Find circular dependencies and analyze coupling
- **format-compliance-tester**: Test section completeness and content quality

## Validation Pipeline

These skills work together in a validation pipeline:

```
1. skill-spec-validator    → Directory structure & file existence
2. frontmatter-validator   → YAML metadata validation  
3. naming-convention-checker → Naming pattern validation
4. dependency-analyzer    → Dependency graph analysis
5. format-compliance-tester → Content & section validation
```

## Python Utilities

The domain also contains Python validation scripts for programmatic use:

- `simple_validation.py` - Basic logic domain validation
- `validate_logic_domain.py` - Logic domain-specific validation
- `validate_mobile_format.py` - Mobile development format validation
- `master_validation_suite.py` - Full validation suite orchestrator
