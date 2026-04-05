---
name: skillsmp-skill-factory
description: "Use when: needing to both learn from SkillsMP skills AND orchestrate skill assembly in one workflow. Combines skill-learner and skill-orchestrator capabilities. Triggers: 'learn and create', 'generate from examples', 'build from skills', 'factory'. Requires API key from skillsmp.com."
---

# SkillsMP Skill Factory

Unified system that learns from existing SkillsMP skills and can orchestrate skill assembly to accomplish complex tasks. Combines the capabilities of skill-learner and skill-orchestrator.

## Dependencies

- Requires `skillsmp-api-client` skill
- Uses `skillsmp-skill-learner` patterns
- Uses `skillsmp-skill-orchestrator` patterns

## Two Modes of Operation

### Mode 1: Skill Generation (Learn & Create)

Use when you want to:
- Learn patterns from existing SkillsMP skills
- Generate improved derivative skills
- Synthesize multiple skills into new capabilities

### Mode 2: Skill Orchestration (Task Planning)

Use when you want to:
- Decompose a complex task into sub-tasks
- Find SkillsMP skills to handle each sub-task
- Build an execution pipeline from available skills

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SkillsMP Skill Factory                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │   LEARN MODE     │         │   ORCHESTRATE MODE        │ │
│  │                  │         │                          │ │
│  │ • Search skills  │         │ • Decompose task         │ │
│  │ • Analyze structure│       │ • Discover skills        │ │
│  │ • Extract patterns│        │ • Rank & select          │ │
│  │ • Generate new   │         │ • Build pipeline          │ │
│  └────────┬─────────┘         └───────────┬──────────────┘ │
│           │                                 │                │
│           v                                 v                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                   Skill Cache / Registry              │  │
│  │   • Discovered skills                                  │  │
│  │   • Extracted patterns                                 │  │
│  │   • Execution histories                                │  │
│  │   • Success/failure tracking                           │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Usage Patterns

### Pattern 1: Generate New Skill from Examples

```python
# User wants to create a skill similar to existing ones
factory = SkillFactory(api_key="your-key")

# Step 1: Find reference skills
reference_skills = factory.search(
    query="web data extraction",
    mode="learn",
    count=10
)

# Step 2: Analyze patterns
analysis = factory.analyze_skills(reference_skills)
patterns = analysis.extract_patterns()

# Step 3: Generate new skill specification
new_skill = factory.generate_skill(
    base_patterns=patterns,
    requirements={
        "name": "enhanced-web-scraper",
        "improvements": [
            "add retry logic",
            "add rate limiting",
            "add multiple output formats"
        ]
    }
)

# Step 4: Output skill specification
print(new_skill.to_yaml())
```

### Pattern 2: Orchestrate Skills for Task

```python
# User has a task that needs multiple skills
factory = SkillFactory(api_key="your-key")

# Step 1: Decompose task
pipeline = factory.orchestrate(
    task="Build a system that monitors website changes and notifies me",
    mode="orchestrate"
)

# Step 2: Review assembled pipeline
print(f"Pipeline: {pipeline.name}")
for step in pipeline.steps:
    print(f"  {step.order}. {step.skill_name} (depends on: {step.depends_on})")

# Step 3: Export for execution
execution_plan = pipeline.to_execution_spec()
```

### Pattern 3: Hybrid - Learn then Orchestrate

```python
# First learn about domain, then build pipeline
factory = SkillFactory(api_key="your-key")

# Learn what skills exist in the domain
domain_skills = factory.learn_domain("data processing")

# Build pipeline using learned knowledge
pipeline = factory.orchestrate(
    task="Process uploaded CSV files and generate reports",
    domain_knowledge=domain_skills
)
```

## Skill Cache

The factory maintains a local cache to avoid repeated API calls:

```python
class SkillCache:
    def __init__(self, ttl_seconds=3600):
        self.skills = {}           # skill_id -> skill_data
        self.patterns = {}         # pattern_id -> pattern_data
        self.search_results = {}   # query -> results
        self.execution_history = [] # past executions
        
    def get_skill(self, skill_id: str) -> Optional[Skill]:
        if skill_id in self.skills:
            if not self.is_expired(self.skills[skill_id]):
                return self.skills[skill_id]
        return None
    
    def cache_skill(self, skill: Skill):
        self.skills[skill.id] = {
            "skill": skill,
            "cached_at": datetime.now()
        }
        
    def get_patterns(self, category: str) -> List[Pattern]:
        return self.patterns.get(category, [])
        
    def record_execution(self, pipeline: Pipeline, success: bool):
        self.execution_history.append({
            "pipeline": pipeline,
            "success": success,
            "timestamp": datetime.now()
        })
        
    def get_success_rate(self, skill_id: str) -> float:
        """Calculate success rate for a skill based on execution history."""
        executions = [e for e in self.execution_history 
                      if skill_id in e.pipeline.skills]
        if not executions:
            return 0.5  # Default unknown
        return sum(1 for e in executions if e.success) / len(executions)
```

## Self-Improvement Loop

The factory continuously improves by:

```python
def self_improve(factory: SkillFactory):
    """Run improvement cycle."""
    
    # 1. Analyze execution history
    failures = [e for e in factory.cache.execution_history if not e.success]
    
    # 2. For each failure, try to find better skills
    for failure in failures:
        better_alternative = factory.find_alternative(
            failed_skill=failure.pipeline.failed_step,
            requirements=failure.task_requirements
        )
        
        # 3. If found, update recommendation
        if better_alternative:
            factory.update_skill_recommendation(
                task_type=failure.task_type,
                recommended=better_alternative
            )
    
    # 4. Generate insights about pattern effectiveness
    insights = factory.analyze_pattern_effectiveness()
    
    return insights
```

## API Integration

All SkillsMP API endpoints are used:

```python
class SkillsMPFactory(SkillFactory):
    def __init__(self, api_key: str):
        self.client = SkillsMPClient(api_key)
        self.cache = SkillCache()
        
    def search_skills(self, query: str, **kwargs) -> List[Skill]:
        # Check cache first
        cache_key = f"search:{query}:{kwargs}"
        if cache_key in self.cache.search_results:
            return self.cache.search_results[cache_key]
        
        # Keyword search
        results = self.client.search(q=query, **kwargs)
        
        # AI search for semantic matches
        ai_results = self.client.ai_search(q=query)
        
        # Merge and cache
        merged = self.merge_results(results, ai_results)
        self.cache.search_results[cache_key] = merged
        
        return merged
        
    def get_skill_details(self, skill_id: str) -> Skill:
        # Fetch full skill details
        return self.client.get_skill(skill_id)
        
    def get_categories(self) -> List[Category]:
        return self.client.get_categories()
        
    def get_occupations(self) -> List[Occupation]:
        return self.client.get_occupations()
```

## Constraints

- MUST handle API rate limits (500/day)
- SHOULD cache results to minimize API calls
- MUST validate generated skills are complete
- SHOULD track execution success for improvement
- MAY operate in learn-only or orchestrate-only mode
- SHOULD provide explanations for skill recommendations
- MUST handle missing skills gracefully (suggest creation)