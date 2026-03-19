#!/usr/bin/env python3
"""
Logic Domain Validation Script

Validates the skills/DOMAIN/logic/ domain using all 5 validation skills.
"""

import json
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def validate_logic_domain():
    """Validate the logic domain using all validation skills"""
    
    print("🔍 Validating skills/DOMAIN/logic/ domain...")
    print("=" * 50)
    
    # Find logic domain files
    logic_dir = Path("skills/DOMAIN/logic")
    if not logic_dir.exists():
        # Try absolute path
        logic_dir = Path(__file__).parent.parent.parent / "DOMAIN" / "logic"
        if not logic_dir.exists():
            print("❌ Logic domain directory not found")
            return
    
    logic_files = list(logic_dir.glob("SKILL.*.md"))
    print(f"📁 Found {len(logic_files)} skill files in logic domain")
    
    if not logic_files:
        print("⚠️  No skill files found in logic domain")
        return
    
    # Import validators
    try:
        # Import validators from current directory
        import sys
        sys.path.insert(0, '.')
        from dependency_analyzer import DependencyAnalyzer
        from format_compliance_tester import FormatComplianceTester
        from frontmatter_validator import FrontmatterValidator
        from naming_convention_checker import NamingConventionChecker
        from skill_spec_validator import AgentSkillsValidator
    except ImportError as e:
        print(f"❌ Failed to import validators: {e}")
        return
    
    # Initialize validators
    spec_validator = AgentSkillsValidator("skills")
    frontmatter_validator = FrontmatterValidator()
    naming_checker = NamingConventionChecker()
    dependency_analyzer = DependencyAnalyzer("skills")
    compliance_tester = FormatComplianceTester("skills")
    
    # Results storage
    results = {}
    
    # 1. Skill Spec Validator
    print("\\n1. Skill Spec Validator...")
    try:
        spec_report = spec_validator.run_full_validation()
        spec_failures = spec_report['summary']['fail_count']
        spec_status = "PASS" if spec_failures == 0 else "FAIL"
        results['skill_spec'] = {
            'status': spec_status,
            'failures': spec_failures,
            'details': spec_report
        }
        print(f"   Status: {spec_status} ({spec_failures} failures)")
    except Exception as e:
        results['skill_spec'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 2. Frontmatter Validator
    print("\\n2. Frontmatter Validator...")
    try:
        frontmatter_issues = []
        for skill_file in logic_files:
            issues = frontmatter_validator.validate_file(str(skill_file))
            frontmatter_issues.extend(issues)
        
        frontmatter_status = "PASS" if len(frontmatter_issues) == 0 else "FAIL"
        results['frontmatter'] = {
            'status': frontmatter_status,
            'issues': len(frontmatter_issues),
            'details': [vars(issue) for issue in frontmatter_issues]
        }
        print(f"   Status: {frontmatter_status} ({len(frontmatter_issues)} issues)")
    except Exception as e:
        results['frontmatter'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 3. Naming Convention Checker
    print("\\n3. Naming Convention Checker...")
    try:
        naming_violations = naming_checker.validate_repository(str(logic_dir))
        naming_status = "PASS" if len(naming_violations) == 0 else "FAIL"
        results['naming'] = {
            'status': naming_status,
            'violations': len(naming_violations),
            'details': [vars(violation) for violation in naming_violations]
        }
        print(f"   Status: {naming_status} ({len(naming_violations)} violations)")
    except Exception as e:
        results['naming'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 4. Dependency Analyzer
    print("\\n4. Dependency Analyzer...")
    try:
        dependency_report = dependency_analyzer.analyze_repository()
        dep_issues = (dependency_report['summary']['circular_dependencies'] + 
                     dependency_report['summary']['missing_dependencies'])
        dependency_status = "PASS" if dep_issues == 0 else "FAIL"
        results['dependencies'] = {
            'status': dependency_status,
            'issues': dep_issues,
            'details': dependency_report
        }
        print(f"   Status: {dependency_status} ({dep_issues} dependency issues)")
    except Exception as e:
        results['dependencies'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 5. Format Compliance Tester
    print("\\n5. Format Compliance Tester...")
    try:
        compliance_report = compliance_tester.test_repository_compliance()
        compliance_score = compliance_report['summary']['overall_compliance_score']
        compliance_status = "PASS" if compliance_score >= 80 else "FAIL"
        results['compliance'] = {
            'status': compliance_status,
            'score': compliance_score,
            'details': compliance_report
        }
        print(f"   Status: {compliance_status} (Score: {compliance_score}/100)")
    except Exception as e:
        results['compliance'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # Summary
    print("\\n📊 VALIDATION SUMMARY:")
    print(f"   Skill Spec Validator: {results.get('skill_spec', {}).get('status', 'N/A')}")
    print(f"   Frontmatter Validator: {results.get('frontmatter', {}).get('status', 'N/A')}")
    print(f"   Naming Convention Checker: {results.get('naming', {}).get('status', 'N/A')}")
    print(f"   Dependency Analyzer: {results.get('dependencies', {}).get('status', 'N/A')}")
    print(f"   Format Compliance Tester: {results.get('compliance', {}).get('status', 'N/A')}")
    
    # Save results
    with open("logic_domain_validation_report.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\\n📁 Detailed report saved: logic_domain_validation_report.json")
    
    # Return results for further processing
    return results

if __name__ == "__main__":
    validate_logic_domain()
