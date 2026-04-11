---
name: multi-agent-workflow-generator
description: "Use when: generating multi-agent workflows, creating agent pipelines, orchestrating multiple AI agents, designing agent collaboration, or building complex agent systems. Triggers: 'multi-agent', 'agent workflow', 'agent pipeline', 'agent orchestration', 'multi-agent system', 'agent collaboration'. NOT for: single agent tasks, simple sequential processing, or when manual agent coordination is preferred."
---

# Multi-Agent Workflow Generator

Generates complete multi-agent workflow architectures with defined roles, communication patterns, and execution flows. This skill creates scalable agent systems.

## When to Use This Skill

Use this skill when:
- Generating multi-agent workflows
- Creating agent pipelines
- Orchestrating multiple AI agents
- Designing agent collaboration
- Building complex agent systems

Do NOT use this skill when:
- Single agent tasks
- Simple sequential processing
- Manual agent coordination preferred
- No multi-agent coordination needed

## Input Format

```yaml
workflow_request:
  num_agents: number            # Number of agents needed
  agent_types: array             # Types of agents (planner, executor, critic)
  collaboration_pattern: string  # How agents work together
  communication: string          # Communication style (sync, async, message bus)
```

## Output Format

```yaml
workflow_result:
  workflow_definition: object    # Complete workflow config
  agent_configs: array           # Configuration for each agent
  communication_flow: object    # Message flows between agents
  execution_plan: object         # How to run the workflow
```

## Capabilities

### 1. Workflow Design (15 min)

- Define agent roles and responsibilities
- Create collaboration patterns
- Design information flows
- Plan error handling strategies

### 2. Agent Configuration (15 min)

- Configure agent capabilities
- Set up tool access
- Define prompt templates
- Configure memory systems

### 3. Communication Architecture (10 min)

- Design message passing
- Implement coordination mechanisms
- Create shared state management
- Build error propagation

### 4. Code Generation (20 min)

- Generate agent code
- Create orchestration logic
- Implement communication handlers
- Build execution framework

### 5. Testing & Validation (10 min)

- Test agent interactions
- Validate communication flows
- Verify error handling
- Measure performance

## Usage Examples

### Basic Usage

"Generate a multi-agent workflow with planner and executor."

### Advanced Usage

"Create complete multi-agent system with 4 agents, async messaging, and shared memory."

## Configuration Options

- `num_agents`: 2-10+ agents
- `framework`: langgraph, crewai, autogen, custom
- `communication`: sync, async, message-queue
- `memory_type`: short-term, long-term, episodic

## Constraints

- MUST generate working code
- SHOULD follow agent framework best practices
- MUST include error handling
- SHOULD be scalable

## Integration Examples

- LangGraph: Generate LangGraph workflows
- CrewAI: Create CrewAI crews
- AutoGen: Build AutoGen studios
- Custom: Generate custom frameworks

## Dependencies

- Python 3.10+
- Agent frameworks (langgraph, crewai, autogen)
- Message passing libraries
