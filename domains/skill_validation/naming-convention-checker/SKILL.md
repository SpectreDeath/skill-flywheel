---
Domain: skill_validation
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: naming-convention-checker
---



## Description

Enforces consistent naming conventions across the AgentSkills repository. This skill validates file names, directory names, and internal identifiers to ensure they follow established patterns and conventions for maintainability and discoverability.


## Purpose

*[Content for Purpose section to be added based on the specific skill requirements]*

## Input Format

### Deployment Configuration Request

```yaml
deployment_configuration_request:
  application_id: string          # Unique application identifier
  application_name: string        # Application name
  target_stores: array            # Target app stores (App Store, Google Play, etc.)
  
  platform_configurations:
    ios:
      bundle_identifier: string   # iOS bundle identifier
      team_id: string             # Apple Developer Team ID
      provisioning_profile: string # Provisioning profile name
      certificate_id: string      # Certificate identifier
    
    android:
      package_name: string        # Android package name
      keystore_file: string       # Keystore file path
      keystore_password: string   # Keystore password
      key_alias: string           # Key alias
      key_password: string        # Key password
  
  compliance_requirements:
    privacy_policy_url: string    # Privacy policy URL
    terms_of_service_url: string  # Terms of service URL
    data_usage_disclosure: object # Data usage disclosure information
    age_rating: string            # App age rating
    content_descriptors: array    # Content descriptors
  
  deployment_strategy:
    rollout_strategy: "immediate|staged|phased"
    rollout_percentage: number    # Initial rollout percentage
    monitoring_enabled: boolean   # Whether monitoring is enabled
    rollback_enabled: boolean     # Whether automatic rollback is enabled
```

### App Store Metadata Schema

```yaml
app_store_metadata:
  app_information:
    app_name: string              # App name
    subtitle: string              # App subtitle (iOS only)
    app_description: string       # App description
    keywords: array               # App keywords
    support_url: string           # Support URL
    marketing_url: string         # Marketing URL
  
  visual_assets:
    app_icon: string              # App icon file path
    screenshots: array            # Screenshots for different devices
    app_preview: string           # App preview video (iOS only)
    feature_graphic: string       # Feature graphic (Android only)
  
  technical_information:
    bundle_size: string           # App bundle size
    supported_devices: array      # Supported device types
    required_permissions: array   # Required app permissions
    background_modes: array       # Background modes (iOS only)
  
  compliance_information:
    privacy_policy: string        # Privacy policy content
    terms_of_service: string      # Terms of service content
    data_collection_purposes: array # Data collection purposes
    third_party_integrations: array # Third-party integrations
```

## Output Format

### Deployment Report

```yaml
deployment_report:
  application_id: string
  deployment_timestamp: timestamp
  target_stores: array
  overall_status: "success|failed|partial"
  
  store_specific_reports:
    - store_name: "Apple App Store"
      status: "submitted|approved|rejected|in_review"
      submission_id: string
      review_status: string
      estimated_review_time: string
      compliance_status: "compliant|non_compliant"
      compliance_issues: array
      next_steps: array
    
    - store_name: "Google Play Store"
      status: "published|pending|rejected"
      track: "internal|alpha|beta|production"
      rollout_percentage: number
      compliance_status: "compliant|non_compliant"
      compliance_issues: array
      next_steps: array
  
  build_information:
    build_number: string
    build_time: string
    build_artifacts: array
    code_signing_status: "valid|invalid"
    bundle_size: string
  
  compliance_summary:
    total_checks: number
    passed_checks: number
    failed_checks: number
    compliance_percentage: number
    critical_issues: array
    warnings: array
  
  deployment_metrics:
    deployment_time: string
    success_rate: number
    rollback_count: number
    user_impact: string
```

### Compliance Validation Report

