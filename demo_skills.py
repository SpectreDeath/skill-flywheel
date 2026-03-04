#!/usr/bin/env python3
"""
Skill Flywheel Demonstration Script

This script demonstrates how the AgentSkills work by simulating MCP tool calls
and showing the skill execution workflow without requiring Docker.
"""

import json
import os
from pathlib import Path

def load_skill_registry():
    """Load the skill registry from the JSON file."""
    registry_path = Path("skill_registry.json")
    if not registry_path.exists():
        print("❌ Skill registry not found. Please run the indexing script first.")
        return []
    
    with open(registry_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_skills_by_domain(domain):
    """Find all skills in a specific domain."""
    registry = load_skill_registry()
    return [skill for skill in registry if skill['domain'] == domain]

def find_skill_by_name(name):
    """Find a specific skill by name."""
    registry = load_skill_registry()
    for skill in registry:
        if skill['name'] == name:
            return skill
    return None

def load_skill_content(skill):
    """Load the content of a skill from its SKILL.md file."""
    skill_path = Path(skill['path'])
    if not skill_path.exists():
        return f"❌ Skill content not found at {skill_path}"
    
    with open(skill_path, 'r', encoding='utf-8') as f:
        return f.read()

def demonstrate_skill_execution(skill_name, request=""):
    """Demonstrate executing a skill with a given request."""
    print(f"\n🚀 Executing Skill: {skill_name}")
    print("=" * 60)
    
    skill = find_skill_by_name(skill_name)
    if not skill:
        print(f"❌ Skill '{skill_name}' not found in registry")
        return
    
    print(f"📋 Domain: {skill['domain']}")
    print(f"📝 Description: {skill['description']}")
    print(f"📁 Path: {skill['path']}")
    print(f"🕐 Last Modified: {skill['last_modified']}")
    
    # Load and display skill content
    content = load_skill_content(skill)
    print(f"\n📄 Skill Content Preview:")
    print("-" * 40)
    print(content[:500] + "..." if len(content) > 500 else content)
    
    # Simulate skill execution
    print(f"\n⚡ Simulated Execution:")
    print("-" * 40)
    if request:
        print(f"📥 Input Request: {request}")
    else:
        print("📥 Input Request: (default)")
    
    print(f"📤 Output: SYSTEM INSTRUCTIONS FOR SKILL: {content[:200]}...")
    print(f"✅ Skill execution completed successfully")

def show_domain_overview():
    """Show an overview of all domains and their skills."""
    registry = load_skill_registry()
    
    # Group skills by domain
    domains = {}
    for skill in registry:
        domain = skill['domain']
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(skill)
    
    print("\n📊 DOMAIN OVERVIEW")
    print("=" * 60)
    print(f"Total Skills: {len(registry)}")
    print(f"Total Domains: {len(domains)}")
    
    for domain, skills in sorted(domains.items()):
        print(f"\n📁 {domain} ({len(skills)} skills)")
        for skill in skills[:5]:  # Show first 5 skills
            print(f"  • {skill['name']}")
        if len(skills) > 5:
            print(f"  ... and {len(skills) - 5} more")

def main():
    """Main demonstration function."""
    print("🎯 Skill Flywheel Demonstration")
    print("=" * 60)
    print("This script demonstrates the AgentSkills ecosystem")
    print("without requiring Docker or external services.")
    
    # Show domain overview
    show_domain_overview()
    
    # Demonstrate specific skills
    print("\n🧪 SKILL DEMONSTRATIONS")
    print("=" * 60)
    
    # Demo 1: Repository Reconnaissance
    demonstrate_skill_execution("repo-recon", "Analyze the current repository structure")
    
    # Demo 2: Security Scan
    demonstrate_skill_execution("security-scan", "Scan for security vulnerabilities")
    
    # Demo 3: API Design
    demonstrate_skill_execution("api-design", "Design a REST API for user management")
    
    # Demo 4: ML Deep Learning Frameworks
    demonstrate_skill_execution("ml-deep-learning-frameworks", "Implement a CNN for image classification")
    
    print("\n🎉 DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("The Skill Flywheel ecosystem provides:")
    print("• 234+ specialized skills across 9 domains")
    print("• MCP-compatible tool interfaces")
    print("• Comprehensive documentation and examples")
    print("• Automated skill discovery and execution")
    print("\nTo use these skills in practice:")
    print("1. Deploy the MCP servers (Docker or direct Python)")
    print("2. Connect your LLM agent to the MCP servers")
    print("3. Use natural language to invoke skills")
    print("4. Let the skills handle complex tasks automatically")

if __name__ == "__main__":
    main()