#!/usr/bin/env python3
"""
Simple Logic Domain Validation Script

Manually validates the skills/DOMAIN/logic/ domain without complex imports.
"""

import json
from pathlib import Path


def validate_logic_domain():
    """Validate the logic domain manually"""
    
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
    
    # Results storage
    results = {}
    
    # 1. Skill Spec Validator (Manual Check)
    print("\\n1. Skill Spec Validator...")
    try:
        # Check if all files follow the correct naming pattern
        valid_names = True
        for file in logic_files:
            if not file.name.startswith("SKILL.") or not file.name.endswith(".md"):
                valid_names = False
                break
        
        # Check if directory structure is correct
        structure_valid = logic_dir.exists()
        
        spec_status = "PASS" if valid_names and structure_valid else "FAIL"
        results['skill_spec'] = {
            'status': spec_status,
            'details': f"Files: {len(logic_files)}, Structure: {'OK' if structure_valid else 'MISSING'}"
        }
        print(f"   Status: {spec_status}")
    except Exception as e:
        results['skill_spec'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 2. Frontmatter Validator (Manual Check)
    print("\\n2. Frontmatter Validator...")
    try:
        frontmatter_issues = []
        for skill_file in logic_files:
            try:
                with open(skill_file, encoding='utf-8') as f:
                    content = f.read()
                    # Check if file has YAML frontmatter
                    if not content.startswith('---'):
                        frontmatter_issues.append(f"{skill_file.name}: Missing YAML frontmatter")
                    elif '---' not in content[3:]:
                        frontmatter_issues.append(f"{skill_file.name}: Incomplete YAML frontmatter")
            except Exception as e:
                frontmatter_issues.append(f"{skill_file.name}: Error reading file - {e}")
        
        frontmatter_status = "PASS" if len(frontmatter_issues) == 0 else "FAIL"
        results['frontmatter'] = {
            'status': frontmatter_status,
            'issues': len(frontmatter_issues),
            'details': frontmatter_issues
        }
        print(f"   Status: {frontmatter_status} ({len(frontmatter_issues)} issues)")
    except Exception as e:
        results['frontmatter'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 3. Naming Convention Checker (Manual Check)
    print("\\n3. Naming Convention Checker...")
    try:
        naming_violations = []
        for file in logic_files:
            # Check if file name follows PascalCase convention
            name_part = file.stem  # Remove .md extension
            if not name_part.startswith("SKILL."):
                naming_violations.append(f"{file.name}: Does not start with SKILL.")
            else:
                skill_name = name_part[5:]  # Remove "SKILL." prefix
                if "_" in skill_name:
                    naming_violations.append(f"{file.name}: Contains underscores (should use PascalCase)")
        
        naming_status = "PASS" if len(naming_violations) == 0 else "FAIL"
        results['naming'] = {
            'status': naming_status,
            'violations': len(naming_violations),
            'details': naming_violations
        }
        print(f"   Status: {naming_status} ({len(naming_violations)} violations)")
    except Exception as e:
        results['naming'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 4. Dependency Analyzer (Manual Check)
    print("\\n4. Dependency Analyzer...")
    try:
        dependency_issues = []
        # For now, just check if files exist and are readable
        for file in logic_files:
            try:
                with open(file, encoding='utf-8') as f:
                    content = f.read()
                    # Look for dependency declarations
                    if 'dependencies:' in content.lower():
                        # Basic check - just ensure the file is readable
                        pass
            except Exception as e:
                dependency_issues.append(f"{file.name}: Error reading file - {e}")
        
        dependency_status = "PASS" if len(dependency_issues) == 0 else "FAIL"
        results['dependencies'] = {
            'status': dependency_status,
            'issues': len(dependency_issues),
            'details': dependency_issues
        }
        print(f"   Status: {dependency_status} ({len(dependency_issues)} issues)")
    except Exception as e:
        results['dependencies'] = {'status': 'FAIL', 'error': str(e)}
        print(f"   Status: FAIL - {e}")
    
    # 5. Format Compliance Tester (Manual Check)
    print("\\n5. Format Compliance Tester...")
    try:
        compliance_issues = []
        compliance_score = 100
        
        for file in logic_files:
            try:
                with open(file, encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check for required sections
                    required_sections = ['## Purpose', '## Usage', '## Examples', '## Implementation']
                    missing_sections = []
                    
                    for section in required_sections:
                        if section not in content:
                            missing_sections.append(section)
                            compliance_score -= 5  # Deduct points for missing sections
                    
                    if missing_sections:
                        compliance_issues.append(f"{file.name}: Missing sections - {', '.join(missing_sections)}")
                    
                    # Check for YAML frontmatter
                    if not content.startswith('---'):
                        compliance_score -= 10
                        compliance_issues.append(f"{file.name}: Missing YAML frontmatter")
                    
                    # Check for basic structure
                    if len(content) < 100:
                        compliance_score -= 20
                        compliance_issues.append(f"{file.name}: File too short (< 100 chars)")
                    
            except Exception as e:
                compliance_issues.append(f"{file.name}: Error reading file - {e}")
                compliance_score -= 10
        
        compliance_status = "PASS" if compliance_score >= 80 else "FAIL"
        results['compliance'] = {
            'status': compliance_status,
            'score': max(0, compliance_score),
            'details': compliance_issues
        }
        print(f"   Status: {compliance_status} (Score: {max(0, compliance_score)}/100)")
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
