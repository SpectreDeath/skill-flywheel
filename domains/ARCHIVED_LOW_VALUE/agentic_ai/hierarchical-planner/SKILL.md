---
name: hierarchical-planner
description: "Use when: creating hierarchical plans, breaking down complex goals, multi-level task decomposition, planning with subtasks, or implementing planning agents. Triggers: 'hierarchical planning', 'task decomposition', 'break down goals', 'subtask planning', 'multi-level planning', 'planning agent'. NOT for: simple single-step tasks, when flat planning is sufficient, or when tasks are already decomposed."
---

# Hierarchical Planner

Creates hierarchical task plans with multiple levels of abstraction. This skill decomposes complex goals into manageable subtasks with dependencies and priorities.

## When to Use This Skill

Use this skill when:
- Creating hierarchical plans
- Breaking down complex goals
- Multi-level task decomposition
- Planning with subtasks
- Implementing planning agents

Do NOT use this skill when:
- Simple single-step tasks
- Flat planning sufficient
- Tasks already decomposed
- No planning needed

## Input Format

```yaml
planning_request:
  goal: string                   # High-level goal to achieve
  decomposition_depth: number    # How many levels
  constraints: object            # Time, resource constraints
  task_dependencies: boolean     # Track dependencies
```

## Output Format

```yaml
planning_result:
  plan_tree: object              # Hierarchical plan structure
  tasks: array                  # Flat task list
  dependencies: object          # Task dependencies
  timeline: object              # Suggested execution order
  estimates: object             # Effort estimates
```

## Capabilities

### 1. Goal Analysis (10 min)

- Understand high-level objectives
- Identify success criteria
- Determine constraints
- Assess complexity

### 2. Task Decomposition (15 min)

- Break goals into major phases
- Decompose into subtasks
- Identify task relationships
- Create hierarchy

### 3. Dependency Mapping (10 min)

- Identify task dependencies
- Detect parallel opportunities
- Find critical path
- Resolve conflicts

### 4. Prioritization (10 min)

- Rank tasks by value
- Consider dependencies
- Factor in constraints
- Create execution order

### 5. Plan Generation (15 min)

- Generate execution plan
- Add time estimates
- Create milestones
- Add contingency

## Usage Examples

### Basic Usage

"Create a hierarchical plan for this goal."

### Advanced Usage

"Full decomposition with dependencies and estimates."

## Configuration Options

- `decomposition_depth`: 2-5 levels
- `dependency_tracking`: Basic or detailed
- `estimation_method`: Heuristic, historical, expert
- `output_format`: tree, list, timeline

## Constraints

- MUST create actionable tasks
- SHOULD track dependencies
- MUST be realistic with estimates
- SHOULD handle complexity

## Integration Examples

- Planning agents: Integrate with agents
- Project management: Export to PM tools
- Code generation: Generate task code
- Execution: Execute plans

## Dependencies

- Python 3.10+
- Planning algorithms
- Task management
