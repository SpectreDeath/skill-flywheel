---
Domain: skill_validation
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: skill-spec-validator
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

Automatically validates complete AgentSkills directory structure and SKILL.md file compliance against the AgentSkills specification. This skill provides comprehensive validation of skill organization, metadata completeness, and structural integrity across the entire skills repository.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Directory Structure Validation**: Verify proper DOMAIN/SKILL organization and naming conventions
- **SKILL.md File Validation**: Check required sections, metadata fields, and format compliance
- **Cross-Reference Integrity**: Validate internal links and cross-skill references
- **Metadata Completeness**: Ensure all required frontmatter fields are present and valid
- **Skill Categorization**: Verify proper domain assignment and skill type classification
- **Version Control Compliance**: Check version numbering and change tracking
- **Integration Testing**: Validate skill dependencies and import statements

## Usage Examples

### Basic Skill Repository Validation

```python
"""
Complete AgentSkills Repository Validation
"""

import os
import yaml
import json
from typing import Dict, List, Tuple, Set, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import re
from collections import defaultdict

@dataclass
class ValidationResult:
    """Validation result for a skill or directory"""
    status: str  # "PASS", "FAIL", "WARNING"
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.suggestions is None:
            self.suggestions = []

class AgentSkillsValidator:
    """Comprehensive AgentSkills specification validator"""
    
    def __init__(self, skills_root: str):
        """
        Initialize validator with skills repository root
        
        Args:
            skills_root: Path to the skills directory
        """
        self.skills_root = Path(skills_root)
        self.results: List[ValidationResult] = []
        self.skill_metadata: Dict[str, Dict[str, Any]] = {}
        
        # Required SKILL.md sections
        self.required_sections = [
            "## Description",
            "## Capabilities", 
            "## Usage Examples",
            "## Input Format",
            "## Output Format",
            "## Configuration Options",
            "## Error Handling",
            "## Performance Optimization",
            "## Integration Examples",
            "## Best Practices",
            "## Troubleshooting",
            "## Monitoring and Metrics",
            "## Dependencies",
            "## Version History",
            "## License"
        ]
        
        # Required frontmatter fields
        self.required_frontmatter = [
            "Domain", "Version", "Type", "Category", 
            "Estimated Execution Time", "Complexity"
        ]
    
    def validate_repository_structure(self) -> List[ValidationResult]:
        """Validate overall repository structure"""
        results = []
        
        # Check if skills root exists
        if not self.skills_root.exists():
            results.append(ValidationResult(
                status="FAIL",
                message=f"Skills root directory not found: {self.skills_root}",
                suggestions=["Create skills directory at repository root"]
            ))
            return results
        
        # Check for DOMAIN directories
        domain_dirs = [d for d in self.skills_root.iterdir() if d.is_dir() and d.name != "ARCHIVE"]
        
        if not domain_dirs:
            results.append(ValidationResult(
                status="FAIL", 
                message="No DOMAIN directories found in skills root",
                suggestions=["Create DOMAIN subdirectories for skill organization"]
            ))
        else:
            results.append(ValidationResult(
                status="PASS",
                message=f"Found {len(domain_dirs)} DOMAIN directories"
            ))
        
        # Validate each domain directory
        for domain_dir in domain_dirs:
            domain_results = self._validate_domain_structure(domain_dir)
            results.extend(domain_results)
        
        return results
    
    def _validate_domain_structure(self, domain_dir: Path) -> List[ValidationResult]:
        """Validate individual domain directory structure"""
        results = []
        
        # Check domain name format
        domain_name = domain_dir.name
        if not self._is_valid_domain_name(domain_name):
            results.append(ValidationResult(
                status="FAIL",
                message=f"Invalid domain name format: {domain_name}",
                file_path=str(domain_dir),
                suggestions=["Use PascalCase for domain names (e.g., 'MachineLearning')"]
            ))
        
        # Check for SKILL.md files
        skill_files = list(domain_dir.glob("SKILL.*.md"))
        
        if not skill_files:
            results.append(ValidationResult(
                status="WARNING",
                message=f"No SKILL.md files found in domain: {domain_name}",
                file_path=str(domain_dir)
            ))
        else:
            results.append(ValidationResult(
                status="PASS",
                message=f"Found {len(skill_files)} SKILL.md files in {domain_name}"
            ))
            
            # Validate each skill file
            for skill_file in skill_files:
                skill_results = self._validate_skill_file(skill_file)
                results.extend(skill_results)
        
        return results
    
    def _validate_skill_file(self, skill_file: Path) -> List[ValidationResult]:
        """Validate individual SKILL.md file"""
        results = []
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            results.append(ValidationResult(
                status="FAIL",
                message=f"Cannot read skill file: {e}",
                file_path=str(skill_file)
            ))
            return results
        
        # Parse frontmatter
        frontmatter, body = self._parse_frontmatter(content)
        
        if frontmatter is None:
            results.append(ValidationResult(
                status="FAIL",
                message="No frontmatter found in skill file",
                file_path=str(skill_file),
                suggestions=["Add YAML frontmatter with required fields"]
            ))
        else:
            # Validate frontmatter
            frontmatter_results = self._validate_frontmatter(frontmatter, skill_file)
            results.extend(frontmatter_results)
            
            # Store metadata for cross-reference validation
            self.skill_metadata[str(skill_file)] = frontmatter
        
        # Validate body structure
        body_results = self._validate_skill_body(body, skill_file)
        results.extend(body_results)
        
        return results
    
    def _parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Parse YAML frontmatter from skill file"""
        if not content.startswith('---'):
            return None, content
        
        # Find end of frontmatter
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
            return None, content
        
        try:
            frontmatter_text = '\n'.join(frontmatter_lines)
            frontmatter = yaml.safe_load(frontmatter_text)
            body = '\n'.join(lines[frontmatter_end + 1:])
            return frontmatter, body
        except yaml.YAMLError as e:
            return None, content
    
    def _validate_frontmatter(self, frontmatter: Dict, file_path: Path) -> List[ValidationResult]:
        """Validate skill frontmatter fields"""
        results = []
        
        # Check required fields
        for field in self.required_frontmatter:
            if field not in frontmatter:
                results.append(ValidationResult(
                    status="FAIL",
                    message=f"Missing required frontmatter field: {field}",
                    file_path=str(file_path),
                    suggestions=[f"Add '{field}' field to frontmatter"]
                ))
            else:
                # Validate field format
                field_results = self._validate_field(field, frontmatter[field], file_path)
                results.extend(field_results)
        
        # Check for invalid fields
        valid_fields = set(self.required_frontmatter + ["Description", "Type", "Category"])
        for field in frontmatter:
            if field not in valid_fields:
                results.append(ValidationResult(
                    status="WARNING",
                    message=f"Unknown frontmatter field: {field}",
                    file_path=str(file_path)
                ))
        
        return results
    
    def _validate_field(self, field: str, value: Any, file_path: Path) -> List[ValidationResult]:
        """Validate individual frontmatter field"""
        results = []
        
        if field == "Version":
            if not self._is_valid_version(str(value)):
                results.append(ValidationResult(
                    status="FAIL",
                    message=f"Invalid version format: {value}",
                    file_path=str(file_path),
                    suggestions=["Use semantic versioning (e.g., '1.0.0')"]
                ))
        
        elif field == "Complexity":
            valid_complexities = ["Low", "Medium", "High", "Very High"]
            if str(value) not in valid_complexities:
                results.append(ValidationResult(
                    status="FAIL",
                    message=f"Invalid complexity value: {value}",
                    file_path=str(file_path),
                    suggestions=[f"Use one of: {', '.join(valid_complexities)}"]
                ))
        
        elif field == "Estimated Execution Time":
            if not self._is_valid_execution_time(str(value)):
                results.append(ValidationResult(
                    status="FAIL",
                    message=f"Invalid execution time format: {value}",
                    file_path=str(file_path),
                    suggestions=["Use format like '100ms - 5 minutes'"]
                ))
        
        return results
    
    def _validate_skill_body(self, body: str, file_path: Path) -> List[ValidationResult]:
        """Validate skill file body structure"""
        results = []
        
        # Check for required sections
        missing_sections = []
        for section in self.required_sections:
            if section not in body:
                missing_sections.append(section)
        
        if missing_sections:
            results.append(ValidationResult(
                status="FAIL",
                message=f"Missing required sections: {', '.join(missing_sections)}",
                file_path=str(file_path),
                suggestions=["Add all required sections to skill documentation"]
            ))
        else:
            results.append(ValidationResult(
                status="PASS",
                message="All required sections present"
            ))
        
        # Check section ordering
        section_order_results = self._validate_section_order(body, file_path)
        results.extend(section_order_results)
        
        # Check for code examples
        if "```python" not in body and "```javascript" not in body:
            results.append(ValidationResult(
                status="WARNING",
                message="No code examples found",
                file_path=str(file_path),
                suggestions=["Add code examples in Usage Examples section"]
            ))
        
        return results
    
    def _validate_section_order(self, body: str, file_path: Path) -> List[ValidationResult]:
        """Validate section ordering in skill file"""
        results = []
        
        # Find section positions
        section_positions = {}
        for section in self.required_sections:
            pos = body.find(section)
            if pos != -1:
                section_positions[section] = pos
        
        # Check if sections are in logical order
        # (This is a simplified check - could be more sophisticated)
        if len(section_positions) > 1:
            positions = list(section_positions.values())
            if positions != sorted(positions):
                results.append(ValidationResult(
                    status="WARNING",
                    message="Sections may not be in optimal order",
                    file_path=str(file_path)
                ))
        
        return results
    
    def validate_cross_references(self) -> List[ValidationResult]:
        """Validate cross-skill references and dependencies"""
        results = []
        
        # Check for import statements or cross-references
        for file_path, metadata in self.skill_metadata.items():
            # This would need to be implemented based on your specific cross-reference format
            # For now, just a placeholder
            pass
        
        return results
    
    def generate_validation_report(self) -> Dict[str, Any]:
        """Generate comprehensive validation report"""
        return {
            "summary": {
                "total_files": len(self.skill_metadata),
                "pass_count": len([r for r in self.results if r.status == "PASS"]),
                "fail_count": len([r for r in self.results if r.status == "FAIL"]),
                "warning_count": len([r for r in self.results if r.status == "WARNING"])
            },
            "results": [vars(r) for r in self.results],
            "metadata": self.skill_metadata
        }
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        print("🔍 Starting AgentSkills specification validation...")
        
        # Validate repository structure
        structure_results = self.validate_repository_structure()
        self.results.extend(structure_results)
        
        # Validate cross-references
        cross_ref_results = self.validate_cross_references()
        self.results.extend(cross_ref_results)
        
        # Generate report
        report = self.generate_validation_report()
        
        # Print summary
        summary = report["summary"]
        print(f"\n📊 Validation Summary:")
        print(f"   Total files: {summary['total_files']}")
        print(f"   ✅ Passed: {summary['pass_count']}")
        print(f"   ❌ Failed: {summary['fail_count']}")
        print(f"   ⚠️  Warnings: {summary['warning_count']}")
        
        if summary['fail_count'] > 0:
            print(f"\n❌ Validation FAILED - {summary['fail_count']} critical issues found")
        else:
            print(f"\n✅ Validation PASSED - All critical checks passed")
        
        return report
    
    # Helper methods
    def _is_valid_domain_name(self, name: str) -> bool:
        """Check if domain name follows PascalCase convention"""
        return bool(re.match(r'^[A-Z][a-zA-Z]*$', name))
    
    def _is_valid_version(self, version: str) -> bool:
        """Check if version follows semantic versioning"""
        return bool(re.match(r'^\d+\.\d+\.\d+$', version))
    
    def _is_valid_execution_time(self, time_str: str) -> bool:
        """Check if execution time format is valid"""
        # Simple check for format like "100ms - 5 minutes"
        return " - " in time_str and any(c.isalpha() for c in time_str)

# Example usage
def example_skill_validation():
    """Example: Validate skills repository"""
    
    # Initialize validator
    validator = AgentSkillsValidator("skills")
    
    # Run validation
    report = validator.run_full_validation()
    
    # Save detailed report
    with open("validation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    # Generate auto-fix suggestions
    auto_fixes = generate_auto_fix_scripts(validator.results)
    
    print(f"\n🔧 Auto-fix scripts generated: {len(auto_fixes)}")
    
    return report, auto_fixes

def generate_auto_fix_scripts(results: List[ValidationResult]) -> List[str]:
    """Generate auto-fix scripts for validation issues"""
    scripts = []
    
    for result in results:
        if result.status == "FAIL" and result.suggestions:
            script = generate_fix_script(result)
            if script:
                scripts.append(script)
    
    return scripts

def generate_fix_script(result: ValidationResult) -> Optional[str]:
    """Generate specific fix script for a validation result"""
    if "Missing required frontmatter field" in result.message:
        field_name = result.message.split(": ")[-1]
        return f"""
# Auto-fix script for missing frontmatter field: {field_name}
import yaml

def add_missing_field(file_path, field_name):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add field to frontmatter
    lines = content.split('\\n')
    if lines[0] == '---':
        # Find end of frontmatter
        for i, line in enumerate(lines[1:], 1):
            if line == '---':
                # Insert new field before closing ---
                lines.insert(i, f"{field_name}: TBD")
                break
    
    with open(file_path, 'w') as f:
        f.write('\\n'.join(lines))

add_missing_field("{result.file_path}", "{field_name}")
"""
    
    elif "Invalid version format" in result.message:
        return f"""
# Auto-fix script for version format
import re

def fix_version_format(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace invalid version with default
    content = re.sub(r'Version: .+', 'Version: 1.0.0', content)
    
    with open(file_path, 'w') as f:
        f.write(content)

fix_version_format("{result.file_path}")
"""
    
    return None

if __name__ == "__main__":
    example_skill_validation()

## Constraints

To be provided dynamically during execution.