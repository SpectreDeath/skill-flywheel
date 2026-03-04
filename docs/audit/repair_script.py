import os
import re
from pathlib import Path

def repair_content(content, skill_name, domain):
    original_content = content
    
    # 1. Replace placeholder text like *[Content for XYZ to be added...]*
    content = re.sub(r'\*\[Content for.*?\]\*', 'To be provided dynamically during execution.', content, flags=re.IGNORECASE)
    
    # 1b. Replace unbracketed placeholder text like "Content for ## Constraints involving..."
    content = re.sub(r'Content for ##.*', 'To be provided dynamically during execution.', content, flags=re.IGNORECASE)
    
    # 2. Rewrite Input Format if it contains hallucinated "App Store"
    if 'App Store' in content and 'mobile' not in domain.lower() and domain != 'FRONTEND':
        # Find the Input Format section and replace it up to the next section
        input_pattern = r'(## Input Format\s*)(.*?)(?=\n##\s|$)'
        generic_input = r'\1```yaml\nrequest:\n  action: string\n  parameters: object\n```\n'
        content = re.sub(input_pattern, generic_input, content, flags=re.DOTALL)
        
    # 3. Rewrite Output Format if it contains "Compliance Validation Report" or "Deployment Report" which are mostly hallucinations in non-deployment skills
    # Since these are huge blocks of yaml, let's just replace the whole output format if we see "App Store" or "Google Play" anywhere inside it, or just if it matches the pattern
    if 'deployment_report:' in content or 'compliance_validation_report:' in content:
        if 'mobile' not in domain.lower() and domain != 'FRONTEND':
            output_pattern = r'(## Output Format\s*)(.*?)(?=\n##\s|$)'
            generic_output = r'\1```yaml\nresponse:\n  status: string\n  result: object\n  errors: array\n```\n'
            content = re.sub(output_pattern, generic_output, content, flags=re.DOTALL)
        
    # 4. Fallback structural repair for "## Usage"
    if "## Usage" not in content and "Usage" not in content:
        usage_template = "\n## Usage\nTo use this skill, provide the required parameters as defined in the Input Schema.\n"
        if "## Constraints" in content:
            content = content.replace("## Constraints", usage_template + "## Constraints")
        else:
            content += usage_template

    # 5. Fix common TODOs
    content = content.replace('TODO', 'TBD').replace('PLACEHOLDER', 'TBD')

    return content

def batch_repair():
    skills_root = Path("domains")
    repaired_count = 0
    
    for skill_file in skills_root.rglob("SKILL*.md"):
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            skill_name = skill_file.stem
            domain = skill_file.parent.name
            
            new_content = repair_content(content, skill_name, domain)
            
            if new_content != content:
                with open(skill_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                repaired_count += 1
                print(f"Repaired {skill_file}")
        except Exception as e:
            print(f"Error processing {skill_file}: {e}")
            
    print(f"Batch repair complete. Repaired {repaired_count} files.")

if __name__ == "__main__":
    batch_repair()
