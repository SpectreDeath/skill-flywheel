#!/usr/bin/env python3
"""
Mobile Development Format Validation Script

This script validates all skills in the repository against the mobile_development format
and generates comprehensive reports on compliance and quality.
"""

import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add skills directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

@dataclass
class MobileValidationIssue:
    """Issue found during mobile development format validation"""
    file_path: str
    section: str
    issue_type: str  # "missing", "format_error", "content_error", "mobile_specific"
    message: str
    severity: str  # "critical", "warning", "info"
    suggestion: Optional[str] = None
    line_number: Optional[int] = None

class MobileDevelopmentValidator:
    """Validates skills against mobile development format requirements"""
    
    def __init__(self, skills_root: str):
        """
        Initialize mobile development validator
        
        Args:
            skills_root: Path to the skills directory
        """
        self.skills_root = Path(skills_root)
        
        # Mobile development specific requirements
        self.mobile_required_sections = [
            "## Platform Support",
            "## Mobile Performance Considerations", 
            "## Platform Constraints",
            "## Mobile Testing Strategies"
        ]
        
        self.mobile_recommended_sections = [
            "## Battery Optimization",
            "## Network Considerations",
            "## Offline Functionality",
            "## Mobile Security"
        ]
        
        # Mobile-specific content patterns
        self.mobile_keywords = [
            "iOS", "Android", "mobile", "platform", "battery", "network", 
            "offline", "performance", "constraint", "testing", "framework"
        ]
        
        self.mobile_frameworks = [
            "React Native", "Flutter", "Xamarin", "Ionic", "Cordova",
            "Swift", "Kotlin", "Java", "Objective-C", "UIKit", "Android SDK"
        ]
    
    def validate_all_skills(self) -> Dict[str, Any]:
        """Validate all skills against mobile development format"""
        print("📱 Validating skills against mobile development format...")
        
        # Find all skill files
        skill_files = list(self.skills_root.glob("**/SKILL.*.md"))
        
        all_issues = []
        compliance_scores = {}
        mobile_skill_count = 0
        
        for skill_file in skill_files:
            issues = self._validate_skill_mobile_format(skill_file)
            all_issues.extend(issues)
            
            # Calculate mobile compliance score
            mobile_issues = [i for i in issues if i.issue_type == "mobile_specific"]
            total_issues = len(issues)
            mobile_compliance = max(0, 100 - (len(mobile_issues) * 15) - (total_issues * 5))
            
            compliance_scores[str(skill_file)] = {
                "mobile_compliance_score": mobile_compliance,
                "total_issues": total_issues,
                "mobile_issues": len(mobile_issues),
                "is_mobile_skill": self._is_mobile_skill(skill_file)
            }
            
            if self._is_mobile_skill(skill_file):
                mobile_skill_count += 1
        
        # Generate comprehensive report
        report = self._generate_mobile_validation_report(
            all_issues, compliance_scores, skill_files, mobile_skill_count
        )
        
        return report
    
    def _validate_skill_mobile_format(self, skill_file: Path) -> List[MobileValidationIssue]:
        """Validate individual skill against mobile development format"""
        issues = []
        
        try:
            with open(skill_file, encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            issues.append(MobileValidationIssue(
                file_path=str(skill_file),
                section="file",
                issue_type="read_error",
                message=f"Cannot read file: {e}",
                severity="critical"
            ))
            return issues
        
        # Check if this is a mobile development skill
        is_mobile_skill = self._is_mobile_skill(skill_file)
        
        if not is_mobile_skill:
            return issues  # Skip non-mobile skills for mobile-specific validation
        
        # Validate mobile-specific sections
        mobile_section_issues = self._validate_mobile_sections(content, skill_file)
        issues.extend(mobile_section_issues)
        
        # Validate mobile-specific content
        mobile_content_issues = self._validate_mobile_content(content, lines, skill_file)
        issues.extend(mobile_content_issues)
        
        # Validate mobile-specific frontmatter
        mobile_frontmatter_issues = self._validate_mobile_frontmatter(content, skill_file)
        issues.extend(mobile_frontmatter_issues)
        
        return issues
    
    def _is_mobile_skill(self, skill_file: Path) -> bool:
        """Determine if this is a mobile development skill"""
        try:
            with open(skill_file, encoding='utf-8') as f:
                content = f.read().lower()
        except:
            return False
        
        # Check frontmatter Domain
        frontmatter = self._extract_frontmatter(content)
        if frontmatter and frontmatter.get("Domain", "").lower() == "mobiledevelopment":
            return True
        
        # Check content for mobile keywords
        mobile_mentions = sum(1 for keyword in self.mobile_keywords if keyword.lower() in content)
        
        # Check for mobile frameworks
        framework_mentions = sum(1 for framework in self.mobile_frameworks if framework.lower() in content)
        
        # Consider it a mobile skill if it mentions mobile keywords or frameworks
        return mobile_mentions > 3 or framework_mentions > 1
    
    def _validate_mobile_sections(self, content: str, file_path: Path) -> List[MobileValidationIssue]:
        """Validate mobile-specific sections"""
        issues = []
        
        # Check for required mobile sections
        missing_mobile_sections = []
        for section in self.mobile_required_sections:
            if section not in content:
                missing_mobile_sections.append(section)
        
        if missing_mobile_sections:
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="mobile_sections",
                issue_type="mobile_specific",
                message=f"Missing required mobile sections: {', '.join(missing_mobile_sections)}",
                severity="critical",
                suggestion="Add all required mobile development sections"
            ))
        
        # Check for recommended mobile sections
        missing_recommended_sections = []
        for section in self.mobile_recommended_sections:
            if section not in content:
                missing_recommended_sections.append(section)
        
        if missing_recommended_sections:
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="mobile_sections",
                issue_type="mobile_specific",
                message=f"Consider adding recommended mobile sections: {', '.join(missing_recommended_sections)}",
                severity="warning",
                suggestion="Add recommended sections for better mobile development coverage"
            ))
        
        return issues
    
    def _validate_mobile_content(self, content: str, lines: List[str], file_path: Path) -> List[MobileValidationIssue]:
        """Validate mobile-specific content quality"""
        issues = []
        
        # Check for platform-specific considerations
        if "iOS" not in content and "Android" not in content:
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="content",
                issue_type="mobile_specific",
                message="No platform-specific considerations mentioned",
                severity="warning",
                suggestion="Include iOS and Android platform considerations"
            ))
        
        # Check for performance considerations
        if "performance" not in content.lower():
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="content",
                issue_type="mobile_specific",
                message="No mobile performance considerations mentioned",
                severity="warning",
                suggestion="Include mobile-specific performance considerations"
            ))
        
        # Check for testing strategies
        if "testing" not in content.lower() and "test" not in content.lower():
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="content",
                issue_type="mobile_specific",
                message="No mobile testing strategies mentioned",
                severity="warning",
                suggestion="Include mobile-specific testing strategies"
            ))
        
        # Check for framework mentions
        framework_count = sum(1 for framework in self.mobile_frameworks if framework.lower() in content.lower())
        if framework_count == 0:
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="content",
                issue_type="mobile_specific",
                message="No mobile development frameworks mentioned",
                severity="info",
                suggestion="Consider mentioning relevant mobile frameworks"
            ))
        
        return issues
    
    def _validate_mobile_frontmatter(self, content: str, file_path: Path) -> List[MobileValidationIssue]:
        """Validate mobile-specific frontmatter requirements"""
        issues = []
        
        frontmatter = self._extract_frontmatter(content)
        if not frontmatter:
            return issues
        
        # Check for mobile-specific frontmatter fields
        if "Platform Support" not in str(frontmatter):
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="frontmatter",
                issue_type="mobile_specific",
                message="No platform support information in frontmatter",
                severity="info",
                suggestion="Consider adding platform support details"
            ))
        
        # Check complexity for mobile skills
        complexity = frontmatter.get("Complexity", "").lower()
        if complexity in ["low", "medium"] and "mobile" in content.lower():
            issues.append(MobileValidationIssue(
                file_path=str(file_path),
                section="frontmatter",
                issue_type="mobile_specific",
                message="Mobile development typically requires higher complexity rating",
                severity="info",
                suggestion="Consider rating mobile skills as High or Very High complexity"
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
    
    def _generate_mobile_validation_report(self, all_issues: List[MobileValidationIssue],
                                         compliance_scores: Dict[str, Dict],
                                         skill_files: List[Path], 
                                         mobile_skill_count: int) -> Dict[str, Any]:
        """Generate comprehensive mobile validation report"""
        
        # Categorize issues
        issue_summary = defaultdict(int)
        severity_counts = defaultdict(int)
        mobile_issues = [i for i in all_issues if i.issue_type == "mobile_specific"]
        general_issues = [i for i in all_issues if i.issue_type != "mobile_specific"]
        
        for issue in all_issues:
            issue_summary[issue.issue_type] += 1
            severity_counts[issue.severity] += 1
        
        # Calculate overall mobile compliance
        total_mobile_issues = len(mobile_issues)
        total_skills = len(skill_files)
        mobile_compliance_score = max(0, 100 - (total_mobile_issues * 10))
        
        # Generate mobile-specific recommendations
        recommendations = self._generate_mobile_recommendations(mobile_issues, general_issues)
        
        report = {
            "summary": {
                "total_skills": total_skills,
                "mobile_skills": mobile_skill_count,
                "total_issues": len(all_issues),
                "mobile_specific_issues": total_mobile_issues,
                "general_issues": len(general_issues),
                "mobile_compliance_score": mobile_compliance_score,
                "issue_summary": dict(issue_summary),
                "severity_breakdown": dict(severity_counts)
            },
            "compliance_scores": compliance_scores,
            "issues": [vars(issue) for issue in all_issues],
            "mobile_issues": [vars(issue) for issue in mobile_issues],
            "general_issues": [vars(issue) for issue in general_issues],
            "recommendations": recommendations,
            "mobile_skill_details": {
                str(f): compliance_scores.get(str(f), {})
                for f in skill_files
                if compliance_scores.get(str(f), {}).get("is_mobile_skill", False)
            }
        }
        
        return report
    
    def _generate_mobile_recommendations(self, mobile_issues: List[MobileValidationIssue],
                                       general_issues: List[MobileValidationIssue]) -> List[str]:
        """Generate mobile-specific recommendations"""
        recommendations = []
        
        # Mobile-specific recommendations
        if any("missing" in issue.message.lower() for issue in mobile_issues):
            recommendations.append("Add all required mobile development sections to skills")
        
        if any("platform" in issue.message.lower() for issue in mobile_issues):
            recommendations.append("Include comprehensive platform-specific considerations")
        
        if any("performance" in issue.message.lower() for issue in mobile_issues):
            recommendations.append("Add mobile-specific performance optimization strategies")
        
        if any("testing" in issue.message.lower() for issue in mobile_issues):
            recommendations.append("Include mobile testing strategies and tools")
        
        # General recommendations
        recommendations.extend([
            "Use consistent mobile development terminology",
            "Include real-world mobile development examples",
            "Document platform-specific limitations and workarounds",
            "Add mobile-specific error handling patterns",
            "Include mobile security best practices",
            "Document battery and network optimization techniques",
            "Add offline functionality considerations",
            "Include mobile-specific deployment strategies"
        ])
        
        return recommendations

def main():
    """Main validation function"""
    print("📱 Mobile Development Format Validation")
    print("=" * 50)
    
    # Initialize validator
    validator = MobileDevelopmentValidator("skills")
    
    # Run validation
    report = validator.validate_all_skills()
    
    # Print summary
    summary = report["summary"]
    print("📊 Validation Summary:")
    print(f"   Total skills: {summary['total_skills']}")
    print(f"   Mobile skills: {summary['mobile_skills']}")
    print(f"   Total issues: {summary['total_issues']}")
    print(f"   Mobile-specific issues: {summary['mobile_specific_issues']}")
    print(f"   General issues: {summary['general_issues']}")
    print(f"   Mobile compliance score: {summary['mobile_compliance_score']}/100")
    
    # Print issue breakdown
    print("\\n🔍 Issue Breakdown:")
    for issue_type, count in summary['issue_summary'].items():
        print(f"   {issue_type}: {count}")
    
    print("\\n⚠️  Severity Breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        print(f"   {severity}: {count}")
    
    # Print top mobile issues
    if report["mobile_issues"]:
        print("\\n📱 Top Mobile Issues:")
        for i, issue in enumerate(report["mobile_issues"][:5]):
            print(f"   {i+1}. {issue['message']}")
    
    # Print recommendations
    if report["recommendations"]:
        print("\\n💡 Recommendations:")
        for i, rec in enumerate(report["recommendations"][:10]):
            print(f"   {i+1}. {rec}")
    
    # Save detailed report
    with open("mobile_validation_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\\n📁 Detailed report saved: mobile_validation_report.json")
    
    # Return success/failure based on compliance score
    if summary['mobile_compliance_score'] < 70:
        print("\\n❌ Mobile compliance score below 70% - review required")
        return 1
    else:
        print("\\n✅ Mobile compliance score acceptable")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
