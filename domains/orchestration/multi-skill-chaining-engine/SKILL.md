---
name: multi-skill-chaining-engine
description: "Use when: chaining multiple skills together, creating skill pipelines, orchestrating sequential skill execution, or building complex workflows from skills. Triggers: 'chain skills', 'skill pipeline', 'skill sequence', 'orchestrate skills', 'skill workflow', 'multi-skill'. NOT for: single skill execution, simple direct calls, or when skills have no dependencies."
---

# Multi-Skill Chaining Engine

Orchestrates execution of multiple skills in sequence or parallel. This engine manages skill dependencies, passes data between skills, and handles error recovery.

## When to Use This Skill

Use this skill when:
- Chaining multiple skills together
- Creating skill pipelines
- Orchestrating sequential skill execution
- Building complex workflows from skills
- Managing skill dependencies

Do NOT use this skill when:
- Single skill execution
- Simple direct calls
- Skills have no dependencies
- Direct invocation sufficient

## Input Format

```yaml
chaining_request:
  skills: array                  # Skills to chain
  dependencies: object           # Skill dependencies
  parameters: object            # Initial parameters
  execution_mode: string        # sequential, parallel, or adaptive
  error_handling: string        # How to handle failures
```

## Output Format

```yaml
chaining_result:
  execution_order: array        # Order of execution
  results: object               # Results from each skill
  data_flow: object             # Data passed between skills
  errors: array                 # Any errors encountered
  status: string               # success, partial, failed
```

## Capabilities

### 1. Dependency Analysis (10 min)

- Analyze skill dependencies
- Build execution graph
- Detect circular dependencies
- Optimize execution order

### 2. Execution Planning (15 min)

- Plan skill execution sequence
- Identify parallel opportunities
- Determine data flow
- Handle conditional branches

### 3. Parameter Management (10 min)

- Collect initial parameters
- Transform outputs to inputs
- Handle parameter mappings
- Manage shared state

### 4. Execution Orchestration (15 min)

- Execute skills in order
- Handle parallel execution
- Pass data between skills
- Monitor progress

### 5. Error Recovery (10 min)

- Handle skill failures
- Implement retry logic
- Provide rollback options
- Generate error reports

## Usage Examples

### Basic Usage

"Chain these skills together in sequence."

### Advanced Usage

"Execute skills in parallel where possible with error recovery."

## Configuration Options

- `execution_mode`: sequential, parallel, adaptive
- `error_handling`: fail-fast, retry, skip, fallback
- `max_parallel`: Maximum parallel executions
- `timeout`: Overall timeout

## Constraints

- MUST handle skill failures gracefully
- SHOULD optimize execution order
- MUST pass data correctly between skills
- SHOULD provide execution reports

## Integration Examples

- Complex workflows: Combine skills
- Data pipelines: Transform with multiple skills
- Agent systems: Multi-step tasks
- Automation: Orchestrate processes

## Dependencies

- Python 3.10+
- Async execution
- State management
- Error handling
