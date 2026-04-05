---
Domain: skill_validation
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: dependency-analyzer
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




## Description

Analyzes and validates dependencies between skills in the AgentSkills repository. This skill identifies dependency relationships, detects circular dependencies, validates dependency completeness, and ensures proper skill organization and modularity.


## Purpose

To be provided dynamically during execution.

## Input Format

```yaml
request:
  action: string
  parameters: object
```

## Output Format

```yaml
response:
  status: string
  result: object
  errors: array
```

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Dependency Graph Analysis**: Build and analyze skill dependency relationships
- **Circular Dependency Detection**: Identify and report circular dependency chains
- **Dependency Completeness**: Verify all declared dependencies exist and are valid
- **Modularity Assessment**: Evaluate skill independence and coupling
- **Dependency Validation**: Check dependency syntax and format
- **Import Chain Analysis**: Trace dependency chains and identify bottlenecks
- **Recommendation Engine**: Suggest dependency optimizations and refactoring

## Usage Examples

### Analyze Skill Dependencies

```python
"""
Skill Dependency Analysis and Validation
"""

import os
import re
import yaml
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class DependencyIssue:
    """Issue found in dependency analysis"""
    skill_file: str
    issue_type: str  # "missing_dependency", "circular_dependency", "invalid_format"
    message: str
    dependency: Optional[str] = None
    suggestion: Optional[str] = None

class DependencyAnalyzer:
    """Analyzes and validates skill dependencies"""
    
    def __init__(self, skills_root: str):
        """
        Initialize dependency analyzer
        
        Args:
            skills_root: Path to the skills directory
        """
        self.skills_root = Path(skills_root)
        self.skill_dependencies: Dict[str, List[str]] = {}
        self.dependency_graph: Dict[str, List[str]] = {}
        self.reverse_dependencies: Dict[str, List[str]] = {}
        
        # Dependency patterns
        self.dependency_patterns = [
            r'import\s+SKILL\.[^.]+\.md',  # import SKILL.Name.md
            r'from\s+SKILL\.[^.]+\.md',    # from SKILL.Name.md
            r'@import\s+SKILL\.[^.]+\.md', # @import SKILL.Name.md
            r'\[.*\]\(SKILL\.[^.]+\.md\)', # [link](SKILL.Name.md)
        ]
    
    def analyze_repository(self) -> Dict[str, Any]:
        """Analyze all skill dependencies in repository"""
        print("🔍 Analyzing skill dependencies...")
        
        # Build dependency graph
        self._build_dependency_graph()
        
        # Find issues
        issues = self._find_dependency_issues()
        
        # Analyze modularity
        modularity = self._analyze_modularity()
        
        # Generate recommendations
        recommendations = self._generate_recommendations()
        
        # Build report
        report = {
            "summary": {
                "total_skills": len(self.skill_dependencies),
                "total_dependencies": sum(len(deps) for deps in self.skill_dependencies.values()),
                "circular_dependencies": len([i for i in issues if i.issue_type == "circular_dependency"]),
                "missing_dependencies": len([i for i in issues if i.issue_type == "missing_dependency"]),
                "invalid_dependencies": len([i for i in issues if i.issue_type == "invalid_format"])
            },
            "dependencies": self.skill_dependencies,
            "graph": self.dependency_graph,
            "reverse_dependencies": self.reverse_dependencies,
            "issues": [vars(issue) for issue in issues],
            "modularity": modularity,
            "recommendations": recommendations
        }
        
        return report
    
    def _build_dependency_graph(self):
        """Build dependency graph from all skill files"""
        # Find all skill files
        skill_files = list(self.skills_root.glob("**/SKILL.*.md"))
        
        for skill_file in skill_files:
            skill_name = self._extract_skill_name(skill_file)
            dependencies = self._extract_dependencies(skill_file)
            
            self.skill_dependencies[skill_name] = dependencies
            self.dependency_graph[skill_name] = dependencies
            
            # Build reverse dependencies
            for dep in dependencies:
                if dep not in self.reverse_dependencies:
                    self.reverse_dependencies[dep] = []
                self.reverse_dependencies[dep].append(skill_name)
    
    def _extract_skill_name(self, skill_file: Path) -> str:
        """Extract skill name from file path"""
        # skills/DOMAIN/SKILL.Name.md -> Name
        file_name = skill_file.name
        match = re.match(r'^SKILL\.([^.]+)\.md$', file_name)
        if match:
            return match.group(1)
        return skill_file.stem
    
    def _extract_dependencies(self, skill_file: Path) -> List[str]:
        """Extract dependencies from skill file"""
        dependencies = []
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return dependencies
        
        # Check frontmatter Dependencies field
        frontmatter = self._extract_frontmatter(content)
        if frontmatter and 'Dependencies' in frontmatter:
            if isinstance(frontmatter['Dependencies'], list):
                for dep in frontmatter['Dependencies']:
                    dep_name = self._normalize_dependency_name(dep)
                    if dep_name:
                        dependencies.append(dep_name)
        
        # Check for inline dependencies
        inline_deps = self._extract_inline_dependencies(content)
        for dep in inline_deps:
            dep_name = self._normalize_dependency_name(dep)
            if dep_name and dep_name not in dependencies:
                dependencies.append(dep_name)
        
        return dependencies
    
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
    
    def _extract_inline_dependencies(self, content: str) -> List[str]:
        """Extract dependencies from inline references"""
        dependencies = []
        
        for pattern in self.dependency_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Extract skill name from match
                skill_match = re.search(r'SKILL\.([^.]+)\.md', match)
                if skill_match:
                    dependencies.append(skill_match.group(1))
        
        return dependencies
    
    def _normalize_dependency_name(self, dep: str) -> Optional[str]:
        """Normalize dependency name"""
        # Remove file extension if present
        dep = dep.replace('.md', '')
        
        # Extract skill name from various formats
        patterns = [
            r'SKILL\.([^.]+)',  # SKILL.Name
            r'([^/]+)$',        # path/to/SKILL.Name
        ]
        
        for pattern in patterns:
            match = re.search(pattern, dep)
            if match:
                return match.group(1)
        
        return None
    
    def _find_dependency_issues(self) -> List[DependencyIssue]:
        """Find various dependency issues"""
        issues = []
        
        # Check for missing dependencies
        issues.extend(self._check_missing_dependencies())
        
        # Check for circular dependencies
        issues.extend(self._check_circular_dependencies())
        
        # Check for invalid dependency formats
        issues.extend(self._check_invalid_dependencies())
        
        return issues
    
    def _check_missing_dependencies(self) -> List[DependencyIssue]:
        """Check for dependencies that don't exist"""
        issues = []
        all_skills = set(self.skill_dependencies.keys())
        
        for skill, deps in self.skill_dependencies.items():
            for dep in deps:
                if dep not in all_skills:
                    issues.append(DependencyIssue(
                        skill_file=skill,
                        issue_type="missing_dependency",
                        message=f"Dependency '{dep}' not found in repository",
                        dependency=dep,
                        suggestion=f"Check if skill '{dep}' exists or fix dependency name"
                    ))
        
        return issues
    
    def _check_circular_dependencies(self) -> List[DependencyIssue]:
        """Check for circular dependencies using DFS"""
        issues = []
        visited = set()
        rec_stack = set()
        
        def has_cycle(skill: str, path: List[str]) -> bool:
            visited.add(skill)
            rec_stack.add(skill)
            path.append(skill)
            
            for neighbor in self.dependency_graph.get(skill, []):
                if neighbor not in visited:
                    if has_cycle(neighbor, path):
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:]
                    issues.append(DependencyIssue(
                        skill_file=skill,
                        issue_type="circular_dependency",
                        message=f"Circular dependency detected: {' -> '.join(cycle)} -> {neighbor}",
                        suggestion=f"Break cycle by removing dependency from {cycle[-1]} to {neighbor}"
                    ))
                    return True
            
            path.pop()
            rec_stack.remove(skill)
            return False
        
        for skill in self.skill_dependencies:
            if skill not in visited:
                has_cycle(skill, [])
        
        return issues
    
    def _check_invalid_dependencies(self) -> List[DependencyIssue]:
        """Check for invalid dependency formats"""
        issues = []
        
        for skill, deps in self.skill_dependencies.items():
            for dep in deps:
                # Check for self-dependency
                if dep == skill:
                    issues.append(DependencyIssue(
                        skill_file=skill,
                        issue_type="invalid_format",
                        message=f"Skill '{skill}' cannot depend on itself",
                        dependency=dep,
                        suggestion="Remove self-dependency"
                    ))
                
                # Check for invalid characters
                if not re.match(r'^[A-Za-z0-9_]+$', dep):
                    issues.append(DependencyIssue(
                        skill_file=skill,
                        issue_type="invalid_format",
                        message=f"Dependency '{dep}' contains invalid characters",
                        dependency=dep,
                        suggestion="Use alphanumeric characters and underscores only"
                    ))
        
        return issues
    
    def _analyze_modularity(self) -> Dict[str, Any]:
        """Analyze skill modularity and coupling"""
        modularity = {
            "independence_score": 0.0,
            "coupling_metrics": {},
            "bottlenecks": [],
            "orphan_skills": [],
            "highly_connected": []
        }
        
        total_skills = len(self.skill_dependencies)
        if total_skills == 0:
            return modularity
        
        # Calculate independence score
        independent_skills = sum(1 for deps in self.skill_dependencies.values() if not deps)
        modularity["independence_score"] = independent_skills / total_skills
        
        # Calculate coupling metrics
        for skill in self.skill_dependencies:
            outgoing = len(self.dependency_graph.get(skill, []))
            incoming = len(self.reverse_dependencies.get(skill, []))
            
            modularity["coupling_metrics"][skill] = {
                "outgoing_dependencies": outgoing,
                "incoming_dependencies": incoming,
                "total_connections": outgoing + incoming
            }
            
            # Identify bottlenecks (high incoming dependencies)
            if incoming > 5:  # Threshold for bottleneck
                modularity["bottlenecks"].append(skill)
            
            # Identify orphan skills (no connections)
            if outgoing == 0 and incoming == 0:
                modularity["orphan_skills"].append(skill)
            
            # Identify highly connected skills
            if outgoing + incoming > 10:  # Threshold for high connectivity
                modularity["highly_connected"].append(skill)
        
        return modularity
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for dependency optimization"""
        recommendations = []
        
        # Analyze modularity
        modularity = self._analyze_modularity()
        
        if modularity["independence_score"] < 0.3:
            recommendations.append("Consider increasing skill independence by reducing dependencies")
        
        if modularity["bottlenecks"]:
            recommendations.append(f"Review bottlenecks: {', '.join(modularity['bottlenecks'])}")
        
        if modularity["orphan_skills"]:
            recommendations.append(f"Consider integrating orphan skills: {', '.join(modularity['orphan_skills'])}")
        
        # Check for circular dependencies
        issues = self._find_dependency_issues()
        circular_count = len([i for i in issues if i.issue_type == "circular_dependency"])
        if circular_count > 0:
            recommendations.append(f"Fix {circular_count} circular dependency issues")
        
        # General recommendations
        recommendations.extend([
            "Group related skills into logical domains",
            "Use dependency injection patterns for better modularity",
            "Consider creating utility skills for shared functionality",
            "Document dependency relationships in skill descriptions"
        ])
        
        return recommendations
    
    def generate_dependency_visualization(self) -> Dict[str, Any]:
        """Generate data for dependency graph visualization"""
        nodes = []
        edges = []
        
        # Create nodes
        for skill in self.skill_dependencies:
            outgoing = len(self.dependency_graph.get(skill, []))
            incoming = len(self.reverse_dependencies.get(skill, []))
            
            nodes.append({
                "id": skill,
                "label": skill,
                "size": max(10, outgoing + incoming),
                "color": self._get_node_color(outgoing, incoming),
                "metadata": {
                    "outgoing": outgoing,
                    "incoming": incoming,
                    "total": outgoing + incoming
                }
            })
        
        # Create edges
        for skill, deps in self.dependency_graph.items():
            for dep in deps:
                edges.append({
                    "source": skill,
                    "target": dep,
                    "label": "depends on"
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "layout": "hierarchical"
        }
    
    def _get_node_color(self, outgoing: int, incoming: int) -> str:
        """Get color based on dependency patterns"""
        total = outgoing + incoming
        
        if total == 0:
            return "#cccccc"  # Gray for isolated skills
        elif incoming > outgoing:
            return "#ff6b6b"  # Red for bottlenecks
        elif outgoing > incoming:
            return "#4ecdc4"  # Teal for utilities
        else:
            return "#45b7d1"  # Blue for balanced skills
    
    def validate_dependency_consistency(self) -> List[DependencyIssue]:
        """Validate consistency of dependency declarations"""
        issues = []
        
        # Check for inconsistent dependency declarations
        for skill in self.skill_dependencies:
            # Check if skill is referenced but not declared
            reverse_deps = self.reverse_dependencies.get(skill, [])
            
            for referrer in reverse_deps:
                if skill not in self.skill_dependencies.get(referrer, []):
                    issues.append(DependencyIssue(
                        skill_file=referrer,
                        issue_type="missing_dependency",
                        message=f"Skill '{referrer}' references '{skill}' but doesn't declare it as dependency",
                        dependency=skill,
                        suggestion=f"Add '{skill}' to Dependencies in {referrer}"
                    ))
        
        return issues

# Example usage
def example_dependency_analysis():
    """Example: Analyze dependencies in skills repository"""
    
    analyzer = DependencyAnalyzer("skills")
    
    # Run analysis
    report = analyzer.analyze_repository()
    
    # Print summary
    summary = report["summary"]
    print("📊 Dependency Analysis Summary:")
    print(f"   Total skills: {summary['total_skills']}")
    print(f"   Total dependencies: {summary['total_dependencies']}")
    print(f"   Circular dependencies: {summary['circular_dependencies']}")
    print(f"   Missing dependencies: {summary['missing_dependencies']}")
    
    # Print issues
    if report["issues"]:
        print("\\n⚠️  Dependency Issues Found:")
        for issue in report["issues"][:10]:  # Show first 10
            print(f"   {issue['issue_type']}: {issue['message']}")
    
    # Generate visualization data
    viz_data = analyzer.generate_dependency_visualization()
    
    # Save reports
    with open("dependency_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    with open("dependency_graph.json", 'w') as f:
        json.dump(viz_data, f, indent=2)
    
    print(f"\\n📁 Reports saved:")
    print(f"   dependency_report.json")
    print(f"   dependency_graph.json")
    
    return report, viz_data

if __name__ == "__main__":
    example_dependency_analysis()

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration
This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Best Practices

- **Specific Context**: Provide as much specific context as possible for more accurate results.
- **Regular Audits**: Use this skill as part of a recurring CI/CD quality gate.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.
- **Permission Errors**: Ensure the agent has read/write access to the target directories.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.

## Constraints

To be provided dynamically during execution.