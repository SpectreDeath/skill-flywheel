#!/usr/bin/env python3
"""
Skill Indexer - Enhanced Skill Discovery and Management System

This module provides comprehensive indexing and discovery capabilities for the Skill Flywheel.
It scans all domains, extracts metadata from SKILL.md files, and builds a searchable skill database.
"""

import json
import logging
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class SkillMetadata:
    """Enhanced skill metadata structure with additional indexing fields."""
    name: str
    domain: str
    version: str
    purpose: str
    description: str
    path: str
    last_modified: float
    complexity: str | None = None
    skill_type: str | None = None
    category: str | None = None
    source: str | None = None
    tags: List[str] = None
    dependencies: List[str] = None
    prerequisites: List[str] = None
    estimated_time: str | None = None
    difficulty_level: int | None = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.dependencies is None:
            self.dependencies = []
        if self.prerequisites is None:
            self.prerequisites = []


class SkillIndexer:
    """Enhanced skill indexing system for the Skill Flywheel."""
    
    def __init__(self, base_path: str = "domains"):
        """
        Initialize the skill indexer.
        
        Args:
            base_path (str): Base path to scan for domains and skills
        """
        self.base_path = Path(base_path)
        self.skills: Dict[str, SkillMetadata] = {}
        self.domain_index: Dict[str, List[str]] = {}
        self.tag_index: Dict[str, List[str]] = {}
        self.complexity_index: Dict[str, List[str]] = {}
        self.type_index: Dict[str, List[str]] = {}
        
    def scan_all_skills(self) -> Dict[str, SkillMetadata]:
        """
        Scan all domains and extract skill metadata from SKILL.md files.
        
        Returns:
            Dict[str, SkillMetadata]: Dictionary of skill name to metadata
        """
        logger.info(f"Starting comprehensive skill scan from {self.base_path}")
        
        # Find all SKILL.md files recursively
        skill_files = list(self.base_path.glob("**/SKILL.md"))
        logger.info(f"Found {len(skill_files)} SKILL.md files")
        
        for skill_file in skill_files:
            try:
                skill_metadata = self._parse_skill_file(skill_file)
                if skill_metadata:
                    self.skills[skill_metadata.name] = skill_metadata
                    
                    # Build domain index
                    if skill_metadata.domain not in self.domain_index:
                        self.domain_index[skill_metadata.domain] = []
                    self.domain_index[skill_metadata.domain].append(skill_metadata.name)
                    
                    # Build tag index
                    for tag in skill_metadata.tags:
                        if tag not in self.tag_index:
                            self.tag_index[tag] = []
                        self.tag_index[tag].append(skill_metadata.name)
                    
                    # Build complexity index
                    if skill_metadata.complexity:
                        if skill_metadata.complexity not in self.complexity_index:
                            self.complexity_index[skill_metadata.complexity] = []
                        self.complexity_index[skill_metadata.complexity].append(skill_metadata.name)
                    
                    # Build type index
                    if skill_metadata.skill_type:
                        if skill_metadata.skill_type not in self.type_index:
                            self.type_index[skill_metadata.skill_type] = []
                        self.type_index[skill_metadata.skill_type].append(skill_metadata.name)
                        
            except Exception as e:
                logger.error(f"Error parsing skill file {skill_file}: {e}")
                continue
        
        logger.info(f"Successfully indexed {len(self.skills)} skills")
        return self.skills
    
    def _parse_skill_file(self, skill_file: Path) -> SkillMetadata | None:
        """
        Parse a SKILL.md file and extract metadata.
        Support both legacy Markdown formatting and new YAML frontmatter.
        """
        try:
            with open(skill_file, encoding='utf-8') as f:
                content = f.read()
            
            metadata = {
                'path': str(skill_file.relative_to(self.base_path.parent)),
                'last_modified': skill_file.stat().st_mtime,
            }

            # Handle YAML Frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        import yaml
                        fm = yaml.safe_load(parts[1])
                        # Map YAML keys to SkillMetadata fields
                        metadata['name'] = str(fm.get('name', '')).replace('SKILL.', '')
                        metadata['domain'] = fm.get('Domain')
                        metadata['version'] = str(fm.get('Version'))
                        metadata['purpose'] = fm.get('Purpose')
                        metadata['description'] = fm.get('Description')
                        metadata['complexity'] = fm.get('Complexity')
                        metadata['skill_type'] = fm.get('Type')
                        metadata['category'] = fm.get('Category')
                        metadata['tags'] = fm.get('Tags', [])
                        metadata['dependencies'] = fm.get('Dependencies', [])
                        metadata['estimated_time'] = fm.get('Estimated Execution Time')
                    except Exception as fm_err:
                        logger.warning(f"YAML parse error in {skill_file}: {fm_err}")

            # Fallback for name from directory name if still missing
            if not metadata.get('name'):
                metadata['name'] = skill_file.parent.name.replace('SKILL.', '')

            # Extract Purpose and Description from body headers if still missing
            if not metadata.get('purpose'):
                # Look for ## Purpose section
                purpose_match = re.search(r'## Purpose\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
                if purpose_match:
                    metadata['purpose'] = purpose_match.group(1).strip()
            
            if not metadata.get('description'):
                description_match = re.search(r'## Description\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
                if description_match:
                    metadata['description'] = description_match.group(1).strip()

            # Legacy Regex Fallbacks (Optional)
            if not metadata.get('domain'):
                metadata['domain'] = self._extract_field(content, r'-\*\*Domain:\*\* (.+)$')
            if not metadata.get('version'):
                metadata['version'] = self._extract_field(content, r'-\*\*Version:\*\* (.+)$')

            # Validate required fields
            required_fields = ['name', 'domain', 'version', 'purpose', 'description']
            for field in required_fields:
                if not metadata.get(field):
                    # Final fallback for name based on directory
                    if field == 'name':
                        metadata['name'] = skill_file.parent.name.replace('SKILL.', '')
                    else:
                        logger.warning(f"Missing required field '{field}' in {skill_file}")
                        return None
            
            return SkillMetadata(**{k: v for k, v in metadata.items() if k in SkillMetadata.__dataclass_fields__})
            
        except Exception as e:
            logger.error(f"Failed to parse {skill_file}: {e}")
            return None
    
    def _extract_field(self, content: str, pattern: str) -> str | None:
        """
        Extract a field from content using regex pattern.
        
        Args:
            content (str): Content to search
            pattern (str): Regex pattern to match
            
        Returns:
            Optional[str]: Extracted field value or None
        """
        match = re.search(pattern, content, re.MULTILINE)
        return match.group(1).strip() if match else None
    
    def search_skills(self, query: str, domain: str | None = None, 
                     complexity: str | None = None, skill_type: str | None = None,
                     tags: List[str] | None = None) -> List[SkillMetadata]:
        """
        Search for skills based on various criteria.
        
        Args:
            query (str): Text query to search in name, purpose, description
            domain (Optional[str]): Filter by domain
            complexity (Optional[str]): Filter by complexity level
            skill_type (Optional[str]): Filter by skill type
            tags (Optional[List[str]]): Filter by tags
            
        Returns:
            List[SkillMetadata]: List of matching skills sorted by relevance
        """
        results = []
        
        for skill in self.skills.values():
            # Apply filters
            if domain and skill.domain != domain:
                continue
            if complexity and skill.complexity != complexity:
                continue
            if skill_type and skill.skill_type != skill_type:
                continue
            if tags and not set(tags).intersection(set(skill.tags)):
                continue
            
            # Text search in name, purpose, and description
            if query:
                search_text = f"{skill.name} {skill.purpose} {skill.description}".lower()
                if query.lower() not in search_text:
                    continue
            
            results.append(skill)
        
        # Sort by name for consistent ordering
        results.sort(key=lambda x: x.name.lower())
        return results
    
    def get_skills_by_domain(self, domain: str) -> List[SkillMetadata]:
        """Get all skills in a specific domain."""
        skill_names = self.domain_index.get(domain, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_skills_by_tag(self, tag: str) -> List[SkillMetadata]:
        """Get all skills with a specific tag."""
        skill_names = self.tag_index.get(tag, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_skills_by_complexity(self, complexity: str) -> List[SkillMetadata]:
        """Get all skills with a specific complexity level."""
        skill_names = self.complexity_index.get(complexity, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_skills_by_type(self, skill_type: str) -> List[SkillMetadata]:
        """Get all skills of a specific type."""
        skill_names = self.type_index.get(skill_type, [])
        return [self.skills[name] for name in skill_names if name in self.skills]
    
    def get_skill_dependencies(self, skill_name: str) -> List[SkillMetadata]:
        """Get all skills that depend on the given skill."""
        dependencies = []
        for skill in self.skills.values():
            if skill_name in skill.dependencies:
                dependencies.append(skill)
        return dependencies
    
    def get_skill_prerequisites(self, skill_name: str) -> List[SkillMetadata]:
        """Get all prerequisite skills for the given skill."""
        skill = self.skills.get(skill_name)
        if not skill:
            return []
        
        prerequisites = []
        for prereq_name in skill.prerequisites:
            if prereq_name in self.skills:
                prerequisites.append(self.skills[prereq_name])
        return prerequisites
    
    def validate_skill_consistency(self) -> Dict[str, List[str]]:
        """
        Validate skill consistency and return any issues found.
        
        Returns:
            Dict[str, List[str]]: Dictionary of issue types and their descriptions
        """
        issues = {
            'missing_dependencies': [],
            'missing_prerequisites': [],
            'orphaned_skills': [],
            'invalid_complexity': [],
            'invalid_types': []
        }
        
        all_skill_names = set(self.skills.keys())
        
        for skill in self.skills.values():
            # Check dependencies
            for dep in skill.dependencies:
                if dep not in all_skill_names:
                    issues['missing_dependencies'].append(f"Skill '{skill.name}' depends on non-existent skill '{dep}'")
            
            # Check prerequisites
            for prereq in skill.prerequisites:
                if prereq not in all_skill_names:
                    issues['missing_prerequisites'].append(f"Skill '{skill.name}' has non-existent prerequisite '{prereq}'")
        
        # Check for orphaned skills (skills not referenced by any other skill)
        referenced_skills = set()
        for skill in self.skills.values():
            referenced_skills.update(skill.dependencies)
            referenced_skills.update(skill.prerequisites)
        
        orphaned = all_skill_names - referenced_skills
        for orphaned_skill in orphaned:
            issues['orphaned_skills'].append(f"Skill '{orphaned_skill}' is not referenced by any other skill")
        
        # Check complexity values
        valid_complexities = {'Low', 'Medium', 'High', 'Very High'}
        for skill in self.skills.values():
            if skill.complexity and skill.complexity not in valid_complexities:
                issues['invalid_complexity'].append(f"Skill '{skill.name}' has invalid complexity '{skill.complexity}'")
        
        # Check type values
        valid_types = {'Tutorial', 'Project', 'Framework', 'Tool', 'Library', 'Pattern'}
        for skill in self.skills.values():
            if skill.skill_type and skill.skill_type not in valid_types:
                issues['invalid_types'].append(f"Skill '{skill.name}' has invalid type '{skill.skill_type}'")
        
        return issues
    
    def generate_skill_report(self) -> Dict[str, Any]:
        """Generate a comprehensive report about the skill index."""
        report = {
            'total_skills': len(self.skills),
            'domains': len(self.domain_index),
            'domains_breakdown': {domain: len(skills) for domain, skills in self.domain_index.items()},
            'complexity_breakdown': {complexity: len(skills) for complexity, skills in self.complexity_index.items()},
            'type_breakdown': {skill_type: len(skills) for skill_type, skills in self.type_index.items()},
            'tag_breakdown': {tag: len(skills) for tag, skills in self.tag_index.items()},
            'validation_issues': self.validate_skill_consistency(),
            'top_tags': sorted(self.tag_index.items(), key=lambda x: len(x[1]), reverse=True)[:10],
            'largest_domains': sorted(self.domain_index.items(), key=lambda x: len(x[1]), reverse=True)[:10]
        }
        return report
    
    def export_index(self, output_path: str = "skill_registry.json"):
        """Export the skill index to a JSON file (legacy compatible list format)."""
        # Maintain legacy format: a list of skill objects
        index_data = [asdict(metadata) for metadata in self.skills.values()]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2, default=str)
        
        logger.info(f"Skill registry exported to {output_path}")
    
    def load_index(self, input_path: str = "skill_index.json"):
        """Load a skill index from a JSON file."""
        try:
            with open(input_path, encoding='utf-8') as f:
                index_data = json.load(f)
            
            self.skills = {name: SkillMetadata(**metadata) for name, metadata in index_data['skills'].items()}
            self.domain_index = index_data['domain_index']
            self.tag_index = index_data['tag_index']
            self.complexity_index = index_data['complexity_index']
            self.type_index = index_data['type_index']
            
            logger.info(f"Skill index loaded from {input_path}")
            return True
        except FileNotFoundError:
            logger.warning(f"Index file {input_path} not found")
            return False
        except Exception as e:
            logger.error(f"Failed to load index from {input_path}: {e}")
            return False


def main():
    """Main function to demonstrate the skill indexer."""
    indexer = SkillIndexer()
    
    # Scan all skills
    skills = indexer.scan_all_skills()
    
    # Generate and print report
    report = indexer.generate_skill_report()
    
    print("\n=== Skill Index Report ===")
    print(f"Total Skills: {report['total_skills']}")
    print(f"Total Domains: {report['domains']}")
    
    print("\n=== Domain Breakdown ===")
    for domain, count in report['domains_breakdown'].items():
        print(f"  {domain}: {count} skills")
    
    print("\n=== Complexity Breakdown ===")
    for complexity, count in report['complexity_breakdown'].items():
        print(f"  {complexity}: {count} skills")
    
    print("\n=== Top 10 Tags ===")
    for tag, skills in report['top_tags'][:10]:
        print(f"  {tag}: {len(skills)} skills")
    
    # Export index (rebuild skill_registry.json)
    indexer.export_index("skill_registry.json")
    
    # Demonstrate search functionality
    print("\n=== Search Examples ===")
    
    # Search by query
    ml_skills = indexer.search_skills("machine learning")
    print(f"Skills matching 'machine learning': {len(ml_skills)}")
    
    # Search by domain
    ml_ai_skills = indexer.get_skills_by_domain("ML_AI")
    print(f"Skills in ML_AI domain: {len(ml_ai_skills)}")
    
    # Search by complexity
    high_complexity_skills = indexer.get_skills_by_complexity("High")
    print(f"High complexity skills: {len(high_complexity_skills)}")
    
    # Show validation issues
    issues = report['validation_issues']
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    print(f"\nValidation Issues: {total_issues}")
    
    if total_issues > 0:
        for issue_type, issue_list in issues.items():
            if issue_list:
                print(f"  {issue_type}: {len(issue_list)} issues")


if __name__ == "__main__":
    main()