```yaml
compliance_validation_report:
  validation_timestamp: timestamp
  validation_scope: "full|partial|targeted"
  
  app_store_guidelines:
    apple_app_store:
      total_guidelines: 100
      validated_guidelines: 95
      compliant_guidelines: 92
      non_compliant_guidelines: 3
      critical_violations: array
      warnings: array
    
    google_play_store:
      total_policies: 50
      validated_policies: 50
      compliant_policies: 50
      non_compliant_policies: 0
      critical_violations: array
      warnings: array
  
  technical_requirements:
    ios_requirements:
      app_size: "compliant|non_compliant"
      launch_screen: "compliant|non_compliant"
      app_icons: "compliant|non_compliant"
      bitcode: "compliant|non_compliant"
    
    android_requirements:
      app_bundle: "compliant|non_compliant"
      target_sdk: "compliant|non_compliant"
      permissions: "compliant|non_compliant"
      app_size: "compliant|non_compliant"
  
  security_compliance:
    data_encryption: "compliant|non_compliant"
    secure_communication: "compliant|non_compliant"
    authentication_requirements: "compliant|non_compliant"
    privacy_compliance: "compliant|non_compliant"
  
  recommendations:
    - priority: "high"
      category: "compliance"
      recommendation: string
      impact: string
      effort: string
    
    - priority: "medium"
      category: "performance"
      recommendation: string
      impact: string
      effort: string
```

## Examples

*[Content for Examples section to be added based on the specific skill requirements]*

## Implementation Notes

*[Content for Implementation Notes section to be added based on the specific skill requirements]*
## Capabilities

- **File Name Validation**: Check SKILL.md files follow SKILL.{name}.md pattern
- **Directory Naming**: Validate DOMAIN directories use PascalCase
- **Internal Identifier Consistency**: Check skill names match file names
- **Cross-Reference Validation**: Ensure links and references use correct names
- **Convention Reporting**: Generate reports on naming violations
- **Auto-Correction Suggestions**: Provide suggestions for fixing naming issues
- **Batch Processing**: Validate entire repository efficiently

## Usage Examples

### Validate Repository Naming Conventions

