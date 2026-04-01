---
name: pipeline-skill-accumulation
description: Use when running sequential task pipelines where each execution builds on previously evolved skills, tracking skill growth, reuse rate increase, and cumulative intelligence accumulation over time.
---

# Multi-Task Pipeline Skill Accumulation

## Overview

Pipeline pattern that executes tasks sequentially, tracking how the skill library grows and reuse rate increases with each task. Demonstrates the self-reinforcing loop: more skills → more reuse → faster execution → more skills evolved from richer context.

## Pipeline Structure

```python
PIPELINE_TASKS = [
    {"name": "CSV Analyzer", "query": "...", "category": "Spreadsheets"},
    {"name": "Text Report Generator", "query": "...", "category": "Documents"},
    {"name": "Data Quality Checker", "query": "...", "category": "Quality Assurance"},
]
```

## Execution Loop with Tracking

```python
async def run_pipeline(tasks):
    results = []

    for i, task_info in enumerate(tasks, 1):
        # Count skills before execution
        skills_before = count_skills()

        # Execute task
        result = await openspace.execute(task_info["query"])

        # Count skills after execution
        skills_after = count_skills()

        # Track accumulation
        results.append({
            "name": task_info["name"],
            "category": task_info["category"],
            "time": elapsed,
            "skills_before": skills_before,
            "skills_after": skills_after,
            "evolved_count": len(result.get("evolved_skills", [])),
            "reused_count": len(result.get("reused_skills", [])),
            "success": True,
        })

    return results
```

## Accumulation Metrics

```python
def print_pipeline_summary(results):
    print(f"{'Task':<25} {'Time':>6} {'Before':>7} {'After':>6} {'Evolved':>8} {'Reused':>7}")
    print("-" * 65)

    cumulative_reuse = 0
    for r in results:
        print(f"{r['name']:<25} {r['time']:>5.1f}s {r['skills_before']:>7} "
              f"{r['skills_after']:>6} {r['evolved_count']:>8} {r['reused_count']:>7}")
        cumulative_reuse += r['reused_count']

    # Show the flywheel effect
    first_reuse = results[0]['reused_count'] if results else 0
    last_reuse = results[-1]['reused_count'] if results else 0

    print(f"\nReuse trend: {first_reuse} → {last_reuse} (tasks 1..N)")
    print(f"Total skills accumulated: {results[-1]['skills_after']}")
    print(f"Total reuse events: {cumulative_reuse}")
```

## Flywheel Effect Visualization

```python
def plot_skill_accumulation(results):
    import plotly.graph_objects as go

    tasks = [r['name'] for r in results]
    skills = [r['skills_after'] for r in results]
    reused = [r['reused_count'] for r in results]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tasks, y=skills, name="Cumulative Skills",
                             mode="lines+markers"))
    fig.add_trace(go.Bar(x=tasks, y=reused, name="Reused Per Task",
                         yaxis="y2"))

    fig.update_layout(
        title="Skill Accumulation Over Pipeline",
        yaxis=dict(title="Total Skills"),
        yaxis2=dict(title="Reused Skills", overlaying="y", side="right"),
    )
    return fig
```

## Skill Growth Patterns

```
Task 1 (cold):  0 skills before → 2 evolved → 0 reused
Task 2 (warm):  2 skills before → 1 evolved → 1 reused
Task 3 (warm):  3 skills before → 1 evolved → 2 reused
Task 4 (warm):  4 skills before → 0 evolved → 3 reused  ← reuse > evolution
Task 5 (warm):  4 skills before → 1 evolved → 3 reused

Key inflection: When reused > evolved, the flywheel is self-sustaining.
```

## Cross-Task Skill Propagation

Skills from one task category can be reused in different categories:

```
"csv-data-validation" (Spreadsheets) → reused by "Data Quality Checker" (Quality Assurance)
"report-gen-fallback" (Documents) → reused by "CSV Analyzer" (Spreadsheets)
"execution-recovery" (Universal) → reused by ALL subsequent tasks
```

## Constraints

- MUST track `skills_before` and `skills_after` per task for accumulation measurement
- MUST distinguish between `evolved_count` (new) and `reused_count` (existing)
- SHOULD execute tasks in dependency order when cross-category reuse is expected
- MUST report cumulative metrics, not just per-task
- SHOULD visualize accumulation as line chart (skills) + bar chart (reuse)
- The flywheel is self-sustaining when `reused_count > evolved_count` for most tasks
- SHOULD include at least one universal skill (e.g., execution-recovery) that applies to all categories
