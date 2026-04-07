---
name: task-skill-router
description: "Use when: mapping user tasks to optimal skills, routing requests to appropriate handlers, selecting best skill for complex queries, or building task-to-skill mappings. Triggers: 'route task', 'skill routing', 'task mapping', 'select skill', 'match task to skill', 'skill selection'. NOT for: simple single-skill tasks, when skills are pre-determined, or when routing logic already exists."
---

# Task Skill Router

Maps complex user tasks to the most appropriate skill or sequence of skills. This router analyzes intent, scores capabilities, and selects optimal execution paths.

## When to Use This Skill

Use this skill when:
- Mapping user tasks to optimal skills
- Routing requests to appropriate handlers
- Selecting best skill for complex queries
- Building task-to-skill mappings for agents
- Creating intelligent routing systems

Do NOT use this skill when:
- Simple single-skill tasks
- Skills are pre-determined
- Routing logic already exists
- Direct skill invocation is sufficient

## Input Format

```yaml
routing_request:
  task: string                   # User task description
  available_skills: array        # List of available skills
  context: object                 # Additional context
  scoring_method: string         # How to score matches
```

## Output Format

```yaml
routing_result:
  selected_skill: string         # Best matching skill
  confidence: number             # Match confidence (0-100)
  alternatives: array            # Alternative skills
  execution_path: array          # Sequence if chaining needed
  reasoning: string              # Why this skill was selected
```

## Capabilities

### 1. Intent Analysis (10 min)

- Parse user task description
- Extract key requirements
- Identify implicit needs
- Categorize task type

### 2. Skill Capability Matching (15 min)

- Match task requirements to skill capabilities
- Score each skill against requirements
- Rank skills by match quality
- Filter by constraints

### 3. Execution Path Planning (10 min)

- Determine if single skill or chain needed
- Plan skill execution sequence
- Handle dependent operations
- Optimize for efficiency

### 4. Confidence Scoring (5 min)

- Calculate match confidence
- Flag low-confidence matches
- Provide alternatives
- Suggest clarifications

### 5. Routing Execution (5 min)

- Route to selected skill
- Pass appropriate parameters
- Handle routing failures
- Log routing decisions

## Usage Examples

### Basic Usage

"Route this user request to the appropriate skill."

### Advanced Usage

"Route with confidence scoring and alternative suggestions."

## Configuration Options

- `scoring_method`: How to calculate match scores
- `chain_threshold`: When to use skill chaining
- `fallback_skill`: Default skill if no match
- `max_alternatives`: Number of alternatives to return

## Constraints

- MUST provide match confidence
- SHOULD offer alternatives
- MUST handle no-match gracefully
- SHOULD explain selection reasoning

## Integration Examples

- Agent frameworks: Route user input
- Skill registries: Match requests
- API gateways: Route to handlers
- Chatbots: Select response skills

## Dependencies

- Python 3.10+
- Text matching libraries
- Scoring algorithms
