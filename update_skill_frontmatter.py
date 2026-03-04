#!/usr/bin/env python3
"""
Update all SKILL.md files with proper AgentSkills YAML frontmatter
"""

import os
import re
from pathlib import Path

def extract_description_from_content(content):
    """
    Extract a concise description from the file content.
    Looks for the first meaningful description after any existing frontmatter.
    """
    # Remove existing YAML frontmatter if present
    content_without_frontmatter = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    # Look for the main title (should be after frontmatter)
    title_match = re.search(r'^# SKILL: (.+)$', content_without_frontmatter, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        return f"{title} - Use for {title.lower()} operations and implementations."
    
    # Fallback: use filename-based description
    return "Algorithm skill for operations. Use when working with systems requiring capabilities."

def update_skill_file(file_path):
    """Update a single SKILL.md file with proper frontmatter"""
    
    # Extract skill name from filename
    filename = file_path.name
    skill_name = filename.replace('SKILL.', '').replace('.md', '')
    
    # Read current content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    # Extract description from content
    description = extract_description_from_content(content)
    
    # Create new frontmatter
    new_frontmatter = f"""---
name: {skill_name}
description: {description}
license: Apache-2.0
---

"""
    
    # Remove existing YAML frontmatter if present
    content_without_frontmatter = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)
    
    # Combine new frontmatter with content
    new_content = new_frontmatter + content_without_frontmatter
    
    # Write back to file
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def process_all_skills():
    """Process all SKILL.md files in the domains"""
    skills_path = Path("skills")
    processed_files = []
    failed_files = []
    
    print("Updating SKILL.md files with proper YAML frontmatter...")
    print("=" * 60)
    
    for domain_path in skills_path.iterdir():
        if domain_path.is_dir() and domain_path.name not in ['archive', 'mcp_tools', 'docs']:
            print(f"\nProcessing domain: {domain_path.name}")
            
            skill_files = list(domain_path.glob("**/SKILL.*.md"))
            for md in domain_path.glob("**/SKILL.md"):
                if md not in skill_files:
                    skill_files.append(md)
            for skill_file in skill_files:
                success = update_skill_file(skill_file)
                
                if success:
                    processed_files.append(skill_file)
                    print(f"  ✓ {skill_file.name}")
                else:
                    failed_files.append(skill_file)
                    print(f"  ✗ {skill_file.name}")
    
    print(f"\n" + "=" * 60)
    print(f"SUMMARY:")
    print(f"  Total files processed: {len(processed_files)}")
    print(f"  Successful updates: {len(processed_files)}")
    print(f"  Failed updates: {len(failed_files)}")
    
    if failed_files:
        print(f"\nFailed files:")
        for file in failed_files:
            print(f"  - {file}")
    
    return processed_files, failed_files

def verify_frontmatter(file_path):
    """Verify that a file has proper frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file starts with YAML frontmatter
        if not content.startswith('---'):
            return False, "Missing YAML frontmatter"
        
        # Check for required fields
        required_fields = ['name:', 'description:', 'license:']
        for field in required_fields:
            if field not in content:
                return False, f"Missing required field: {field}"
        
        # Check license value
        if 'license: Apache-2.0' not in content:
            return False, "License must be Apache-2.0"
        
        return True, "OK"
    
    except Exception as e:
        return False, f"Error reading file: {e}"

def verify_all_files():
    """Verify all SKILL.md files have proper frontmatter"""
    skills_path = Path("skills")
    verified_files = []
    failed_files = []
    
    print("\nVerifying YAML frontmatter compliance...")
    print("=" * 60)
    
    for domain_path in skills_path.iterdir():
        if domain_path.is_dir() and domain_path.name not in ['archive', 'mcp_tools', 'docs']:
            skill_files = list(domain_path.glob("**/SKILL.*.md"))
            for md in domain_path.glob("**/SKILL.md"):
                if md not in skill_files:
                    skill_files.append(md)
            for skill_file in skill_files:
                is_valid, message = verify_frontmatter(skill_file)
                
                if is_valid:
                    verified_files.append(skill_file)
                else:
                    failed_files.append((skill_file, message))
    
    print(f"\nVERIFICATION SUMMARY:")
    print(f"  Total files: {len(verified_files) + len(failed_files)}")
    print(f"  Valid files: {len(verified_files)}")
    print(f"  Invalid files: {len(failed_files)}")
    
    if failed_files:
        print(f"\nInvalid files:")
        for file, error in failed_files:
            print(f"  - {file.name}: {error}")
    
    return verified_files, failed_files

if __name__ == "__main__":
    # Process all files
    processed, failed = process_all_skills()
    
    # Verify the results
    verified, invalid = verify_all_files()
    
    print(f"\n" + "=" * 60)
    print("FINAL REPORT:")
    print(f"  Files to update: {len(processed) + len(failed)}")
    print(f"  Successfully updated: {len(processed)}")
    print(f"  Verification passed: {len(verified)}")
    print(f"  Total errors: {len(failed) + len(invalid)}")
    
    if len(failed) + len(invalid) == 0:
        print("\n🎉 All files successfully updated with proper YAML frontmatter!")
    else:
        print(f"\n⚠️  Some files need attention. Check the error messages above.")