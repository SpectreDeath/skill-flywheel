---
Domain: skill_validation
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: frontmatter-validator
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




## Description

Validates YAML frontmatter in SKILL.md files for completeness, format correctness, and semantic accuracy. This skill ensures all required metadata fields are present, properly formatted, and semantically meaningful for the AgentSkills specification.


## Purpose

To be provided dynamically during execution.

## Input Format

```yaml
request:
  action: string
  parameters: object
```

## Output Format

```yaml
response:
  status: string
  result: object
  errors: array
```

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Required Field Validation**: Verify all mandatory frontmatter fields are present
- **Format Validation**: Check field formats (version, complexity, execution time)
- **Semantic Validation**: Validate field values make sense in context
- **Field Completeness**: Ensure optional fields are filled when applicable
- **Cross-Field Validation**: Check relationships between fields
- **Auto-Fix Generation**: Generate scripts to fix common frontmatter issues
- **Batch Processing**: Validate multiple files efficiently

## Usage Examples

### Validate Single Skill File

```python
"""
Frontmatter Validation for Individual Skill
"""

import yaml
import re
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

@dataclass
class FrontmatterIssue:
    """Issue found in frontmatter validation"""
    field: str
    issue_type: str  # "missing", "invalid_format", "invalid_value", "semantic_error"
    message: str
    suggestion: Optional[str] = None

class FrontmatterValidator:
    """Validates YAML frontmatter in SKILL.md files"""
    
    def __init__(self):
        self.required_fields = {
            "Domain": str,
            "Version": str, 
            "Type": str,
            "Category": str,
            "Estimated Execution Time": str,
            "Complexity": str
        }
        
        self.optional_fields = {
            "Description": str,
            "Dependencies": list,
            "License": str,
            "Author": str,
            "Created": str,
            "Last Modified": str
        }
    
    def validate_file(self, file_path: str) -> List[FrontmatterIssue]:
        """Validate frontmatter in a single skill file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return [FrontmatterIssue(
                field="file",
                issue_type="read_error",
                message=f"Cannot read file: {e}"
            )]
        
        frontmatter = self._extract_frontmatter(content)
        if frontmatter is None:
            return [FrontmatterIssue(
                field="frontmatter",
                issue_type="missing",
                message="No YAML frontmatter found",
                suggestion="Add YAML frontmatter with required fields"
            )]
        
        issues = []
        
        # Validate required fields
        for field, field_type in self.required_fields.items():
            issues.extend(self._validate_required_field(field, field_type, frontmatter, file_path))
        
        # Validate optional fields if present
        for field, field_type in self.optional_fields.items():
            if field in frontmatter:
                issues.extend(self._validate_optional_field(field, field_type, frontmatter, file_path))
        
        # Cross-field validation
        issues.extend(self._validate_cross_fields(frontmatter, file_path))
        
        return issues
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from file content"""
        if not content.startswith('---'):
            return None
        
        lines = content.split('\n')
        frontmatter_lines = []
        in_frontmatter = False
        frontmatter_end = -1
        
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    frontmatter_end = i
                    break
            elif in_frontmatter:
                frontmatter_lines.append(line)
        
        if frontmatter_end == -1:
            return None
        
        try:
            frontmatter_text = '\n'.join(frontmatter_lines)
            return yaml.safe_load(frontmatter_text)
        except yaml.YAMLError:
            return None
    
    def _validate_required_field(self, field: str, field_type: type, frontmatter: Dict, file_path: str) -> List[FrontmatterIssue]:
        """Validate a required frontmatter field"""
        issues = []
        
        if field not in frontmatter:
            issues.append(FrontmatterIssue(
                field=field,
                issue_type="missing",
                message=f"Required field '{field}' is missing",
                suggestion=f"Add '{field}' field to frontmatter"
            ))
            return issues
        
        value = frontmatter[field]
        
        # Type validation
        if not isinstance(value, field_type):
            issues.append(FrontmatterIssue(
                field=field,
                issue_type="invalid_format",
                message=f"Field '{field}' should be {field_type.__name__}, got {type(value).__name__}",
                suggestion=f"Ensure '{field}' is properly formatted as {field_type.__name__}"
            ))
        
        # Value-specific validation
        if field == "Domain":
            issues.extend(self._validate_domain_field(value, file_path))
        elif field == "Version":
            issues.extend(self._validate_version_field(value, file_path))
        elif field == "Complexity":
            issues.extend(self._validate_complexity_field(value, file_path))
        elif field == "Estimated Execution Time":
            issues.extend(self._validate_execution_time_field(value, file_path))
        elif field == "Type":
            issues.extend(self._validate_type_field(value, file_path))
        elif field == "Category":
            issues.extend(self._validate_category_field(value, file_path))
        
        return issues
    
    def _validate_domain_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Domain field"""
        issues = []
        
        # Check PascalCase format
        if not re.match(r'^[A-Z][a-zA-Z]*$', value):
            issues.append(FrontmatterIssue(
                field="Domain",
                issue_type="invalid_format",
                message=f"Domain '{value}' should use PascalCase format",
                suggestion="Use PascalCase for domain names (e.g., 'MachineLearning')"
            ))
        
        # Check against known domains
        known_domains = [
            "MachineLearning", "DataScience", "WebDevelopment", "MobileDevelopment",
            "DevOps", "Security", "Testing", "Performance", "Architecture"
        ]
        
        if value not in known_domains:
            issues.append(FrontmatterIssue(
                field="Domain",
                issue_type="semantic_error",
                message=f"Domain '{value}' is not in known domains list",
                suggestion=f"Consider using one of: {', '.join(known_domains)}"
            ))
        
        return issues
    
    def _validate_version_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Version field"""
        issues = []
        
        # Check semantic versioning format
        if not re.match(r'^\d+\.\d+\.\d+$', value):
            issues.append(FrontmatterIssue(
                field="Version",
                issue_type="invalid_format",
                message=f"Version '{value}' should follow semantic versioning (e.g., '1.0.0')",
                suggestion="Use semantic versioning format: major.minor.patch"
            ))
        
        # Check version range
        try:
            major, minor, patch = map(int, value.split('.'))
            if major < 0 or minor < 0 or patch < 0:
                issues.append(FrontmatterIssue(
                    field="Version",
                    issue_type="invalid_value",
                    message=f"Version components must be non-negative",
                    suggestion="Ensure all version components are positive integers"
                ))
        except ValueError:
            pass  # Already caught by format check
        
        return issues
    
    def _validate_complexity_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Complexity field"""
        issues = []
        
        valid_complexities = ["Low", "Medium", "High", "Very High"]
        
        if value not in valid_complexities:
            issues.append(FrontmatterIssue(
                field="Complexity",
                issue_type="invalid_value",
                message=f"Complexity '{value}' is not valid",
                suggestion=f"Use one of: {', '.join(valid_complexities)}"
            ))
        
        return issues
    
    def _validate_execution_time_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Estimated Execution Time field"""
        issues = []
        
        # Check format: should contain range with " - "
        if " - " not in value:
            issues.append(FrontmatterIssue(
                field="Estimated Execution Time",
                issue_type="invalid_format",
                message=f"Execution time '{value}' should specify a range",
                suggestion="Use format like '100ms - 5 minutes'"
            ))
        
        # Check for time units
        time_units = ["ms", "s", "m", "h", "minute", "hour", "second"]
        if not any(unit in value for unit in time_units):
            issues.append(FrontmatterIssue(
                field="Estimated Execution Time",
                issue_type="semantic_error",
                message=f"Execution time '{value}' should include time units",
                suggestion="Include time units (ms, s, m, h, etc.)"
            ))
        
        return issues
    
    def _validate_type_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Type field"""
        issues = []
        
        valid_types = [
            "Tool", "Framework", "Library", "Language", "Platform", 
            "Specification", "Process", "Methodology", "Pattern"
        ]
        
        if value not in valid_types:
            issues.append(FrontmatterIssue(
                field="Type",
                issue_type="semantic_error",
                message=f"Type '{value}' is not in standard types",
                suggestion=f"Consider using one of: {', '.join(valid_types)}"
            ))
        
        return issues
    
    def _validate_category_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate Category field"""
        issues = []
        
        valid_categories = [
            "Quality Assurance", "Development", "Testing", "Deployment",
            "Monitoring", "Security", "Performance", "Documentation"
        ]
        
        if value not in valid_categories:
            issues.append(FrontmatterIssue(
                field="Category",
                issue_type="semantic_error",
                message=f"Category '{value}' is not in standard categories",
                suggestion=f"Consider using one of: {', '.join(valid_categories)}"
            ))
        
        return issues
    
    def _validate_optional_field(self, field: str, field_type: type, frontmatter: Dict, file_path: str) -> List[FrontmatterIssue]:
        """Validate an optional frontmatter field"""
        issues = []
        
        value = frontmatter[field]
        
        # Type validation
        if not isinstance(value, field_type):
            issues.append(FrontmatterIssue(
                field=field,
                issue_type="invalid_format",
                message=f"Field '{field}' should be {field_type.__name__}, got {type(value).__name__}",
                suggestion=f"Ensure '{field}' is properly formatted as {field_type.__name__}"
            ))
        
        # Value-specific validation for optional fields
        if field == "Dependencies" and isinstance(value, list):
            issues.extend(self._validate_dependencies_field(value, file_path))
        elif field == "License":
            issues.extend(self._validate_license_field(value, file_path))
        elif field == "Created" or field == "Last Modified":
            issues.extend(self._validate_date_field(value, field, file_path))
        
        return issues
    
    def _validate_dependencies_field(self, value: List, file_path: str) -> List[FrontmatterIssue]:
        """Validate Dependencies field"""
        issues = []
        
        for i, dep in enumerate(value):
            if not isinstance(dep, str) or not dep.strip():
                issues.append(FrontmatterIssue(
                    field="Dependencies",
                    issue_type="invalid_value",
                    message=f"Dependency at index {i} is invalid: {dep}",
                    suggestion="Dependencies should be non-empty strings"
                ))
        
        return issues
    
    def _validate_license_field(self, value: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate License field"""
        issues = []
        
        # Check for common license formats
        common_licenses = ["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "ISC"]
        
        if value not in common_licenses:
            issues.append(FrontmatterIssue(
                field="License",
                issue_type="semantic_warning",
                message=f"License '{value}' is not in common licenses list",
                suggestion=f"Consider using one of: {', '.join(common_licenses)}"
            ))
        
        return issues
    
    def _validate_date_field(self, value: str, field: str, file_path: str) -> List[FrontmatterIssue]:
        """Validate date fields (Created, Last Modified)"""
        issues = []
        
        # Check ISO date format
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            issues.append(FrontmatterIssue(
                field=field,
                issue_type="invalid_format",
                message=f"Date '{value}' should be in YYYY-MM-DD format",
                suggestion="Use ISO date format: YYYY-MM-DD"
            ))
        
        return issues
    
    def _validate_cross_fields(self, frontmatter: Dict, file_path: str) -> List[FrontmatterIssue]:
        """Validate relationships between fields"""
        issues = []
        
        # Check if Domain matches file path
        domain = frontmatter.get("Domain", "")
        if domain:
            # Extract domain from file path
            path_parts = file_path.split('/')
            if len(path_parts) >= 2:
                path_domain = path_parts[-2]  # skills/DOMAIN/SKILL.md
                if domain != path_domain:
                    issues.append(FrontmatterIssue(
                        field="Domain",
                        issue_type="semantic_error",
                        message=f"Domain '{domain}' doesn't match file path domain '{path_domain}'",
                        suggestion=f"Ensure Domain field matches the directory name: {path_domain}"
                    ))
        
        # Check version vs complexity relationship
        version = frontmatter.get("Version", "")
        complexity = frontmatter.get("Complexity", "")
        
        if version and complexity:
            try:
                major, minor, patch = map(int, version.split('.'))
                if major == 0 and complexity in ["High", "Very High"]:
                    issues.append(FrontmatterIssue(
                        field="Complexity",
                        issue_type="semantic_warning",
                        message=f"Version {version} with complexity '{complexity}' seems inconsistent",
                        suggestion="Consider lowering complexity for early versions"
                    ))
            except ValueError:
                pass
        
        return issues
    
    def generate_auto_fix_script(self, issues: List[FrontmatterIssue], file_path: str) -> Optional[str]:
        """Generate auto-fix script for frontmatter issues"""
        if not issues:
            return None
        
        script_lines = [
            f"# Auto-fix script for {file_path}",
            "import yaml",
            "",
            "def fix_frontmatter(file_path):",
            "    with open(file_path, 'r') as f:",
            "        content = f.read()",
            "",
            "    # Parse frontmatter",
            "    lines = content.split('\\n')",
            "    if lines[0] != '---':",
            "        return  # No frontmatter",
            "",
            "    # Find frontmatter end",
            "    frontmatter_end = -1",
            "    for i, line in enumerate(lines[1:], 1):",
            "        if line == '---':",
            "            frontmatter_end = i",
            "            break",
            "",
            "    if frontmatter_end == -1:",
            "        return",
            "",
            "    # Extract and parse frontmatter",
            "    frontmatter_lines = lines[1:frontmatter_end]",
            "    frontmatter_text = '\\n'.join(frontmatter_lines)",
            "    frontmatter = yaml.safe_load(frontmatter_text)",
            ""
        ]
        
        # Generate fixes for each issue
        for issue in issues:
            if issue.issue_type == "missing":
                script_lines.append(f"    # Add missing field: {issue.field}")
                script_lines.append(f"    if '{issue.field}' not in frontmatter:")
                script_lines.append(f"        frontmatter['{issue.field}'] = 'TBD'")
                script_lines.append("")
            
            elif issue.issue_type == "invalid_format" and issue.field == "Version":
                script_lines.append("    # Fix version format")
                script_lines.append("    if 'Version' in frontmatter:")
                script_lines.append("        frontmatter['Version'] = '1.0.0'")
                script_lines.append("")
        
        script_lines.extend([
            "    # Reconstruct file",
            "    new_frontmatter = yaml.dump(frontmatter, default_flow_style=False)",
            "    new_content = '---\\n' + new_frontmatter + '---\\n' + '\\n'.join(lines[frontmatter_end + 1:])",
            "",
            "    with open(file_path, 'w') as f:",
            "        f.write(new_content)",
            "",
            f"fix_frontmatter('{file_path}')"
        ])
        
        return '\\n'.join(script_lines)

# Example usage
def example_frontmatter_validation():
    """Example: Validate frontmatter in skills directory"""
    
    validator = FrontmatterValidator()
    
    # Validate all skill files
    import glob
    from pathlib import Path
    
    skill_files = list(Path("skills").glob("**/SKILL.*.md"))
    
    all_issues = []
    for skill_file in skill_files:
        issues = validator.validate_file(str(skill_file))
        if issues:
            print(f"\\n⚠️  Issues in {skill_file}:")
            for issue in issues:
                print(f"   {issue.issue_type}: {issue.message}")
            all_issues.extend(issues)
    
    print(f"\\n📊 Total issues found: {len(all_issues)}")
    
    # Generate auto-fix scripts
    if all_issues:
        print("\\n🔧 Generating auto-fix scripts...")
        for skill_file in skill_files:
            issues = validator.validate_file(str(skill_file))
            if issues:
                script = validator.generate_auto_fix_script(issues, str(skill_file))
                if script:
                    script_file = f"{skill_file}_fix.py"
                    with open(script_file, 'w') as f:
                        f.write(script)
                    print(f"   Generated: {script_file}")
    
    return all_issues

if __name__ == "__main__":
    example_frontmatter_validation()

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration
This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Best Practices

- **Specific Context**: Provide as much specific context as possible for more accurate results.
- **Regular Audits**: Use this skill as part of a recurring CI/CD quality gate.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.
- **Permission Errors**: Ensure the agent has read/write access to the target directories.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.

## Constraints

To be provided dynamically during execution.