---
name: spec-to-task-decomposition
description: "Use when: breaking complex specifications into actionable tasks, generating implementation work items from requirements, planning feature development from specs, or estimating effort from specifications. Triggers: 'break down spec', 'spec to task', 'task from spec', 'decompose requirements', 'implementation plan', 'effort estimation', 'work breakdown'. NOT for: simple specs already at task level, early exploration, or when task breakdown already exists."
---

# Spec to Task Decomposition

Break complex specifications into actionable, manageable tasks. This skill transforms requirements into implementation work items with dependencies and estimates.

## When to Use This Skill

Use this skill when:
- Breaking complex specifications into actionable tasks
- Generating implementation work items from requirements
- Planning feature development from specs
- Estimating effort from specifications
- Creating work breakdown structures

Do NOT use this skill when:
- Specifications already at task level
- Early exploration with high uncertainty
- Task breakdown already exists
- Team uses different planning format

## Input Format

```yaml
decomposition_request:
  specification: string         # Specification document path
  granularity: string           # Task size (fine, medium, coarse)
  constraints: object           # Resource/timeline constraints
  dependencies: array           # Known external dependencies
```

## Output Format

```yaml
decomposition_result:
  tasks: array                  # Generated task list
  dependencies: object          # Task dependency graph
  estimates: object             # Effort estimates
  timeline: object              # Suggested timeline
  priorities: array             # Task priorities
```

## Capabilities

### 1. Requirement Extraction (10 min)

- Parse requirements from specifications
- Identify functional requirements
- Extract non-functional requirements
- Categorize by type and priority

### 2. Task Generation (15 min)

- Generate implementation tasks from requirements
- Identify subtasks for complex requirements
- Create task dependencies
- Define task boundaries

### 3. Dependency Analysis (10 min)

- Map task dependencies
- Identify parallelization opportunities
- Find critical path
- Detect circular dependencies

### 4. Effort Estimation (15 min)

- Estimate task effort
- Identify complexity factors
- Calculate buffer time
- Generate confidence intervals

### 5. Prioritization (10 min)

- Prioritize tasks by value/urgency
- Identify blockers
- Create milestone markers
- Generate timeline suggestions

## Usage Examples

### Basic Usage

"Break down this feature spec into implementation tasks."

### Advanced Usage

"Decompose spec with fine granularity, dependency analysis, and effort estimates."

## Configuration Options

- `granularity`: Fine, medium, or coarse
- `estimation_method`: Expert, analogical, parametric
- `include_testing`: Include test task generation
- `include_docs`: Include documentation tasks

## Constraints

- MUST generate actionable tasks
- SHOULD include dependencies
- MUST provide clear task definitions
- SHOULD estimate effort when possible

## Integration Examples

- Project management: Export to Jira, Asana
- Planning: Create sprint backlogs
- Estimation: Feed into capacity planning
- Tracking: Generate progress dashboards

## Dependencies

- Python 3.10+
- Project management integrations
- Estimation algorithms
