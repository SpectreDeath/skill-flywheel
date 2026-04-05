---
name: skillsmp-skill-learner
description: "Use when: analyzing existing skills from SkillsMP to learn patterns, extract reusable components, generate improved derivative skills, or synthesize multiple skills. Works with skillsmp-api-client. Triggers: 'learn from skills', 'analyze skill patterns', 'generate skill', 'improve skill', 'synthesize skills', 'extract patterns'. NOT for: directly executing tasks (use appropriate execution skills)."
---

# SkillsMP Skill Learner

Learns from existing skills on SkillsMP to understand patterns, architecture patterns, and generate improved derivative skills.

## Dependencies

- Requires `skillsmp-api-client` skill for API access
- Uses Python with AST parsing for skill analysis

## Workflow

```
1. Search SkillsMP for relevant skills (keyword + AI search)
2. Fetch detailed skill documentation
3. Parse and analyze skill structure (inputs, outputs, dependencies)
4. Extract reusable patterns and components
5. Identify improvement opportunities
6. Generate derivative skill with enhancements
```

## Analyzing Skill Structure

When analyzing a skill from SkillsMP, extract:

```python
class SkillAnalysis:
    name: str                          # Skill name
    description: str                    # What it does
    triggers: List[str]               # When to use this skill
    dependencies: List[str]             # Required skills/tools
    inputs: Dict[str, Any]            # Required inputs
    outputs: Dict[str, Any]            # Produces outputs
    patterns: List[str]                # Reusable patterns identified
    improvements: List[str]            # Potential enhancements
```

## Pattern Extraction

Extract common patterns across multiple skills:

1. **Input Patterns** - Common input types and validation
2. **Output Patterns** - Standard output formats
3. **Dependency Patterns** - Common skill combinations
4. **Error Handling Patterns** - How skills handle failures
5. **State Management** - How skills persist/manage state
6. **API Interaction Patterns** - How skills call external services

## Generating Improved Skills

When generating a derivative skill:

```python
def generate_derivative(base_skill: SkillAnalysis, improvements: List[str]) -> dict:
    """
    Generate an improved skill based on analysis.
    
    Improvements could include:
    - Better error handling with retry logic
    - More comprehensive input validation
    - Additional output formats
    - Better documentation
    - More robust state management
    - Performance optimizations
    """
    return {
        "name": f"improved-{base_skill.name}",
        "description": f"Enhanced version of {base_skill.name} with...",
        "triggers": base_skill.triggers,
        "dependencies": base_skill.dependencies,
        "implementation": generate_implementation(base_skill, improvements)
    }
```

## Multi-Skill Learning

To learn from multiple skills and synthesize:

```python
def synthesize_skills(skills: List[SkillAnalysis]) -> SkillAnalysis:
    """Combine patterns from multiple skills into a unified skill."""
    
    # Extract common patterns
    common_inputs = intersection([s.inputs for s in skills])
    common_outputs = intersection([s.outputs for s in skills])
    
    # Merge dependencies intelligently
    merged_deps = merge_dependencies([s.dependencies for s in skills])
    
    # Identify gaps in individual skills
    gaps = identify_coverage_gaps(skills)
    
    return SkillAnalysis(
        name=f"synthesized-{skills[0].category}",
        description=f"Unified skill combining {len(skills)} source skills",
        patterns=common_patterns,
        improvements=gaps
    )
```

## Usage with API Client

```python
from skillsmp_api_client import SkillsMPClient

client = SkillsMPClient("your-api-key")

# Search for related skills
results = client.search(q="web scraper", sortBy="stars", limit=20)
ai_results = client.ai_search(q="how to extract data from websites")

# Analyze each skill
for skill in results["data"]["skills"]:
    analysis = analyze_skill(skill)
    patterns = extract_patterns(analysis)
    print(f"Pattern: {patterns}")
```

## Quality Criteria for Generated Skills

A good derivative skill should:

- Inherit the core functionality of the base skill
- Add meaningful improvements (not just cosmetic)
- Have clear, specific triggers
- Include proper error handling
- Be well-documented with examples
- Have appropriate dependencies
- Follow skill writing best practices

## Constraints

- MUST verify generated skills are syntactically valid
- MUST ensure dependencies are resolvable
- SHOULD test generated skills before deployment
- SHOULD maintain backward compatibility when extending
- MAY combine multiple base skills into one improved skill
- SHOULD document what was learned from each source skill