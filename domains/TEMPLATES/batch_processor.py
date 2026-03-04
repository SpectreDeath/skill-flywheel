#!/usr/bin/env python3
"""
Batch processor for adding required sections to skill files.
This script handles both auto-generated and manually created skills.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

class SkillBatchProcessor:
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
    
    def analyze_skill_type(self, skill_path: Path) -> Dict:
        """Analyze a skill file to determine its type and current content."""
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract existing sections
            sections = self.extract_sections(content)
            
            # Determine skill type
            skill_type = self.classify_skill_type(skill_path, content, sections)
            
            return {
                'path': skill_path,
                'content': content,
                'sections': sections,
                'skill_type': skill_type,
                'missing_sections': self.get_missing_sections(sections)
            }
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
    
    def classify_skill_type(self, skill_path: Path, content: str, sections: Dict) -> str:
        """Classify the skill type based on path and content."""
        path_str = str(skill_path).lower()
        
        # Auto-generated skills (usually have boilerplate content)
        if "auto-generated boilerplate" in content.lower():
            return "auto_generated"
        
        # Check for domain indicators in path
        if "application_security" in path_str:
            return "application_security"
        elif "database_engineering" in path_str:
            return "database_engineering"
        elif "devops" in path_str:
            return "devops"
        elif "algo_patterns" in path_str:
            return "algo_patterns"
        elif "frontend" in path_str:
            return "frontend"
        elif "ml_ai" in path_str:
            return "ml_ai"
        elif "modern_backend_development" in path_str:
            return "modern_backend"
        elif "web3" in path_str:
            return "web3"
        elif "epistemology" in path_str:
            return "epistemology"
        elif "logic" in path_str:
            return "logic"
        elif "formal_methods" in path_str:
            return "formal_methods"
        else:
            return "general"
    
    def get_missing_sections(self, sections: Dict) -> List[str]:
        """Determine which required sections are missing."""
        required_sections = ['Purpose', 'Examples', 'Implementation Notes', 'Constraints']
        return [section for section in required_sections if section not in sections]
    
    def generate_purpose_section(self, skill_info: Dict) -> str:
        """Generate a Purpose section based on skill type and existing content."""
        skill_type = skill_info['skill_type']
        path = skill_info['path']
        sections = skill_info['sections']
        
        # Extract skill name from path
        skill_name = path.parent.name.replace('_', ' ').title()
        
        if skill_type == "auto_generated":
            # For auto-generated skills, create a generic but meaningful purpose
            if "iac-drift-detection" in str(path):
                return f"## Purpose\nInfrastructure as Code drift detection."
            else:
                return f"## Purpose\n{skill_name} functionality."
        
        # For manually created skills, try to extract from existing content
        if 'Description' in sections:
            description = sections['Description']
            # Extract first 1-3 sentences
            sentences = re.split(r'[.!?]+', description)
            purpose_sentences = sentences[:3] if len(sentences) >= 3 else sentences[:2]
            purpose_text = '. '.join(purpose_sentences).strip()
            if purpose_text:
                return f"## Purpose\n{purpose_text}"
        
        # Fallback to generic purpose
        return f"## Purpose\n{skill_name} implementation and usage."
    
    def generate_examples_section(self, skill_info: Dict) -> str:
        """Generate an Examples section."""
        skill_type = skill_info['skill_type']
        path = skill_info['path']
        
        examples = []
        
        if skill_type == "auto_generated":
            examples = [
                "### Example 1: Basic Usage\n**Input**: 'Use {skill_name} to analyze my current project context.'\n**Output**: Analysis report with findings and recommendations\n**Use Case**: Initial project assessment and context gathering",
                "### Example 2: Advanced Usage\n**Input**: 'Run {skill_name} with focus on high-priority optimization targets.'\n**Output**: Detailed analysis with prioritized recommendations\n**Use Case**: Targeted optimization and improvement planning"
            ]
        else:
            examples = [
                "### Example 1: Basic Usage\n**Input**: 'Use {skill_name} to analyze my current project context.'\n**Output**: Analysis report with findings and recommendations\n**Use Case**: Initial project assessment and context gathering",
                "### Example 2: Advanced Usage\n**Input**: 'Run {skill_name} with focus on high-priority optimization targets.'\n**Output**: Detailed analysis with prioritized recommendations\n**Use Case**: Targeted optimization and improvement planning"
            ]
        
        skill_name = path.parent.name.replace('_', ' ').title()
        examples_text = '\n\n'.join([ex.format(skill_name=skill_name) for ex in examples])
        
        return f"## Examples\n\n{examples_text}"
    
    def generate_implementation_notes_section(self, skill_info: Dict) -> str:
        """Generate an Implementation Notes section."""
        skill_type = skill_info['skill_type']
        
        if skill_type == "auto_generated":
            notes = [
                "## Implementation Notes",
                "Auto-generated boilerplate for {skill_type}.",
                "",
                "## Configuration Options",
                "- `execution_depth`: Control the thoroughness of the analysis (default: standard).",
                "- `report_format`: Choose between markdown, json, or console output.",
                "- `verbose`: Enable detailed logging for debugging purposes.",
                "",
                "## Error Handling",
                "- **Invalid Input**: The skill will report specific missing parameters and request clarification.",
                "- **Timeout**: Large-scale operations will be chunked to avoid process hangs.",
                "- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.",
                "",
                "## Performance Optimization",
                "- **Caching**: Results are cached when applicable to reduce redundant computations.",
                "- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.",
                "- **Parallelization**: Multi-target scans are executed in parallel where supported."
            ]
        else:
            notes = [
                "## Implementation Notes",
                "Content for ## Implementation Notes section to be added based on the specific skill requirements."
            ]
        
        return '\n'.join(notes)
    
    def generate_constraints_section(self, skill_info: Dict) -> str:
        """Generate a Constraints section."""
        skill_type = skill_info['skill_type']
        
        if skill_type == "auto_generated":
            constraints = [
                "## Constraints",
                "Auto-generated boilerplate for {skill_type}."
            ]
        else:
            constraints = [
                "## Constraints",
                "Content for ## Constraints section to be added based on the specific skill requirements."
            ]
        
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
            skill_info = self.analyze_skill_type(skill_path)
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
        print("Starting batch processing of skill files...")
        print("=" * 60)
        
        skill_files = self.get_all_skill_files()
        print(f"Found {len(skill_files)} skill files to process")
        print()
        
        for skill_file in skill_files:
            self.process_skill_file(skill_file)
        
        print()
        print("=" * 60)
        print(f"Processing complete!")
        print(f"Processed: {self.processed_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Total: {len(skill_files)}")

def main():
    """Main entry point."""
    processor = SkillBatchProcessor()
    processor.process_all_skills()

if __name__ == "__main__":
    main()