---
name: agent-architecture-designer
description: "Use when: designing agent architectures, planning multi-agent systems, creating agent system blueprints, defining agent components, or architecting AI agent solutions. Triggers: 'agent architecture', 'design agent', 'agent system', 'architecture design', 'agent blueprint', 'multi-agent architecture'. NOT for: simple single-agent tasks, when off-the-shelf frameworks are sufficient, or when no architectural planning needed."
---

# Agent Architecture Designer

Designs comprehensive agent architectures for multi-agent systems. This skill creates blueprints, component definitions, and implementation plans.

## When to Use This Skill

Use this skill when:
- Designing agent architectures
- Planning multi-agent systems
- Creating agent system blueprints
- Defining agent components
- Architecting AI agent solutions

Do NOT use this skill when:
- Simple single-agent tasks
- Off-the-shelf frameworks sufficient
- No architectural planning needed
- Ready-to-use solutions exist

## Input Format

```yaml
architecture_request:
  use_case: string               # What the agents will do
  num_agents: number             # Number of agents needed
  agent_types: array              # Types of agents required
  requirements: object            # Non-functional requirements
  constraints: object            # Technical constraints
```

## Output Format

```yaml
architecture_result:
  architecture_diagram: object    # Visual architecture
  component_specs: object         # Component definitions
  agent_designs: array            # Individual agent specs
  integration_plan: object       # How components connect
  implementation_roadmap: object # Phases to build
```

## Capabilities

### 1. Requirements Analysis (15 min)

- Analyze use case requirements
- Identify agent responsibilities
- Determine communication needs
- Assess performance requirements

### 2. Architecture Design (20 min)

- Design overall system architecture
- Define component boundaries
- Create data flows
- Plan scalability

### 3. Component Specification (15 min)

- Specify agent components
- Define interfaces
- Design memory systems
- Plan tool integrations

### 4. Communication Design (10 min)

- Design inter-agent communication
- Define message protocols
- Plan coordination mechanisms
- Handle error flows

### 5. Implementation Planning (15 min)

- Create build roadmap
- Identify dependencies
- Estimate effort
- Define milestones

## Usage Examples

### Basic Usage

"Design agent architecture for this use case."

### Advanced Usage

"Full architecture with component specs and implementation plan."

## Configuration Options

- `architecture_style`: centralized, decentralized, hybrid
- `framework`: langgraph, crewai, custom
- `communication`: sync, async, event-driven
- `scale`: single, small team, large system

## Constraints

- MUST create actionable designs
- SHOULD follow best practices
- MUST consider scalability
- SHOULD be implementation-ready

## Integration Examples

- LangGraph: Generate LangGraph architecture
- Custom: Create custom frameworks
- Migration: Plan from existing systems
- Documentation: Generate architecture docs

## Dependencies

- Python 3.10+
- Architecture tools
- Diagram generation
