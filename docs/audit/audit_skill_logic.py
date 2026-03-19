import json
import os
from pathlib import Path

# Load audit criteria from file
CRITERIA_PATH = Path("audit_criteria.md")
with open(CRITERIA_PATH, encoding='utf-8') as f:
    AUDIT_CRITERIA = f.read()

def audit_skill(skill_path):
    """Call an LLM to audit a skill based on criteria."""
    try:
        with open(skill_path, encoding='utf-8', errors='ignore') as f:
            skill_content = f.read()
    except Exception as e:
        return {"error": f"Read error: {e}"}

    prompt = f"""You are a Senior Skill Architect auditing an Agent Skill library.
Your task is to evaluate the following skill based on the provided AUDIT CRITERIA.

AUDIT CRITERIA:
{AUDIT_CRITERIA}

SKILL TO AUDIT ({skill_path}):
{skill_content}

Strictly evaluate if the logic is solid. Look for:
1. Irrelevant schemas (e.g. schemas that seem to be copied from a different domain).
2. Vague or unexecutable workflow steps.
3. Missing or weak constraints.
4. Mismatch between purpose and capabilities.

Return a JSON object with:
- "score": 1-10 (10 being perfect)
- "issues": list of strings (specific logic flaws)
- "recommendation": string (how to fix it)
"""
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Gemini API error for {skill_path}: {e}")

    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"OpenAI API error for {skill_path}: {e}")
            
    # Mock response if no keys
    return {"score": 0, "issues": ["No API Key available for semantic audit"], "recommendation": "Set API KEY"}

def run_audit(target_domains=None):
    skills_dir = Path("skills")
    report = {}
    
    # Iterate through domains
    for domain_path in skills_dir.iterdir():
        if not domain_path.is_dir() or domain_path.name in ['archive', 'mcp_tools', 'docs']:
            continue
            
        if target_domains and domain_path.name not in target_domains:
            continue
            
        print(f"Auditing domain: {domain_path.name}")
        report[domain_path.name] = []
        
        # Find all skills in domain
        skill_files = list(domain_path.glob("**/SKILL.md")) + list(domain_path.glob("**/SKILL.*.md"))
        
        # Deduplicate
        seen = set()
        unique_skills = []
        for f in skill_files:
            if f not in seen:
                seen.add(f)
                unique_skills.append(f)

        for skill_file in unique_skills:
            print(f"  - Auditing {skill_file.name} in {skill_file.parent.name}...")
            result = audit_skill(skill_file)
            result["file"] = str(skill_file)
            report[domain_path.name].append(result)
            
            if result.get("score", 10) < 7:
                print(f"    ⚠️ LOW SCORE ({result['score']}): {', '.join(result.get('issues', []))[:100]}...")

    with open("audit_report.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("\nAudit complete. Results saved to audit_report.json")

if __name__ == "__main__":
    # For testing, just audit a few representative domains first
    test_domains = ["APPLICATION_SECURITY", "DATABASE_ENGINEERING", "meta_agent_enhancement"]
    run_audit(test_domains)
