import os
import json
import re
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
        print("Error: GEMINI_API_KEY not found.")
        return content

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
    registry_path = Path("skill_registry.json")
    if not registry_path.exists():
        print("Registry not found.")
        return

    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    # Focus on core domains for this pass
    core_domains = ["APPLICATION_SECURITY", "DATABASE_ENGINEERING", "orchestration", "DEVOPS"]
    
    enriched_count = 0
    for skill in registry:
        domain = skill.get('domain')
        if domain not in core_domains:
            continue
            
        skill_path = Path(skill['path'])
        if not skill_path.exists():
            continue

        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if enrichment is needed (contains identifiable placeholders)
        placeholders = ["dynamically during execution", "*[Content for", "Auto-generated boilerplate"]
        if any(p in content for p in placeholders):
            print(f"Enriching {skill['name']} in {domain}...")
            new_content = enrich_skill_content(content, skill['name'], domain)
            
            if new_content and new_content != content:
                # Basic safety check: ensure some markdown headers still exist
                if "## " in new_content:
                    with open(skill_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    enriched_count += 1
                    print(f"Successfully enriched {skill['name']}")
                else:
                    print(f"Skipping {skill['name']} - generated content failed sanity check.")

    print(f"Enrichment session complete. Updated {enriched_count} skills.")

if __name__ == "__main__":
    main()
