---
name: blueprint-planning
description: "Use when: turning a one-line objective into a step-by-step construction plan for multi-session, multi-agent engineering projects. Each step has a self-contained context brief so a fresh agent can execute it cold. Triggers: 'plan', 'blueprint', 'roadmap', 'multI-PR task', 'multi-session', 'execution plan', 'decompose task', 'step-by-step'. NOT for: tasks completable in a single PR or fewer than 3 tool calls, or when user says 'just do it'."
---

# Blueprint Planning

Turn a one-line objective into a step-by-step construction plan for multi-session, multi-agent engineering projects. Each step has a self-contained context brief so a fresh agent can execute it cold.

## When to Use This Skill

Use this skill when:
- User requests a plan, blueprint, or roadmap for a complex multi-PR task
- User describes work that needs multiple sessions
- Task involves multiple agents or team members
- User wants to break down a large feature into manageable steps
- Project spans several days or weeks

Do NOT use when:
- Task is completable in a single PR
- Task requires fewer than 3 tool calls
- User says "just do it" or "do it now"
- Simple, straightforward implementation

## Input Requirements

The skill requires:
1. **Objective**: One-line description of what to build
2. **Constraints**: Any known limitations (budget, timeline, tech stack)
3. **Context**: Relevant background information about the project
4. **Stakeholders**: Who will execute and review each step

## Output Format

The skill generates a structured blueprint with:

### 1. Executive Summary
- High-level overview of the objective
- Total estimated effort (time, PRs, agents)
- Key milestones and dependencies

### 2. Step Breakdown
Each step includes:
- **Step ID**: Sequential identifier
- **Title**: Short descriptive name
- **Objective**: What this step accomplishes
- **Context Brief**: Self-contained info for cold agent execution
- **Dependencies**: What must complete first
- **Estimated Effort**: Time and complexity
- **Deliverables**: What gets produced
- **Verification**: How to confirm completion
- **Parallelizable**: Whether this can run with other steps

### 3. Dependency Graph
Visual representation of step relationships showing:
- Critical path (longest dependency chain)
- Parallel execution opportunities
- Risk points where blocking occurs

### 4. Agent Assignment Matrix
Who executes each step:
- Primary agent/developer
- Reviewer
- Stakeholders for sign-off

### 5. Review Gates
Checkpoint locations where:
- Technical review occurs
- Stakeholder approval needed
- Integration testing happens

## Anti-Patterns to Detect

The skill includes an anti-pattern catalog to warn about:
- **Waterfall traps**: Plans that assume perfect upfront specification
- **Parallelization myths**: Steps marked parallel that have hidden dependencies
- **Context leaks**: Steps requiring information from future steps
- **Review bottlenecks**: Too many steps requiring same reviewer
- **Integration cramming**: Multiple complex features in single step

## Plan Mutation Protocol

When execution reveals the plan needs adjustment:
1. Identify the discrepancy
2. Assess impact on remaining steps
3. Propose specific modifications
4. Get stakeholder approval for changes
5. Update the blueprint with rationale

## Example Blueprint Structure

```
## Blueprint: Add OAuth2 Social Login

### Executive Summary
- Objective: Implement OAuth2 login for Google, GitHub, Microsoft
- Effort: 5 PRs, ~2 weeks
- Key Dependencies: User model exists, API framework in place

### Step 1: OAuth Provider Interface
- Context: Create abstraction for OAuth providers
- Deliverables: Provider interface, 3 provider implementations
- Effort: 1 day
- Parallel: No

### Step 2: OAuth Controller Endpoints  
- Context: Add /auth/google, /auth/github, /auth/microsoft
- Deliverables: OAuth controllers, redirect handling
- Effort: 1 day
- Parallel: Yes (all 3 providers)

### Step 3: Token Management
- Context: JWT token generation and refresh
- Deliverables: Token service, refresh endpoint
- Effort: 1 day
- Depends on: Step 1

### Step 4: Frontend Integration
- Context: Add login buttons and OAuth flow
- Deliverables: Login page updates, token storage
- Effort: 1 day
- Depends on: Step 2, Step 3

### Step 5: Integration Testing
- Context: Test full OAuth flow end-to-end
- Deliverables: E2E tests for each provider
- Effort: 1 day
- Depends on: All previous
```

## Constraints

- Each step must be executable by a cold agent with only the context brief
- No step should require more than 1 day of focused work
- Critical path should be minimized
- Review gates should be distributed, not all at the end
- Plan should be feasible given stated constraints
