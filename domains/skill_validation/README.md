# Skill Validation Suite

This directory contains a comprehensive suite of validation tools for the AgentSkills repository. These tools ensure that all SKILL.md files adhere to the established specification and maintain high quality standards.

## Overview

The validation suite consists of 5 specialized skills that work together to validate different aspects of the AgentSkills specification:

### 1. Skill Spec Validator (`SKILL.skill_spec_validator.md`)
**Purpose**: Validates complete AgentSkills directory structure and SKILL.md file compliance
**Key Features**:
- Directory structure validation
- SKILL.md file format checking
- Cross-reference integrity validation
- Metadata completeness verification
- Auto-fix script generation

### 2. Frontmatter Validator (`SKILL.frontmatter_validator.md`)
**Purpose**: Validates YAML frontmatter in SKILL.md files for completeness and correctness
**Key Features**:
- Required field validation
- Format validation (version, complexity, execution time)
- Semantic validation of field values
- Cross-field relationship checking
- Auto-fix generation

### 3. Naming Convention Checker (`SKILL.naming_convention_checker.md`)
**Purpose**: Enforces consistent naming conventions across the repository
**Key Features**:
- File name validation (SKILL.{Name}.md pattern)
- Directory naming validation (PascalCase)
- Internal identifier consistency checking
- Cross-reference validation
- Auto-correction suggestions

### 4. Dependency Analyzer (`SKILL.dependency_analyzer.md`)
**Purpose**: Analyzes and validates dependencies between skills
**Key Features**:
- Dependency graph analysis
- Circular dependency detection
- Dependency completeness verification
- Modularity assessment
- Dependency visualization

### 5. Format Compliance Tester (`SKILL.format_compliance_tester.md`)
**Purpose**: Comprehensive format compliance testing against specifications
**Key Features**:
- Section completeness validation
- Format consistency checking
- Content quality assessment
- Cross-reference validation
- Compliance reporting

## Usage

### Quick Start

Run all validation tools on your skills repository:

```python
from skills.DOMAIN.skill_validation.SKILL.skill_spec_validator import AgentSkillsValidator
from skills.DOMAIN.skill_validation.SKILL.frontmatter_validator import FrontmatterValidator
from skills.DOMAIN.skill_validation.SKILL.naming_convention_checker import NamingConventionChecker
from skills.DOMAIN.skill_validation.SKILL.dependency_analyzer import DependencyAnalyzer
from skills.DOMAIN.skill_validation.SKILL.format_compliance_tester import FormatComplianceTester

# Initialize validators
spec_validator = AgentSkillsValidator("skills")
frontmatter_validator = FrontmatterValidator()
naming_checker = NamingConventionChecker()
dependency_analyzer = DependencyAnalyzer("skills")
compliance_tester = FormatComplianceTester("skills")

# Run validations
spec_report = spec_validator.run_full_validation()
naming_violations = naming_checker.validate_repository("skills")
dependency_report = dependency_analyzer.analyze_repository()
compliance_report = compliance_tester.test_repository_compliance()

print("✅ All validation tools ready to use!")
```

### Individual Tool Usage

Each validation skill can be used independently:

#### Skill Spec Validator
```python
validator = AgentSkillsValidator("skills")
report = validator.run_full_validation()
```

#### Frontmatter Validator
```python
validator = FrontmatterValidator()
issues = validator.validate_file("skills/DOMAIN/SKILL.example.md")
```

#### Naming Convention Checker
```python
checker = NamingConventionChecker()
violations = checker.validate_repository("skills")
```

#### Dependency Analyzer
```python
analyzer = DependencyAnalyzer("skills")
report = analyzer.analyze_repository()
```

#### Format Compliance Tester
```python
tester = FormatComplianceTester("skills")
report = tester.test_repository_compliance()
```

## Validation Reports

Each tool generates detailed reports with:

- **Summary statistics**: Total files, issues found, compliance scores
- **Detailed issue lists**: Specific problems with file paths, line numbers, and suggestions
- **Recommendations**: Actionable advice for improving compliance
- **Auto-fix scripts**: Generated scripts to automatically fix common issues

### Report Formats

- **JSON reports**: Machine-readable detailed reports
- **Console output**: Human-readable summaries with color coding
- **Auto-fix scripts**: Python scripts to automatically resolve issues

## Integration with CI/CD

These validation tools can be integrated into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Validate Skills
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Skill Validation
        run: |
          python skills/DOMAIN/skill_validation/validate_all.py
      - name: Check Compliance Score
        run: |
          python -c "
          import json
          with open('compliance_report.json') as f:
              report = json.load(f)
          if report['summary']['overall_compliance_score'] < 80:
              exit(1)
          "
```

## Mobile Development Format Validation

The validation suite includes specific checks for the mobile_development format:

### Mobile Development Requirements

1. **Required Sections**: All standard sections plus mobile-specific sections
2. **Platform Support**: iOS, Android, cross-platform frameworks
3. **Performance Metrics**: Mobile-specific performance considerations
4. **Platform Constraints**: Platform-specific limitations and capabilities
5. **Testing Requirements**: Mobile testing strategies and tools

### Validation Against Mobile Development Format

```python
from skills.DOMAIN.skill_validation.SKILL.format_compliance_tester import FormatComplianceTester

# Test against mobile development format
tester = FormatComplianceTester("skills")
report = tester.test_repository_compliance()

# Check mobile-specific compliance
mobile_issues = []
for issue in report["issues"]:
    if "mobile" in issue["message"].lower():
        mobile_issues.append(issue)

print(f"Mobile development format issues: {len(mobile_issues)}")
```

## Best Practices

### 1. Regular Validation
Run validation tools regularly to catch issues early:
- Before committing changes
- As part of CI/CD pipeline
- Weekly repository health checks

### 2. Address Critical Issues First
Prioritize issues by severity:
- **Critical**: Missing required sections, invalid frontmatter
- **Warning**: Formatting issues, content quality
- **Info**: Style suggestions, minor improvements

### 3. Use Auto-fix Scripts
Leverage generated auto-fix scripts to quickly resolve common issues:
```bash
python auto_fix_script_1.py
python auto_fix_script_2.py
```

### 4. Continuous Improvement
Use validation reports to improve skill quality:
- Track compliance scores over time
- Identify common issues across skills
- Update templates based on findings

## Troubleshooting

### Common Issues

1. **File Not Found Errors**: Ensure skills directory path is correct
2. **Permission Errors**: Check file read permissions
3. **YAML Parsing Errors**: Validate YAML frontmatter syntax
4. **Circular Dependencies**: Review and break dependency cycles

### Getting Help

- Check the individual skill documentation for specific usage
- Review generated reports for detailed error information
- Use the `--help` flag for command-line tools
- Consult the main AgentSkills specification

## Contributing

To contribute to the validation suite:

1. **Add New Validation Rules**: Extend existing validators with new checks
2. **Improve Auto-fix Scripts**: Enhance script generation for better fixes
3. **Add New Validators**: Create specialized validators for specific domains
4. **Improve Documentation**: Update README and inline documentation

## License

This validation suite is part of the AgentSkills project and follows the same licensing terms.