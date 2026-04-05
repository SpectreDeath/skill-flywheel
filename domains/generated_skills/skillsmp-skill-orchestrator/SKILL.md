---
name: skillsmp-skill-orchestrator
description: "Use when: given a task requiring multiple capabilities, decompose it into sub-tasks, search SkillsMP for matching skills, rank and select skills, resolve dependencies, and build an execution pipeline. Triggers: 'orchestrate', 'build pipeline', 'compose skills', 'decompose task', 'find skills for task', 'skill assembly', 'workflow'. Works with skillsmp-api-client."
---

# SkillsMP Skill Orchestrator

Decomposes complex tasks into sub-tasks, searches SkillsMP for matching skills, and orchestrates skill assembly to accomplish goals.

## Dependencies

- Requires `skillsmp-api-client` skill for API access
- May use `skillsmp-skill-learner` for deeper analysis

## Core Workflow

```
Task Input
    |
    v
Task Decomposition (break into sub-tasks)
    |
    v
Skill Discovery (search SkillsMP for each sub-task)
    |
    v
Skill Ranking (score and select best skills)
    |
    v
Dependency Resolution (order skills correctly)
    |
    v
Pipeline Assembly (create execution plan)
    |
    v
Execution / Output Specification
```

## Task Decomposition

Break complex tasks into atomic sub-tasks:

```python
def decompose_task(task: str) -> List[SubTask]:
    """
    Decompose a high-level task into sub-tasks.
    
    Example:
    "Build a web scraper that extracts product prices" ->
    [
        SubTask(name="fetch_html", description="Fetch webpage HTML"),
        SubTask(name="parse_html", description="Parse HTML for product data"),
        SubTask(name="extract_prices", description="Extract price values"),
        SubTask(name="format_output", description="Format as structured data")
    ]
    """
    # Use LLM or rule-based decomposition
    pass
```

## Skill Discovery

For each sub-task, search SkillsMP:

```python
def discover_skills(subtask: SubTask) -> List[SkillMatch]:
    """Find skills matching a sub-task."""
    
    # 1. Keyword search
    keyword_results = client.search(
        q=subtask.name,
        limit=10,
        sortBy="stars"
    )
    
    # 2. AI semantic search for contextual matches
    ai_results = client.ai_search(
        q=f"how to {subtask.description}"
    )
    
    # 3. Category/occupation filtering if applicable
    if subtask.category:
        filtered = client.search(
            q=subtask.name,
            category=subtask.category,
            limit=5
        )
    
    return merge_and_dedupe([keyword_results, ai_results, filtered])
```

## Skill Ranking

Score and rank discovered skills:

```python
class SkillScore:
    relevance: float      # How well it matches the sub-task (0-1)
    quality: float       # Stars, usage count, etc (0-1)
    freshness: float     # Recent activity (0-1)
    compatibility: float # Works with other selected skills (0-1)
    
    def total(self) -> float:
        return (self.relevance * 0.4 + 
                self.quality * 0.3 + 
                self.freshness * 0.1 + 
                self.compatibility * 0.2)

def rank_skills(skills: List[Skill], subtask: SubTask) -> List[SkillScore]:
    """Score skills for a specific sub-task."""
    # Score based on:
    # - Description match (BM25 or semantic similarity)
    # - Star count / popularity
    # - Last updated date
    # - Dependency compatibility
    pass
```

## Dependency Resolution

Determine execution order:

```python
def resolve_dependencies(skills: List[SelectedSkill]) -> List[Skill]:
    """
    Order skills for execution based on dependencies.
    
    Build dependency graph:
    - Explicit dependencies from skill metadata
    - Implicit dependencies (output -> input matching)
    - Resource conflicts
    """
    
    # Topological sort with cycle detection
    # Consider parallel execution for independent skills
    # Handle shared resources / state
    pass
```

## Pipeline Assembly

Create execution specification:

```python
class SkillPipeline:
    name: str
    description: str
    tasks: List[TaskSpec]
    skills: List[SkillReference]
    dependencies: Dict[str, List[str]]
    parallel_groups: List[List[str]]  # Skills that can run in parallel
    
    def to_execution_plan(self) -> dict:
        """Generate detailed execution specification."""
        return {
            "pipeline_name": self.name,
            "steps": [
                {
                    "step": i,
                    "skill": skill.name,
                    "depends_on": self.dependencies.get(skill.id, []),
                    "inputs": skill.inputs,
                    "outputs": skill.outputs
                }
                for i, skill in enumerate(self.skills)
            ]
        }
```

## Smart Skill Combination

The orchestrator should recognize when to:

1. **Compose** - Chain skills where output of one feeds input of next
2. **Parallelize** - Run independent skills simultaneously
3. **Fallback** - Use secondary skill if primary fails
4. **Fallback Chain** - Try multiple skills until one succeeds
5. **Aggregate** - Merge outputs from multiple skills
6. **Route** - Select skill based on runtime conditions

## Example: Building a Data Pipeline

```python
task = "Extract product data from multiple e-commerce sites, clean it, and save to database"

# Decompose
subtasks = decompose_task(task)
# [
#   "fetch_product_pages",
#   "parse_product_data", 
#   "validate_data",
#   "deduplicate_records",
#   "transform_to_schema",
#   "insert_into_database"
# ]

# Discover skills for each
pipeline = assemble_pipeline(subtasks, client)
# Returns: SkillPipeline with ordered skills

# Output execution plan
print(pipeline.to_execution_plan())
# {
#   "steps": [
#     {"skill": "web-scraper", "depends_on": []},
#     {"skill": "html-parser", "depends_on": ["web-scraper"]},
#     ...
#   ]
# }
```

## Continuous Learning

The orchestrator can improve by:

1. **Tracking Success** - Record which skill combinations work
2. **Learning Preferences** - Remember user's preferred tools
3. **Feedback Integration** - Incorporate failure feedback
4. **A/B Testing** - Try alternative skills for same sub-task

## Constraints

- MUST handle cases where no suitable skill exists
- SHOULD provide fallback options
- SHOULD handle API rate limits gracefully
- MUST validate skill compatibility before assembling
- SHOULD minimize total pipeline complexity
- MAY suggest new skills to create if gaps exist
- SHOULD cache skill metadata to reduce API calls