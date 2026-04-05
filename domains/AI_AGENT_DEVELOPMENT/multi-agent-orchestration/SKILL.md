---
name: multi-agent-orchestration
description: "Use when: coordinating multiple AI agents in parallel, managing multi-agent workflows, assigning tasks to different agents, or building agent teams. Triggers: 'parallel agents', 'multi-agent', 'team of agents', 'coordinate agents', 'dispatch', 'parallel execution', 'agent orchestration'. NOT for: single agent tasks, or when sequential execution is required."
---

# Multi-Agent Orchestration

Patterns for coordinating multiple AI agents in parallel, managing multi-agent workflows, and building effective agent teams.

## When to Use This Skill

Use this skill when:
- Running multiple agent sessions in parallel
- Coordinating multi-agent development workflows
- Decomposing tasks for parallel execution
- Building agent teams with specialized roles
- Managing dependencies between agents

Do NOT use when:
- Single agent can complete the task
- Tasks have strict sequential dependencies
- Resource constraints limit parallelism
- Debugging requires single-threaded execution

## Orchestration Patterns

### Parallel Execution Pattern
```
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Agent A │  │ Agent B │  │ Agent C │
│ (Frontend) │  │ (Backend) │  │ (Tests) │
└────┬────┘  └────┬────┘  └────┬────┘
     │            │            │
     └────────────┼────────────┘
                  │
            ┌────▼────┐
            │ Integrate │
            │ & Verify │
            └─────────┘
```

### Sequential Handoff Pattern
```
┌─────────┐    ┌─────────┐    ┌─────────┐
│ Planner │───▶│ Builder │───▶│ Reviewer │
│ (Design)│    │ (Code)  │    │ (Verify)│
└─────────┘    └─────────┘    └─────────┘
```

### Supervisor Pattern
```
┌──────────────┐
│ Supervisor   │
│ (Coordinates)│
└──────┬───────┘
       │
  ┌───┴───┬───┐
  ▼       ▼   ▼
┌───┐ ┌───┐ ┌───┐
│ A │ │ B │ │ C │
└───┘ └───┘ └───┘
```

## Agent Team Composition

### Common Team Roles

| Role | Responsibility | Best For |
|------|----------------|----------|
| **Planner** | Decompose tasks, create plans | Complex features |
| **Builder** | Write code, implement features | Feature development |
| **Reviewer** | Code review, quality checks | PR review |
| **Tester** | Write tests, verify behavior | Test coverage |
| **Researcher** | Find solutions, explore options | Unknown problems |

### Team Size Guidelines
- **2-3 agents**: Small features, focused work
- **4-5 agents**: Medium features with distinct parts
- **6+ agents**: Large projects, consider splitting instead

## Task Decomposition

### For Parallel Execution
1. Identify independent subtasks
2. Define clear interfaces between parts
3. Assign each subtask to appropriate agent
4. Plan integration step

### Example Decomposition
```
Task: Add user authentication system

Subtask A (Agent 1):
- Database schema for users
- User model and repository
- Password hashing

Subtask B (Agent 2):
- Login API endpoint
- Token generation
- Session management

Subtask C (Agent 3):
- Registration API
- Email verification flow
- Password reset

Integration (Agent 1 or 4):
- Connect components
- End-to-end tests
- Documentation
```

## Conflict Avoidance

### File Ownership Strategy
```python
# Assign ownership to prevent conflicts
FILE_OWNERS = {
    "frontend/": "Agent 1",
    "backend/api/": "Agent 2", 
    "backend/auth/": "Agent 2",
    "tests/": "Agent 3",
}
```

### Interface Contracts
```markdown
## API Contract: User Service

### Endpoints
- GET /users/{id}
- POST /users
- PUT /users/{id}

### Data Models
User {
  id: string
  email: string  
  name: string
}

### Dependencies
- Requires: Database service initialized
- Provides: User CRUD operations
```

## Communication Protocols

### Agent-to-Agent Messages
```python
class AgentMessage:
    sender: str
    receiver: str
    type: "request" | "response" | "notification"
    content: dict
    requires_ack: bool

# Example
message = AgentMessage(
    sender="builder_agent",
    receiver="test_agent",
    type="request",
    content={
        "action": "run_tests",
        "files": ["src/auth/*.py"],
        "coverage_threshold": 80
    }
)
```

### Shared Context
```python
# Shared workspace for agents
SHARED_CONTEXT = {
    "project_root": "/workspace/project",
    "branch": "feature/auth",
    "api_spec": "docs/api.yaml",
    "test_config": "pytest.ini"
}
```

## Execution Management

### Starting Parallel Agents
```python
async def execute_parallel(agents: list[Agent], task: str):
    """Start multiple agents simultaneously"""
    tasks = [agent.execute(task) for agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# With progress tracking
async def execute_with_tracking(agents: list[Agent], task: str):
    """Track agent progress"""
    status = {agent.id: "pending" for agent in agents}
    
    async def run_agent(agent):
        status[agent.id] = "running"
        result = await agent.execute(task)
        status[agent.id] = "complete"
        return result
    
    await asyncio.gather(*[run_agent(a) for a in agents])
```

### Handling Agent Failures
```python
async def execute_with_fallback(agents: list[Agent], task: str):
    """Handle agent failures gracefully"""
    for agent in agents:
        try:
            return await agent.execute(task)
        except AgentError as e:
            log(f"Agent {agent.id} failed: {e}")
            continue
    
    raise AllAgentsFailedError("All agents failed")
```

## Coordination Checkpoints

### Key Synchronization Points

| Point | Purpose | Action |
|-------|---------|--------|
| **Start** | Align context | Share task, constraints |
| **Mid-point** | Check progress | Review partial work |
| **Integration** | Combine work | Resolve conflicts |
| **End** | Final verification | Run full test suite |

### Checkpoint Implementation
```python
class OrchestrationCheckpoint:
    @staticmethod
    async def wait_for_all(agents: list[Agent], timeout: int = 300):
        """Wait for all agents to complete"""
        start = time.time()
        while time.time() - start < timeout:
            if all(agent.status == "complete" for agent in agents):
                return True
            await asyncio.sleep(5)
        return False
    
    @staticmethod
    async def check_progress(agents: list[Agent]) -> dict:
        """Get progress status"""
        return {a.id: a.status for a in agents}
```

## Tools for Multi-Agent

### CLI Tools
- **tmux/dmux**: Terminal multiplexer for parallel sessions
- **Claude DevFleet**: Orchestrate multi-agent coding
- **Continue**: Multi-agent code editing

### Frameworks
- **LangGraph**: Graph-based agent orchestration
- **CrewAI**: Multi-agent framework
- **AutoGen**: Microsoft multi-agent framework

## Constraints

- Assign clear file ownership to avoid conflicts
- Define interfaces before parallel execution
- Always have integration checkpoint
- Handle agent failures gracefully
- Track progress of each agent
- Keep teams small (2-5 agents optimal)
- Consider resource costs of parallel execution
