---
Domain: skill_validation
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: format-compliance-tester
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

Comprehensive format compliance testing for SKILL.md files against the AgentSkills specification. This skill validates document structure, section completeness, formatting consistency, and adherence to established standards across the entire skills repository.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Section Completeness Validation**: Verify all required sections are present and properly formatted
- **Format Consistency Checking**: Ensure consistent formatting across all skill files
- **Content Quality Assessment**: Validate content quality and completeness
- **Cross-Reference Validation**: Check internal and external links
- **Template Compliance**: Verify adherence to skill templates
- **Automated Testing**: Run comprehensive test suites against specifications
- **Compliance Reporting**: Generate detailed compliance reports with actionable insights

## Usage Examples

### Comprehensive Format Compliance Testing

```python
"""
Format Compliance Testing for AgentSkills Repository
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ComplianceIssue:
    """Issue found during compliance testing"""
    file_path: str
    section: str
    issue_type: str  # "missing", "format_error", "content_error", "incomplete"
    message: str
    severity: str  # "critical", "warning", "info"
    suggestion: Optional[str] = None
    line_number: Optional[int] = None

class FormatComplianceTester:
    """Tests SKILL.md files for format compliance"""
    
    def __init__(self, skills_root: str):
        """
        Initialize compliance tester
        
        Args:
            skills_root: Path to the skills directory
        """
        self.skills_root = Path(skills_root)
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
        
        self.section_patterns = {
            "Description": r'^## Description\s*$',
            "Capabilities": r'^## Capabilities\s*$',
            "Usage Examples": r'^## Usage Examples\s*$',
            "Input Format": r'^## Input Format\s*$',
            "Output Format": r'^## Output Format\s*$',
            "Configuration Options": r'^## Configuration Options\s*$',
            "Error Handling": r'^## Error Handling\s*$',
            "Performance Optimization": r'^## Performance Optimization\s*$',
            "Integration Examples": r'^## Integration Examples\s*$',
            "Best Practices": r'^## Best Practices\s*$',
            "Troubleshooting": r'^## Troubleshooting\s*$',
            "Monitoring and Metrics": r'^## Monitoring and Metrics\s*$',
            "Dependencies": r'^## Dependencies\s*$',
            "Version History": r'^## Version History\s*$',
            "License": r'^## License\s*$'
        }
    
    def test_repository_compliance(self) -> Dict[str, Any]:
        """Test compliance across entire repository"""
        print("🔍 Testing format compliance across repository...")
        
        # Find all skill files
        skill_files = list(self.skills_root.glob("**/SKILL.*.md"))
        
        all_issues = []
        compliance_scores = {}
        
        for skill_file in skill_files:
            issues = self._test_skill_compliance(skill_file)
            all_issues.extend(issues)
            
            # Calculate compliance score
            total_checks = len(self.required_sections) + 5  # Sections + other checks
            failed_checks = len([i for i in issues if i.severity == "critical"])
            compliance_scores[str(skill_file)] = {
                "score": max(0, 100 - (failed_checks * 10)),
                "total_issues": len(issues),
                "critical_issues": failed_checks
            }
        
        # Generate compliance report
        report = self._generate_compliance_report(all_issues, compliance_scores, skill_files)
        
        return report
    
    def _test_skill_compliance(self, skill_file: Path) -> List[ComplianceIssue]:
        """Test compliance of individual skill file"""
        issues = []
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            issues.append(ComplianceIssue(
                file_path=str(skill_file),
                section="file",
                issue_type="read_error",
                message=f"Cannot read file: {e}",
                severity="critical"
            ))
            return issues
        
        # Test frontmatter compliance
        frontmatter_issues = self._test_frontmatter_compliance(content, skill_file)
        issues.extend(frontmatter_issues)
        
        # Test section compliance
        section_issues = self._test_section_compliance(content, lines, skill_file)
        issues.extend(section_issues)
        
        # Test content quality
        content_issues = self._test_content_quality(content, lines, skill_file)
        issues.extend(content_issues)
        
        # Test formatting consistency
        format_issues = self._test_formatting_consistency(content, lines, skill_file)
        issues.extend(format_issues)
        
        return issues
    
    def _test_frontmatter_compliance(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Test frontmatter compliance"""
        issues = []
        
        # Check for frontmatter
        if not content.startswith('---'):
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="frontmatter",
                issue_type="missing",
                message="No YAML frontmatter found",
                severity="critical",
                suggestion="Add YAML frontmatter with required fields"
            ))
            return issues
        
        # Parse frontmatter
        frontmatter = self._extract_frontmatter(content)
        if frontmatter is None:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="frontmatter",
                issue_type="format_error",
                message="Invalid YAML frontmatter format",
                severity="critical",
                suggestion="Fix YAML frontmatter syntax"
            ))
            return issues
        
        # Test required fields
        required_fields = ["Domain", "Version", "Type", "Category", "Estimated Execution Time", "Complexity"]
        for field in required_fields:
            if field not in frontmatter:
                issues.append(ComplianceIssue(
                    file_path=str(file_path),
                    section="frontmatter",
                    issue_type="missing",
                    message=f"Required field '{field}' missing from frontmatter",
                    severity="critical",
                    suggestion=f"Add '{field}' field to frontmatter"
                ))
            else:
                # Validate field format
                field_issues = self._validate_field_format(field, frontmatter[field], file_path)
                issues.extend(field_issues)
        
        return issues
    
    def _test_section_compliance(self, content: str, lines: List[str], file_path: Path) -> List[ComplianceIssue]:
        """Test section compliance"""
        issues = []
        
        # Check for required sections
        missing_sections = []
        for section in self.required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="sections",
                issue_type="missing",
                message=f"Missing required sections: {', '.join(missing_sections)}",
                severity="critical",
                suggestion="Add all required sections to skill documentation"
            ))
        
        # Check section ordering (basic check)
        section_positions = {}
        for section in self.required_sections:
            pos = content.find(section)
            if pos != -1:
                section_positions[section] = pos
        
        if len(section_positions) > 1:
            positions = list(section_positions.values())
            if positions != sorted(positions):
                issues.append(ComplianceIssue(
                    file_path=str(file_path),
                    section="sections",
                    issue_type="format_error",
                    message="Sections may not be in optimal order",
                    severity="warning",
                    suggestion="Consider reordering sections for better flow"
                ))
        
        # Check section content quality
        for section_name, pattern in self.section_patterns.items():
            if section_name in [s.replace("## ", "") for s in self.required_sections]:
                section_issues = self._test_section_content(content, section_name, pattern, file_path)
                issues.extend(section_issues)
        
        return issues
    
    def _test_section_content(self, content: str, section_name: str, pattern: str, file_path: Path) -> List[ComplianceIssue]:
        """Test individual section content quality"""
        issues = []
        
        # Find section
        section_match = re.search(pattern, content, re.MULTILINE)
        if not section_match:
            return issues
        
        section_start = section_match.end()
        
        # Find next section or end of file
        next_section_match = re.search(r'^## \w+', content[section_start:], re.MULTILINE)
        if next_section_match:
            section_end = section_start + next_section_match.start()
        else:
            section_end = len(content)
        
        section_content = content[section_start:section_end].strip()
        
        # Check content quality based on section type
        if section_name == "Description":
            desc_issues = self._validate_description_content(section_content, file_path)
            issues.extend(desc_issues)
        elif section_name == "Capabilities":
            cap_issues = self._validate_capabilities_content(section_content, file_path)
            issues.extend(cap_issues)
        elif section_name == "Usage Examples":
            example_issues = self._validate_usage_examples_content(section_content, file_path)
            issues.extend(example_issues)
        
        return issues
    
    def _validate_description_content(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Validate Description section content"""
        issues = []
        
        if not content or len(content.strip()) < 50:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Description",
                issue_type="content_error",
                message="Description is too short or missing",
                severity="warning",
                suggestion="Provide a comprehensive description of the skill"
            ))
        
        # Check for placeholder text
        if "TBD" in content or "TBD" in content or "EXAMPLE" in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Description",
                issue_type="content_error",
                message="Description contains placeholder text",
                severity="warning",
                suggestion="Replace placeholder text with actual content"
            ))
        
        return issues
    
    def _validate_capabilities_content(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Validate Capabilities section content"""
        issues = []
        
        # Check for bullet points
        if "•" not in content and "-" not in content and "*" not in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Capabilities",
                issue_type="format_error",
                message="Capabilities should be listed as bullet points",
                severity="warning",
                suggestion="Use bullet points to list capabilities"
            ))
        
        # Check for empty capabilities
        if len(content.strip()) < 20:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Capabilities",
                issue_type="content_error",
                message="Capabilities section is too short",
                severity="warning",
                suggestion="Provide detailed capabilities with specific examples"
            ))
        
        return issues
    
    def _validate_usage_examples_content(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Validate Usage Examples section content"""
        issues = []
        
        # Check for code blocks
        if "```" not in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Usage Examples",
                issue_type="format_error",
                message="Usage examples should include code blocks",
                severity="warning",
                suggestion="Add code examples with proper syntax highlighting"
            ))
        
        # Check for language specification in code blocks
        if "```python" not in content and "```javascript" not in content and "```bash" not in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="Usage Examples",
                issue_type="format_error",
                message="Code blocks should specify language for syntax highlighting",
                severity="info",
                suggestion="Specify language in code block headers (e.g., ```python)"
            ))
        
        return issues
    
    def _test_content_quality(self, content: str, lines: List[str], file_path: Path) -> List[ComplianceIssue]:
        """Test overall content quality"""
        issues = []
        
        # Check for excessive placeholder content
        placeholder_count = content.count("TBD") + content.count("TBD") + content.count("EXAMPLE")
        if placeholder_count > 5:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="content",
                issue_type="content_error",
                message=f"Too many placeholder references ({placeholder_count})",
                severity="warning",
                suggestion="Replace placeholders with actual content"
            ))
        
        # Check for proper markdown formatting
        if "# " in content and "## " not in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="content",
                issue_type="format_error",
                message="Inconsistent heading levels detected",
                severity="info",
                suggestion="Use consistent heading hierarchy"
            ))
        
        # Check for broken links
        link_issues = self._check_broken_links(content, file_path)
        issues.extend(link_issues)
        
        return issues
    
    def _test_formatting_consistency(self, content: str, lines: List[str], file_path: Path) -> List[ComplianceIssue]:
        """Test formatting consistency"""
        issues = []
        
        # Check for consistent indentation
        indent_issues = self._check_indentation_consistency(lines, file_path)
        issues.extend(indent_issues)
        
        # Check for consistent spacing
        spacing_issues = self._check_spacing_consistency(content, file_path)
        issues.extend(spacing_issues)
        
        # Check for consistent code block formatting
        code_issues = self._check_code_block_consistency(content, file_path)
        issues.extend(code_issues)
        
        return issues
    
    def _check_broken_links(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Check for broken links"""
        issues = []
        
        # Find markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, content)
        
        for link_text, link_url in links:
            # Check relative links to other skill files
            if link_url.startswith("SKILL.") and link_url.endswith(".md"):
                target_path = file_path.parent / link_url
                if not target_path.exists():
                    issues.append(ComplianceIssue(
                        file_path=str(file_path),
                        section="links",
                        issue_type="content_error",
                        message=f"Broken link to skill file: {link_url}",
                        severity="warning",
                        suggestion=f"Check if skill file exists: {link_url}"
                    ))
        
        return issues
    
    def _check_indentation_consistency(self, lines: List[str], file_path: Path) -> List[ComplianceIssue]:
        """Check for consistent indentation"""
        issues = []
        
        # Check for mixed tabs and spaces
        has_tabs = any('\t' in line for line in lines)
        has_spaces = any(line.startswith(' ') for line in lines)
        
        if has_tabs and has_spaces:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="formatting",
                issue_type="format_error",
                message="Mixed tabs and spaces detected",
                severity="info",
                suggestion="Use consistent indentation (spaces recommended)"
            ))
        
        return issues
    
    def _check_spacing_consistency(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Check for consistent spacing"""
        issues = []
        
        # Check for multiple consecutive blank lines
        if '\n\n\n' in content:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="formatting",
                issue_type="format_error",
                message="Multiple consecutive blank lines detected",
                severity="info",
                suggestion="Use single blank lines for separation"
            ))
        
        # Check for trailing whitespace
        trailing_whitespace_lines = [i+1 for i, line in enumerate(content.split('\n')) if line.endswith(' ') or line.endswith('\t')]
        if len(trailing_whitespace_lines) > 5:  # Allow some trailing whitespace
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="formatting",
                issue_type="format_error",
                message=f"Trailing whitespace on {len(trailing_whitespace_lines)} lines",
                severity="info",
                suggestion="Remove trailing whitespace"
            ))
        
        return issues
    
    def _check_code_block_consistency(self, content: str, file_path: Path) -> List[ComplianceIssue]:
        """Check for consistent code block formatting"""
        issues = []
        
        # Check for unclosed code blocks
        code_block_count = content.count('```')
        if code_block_count % 2 != 0:
            issues.append(ComplianceIssue(
                file_path=str(file_path),
                section="formatting",
                issue_type="format_error",
                message="Unclosed code block detected",
                severity="warning",
                suggestion="Ensure all code blocks are properly closed with ```"
            ))
        
        return issues
    
    def _validate_field_format(self, field: str, value: Any, file_path: Path) -> List[ComplianceIssue]:
        """Validate individual frontmatter field format"""
        issues = []
        
        if field == "Version":
            if not re.match(r'^\d+\.\d+\.\d+$', str(value)):
                issues.append(ComplianceIssue(
                    file_path=str(file_path),
                    section="frontmatter",
                    issue_type="format_error",
                    message=f"Invalid version format: {value}",
                    severity="critical",
                    suggestion="Use semantic versioning format: major.minor.patch"
                ))
        
        elif field == "Complexity":
            valid_complexities = ["Low", "Medium", "High", "Very High"]
            if str(value) not in valid_complexities:
                issues.append(ComplianceIssue(
                    file_path=str(file_path),
                    section="frontmatter",
                    issue_type="format_error",
                    message=f"Invalid complexity value: {value}",
                    severity="critical",
                    suggestion=f"Use one of: {', '.join(valid_complexities)}"
                ))
        
        elif field == "Estimated Execution Time":
            if " - " not in str(value):
                issues.append(ComplianceIssue(
                    file_path=str(file_path),
                    section="frontmatter",
                    issue_type="format_error",
                    message=f"Execution time should specify a range: {value}",
                    severity="warning",
                    suggestion="Use format like '100ms - 5 minutes'"
                ))
        
        return issues
    
    def _extract_frontmatter(self, content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from content"""
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
    
    def _generate_compliance_report(self, all_issues: List[ComplianceIssue], 
                                  compliance_scores: Dict[str, Dict], 
                                  skill_files: List[Path]) -> Dict[str, Any]:
        """Generate comprehensive compliance report"""
        
        # Categorize issues
        issue_summary = defaultdict(int)
        severity_counts = defaultdict(int)
        file_issues = defaultdict(list)
        
        for issue in all_issues:
            issue_summary[issue.issue_type] += 1
            severity_counts[issue.severity] += 1
            file_issues[issue.file_path].append(issue)
        
        # Calculate overall compliance score
        total_files = len(skill_files)
        total_critical_issues = severity_counts.get("critical", 0)
        overall_score = max(0, 100 - (total_critical_issues * 5))
        
        # Generate recommendations
        recommendations = self._generate_compliance_recommendations(all_issues, issue_summary)
        
        report = {
            "summary": {
                "total_files": total_files,
                "total_issues": len(all_issues),
                "overall_compliance_score": overall_score,
                "issue_summary": dict(issue_summary),
                "severity_breakdown": dict(severity_counts)
            },
            "compliance_scores": compliance_scores,
            "issues": [vars(issue) for issue in all_issues],
            "recommendations": recommendations,
            "file_details": {
                str(f): {
                    "issues": [vars(i) for i in file_issues.get(str(f), [])],
                    "score": compliance_scores.get(str(f), {}).get("score", 0)
                }
                for f in skill_files
            }
        }
        
        return report
    
    def _generate_compliance_recommendations(self, all_issues: List[ComplianceIssue], 
                                           issue_summary: Dict[str, int]) -> List[str]:
        """Generate recommendations based on compliance issues"""
        recommendations = []
        
        # Critical issues recommendations
        if issue_summary.get("missing", 0) > 10:
            recommendations.append("Address missing required sections in multiple skill files")
        
        if issue_summary.get("format_error", 0) > 20:
            recommendations.append("Review and standardize formatting across all skill files")
        
        if issue_summary.get("content_error", 0) > 15:
            recommendations.append("Improve content quality and completeness")
        
        # General recommendations
        recommendations.extend([
            "Use consistent heading hierarchy (## for sections, ### for subsections)",
            "Ensure all code examples have proper syntax highlighting",
            "Validate all internal links point to existing files",
            "Remove placeholder text and replace with actual content",
            "Use consistent indentation (2 or 4 spaces recommended)",
            "Follow the established skill template structure",
            "Review frontmatter fields for completeness and accuracy"
        ])
        
        return recommendations

# Example usage
def example_compliance_testing():
    """Example: Test format compliance across skills repository"""
    
    tester = FormatComplianceTester("skills")
    
    # Run compliance testing
    report = tester.test_repository_compliance()
    
    # Print summary
    summary = report["summary"]
    print("📊 Format Compliance Report:")
    print(f"   Total files: {summary['total_files']}")
    print(f"   Total issues: {summary['total_issues']}")
    print(f"   Overall score: {summary['overall_compliance_score']}/100")
    
    # Print issue breakdown
    print("\\n🔍 Issue Breakdown:")
    for issue_type, count in summary['issue_summary'].items():
        print(f"   {issue_type}: {count}")
    
    print("\\n⚠️  Severity Breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        print(f"   {severity}: {count}")
    
    # Save detailed report
    with open("compliance_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\\n📁 Report saved: compliance_report.json")
    
    return report

if __name__ == "__main__":
    example_compliance_testing()

## Constraints

To be provided dynamically during execution.