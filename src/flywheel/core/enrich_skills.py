import contextlib
import json
import os
from pathlib import Path

from google import genai


def enrich_skill_content(content, skill_name, domain):
    """Use Gemini to enrich skill content by replacing placeholders."""
    prompt = f"""You are an expert Skill Architect. Your task is to enrich the following Agent Skill file by replacing all placeholder text with high-quality, professional, and domain-specific content.

PLACEHOLDERS TO REPLACE:
- "To be provided dynamically during execution."
- "*[Content for ...]*"
- "Auto-generated boilerplate for ..."
- Any other text that indicates missing implementation details.

SKILL DETAILS:
Name: {skill_name}
Domain: {domain}

CURRENT CONTENT:
{content}

REQUIREMENTS:
1. Maintain the existing Markdown structure and YAML frontmatter.
2. Replace every placeholder with concrete, actionable instructions, schemas, and examples.
3. Ensure the logic in "Workflow" and "Constraints" is solid and specifically tailored to the skill's purpose.
4. If a section like "Input Format" or "Output Format" is generic, make it specific (e.g., using YAML schemas representing real-world parameters for this domain).
5. The resulting skill should be "Production-Ready".

Return the FULL updated Markdown content.
"""
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        # Accessibility: Graceful disable if key missing
        return f"ENRICHMENT_DISABLED: Requires GEMINI_API_KEY\n\n{content}"

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"Error enriching {skill_name}: {e}")
        return content

def main():
    workspace_root = Path(__file__).parent.parent.parent
    registry_path = workspace_root / "skill_registry.json"
    archive_dir = workspace_root / "domains" / "ARCHIVED" / "PLACEHOLDERS"
    
    if not registry_path.exists():
        print("Registry not found.")
        return

    with open(registry_path, encoding='utf-8') as f:
        json.load(f)

    # 1. Target specifically archived placeholders for systematic re-integration
    archived_skills = list(archive_dir.glob("**/SKILL*.md"))
    print(f"Found {len(archived_skills)} archived placeholder skills.")

    enriched_count = 0
    for skill_file in archived_skills:
        with open(skill_file, encoding='utf-8') as f:
            content = f.read()

        # Simple domain extraction from filename or path
        skill_name = skill_file.parent.name.replace('SKILL.', '')
        
        # Find matching entry in registry or infer domain
        domain = "General"
        with contextlib.suppress(Exception):
            domain = skill_file.relative_to(archive_dir).parts[0]

        print(f"Enriching {skill_name} for domain {domain}...")
        new_content = enrich_skill_content(content, skill_name, domain)
        
        if new_content and new_content != content and "## " in new_content:
            # Re-integration: Move back to production domains/
            target_dir = workspace_root / "domains" / domain / f"SKILL.{skill_name}"
            target_dir.mkdir(parents=True, exist_ok=True)
            target_file = target_dir / "SKILL.md"
            
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            # Remove from archive
            skill_file.unlink()
            with contextlib.suppress(OSError):
                skill_file.parent.rmdir() 
                
            enriched_count += 1
            print(f"Successfully enriched and re-integrated {skill_name} to {domain}")

    # 2. Re-index registry after re-integration
    if enriched_count > 0:
        print("Enrichment complete. Triggering re-index...")
        # Add src to sys.path to ensure reindex_skills can be imported
        import sys
        sys.path.append(str(workspace_root / "src"))
        from core.reindex_skills import reindex
        reindex()

    print(f"Enrichment session complete. Updated and re-integrated {enriched_count} skills.")

if __name__ == "__main__":
    main()
