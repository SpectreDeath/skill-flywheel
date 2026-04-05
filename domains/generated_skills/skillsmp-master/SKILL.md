---
name: skillsmp-master
description: "Use when: working with SkillsMP to discover, learn from, orchestrate, generate skills, or find capability gaps. Master skill that delegates to specialized skills (api-client, skill-learner, skill-orchestrator, skill-factory, gap-discoverer). Triggers: 'skillsmp', 'skill marketplace', 'AI skills', 'agent skills', 'find skills', 'learn skills', 'orchestrate'. Requires API key from skillsmp.com."
---

# SkillsMP Master

Master skill that orchestrates all SkillsMP-related operations. Delegates to specialized skills based on the task.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SkillsMP Master                            │
│                                                                  │
│   "Discover skills, learn from them, generate new ones,        │
│    orchestrate multiple skills, find gaps"                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│   │ api-client  │  │ skill-      │  │ skill-                  │  │
│   │             │  │ learner     │  │ orchestrator            │  │
│   └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│   │ skill-      │  │ skill-      │  │ skill-                  │  │
│   │ factory     │  │ gap-        │  │ evaluator              │  │
│   │             │  │ discoverer  │  │                         │  │
│   └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Delegation Matrix

| Task | Delegate Skill |
|------|-----------------|
| Make API calls | skillsmp-api-client |
| Learn patterns from skills | skillsmp-skill-learner |
| Build skill pipeline for task | skillsmp-skill-orchestrator |
| Learn + orchestrate combined | skillsmp-skill-factory |
| Find missing capabilities | skillsmp-skill-gap-discoverer |
| Evaluate skill quality | (internal) |

## Usage Patterns

### Quick Skill Discovery

```python
# Just find relevant skills
master = SkillsMPMaster(api_key="key")

skills = master.discover(query="web scraping")
# Returns list of relevant skills from SkillsMP
```

### Deep Learning

```python
# Learn from SkillsMP and create improved version
master = SkillsMPMaster(api_key="key")

# Learn patterns from existing skills
learner = master.learn(topic="API integration", count=20)

# Generate improved skill
new_skill = learner.generate_improved(
    name="enhanced-api-integration",
    improvements=["better error handling", "caching", "retry logic"]
)
```

### Task Orchestration

```python
# Build pipeline to accomplish complex task
master = SkillsMPMaster(api_key="key")

pipeline = master.orchestrate(task="""
    Build a system that:
    1. Monitors RSS feeds
    2. Extracts relevant articles
    3. Summarizes each article
    4. Sends to notification system
""")

print(pipeline.to_execution_plan())
```

### Gap Analysis

```python
# Find what's missing
master = SkillsMPMaster(api_key="key")

gaps = master.analyze_gaps("machine learning model deployment")
print(gaps.summary())
# Output: "3 critical gaps, 5 high priority, ..."
```

### Full Workflow

```python
# Complete workflow: discover, learn, fill gaps, create
master = SkillsMPMaster(api_key="key")

# 1. Understand the domain
domain_info = master.explore("data engineering")

# 2. Find existing skills
existing = domain_info.list_skills()

# 3. Identify gaps  
gaps = domain_info.find_gaps()

# 4. For each gap, either:
#    a) Find existing skill to extend
#    b) Generate new skill to fill

for gap in gaps.critical:
    if gap.has_partial_skills():
        # Extend existing
        extended = master.extend(skill=gap.best_skill(), with=gap.requirements)
    else:
        # Create new
        new = master.generate(to_fill=gap)
```

## API Key Management

```python
class SkillsMPConfig:
    # Store API key securely
    api_key: str = os.environ.get("SKILLSMP_API_KEY")
    
    # Rate limit tracking
    daily_limit = 500
    remaining: int = None
    
    @classmethod
    def get_client(cls):
        if not cls.api_key:
            raise ValueError("SKILLSMP_API_KEY not set")
        return SkillsMPClient(cls.api_key)
    
    @classmethod
    def check_limits(cls, response):
        cls.remaining = int(response.headers.get(
            "X-RateLimit-Daily-Remaining", 500
        ))
        if cls.remaining < 10:
            warn("Low API quota remaining")
```

## Caching Strategy

```python
class MasterCache:
    """Smart caching for SkillsMP operations."""
    
    def __init__(self):
        self.skills = TTLCache(maxsize=1000, ttl=3600)
        self.searches = TTLCache(maxsize=500, ttl=1800)
        self.patterns = TTLCache(maxsize=100, ttl=7200)
        
    def get_skill(self, skill_id: str):
        return self.skills.get(skill_id)
        
    def cache_skill(self, skill):
        self.skills[skill.id] = skill
        
    def search(self, query: str):
        return self.searches.get(query)
        
    def cache_search(self, query: str, results):
        self.searches[query] = results
```

## Error Handling

```python
class MasterError(Exception):
    pass

class RateLimitError(MasterError):
    pass

class SkillNotFoundError(MasterError):
    pass

class GenerationError(MasterError):
    pass

def handle_error(e: Exception) -> str:
    if isinstance(e, RateLimitError):
        return "Rate limit exceeded. Wait until midnight UTC or upgrade."
    if isinstance(e, SkillNotFoundError):
        return f"Skill not found. Try broader search or create new."
    if isinstance(e, GenerationError):
        return f"Generation failed: {e}. Try simpler requirements."
    return f"Unexpected error: {e}"
```

## Metrics and Monitoring

```python
class MasterMetrics:
    def __init__(self):
        self.api_calls = 0
        self.cache_hits = 0
        self.skills_discovered = 0
        self.skills_generated = 0
        self.pipelines_built = 0
        self.gaps_found = 0
        
    def record_call(self):
        self.api_calls += 1
        
    def record_cache_hit(self):
        self.cache_hits += 1
        
    def get_cache_hit_rate(self) -> float:
        total = self.api_calls + self.cache_hits
        return self.cache_hits / total if total > 0 else 0
```

## Constraints

- MUST handle rate limits gracefully
- SHOULD use caching to minimize API calls
- MUST validate generated skills
- SHOULD track metrics for optimization
- MAY delegate to specialized skills
- MUST provide clear error messages
- SHOULD batch operations when possible