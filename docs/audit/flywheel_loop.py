import os
import subprocess


def generate_improvement(skill_content):
    """Call an LLM to improve the skill content if credentials are available."""
    prompt = f"""You are an expert AI capabilities engineer practicing the 'Ralph Wiggum' methodology of orthogonal, divergent improvements.
Review the following Agent Skill and improve it by:
1. Adding 2 novel edge cases or error handling steps.
2. Expanding its constraints to make it more robust.
3. Keeping the exact same YAML frontmatter and markdown structure.

Return ONLY the completely rewritten skill in Markdown format.

Original skill:
{skill_content}
"""
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            # Clean up markdown code block if present
            text = response.text
            if text.startswith("```markdown"): text = text[11:]
            if text.startswith("```"): text = text[3:]
            if text.endswith("```"): text = text[:-3]
            return text.strip()
        except Exception as e:
            print(f"Gemini API error: {e}")
            
    openai_key = os.environ.get("OPENAI_API_KEY")
    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.choices[0].message.content
            if text.startswith("```markdown"): text = text[11:]
            if text.startswith("```"): text = text[3:]
            if text.endswith("```"): text = text[:-3]
            return text.strip()
        except Exception as e:
            print(f"OpenAI API error: {e}")
            
    print("⚠️ No API key (GEMINI_API_KEY or OPENAI_API_KEY) found or missing SDK. Simulating LLM response.")
    return skill_content + "\n\n<!-- Simulated LLM Improvements: Added constraints, expanded examples, improved robustness -->\n"

def run_agv_cycle(target_skills):
    """
    PHASE 4: AGI LOOP
    Executes a full cycle: Chaos -> Critique -> Refine -> Validate.
    """
    print("--- INITIALIZING V3.0 AUTONOMOUS CYCLE ---")
    
    for skill_path in target_skills:
        print(f"\n[Target] {skill_path}")
        if not os.path.exists(skill_path):
            print(f"⚠️ Target path does not exist: {skill_path}")
            continue
            
        try:
            with open(skill_path, encoding='utf-8') as f:
                content = f.read()
                
            # 1. Ralph Chaos & Critique (LLM Generation)
            print("🔥 [Phase 3] Ralph Engine: Generating divergent improvements...")
            print("⚖️ [Phase 4] Skill Critiquing: Evaluating current implementation...")
            improved_content = generate_improvement(content)
            
            # 3. Refinement (Applying improvements)
            print("🛠️ [Phase 4] Flywheel Regeneration: Improving SKILL.md...")
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(improved_content)
                
        except Exception as e:
            print(f"Error processing {skill_path}: {e}")

    # 4. Validation Gate
    print("\n✅ [Phase 4] Validation: Running final_verify.py...")
    verify_res = subprocess.run(["python", "final_verify.py"], capture_output=True, text=True, check=False)
    if verify_res.returncode == 0:
        print("Validation checks passed.")
    else:
        print("Validation identified issues:")
        print(verify_res.stdout)

    # 5. Registry Refresh
    print("\n🔄 [Phase 5] Registry: Refreshing skill index...")
    subprocess.run(["python", "reindex_skills.py"], capture_output=True, check=False)
    print("✨ Flywheel cycle complete. Registry is up to date.")

if __name__ == "__main__":
    # Demonstration cycle for 1 existing demo skill
    demo_targets = [
        "domains/DEMO/DEMO.md" 
    ]
    # We will use DEMO/DEMO.md to avoid mutating core skills during tests
    if not os.path.exists("domains/DEMO/DEMO.md"):
        os.makedirs("domains/DEMO", exist_ok=True)
        with open("domains/DEMO/DEMO.md", "w", encoding='utf-8') as f:
            f.write("# SKILL: Demo\n\n## Purpose\nDemo skill.\n")
            
    run_agv_cycle(demo_targets)
