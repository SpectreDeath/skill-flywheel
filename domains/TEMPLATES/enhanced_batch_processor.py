#!/usr/bin/env python3
"""
Enhanced batch processor for adding meaningful required sections to skill files.
This script extracts information from existing content to generate meaningful sections.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple

class EnhancedSkillBatchProcessor:
    def __init__(self, skills_root: str = "skills"):
        self.skills_root = Path(skills_root)
        self.processed_count = 0
        self.failed_count = 0
        
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
    
    def analyze_skill_content(self, skill_path: Path) -> Dict:
        """Analyze a skill file to extract meaningful information."""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract existing sections
            sections = self.extract_sections(content)
            
            # Determine skill type and extract meaningful content
            skill_info = self.extract_skill_info(skill_path, content, sections)
            
            return skill_info
        except Exception as e:
            print(f"Error analyzing {skill_path}: {e}")
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
    
    def extract_skill_info(self, skill_path: Path, content: str, sections: Dict) -> Dict:
        """Extract meaningful information from skill content."""
        skill_name = skill_path.parent.name.replace('_', ' ').title()
        domain = skill_path.parts[1] if len(skill_path.parts) > 1 else 'general'
        
        # Extract from Description section
        description = sections.get('Description', '')
        
        # Extract from Capabilities section
        capabilities = sections.get('Capabilities', '')
        
        # Extract from Usage Examples section
        usage_examples = sections.get('Usage Examples', '')
        
        # Extract from Domain-specific sections
        domain_sections = ['Input Format', 'Output Format', 'Configuration Options', 
                          'Error Handling', 'Performance Optimization', 'Integration Examples']
        
        domain_content = []
        for section in domain_sections:
            if section in sections:
                domain_content.append(f"{section}: {sections[section]}")
        
        return {
            'path': skill_path,
            'content': content,
            'sections': sections,
            'skill_name': skill_name,
            'domain': domain,
            'description': description,
            'capabilities': capabilities,
            'usage_examples': usage_examples,
            'domain_content': '\n\n'.join(domain_content),
            'missing_sections': self.get_missing_sections(sections)
        }
    
    def get_missing_sections(self, sections: Dict) -> List[str]:
        """Determine which required sections are missing."""
        required_sections = ['Purpose', 'Examples', 'Implementation Notes', 'Constraints']
        return [section for section in required_sections if section not in sections]
    
    def generate_purpose_section(self, skill_info: Dict) -> str:
        """Generate a meaningful Purpose section."""
        skill_name = skill_info['skill_name']
        description = skill_info['description']
        capabilities = skill_info['capabilities']
        
        # If we have a good description, extract purpose from it
        if description and len(description) > 50:
            # Extract first 1-3 sentences from description
            sentences = re.split(r'[.!?]+', description)
            purpose_sentences = []
            char_count = 0
            
            for sentence in sentences:
                sentence = sentence.strip()
                if sentence and char_count < 200:  # Limit to ~200 characters
                    purpose_sentences.append(sentence)
                    char_count += len(sentence)
                    if len(purpose_sentences) >= 3:  # Max 3 sentences
                        break
            
            if purpose_sentences:
                purpose_text = '. '.join(purpose_sentences).strip()
                if purpose_text.endswith('.'):
                    return f"## Purpose\n{purpose_text}"
                else:
                    return f"## Purpose\n{purpose_text}."
        
        # If we have capabilities, use them to infer purpose
        if capabilities:
            # Extract key capabilities
            capability_lines = [line.strip() for line in capabilities.split('\n') if line.strip()]
            if capability_lines:
                # Take first few capabilities
                key_capabilities = capability_lines[:3]
                capabilities_text = ', '.join(key_capabilities).lower()
                return f"## Purpose\n{skill_name} provides capabilities including {capabilities_text}."
        
        # Fallback to generic purpose
        return f"## Purpose\n{skill_name} implementation and usage."
    
    def generate_examples_section(self, skill_info: Dict) -> str:
        """Generate meaningful Examples section."""
        skill_name = skill_info['skill_name']
        usage_examples = skill_info['usage_examples']
        domain_content = skill_info['domain_content']
        
        examples = []
        
        # If we have existing usage examples, extract from them
        if usage_examples:
            # Look for example patterns in usage examples
            example_pattern = r'### Example \d+.*?(?=\n### Example|\n## |\Z)'
            example_matches = re.findall(example_pattern, usage_examples, re.DOTALL)
            
            if example_matches:
                # Use existing examples
                for i, example in enumerate(example_matches[:3], 1):  # Limit to 3 examples
                    # Clean up the example
                    example_lines = example.strip().split('\n')
                    if example_lines:
                        title = example_lines[0].replace('### ', '').strip()
                        content = '\n'.join(example_lines[1:]).strip()
                        examples.append(f"### Example {i}: {title}\n{content}")
            else:
                # Extract example-like content
                lines = usage_examples.split('\n')
                for line in lines:
                    if 'input' in line.lower() or 'output' in line.lower() or 'example' in line.lower():
                        examples.append(f"### Example {len(examples)+1}: {line.strip()}")
        
        # If we have domain content, create examples from it
        if not examples and domain_content:
            # Create generic examples based on domain
            examples = [
                f"### Example 1: Basic Usage\n**Input**: 'Use {skill_name} to analyze my current project context.'\n**Output**: Analysis report with findings and recommendations\n**Use Case**: Initial project assessment and context gathering",
                f"### Example 2: Advanced Usage\n**Input**: 'Run {skill_name} with focus on high-priority optimization targets.'\n**Output**: Detailed analysis with prioritized recommendations\n**Use Case**: Targeted optimization and improvement planning"
            ]
        
        # Fallback to generic examples
        if not examples:
            examples = [
                f"### Example 1: Basic Usage\n**Input**: 'Use {skill_name} to analyze my current project context.'\n**Output**: Analysis report with findings and recommendations\n**Use Case**: Initial project assessment and context gathering",
                f"### Example 2: Advanced Usage\n**Input**: 'Run {skill_name} with focus on high-priority optimization targets.'\n**Output**: Detailed analysis with prioritized recommendations\n**Use Case**: Targeted optimization and improvement planning"
            ]
        
        return f"## Examples\n\n" + "\n\n".join(examples)
    
    def generate_implementation_notes_section(self, skill_info: Dict) -> str:
        """Generate meaningful Implementation Notes section."""
        skill_name = skill_info['skill_name']
        domain = skill_info['domain']
        capabilities = skill_info['capabilities']
        domain_content = skill_info['domain_content']
        
        notes = ["## Implementation Notes"]
        
        # Add domain-specific notes
        if domain in ['APPLICATION_SECURITY', 'DATABASE_ENGINEERING', 'DEVOPS']:
            notes.append(f"Implementation guidance for {domain} domain.")
        elif domain in ['ALGO_PATTERNS', 'ML_AI', 'FRONTEND']:
            notes.append(f"Technical implementation considerations for {domain}.")
        else:
            notes.append(f"General implementation guidance for {skill_name}.")
        
        # Add capability-specific notes
        if capabilities:
            notes.append("")
            notes.append("### Key Considerations:")
            capability_lines = [line.strip() for line in capabilities.split('\n') if line.strip() and line.startswith('-')]
            for line in capability_lines[:5]:  # Limit to 5 key points
                notes.append(line)
        
        # Add domain content if available
        if domain_content:
            notes.append("")
            notes.append("### Domain-Specific Requirements:")
            notes.append(domain_content[:500])  # Limit to 500 characters
        
        # Add general implementation guidance
        notes.extend([
            "",
            "### Best Practices:",
            "- Follow domain-specific standards and conventions",
            "- Implement proper error handling and validation",
            "- Consider performance implications for large-scale usage",
            "- Ensure security best practices are followed"
        ])
        
        return '\n'.join(notes)
    
    def generate_constraints_section(self, skill_info: Dict) -> str:
        """Generate meaningful Constraints section."""
        skill_name = skill_info['skill_name']
        domain = skill_info['domain']
        
        constraints = ["## Constraints"]
        
        # Add domain-specific constraints
        if domain == 'APPLICATION_SECURITY':
            constraints.extend([
                "- **NEVER** expose sensitive information in logs or outputs",
                "- **ALWAYS** implement proper authentication and authorization",
                "- **MUST** follow security best practices and compliance requirements",
                "- **SHOULD** validate all inputs and sanitize outputs",
                "- **MUST NOT** introduce security vulnerabilities"
            ])
        elif domain == 'DATABASE_ENGINEERING':
            constraints.extend([
                "- **NEVER** perform destructive operations without proper backups",
                "- **ALWAYS** implement proper transaction handling",
                "- **MUST** maintain data integrity and consistency",
                "- **SHOULD** optimize for performance and scalability",
                "- **MUST NOT** expose sensitive database credentials"
            ])
        elif domain == 'DEVOPS':
            constraints.extend([
                "- **NEVER** deploy未经测试的 code to production",
                "- **ALWAYS** maintain proper access controls and permissions",
                "- **MUST** implement rollback mechanisms for deployments",
                "- **SHOULD** follow infrastructure as code best practices",
                "- **MUST NOT** hardcode sensitive information"
            ])
        elif domain in ['ALGO_PATTERNS', 'ML_AI', 'FRONTEND']:
            constraints.extend([
                "- **NEVER** assume specific input formats without validation",
                "- **ALWAYS** handle edge cases and error conditions",
                "- **MUST** maintain code quality and documentation standards",
                "- **SHOULD** optimize for performance and maintainability",
                "- **MUST NOT** introduce breaking changes without proper migration"
            ])
        else:
            constraints.extend([
                "- **NEVER** perform operations that could cause data loss",
                "- **ALWAYS** validate inputs and handle errors gracefully",
                "- **MUST** follow established coding standards and practices",
                "- **SHOULD** consider performance and scalability implications",
                "- **MUST NOT** violate security or compliance requirements"
            ])
        
        return '\n'.join(constraints)
    
    def add_missing_sections(self, skill_info: Dict) -> str:
        """Add missing required sections to skill content."""
        content = skill_info['content']
        missing_sections = skill_info['missing_sections']
        
        # Generate new sections
        new_sections = []
        
        if 'Purpose' in missing_sections:
            new_sections.append(self.generate_purpose_section(skill_info))
        
        if 'Examples' in missing_sections:
            new_sections.append(self.generate_examples_section(skill_info))
        
        if 'Implementation Notes' in missing_sections:
            new_sections.append(self.generate_implementation_notes_section(skill_info))
        
        if 'Constraints' in missing_sections:
            new_sections.append(self.generate_constraints_section(skill_info))
        
        # Insert new sections after the Description section
        if new_sections:
            # Find the end of the Description section
            description_end = content.find('\n## ')
            if description_end == -1:
                # No other sections, append at end
                content += '\n\n' + '\n\n'.join(new_sections)
            else:
                # Insert before the next section
                content = content[:description_end] + '\n\n' + '\n\n'.join(new_sections) + '\n' + content[description_end:]
        
        return content
    
    def process_skill_file(self, skill_path: Path) -> bool:
        """Process a single skill file."""
        try:
            skill_info = self.analyze_skill_content(skill_path)
            if not skill_info:
                return False
            
            # Check if all required sections are present
            missing_sections = skill_info['missing_sections']
            if not missing_sections:
                print(f"✓ {skill_path} - Already complete")
                return True
            
            # Add missing sections
            updated_content = self.add_missing_sections(skill_info)
            
            # Write back to file
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"✓ {skill_path} - Added {len(missing_sections)} sections: {', '.join(missing_sections)}")
            self.processed_count += 1
            return True
            
        except Exception as e:
            print(f"✗ {skill_path} - Error: {e}")
            self.failed_count += 1
            return False
    
    def process_all_skills(self):
        """Process all skill files."""
        print("Starting enhanced batch processing of skill files...")
        print("=" * 60)
        
        skill_files = self.get_all_skill_files()
        print(f"Found {len(skill_files)} skill files to process")
        print()
        
        for skill_file in skill_files:
            self.process_skill_file(skill_file)
        
        print()
        print("=" * 60)
        print(f"Enhanced processing complete!")
        print(f"Processed: {self.processed_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Total: {len(skill_files)}")

def main():
    """Main entry point."""
    processor = EnhancedSkillBatchProcessor()
    processor.process_all_skills()

if __name__ == "__main__":
    main()