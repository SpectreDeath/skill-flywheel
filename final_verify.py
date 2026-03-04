import os
import yaml
from pathlib import Path

def validate_skill(file_path):
    issues = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 1. Frontmatter Check
        if not content.startswith('---'):
            issues.append("Missing frontmatter")
        else:
            parts = content.split('---', 2)
            if len(parts) < 3:
                issues.append("Malformed frontmatter")
            else:
                try:
                    fm = yaml.safe_load(parts[1])
                    req = ['Domain', 'Version', 'Type', 'Category', 'Complexity', 'Estimated Execution Time', 'name']
                    for r in req:
                        if r not in fm:
                            issues.append(f"Missing frontmatter field: {r}")
                    
                    # Check if name field matches parent folder name (standard)
                    if 'name' in fm and fm['name'] != file_path.parent.name:
                        issues.append(f"Frontmatter name '{fm['name']}' does not match folder name '{file_path.parent.name}'")
                except Exception as e:
                    issues.append(f"YAML parse error in frontmatter: {e}")

        # 2. Sections Check (Full Spec)
        req_sections = [
            "## Description", "## Purpose", "## Capabilities", "## Usage Examples",
            "## Input Format", "## Output Format", "## Configuration Options",
            "## Constraints", "## Examples", "## Error Handling",
            "## Performance Optimization", "## Integration Examples", "## Best Practices",
            "## Troubleshooting", "## Monitoring and Metrics", "## Dependencies",
            "## Version History", "## License"
        ]
        for s in req_sections:
            if s not in content:
                issues.append(f"Missing section: {s}")

        # 3. Naming Check
        if file_path.name != 'SKILL.md':
            issues.append(f"Filename should be 'SKILL.md', but found '{file_path.name}'")
            
        return issues
    except Exception as e:
        return [f"Read error: {str(e)}"]

def main():
    skills_dir = Path(r'D:\Skill Flywheel\domains')
    # According to spec, each skill is in a subdirectory and named SKILL.md
    all_skills = list(skills_dir.glob('**/SKILL.md'))
    
    total = 0
    passed = 0
    failed = 0
    
    print("AgentSkills Final Verification Sweep (agentskills.io structure)")
    print("==============================================================")
    
    for skill_file in all_skills:
        total += 1
        issues = validate_skill(skill_file)
        if not issues:
            passed += 1
        else:
            failed += 1
            print(f"[FAIL] {skill_file.parent.name}/SKILL.md")
            for issue in issues:
                print(f"  - {issue}")
                    
    print("==============================================================")
    print(f"Total Skills: {total}")
    print(f"Passed:      {passed}")
    print(f"Failed:      {failed}")
    print(f"Compliance:  {(passed/total)*100:.1f}%" if total > 0 else "N/A")

if __name__ == "__main__":
    main()
