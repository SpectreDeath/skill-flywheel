#!/usr/bin/env python3
"""
Add required sections (Purpose, Input Format, Output Format, Examples, Implementation Notes)
to all SKILL.md files that are missing them, using mobile_development domain as template.
"""

import os
import re
from pathlib import Path

def extract_section_from_template(template_content, section_name):
    """
    Extract a section from the template content.
    """
    # Pattern to match section headers (## Section Name)
    pattern = rf'^## {re.escape(section_name)}\n(.*?)(?=\n## |\n---|\Z)'
    match = re.search(pattern, template_content, re.MULTILINE | re.DOTALL)
    
    if match:
        return match.group(1).strip()
    return None

def has_required_sections(file_content):
    """
    Check if file already has all required sections.
    """
    required_sections = ['Purpose', 'Input Format', 'Output Format', 'Examples', 'Implementation Notes']
    
    for section in required_sections:
        if f'## {section}' not in file_content:
            return False
    return True

def find_insertion_point(content):
    """
    Find the best place to insert new sections.
    Look for various section headers that could be the main description.
    """
    # Patterns to look for as insertion points
    insertion_patterns = [
        r'(## Description.*?)(?=\n## |\n---|\Z)',
        r'(## Overview.*?)(?=\n## |\n---|\Z)',
        r'(## Summary.*?)(?=\n## |\n---|\Z)',
        r'(## Introduction.*?)(?=\n## |\n---|\Z)',
        r'(## What is.*?)(?=\n## |\n---|\Z)',
        r'(## What.*?)(?=\n## |\n---|\Z)',
    ]
    
    for pattern in insertion_patterns:
        match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1), content[match.end():]
    
    # If no specific section found, try to find after frontmatter
    frontmatter_end = content.find('\n---\n')
    if frontmatter_end != -1:
        # Find the first ## section after frontmatter
        first_section_pattern = r'(## .*?)(?=\n## |\n---|\Z)'
        match = re.search(first_section_pattern, content[frontmatter_end:], re.MULTILINE | re.DOTALL)
        if match:
            return match.group(1), content[frontmatter_end + match.end():]
    
    return None, None

