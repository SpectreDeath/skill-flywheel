#!/usr/bin/env python3
"""
Simple compliance checker for required sections in skill files.
This script checks for the presence of required sections without needing API keys.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class ComplianceChecker:
    def __init__(self, skills_root: str = "skills"):
        self.skills_root = Path(skills_root)
        self.required_sections = ['Purpose', 'Examples', 'Implementation Notes', 'Constraints']
        
    def get_all_skill_files(self) -> List[Path]:
        """Get all SKILL.md files in the skills directory."""
        skill_files = []
        for root, dirs, files in os.walk(self.skills_root):
            # Skip template and archive directories
            if any(skip in root.lower() for skip in ['template', 'archive', 'archived']):
                continue
                
            for file in files:
                if file == "SKILL.md":
                    skill_files.append(Path(root) / file)
        return skill_files
    
    def check_skill_compliance(self, skill_path: Path) -> Dict:
        """Check compliance of a single skill file."""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract existing sections
            sections = self.extract_sections(content)
            
            # Check compliance
            missing_sections = [section for section in self.required_sections if section not in sections]
            present_sections = [section for section in self.required_sections if section in sections]
            
            # Calculate compliance score
            compliance_score = len(present_sections) / len(self.required_sections) * 100
            
            return {
                'path': skill_path,
                'compliance_score': compliance_score,
                'missing_sections': missing_sections,
                'present_sections': present_sections,
                'total_sections': len(sections),
                'sections': sections
            }
        except Exception as e:
            print(f"Error checking {skill_path}: {e}")
            return None
    
    def extract_sections(self, content: str) -> Dict[str, str]:
        """Extract existing sections from skill content."""
        sections = {}
        
        # Pattern to match markdown headers
        header_pattern = r'^##\s+(.+)$'
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            if re.match(header_pattern, line):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()  # Remove '## '
                current_content = []
            elif current_section:
                current_content.append(line)
        
        # Don't forget the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections
    
    def get_domain_stats(self, skill_files: List[Path]) -> Dict:
        """Get compliance statistics by domain."""
        domain_stats = {}
        
        for skill_file in skill_files:
            # Extract domain from path
            domain = skill_file.parts[1] if len(skill_file.parts) > 1 else 'root'
            
            if domain not in domain_stats:
                domain_stats[domain] = {
                    'total_skills': 0,
                    'compliant_skills': 0,
                    'total_score': 0,
                    'missing_sections': {}
                }
            
            compliance = self.check_skill_compliance(skill_file)
            if compliance:
                domain_stats[domain]['total_skills'] += 1
                domain_stats[domain]['total_score'] += compliance['compliance_score']
                
                if compliance['compliance_score'] == 100:
                    domain_stats[domain]['compliant_skills'] += 1
                
                # Track missing sections
                for missing in compliance['missing_sections']:
                    if missing not in domain_stats[domain]['missing_sections']:
                        domain_stats[domain]['missing_sections'][missing] = 0
                    domain_stats[domain]['missing_sections'][missing] += 1
        
        # Calculate averages
        for domain in domain_stats:
            stats = domain_stats[domain]
            if stats['total_skills'] > 0:
                stats['average_score'] = stats['total_score'] / stats['total_skills']
            else:
                stats['average_score'] = 0
        
        return domain_stats
    
    def print_compliance_report(self):
        """Print a comprehensive compliance report."""
        print("Agent Skills Library Compliance Report")
        print("=" * 60)
        
        skill_files = self.get_all_skill_files()
        print(f"Total skill files: {len(skill_files)}")
        print()
        
        # Overall statistics
        total_compliant = 0
        total_score = 0
        missing_sections_count = {}
        
        for skill_file in skill_files:
            compliance = self.check_skill_compliance(skill_file)
            if compliance:
                total_score += compliance['compliance_score']
                if compliance['compliance_score'] == 100:
                    total_compliant += 1
                
                for missing in compliance['missing_sections']:
                    if missing not in missing_sections_count:
                        missing_sections_count[missing] = 0
                    missing_sections_count[missing] += 1
        
        overall_score = total_score / len(skill_files) if skill_files else 0
        
        print("OVERALL STATISTICS")
        print(f"Overall compliance score: {overall_score:.1f}%")
        print(f"Fully compliant skills: {total_compliant}/{len(skill_files)} ({total_compliant/len(skill_files)*100:.1f}%)")
        print()
        
        print("MISSING SECTIONS ANALYSIS")
        for section, count in sorted(missing_sections_count.items(), key=lambda x: x[1], reverse=True):
            percentage = count / len(skill_files) * 100
            print(f"- {section}: {count} skills ({percentage:.1f}%)")
        print()
        
        # Domain-wise statistics
        print("DOMAIN-WISE STATISTICS")
        domain_stats = self.get_domain_stats(skill_files)
        
        for domain, stats in sorted(domain_stats.items()):
            if stats['total_skills'] > 0:
                print(f"\n{domain.upper()}:")
                print(f"  Skills: {stats['total_skills']}")
                print(f"  Compliant: {stats['compliant_skills']} ({stats['compliant_skills']/stats['total_skills']*100:.1f}%)")
                print(f"  Average score: {stats['average_score']:.1f}%")
                
                if stats['missing_sections']:
                    print(f"  Missing sections:")
                    for section, count in sorted(stats['missing_sections'].items(), key=lambda x: x[1], reverse=True):
                        percentage = count / stats['total_skills'] * 100
                        print(f"    - {section}: {count} skills ({percentage:.1f}%)")
        
        print()
        print("DETAILED MISSING SECTIONS")
        print("-" * 40)
        
        for skill_file in skill_files:
            compliance = self.check_skill_compliance(skill_file)
            if compliance and compliance['missing_sections']:
                relative_path = skill_file.relative_to(self.skills_root)
                missing_str = ', '.join(compliance['missing_sections'])
                print(f"{relative_path}: {missing_str}")
        
        print()
        print("COMPLIANCE SUMMARY")
        print("-" * 40)
        print(f"✓ Skills with all required sections: {total_compliant}")
        print(f"✗ Skills missing sections: {len(skill_files) - total_compliant}")
        print(f"📊 Overall compliance: {overall_score:.1f}%")
        
        return {
            'total_skills': len(skill_files),
            'compliant_skills': total_compliant,
            'overall_score': overall_score,
            'missing_sections': missing_sections_count,
            'domain_stats': domain_stats
        }

def main():
    """Main entry point."""
    checker = ComplianceChecker()
    results = checker.print_compliance_report()
    
    # Save results to JSON
    import json
    with open('compliance_check_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to compliance_check_results.json")

if __name__ == "__main__":
    main()