```python
"""
Naming Convention Validation for AgentSkills Repository
"""

import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass

@dataclass
class NamingViolation:
    """Violation of naming conventions"""
    file_path: str
    violation_type: str  # "file_name", "directory_name", "internal_consistency"
    message: str
    suggestion: Optional[str] = None
    line_number: Optional[int] = None

class NamingConventionChecker:
    """Enforces naming conventions across AgentSkills repository"""
    
    def __init__(self):
        # Naming patterns
        self.skill_file_pattern = r'^SKILL\.[A-Z][a-zA-Z0-9_]*\.md$'
        self.domain_dir_pattern = r'^[A-Z][a-zA-Z0-9]*$'
        self.skill_name_pattern = r'^[A-Z][a-zA-Z0-9_]*$'
        
        # Common violations and fixes
        self.violation_fixes = {
            "snake_case": "Convert to PascalCase",
            "kebab_case": "Convert to PascalCase", 
            "lowercase": "Convert to PascalCase",
            "spaces": "Remove spaces and use PascalCase",
            "special_chars": "Remove special characters"
        }
    
    def validate_repository(self, root_path: str) -> List[NamingViolation]:
        """Validate naming conventions across entire repository"""
        violations = []
        
        root_path = Path(root_path)
        
        # Check domain directories
        domain_dirs = [d for d in root_path.iterdir() if d.is_dir() and d.name != "ARCHIVE"]
        
        for domain_dir in domain_dirs:
            domain_violations = self._validate_domain_directory(domain_dir)
            violations.extend(domain_violations)
            
            # Check skill files in domain
            skill_files = list(domain_dir.glob("SKILL.*.md"))
            for skill_file in skill_files:
                skill_violations = self._validate_skill_file(skill_file)
                violations.extend(skill_violations)
        
        return violations
    
    def _validate_domain_directory(self, domain_dir: Path) -> List[NamingViolation]:
        """Validate domain directory naming"""
        violations = []
        
        domain_name = domain_dir.name
        
        # Check PascalCase format
        if not re.match(self.domain_dir_pattern, domain_name):
            violations.append(NamingViolation(
                file_path=str(domain_dir),
                violation_type="directory_name",
                message=f"Domain directory '{domain_name}' should use PascalCase",
                suggestion=self._suggest_pascal_case_fix(domain_name)
            ))
        
        # Check for reserved names
        reserved_names = ["ARCHIVE", "TEMPLATE", "EXAMPLE", "TEST"]
        if domain_name in reserved_names:
            violations.append(NamingViolation(
                file_path=str(domain_dir),
                violation_type="directory_name",
                message=f"Domain name '{domain_name}' is reserved",
                suggestion="Use a different domain name"
            ))
        
        return violations
    
    def _validate_skill_file(self, skill_file: Path) -> List[NamingViolation]:
        """Validate individual skill file naming and content"""
        violations = []
        
        # Check file name pattern
        file_name = skill_file.name
        if not re.match(self.skill_file_pattern, file_name):
            violations.append(NamingViolation(
                file_path=str(skill_file),
                violation_type="file_name",
                message=f"Skill file '{file_name}' should follow SKILL.{Name}.md pattern",
                suggestion=self._suggest_skill_file_fix(file_name)
            ))
        
        # Extract skill name from file name
        skill_name = self._extract_skill_name(file_name)
        
        # Validate internal consistency
        internal_violations = self._validate_internal_consistency(skill_file, skill_name)
        violations.extend(internal_violations)
        
        return violations
    
    def _extract_skill_name(self, file_name: str) -> str:
        """Extract skill name from file name"""
        # SKILL.Name.md -> Name
        match = re.match(r'^SKILL\.([^.]+)\.md$', file_name)
        if match:
            return match.group(1)
        return ""
    
    def _validate_internal_consistency(self, skill_file: Path, expected_name: str) -> List[NamingViolation]:
        """Validate that internal references match file name"""
        violations = []
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            violations.append(NamingViolation(
                file_path=str(skill_file),
                violation_type="internal_consistency",
                message=f"Cannot read file: {e}"
            ))
            return violations
        
        # Check title line
        for i, line in enumerate(lines[:10]):  # Check first 10 lines for title
            if line.startswith('# SKILL:'):
                title = line.strip().replace('# SKILL:', '').strip()
                if title != expected_name:
                    violations.append(NamingViolation(
                        file_path=str(skill_file),
                        violation_type="internal_consistency",
                        message=f"Title '{title}' doesn't match file name '{expected_name}'",
                        suggestion=f"Change title to: {expected_name}",
                        line_number=i + 1
                    ))
                break
        
        # Check frontmatter Domain field
        frontmatter_end = self._find_frontmatter_end(lines)
        if frontmatter_end > 0:
            domain_violations = self._validate_frontmatter_domain(lines[:frontmatter_end], skill_file)
            violations.extend(domain_violations)
        
        # Check cross-references
        reference_violations = self._validate_cross_references(lines, skill_file, expected_name)
        violations.extend(reference_violations)
        
        return violations
    
    def _find_frontmatter_end(self, lines: List[str]) -> int:
        """Find end of YAML frontmatter"""
        in_frontmatter = False
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    return i
        return -1
    
    def _validate_frontmatter_domain(self, frontmatter_lines: List[str], file_path: Path) -> List[NamingViolation]:
        """Validate Domain field in frontmatter"""
        violations = []
        
        frontmatter_text = '\n'.join(frontmatter_lines)
        domain_match = re.search(r'Domain:\s*(.+)', frontmatter_text)
        
        if domain_match:
            domain = domain_match.group(1).strip()
            expected_domain = file_path.parent.name
            
            if domain != expected_domain:
                violations.append(NamingViolation(
                    file_path=str(file_path),
                    violation_type="internal_consistency",
                    message=f"Frontmatter Domain '{domain}' doesn't match directory '{expected_domain}'",
                    suggestion=f"Change Domain to: {expected_domain}"
                ))
        
        return violations
    
    def _validate_cross_references(self, lines: List[str], file_path: Path, skill_name: str) -> List[NamingViolation]:
        """Validate cross-references use correct naming"""
        violations = []
        
        # Check for references to this skill
        for i, line in enumerate(lines):
            # Check for skill name references
            if skill_name.lower() in line.lower():
                # Check if case matches
                if skill_name not in line:
                    violations.append(NamingViolation(
                        file_path=str(file_path),
                        violation_type="internal_consistency",
                        message=f"Skill name '{skill_name}' case mismatch in line {i+1}",
                        suggestion=f"Use exact case: {skill_name}",
                        line_number=i + 1
                    ))
            
            # Check for file path references
            if "SKILL." in line and ".md" in line:
                # Validate referenced skill files exist
                referenced_files = re.findall(r'SKILL\.[^.]+\.md', line)
                for ref_file in referenced_files:
                    ref_path = file_path.parent / ref_file
                    if not ref_path.exists():
                        violations.append(NamingViolation(
                            file_path=str(file_path),
                            violation_type="internal_consistency",
                            message=f"Referenced skill file '{ref_file}' does not exist",
                            suggestion=f"Check if file exists or fix reference",
                            line_number=i + 1
                        ))
        
        return violations
    
    def _suggest_pascal_case_fix(self, name: str) -> str:
        """Suggest PascalCase fix for a name"""
        # Remove special characters
        clean_name = re.sub(r'[^a-zA-Z0-9]', '', name)
        
        # Convert to PascalCase
        if not clean_name:
            return "Use alphanumeric characters in PascalCase format"
        
        # Split on common separators and capitalize
        words = re.split(r'[_\-\s]+', clean_name)
        pascal_case = ''.join(word.capitalize() for word in words if word)
        
        if pascal_case != name:
            return f"Consider renaming to: {pascal_case}"
        
        return "Use PascalCase format (e.g., 'MachineLearning')"
    
    def _suggest_skill_file_fix(self, file_name: str) -> str:
        """Suggest fix for skill file name"""
        # Extract potential skill name
        base_name = file_name.replace('.md', '')
        
        # Remove SKILL prefix if present
        if base_name.startswith('SKILL.'):
            base_name = base_name[6:]
        
        # Convert to proper format
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '', base_name)
        
        if clean_name:
            # Capitalize first letter
            proper_name = clean_name[0].upper() + clean_name[1:] if clean_name else clean_name
            return f"Rename to: SKILL.{proper_name}.md"
        
        return "Use format: SKILL.{Name}.md where Name is PascalCase"
    
    def generate_naming_report(self, violations: List[NamingViolation]) -> Dict[str, Any]:
        """Generate comprehensive naming convention report"""
        report = {
            "summary": {
                "total_violations": len(violations),
                "by_type": {},
                "by_file": {},
                "severity": {"critical": 0, "warning": 0}
            },
            "violations": [],
            "recommendations": []
        }
        
        # Categorize violations
        for violation in violations:
            # Count by type
            report["summary"]["by_type"][violation.violation_type] = \
                report["summary"]["by_type"].get(violation.violation_type, 0) + 1
            
            # Count by file
            report["summary"]["by_file"][violation.file_path] = \
                report["summary"]["by_file"].get(violation.file_path, 0) + 1
            
            # Determine severity
            if violation.violation_type in ["file_name", "directory_name"]:
                report["summary"]["severity"]["critical"] += 1
            else:
                report["summary"]["severity"]["warning"] += 1
            
            # Add to violations list
            report["violations"].append({
                "file": violation.file_path,
                "type": violation.violation_type,
                "message": violation.message,
                "suggestion": violation.suggestion,
                "line": violation.line_number
            })
        
        # Generate recommendations
        report["recommendations"] = self._generate_recommendations(violations)
        
        return report
    
    def _generate_recommendations(self, violations: List[NamingViolation]) -> List[str]:
        """Generate recommendations based on violation patterns"""
        recommendations = []
        
        # Count violation types
        violation_counts = {}
        for v in violations:
            violation_counts[v.violation_type] = violation_counts.get(v.violation_type, 0) + 1
        
        # Generate specific recommendations
        if violation_counts.get("file_name", 0) > 5:
            recommendations.append("Consider creating a naming convention guide for skill file names")
        
        if violation_counts.get("directory_name", 0) > 3:
            recommendations.append("Review domain directory naming and establish clear guidelines")
        
        if violation_counts.get("internal_consistency", 0) > 10:
            recommendations.append("Implement automated checks for internal consistency in CI/CD")
        
        # General recommendations
        recommendations.extend([
            "Use consistent PascalCase for all domain and skill names",
            "Ensure file names match internal skill names",
            "Validate cross-references point to existing files",
            "Consider using automated naming validation in your workflow"
        ])
        
        return recommendations
    
    def generate_auto_rename_scripts(self, violations: List[NamingViolation]) -> List[str]:
        """Generate scripts to automatically fix naming violations"""
        scripts = []
        
        # Group violations by file
        file_violations = {}
        for violation in violations:
            if violation.file_path not in file_violations:
                file_violations[violation.file_path] = []
            file_violations[violation.file_path].append(violation)
        
        # Generate rename scripts for files
        for file_path, file_vios in file_violations.items():
            file_path_obj = Path(file_path)
            
            # Check if file name needs fixing
            name_vios = [v for v in file_vios if v.violation_type == "file_name"]
            if name_vios:
                script = self._generate_file_rename_script(file_path_obj, name_vios[0])
                if script:
                    scripts.append(script)
        
        return scripts
    
    def _generate_file_rename_script(self, file_path: Path, violation: NamingViolation) -> Optional[str]:
        """Generate script to rename a file"""
        if "SKILL." in violation.message and ".md" in violation.message:
            # Extract suggested name from message
            suggestion_match = re.search(r'SKILL\.([^\.]+)\.md', violation.suggestion or "")
            if suggestion_match:
                new_name = suggestion_match.group(1)
                new_file_path = file_path.parent / f"SKILL.{new_name}.md"
                
                return f"""
# Auto-rename script for {file_path.name}
import os
import shutil

def rename_skill_file():
    old_path = "{file_path}"
    new_path = "{new_file_path}"
    
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)
        print(f"Renamed: {{old_path}} -> {{new_path}}")
    else:
        print(f"File not found: {{old_path}}")

rename_skill_file()
"""
        
        return None

# Example usage
def example_naming_validation():
    """Example: Validate naming conventions in skills directory"""
    
    checker = NamingConventionChecker()
    
    # Validate repository
    violations = checker.validate_repository("skills")
    
    # Generate report
    report = checker.generate_naming_report(violations)
    
    print("📊 Naming Convention Report:")
    print(f"   Total violations: {report['summary']['total_violations']}")
    print(f"   Critical: {report['summary']['severity']['critical']}")
    print(f"   Warnings: {report['summary']['severity']['warning']}")
    
    # Print violations by type
    print("\\n🔍 Violations by type:")
    for vtype, count in report['summary']['by_type'].items():
        print(f"   {vtype}: {count}")
    
    # Generate auto-fix scripts
    if violations:
        print("\\n🔧 Generating auto-fix scripts...")
        scripts = checker.generate_auto_rename_scripts(violations)
        
        for i, script in enumerate(scripts):
            script_file = f"auto_rename_{i+1}.py"
            with open(script_file, 'w') as f:
                f.write(script)
            print(f"   Generated: {script_file}")
    
    # Save detailed report
    import json
    with open("naming_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    return report, violations

if __name__ == "__main__":
    example_naming_validation()

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

Content for ## Constraints involving Naming Convention Checker.