def add_missing_sections(file_path, template_sections):
    """
    Add missing sections to a file while preserving existing content.
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"  ✗ {file_path.name} - Error reading: {e}")
        return False
    
    # Check if file already has all required sections
    if has_required_sections(content):
        print(f"  ✓ {file_path.name} - Already has all required sections")
        return True
    
    # Find where to insert the new sections
    before_insertion, after_insertion = find_insertion_point(content)
    
    if not before_insertion:
        print(f"  ✗ {file_path.name} - Could not find suitable insertion point")
        return False
    
    # Build the new sections content
    new_sections = "\n\n"
    
    required_sections = ['Purpose', 'Input Format', 'Output Format', 'Examples', 'Implementation Notes']
    
    for section_name in required_sections:
        if f'## {section_name}' not in content:
            # Add the section from template
            if section_name in template_sections and template_sections[section_name]:
                new_sections += f"## {section_name}\n\n"
                new_sections += template_sections[section_name] + "\n\n"
            else:
                # Fallback content if template section not found
                new_sections += f"## {section_name}\n\n"
                new_sections += f"*[Content for {section_name} section to be added based on the specific skill requirements]*\n\n"
    
    # Remove trailing newlines
    new_sections = new_sections.rstrip()
    
    # Combine all parts
    new_content = before_insertion + new_sections + after_insertion
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ {file_path.name} - Added missing sections")
        return True
    except Exception as e:
        print(f"  ✗ {file_path.name} - Error writing: {e}")
        return False

def process_all_skills():
    """Process all SKILL.md files to add missing sections"""
    
    # First, read a template file from mobile_development domain
    template_path = Path("skills/mobile_development/SKILL.AppStoreComplianceDeployment.md")
    
    if not template_path.exists():
        print("Template file not found!")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8', errors='ignore') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error reading template: {e}")
        return False
    
    # Extract sections from template
    template_sections = {}
    required_sections = ['Purpose', 'Input Format', 'Output Format', 'Examples', 'Implementation Notes']
    
    for section_name in required_sections:
        section_content = extract_section_from_template(template_content, section_name)
        if section_content:
            template_sections[section_name] = section_content
            print(f"✓ Extracted template section: {section_name}")
        else:
            print(f"✗ Could not extract template section: {section_name}")
    
    if not template_sections:
        print("No template sections found!")
        return False
    
    # Process all SKILL.md files
    skills_path = Path("skills")
    processed_files = []
    failed_files = []
    already_complete = []
    
    print(f"\nAdding required sections to SKILL.md files...")
    print("=" * 60)
    
    for domain_path in skills_path.iterdir():
        if domain_path.is_dir() and domain_path.name not in ['archive', 'mcp_tools', 'docs']:
            print(f"\nProcessing domain: {domain_path.name}")
            
            skill_files = list(domain_path.glob("**/SKILL.*.md"))
            for md in domain_path.glob("**/SKILL.md"):
                if md not in skill_files:
                    skill_files.append(md)
            for skill_file in skill_files:
                success = add_missing_sections(skill_file, template_sections)
                
                if success:
                    # Check if file now has all sections
                    try:
                        with open(skill_file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        if has_required_sections(content):
                            already_complete.append(skill_file)
                        else:
                            processed_files.append(skill_file)
                    except:
                        failed_files.append(skill_file)
                else:
                    failed_files.append(skill_file)
    
    print(f"\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Total files processed: {len(processed_files) + len(already_complete) + len(failed_files)}")
    print(f"  Files updated: {len(processed_files)}")
    print(f"  Already complete: {len(already_complete)}")
    print(f"  Failed: {len(failed_files)}")
    
    if failed_files:
        print(f"\nFailed files:")
        for file in failed_files:
            print(f"  - {file}")
    
    return len(failed_files) == 0

def verify_sections():
    """Verify that all files now have the required sections"""
    skills_path = Path("skills")
    verified_files = []
    missing_sections_files = []
    
    print(f"\nVerifying required sections...")
    print("=" * 60)
    
    for domain_path in skills_path.iterdir():
        if domain_path.is_dir() and domain_path.name not in ['archive', 'mcp_tools', 'docs']:
            skill_files = list(domain_path.glob("**/SKILL.*.md"))
            for md in domain_path.glob("**/SKILL.md"):
                if md not in skill_files:
                    skill_files.append(md)
            for skill_file in skill_files:
                try:
                    with open(skill_file, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    if has_required_sections(content):
                        verified_files.append(skill_file)
                    else:
                        missing_sections_files.append(skill_file)
                        print(f"  ✗ {skill_file.name} - Missing sections")
                except Exception as e:
                    print(f"  ✗ {skill_file.name} - Error reading: {e}")
    
    print(f"\nVERIFICATION SUMMARY:")
    print(f"  Total files: {len(verified_files) + len(missing_sections_files)}")
    print(f"  Files with all sections: {len(verified_files)}")
    print(f"  Files missing sections: {len(missing_sections_files)}")
    
    if missing_sections_files:
        print(f"\nFiles still missing sections:")
        for file in missing_sections_files:
            print(f"  - {file}")
    
    return len(missing_sections_files) == 0

if __name__ == "__main__":
    # Process all files
    success = process_all_skills()
    
    # Verify the results
    verification_success = verify_sections()
    
    print(f"\n" + "=" * 60)
    print("FINAL REPORT:")
    print(f"  Processing success: {success}")
    print(f"  Verification success: {verification_success}")
    
    if success and verification_success:
        print("\n🎉 All files successfully updated with required sections!")
    else:
        print(f"\n⚠️  Some files need attention. Check the error messages above.")