# Agent Skills Development Guide

## Overview

Agent Skills are modular, reusable workflows that turn messy, variable user tasks into well-scoped, repeatable procedures. This guide provides principles, patterns, and templates for developing effective Agent Skills that work across different LLM platforms and agent frameworks.

## Table of Contents

1. [Core Principles](#core-principles)
2. [Skill Architecture](#skill-architecture)
3. [Development Patterns](#development-patterns)
4. [Templates and Examples](#templates-and-examples)
5. [Meta-Skills for Skill Development](#meta-skills-for-skill-development)
6. [Distribution and Libraries](#distribution-and-libraries)
7. [Best Practices](#best-practices)

---

## Core Principles

### 1. Separate "Rules" from "Judgment"

**Principle**: Push deterministic logic into scripts/templates, let the agent handle interpretation and adaptation.

**Implementation**:

- **Machine-like execution**: Fixed scoring logic, thresholds, validation rules
- **Advisor-like reasoning**: Prioritization, explanation, context adaptation
- **Clear boundaries**: Know what must be consistent vs. what can be creative

**Example**:

```markdown
# Fixed (Rules)
- Score threshold: 70% for "ready"
- Required checks: security, tests, docs

# Variable (Judgment)
- What to fix first based on impact
- How to explain tradeoffs to user
- Which alternative approach to suggest
```

### 2. Design for Discoverability and Routing

**Principle**: Make skills easy to find and match to user needs.

**Guidelines**:

- Precise, descriptive names: "Review PR for Security Issues" vs. "Code Review"
- Clear scope statements: "When to use" and "When NOT to use"
- Input/output descriptions in user-friendly language
- Avoid "kitchen sink" skills - prefer smaller, composable units

**Mental Test**: If you read only the name + 1-2 sentence description, could you confidently tell if this skill applies to a given request?

### 3. Progressive Disclosure of Instructions

**Principle**: Don't dump all instructions at once; reveal complexity as needed.

**Structure**:

- **Frontmatter**: Name, description, tags (for discovery)
- **Main body**: Core procedure (when skill is invoked)
- **Helper assets**: Scripts, examples, reference docs (loaded on demand)

**Benefits**:

- Keeps context clean
- Reduces interference between skills
- Makes core procedures more likely to be followed

### 4. Explicit and Finite Workflows

**Principle**: Write skills as concrete, bounded procedures with clear entry/exit points.

**Requirements**:

- **Inputs**: Required files, parameters, environment assumptions
- **Steps**: Ordered, numbered actions with clear criteria
- **Outputs**: Expected artifacts and format
- **Exit conditions**: When the skill is "done"

**Anti-patterns to avoid**:

- "Analyze thoroughly" (too vague)
- "Be smart" (no specific criteria)
- Open-ended loops without clear stopping points

### 5. Constitution (Constraints and Guardrails)

**Principle**: State hard constraints explicitly to ensure consistency and safety.

**Include**:

- **Hard constraints**: What the skill must never do
- **Safety rules**: Production boundaries, data handling
- **Quality standards**: Formatting, testing, validation requirements
- **User confirmation points**: When to ask before proceeding

**Example Constitution**:

```markdown
## Constraints
- NEVER modify files outside /src directory
- ALWAYS show diff before applying changes
- MUST run tests before finalizing
- STOP if user provides unclear requirements
```

### 6. Design for the "Arc" of Use

**Principle**: Consider what happens after the initial result.

**Design Questions**:

- What will the user want to do next?
- How can outputs feed into follow-up workflows?
- What structured data should be produced for automation?

**Good Practice**: Return structured outputs (JSON, tables, labeled sections) rather than just narrative reports.

### 7. Testability and Evaluation

**Principle**: Define success criteria and enable automated evaluation.

**Success Criteria**:

- What does a "correct" run look like?
- What are typical failure modes?
- How can outputs be machine-validated?

**Evaluation Strategy**:

- Fixed prompts/scenarios for testing
- Expected commands or artifacts
- Format validation (JSON schema, required fields)

### 8. Skills over Bloated Global Prompts

**Principle**: Move repeatable workflows into skills instead of one giant agent instruction file.

**Benefits**:

- Reduces prompt entropy
- Makes behavior modular and portable
- Easier to maintain and update
- Clearer separation of concerns

### 9. Small, Composable, Environment-Aware

**Principle**: Keep skills focused and aware of their operating context.

**Characteristics**:

- Small enough to understand in one sitting
- Composable with other skills
- Explicit environment assumptions (tools, directories, APIs)
- Fail loudly when assumptions are violated

---

## Skill Architecture

### The Skill Stack

```text
┌─────────────────────────────────────┐
│           Workflows                 │  ← Orchestration layer
│  (When/How to combine skills)       │
├─────────────────────────────────────┤
│             Skills                  │  ← Reusable workflows
│  (What to do, how to think)         │
├─────────────────────────────────────┤
│        Rules + System               │  ← Global constraints
│  (Always-on guardrails)             │
├─────────────────────────────────────┤
│           Tools                     │  ← Capabilities
│  (File access, APIs, commands)      │
└─────────────────────────────────────┘
```

### Skill Components

1. **Metadata**: Name, description, tags, version
2. **Purpose**: When to use, when NOT to use
3. **Inputs**: Required data, files, parameters
4. **Outputs**: Expected artifacts and format
5. **Workflow**: Step-by-step procedure
6. **Constraints**: Hard rules and safety checks
7. **Examples**: Canonical usage scenarios
8. **Assets**: Scripts, templates, reference data

### Environment Assumptions

Every skill should explicitly state:

- Required tools (MCP servers, CLI commands)
- Directory structure expectations
- File format requirements
- Permission/authorization needs
- External service dependencies

---

## Development Patterns

### Pattern 1: The Meta-Skill Approach

Start by building skills that help you create better skills:

1. **Skill Drafting**: Turn messy intent into structured `SKILL.md`
2. **Skill Critiquing**: Review and refine skill specifications
3. **Skill Cataloging**: Organize and index your skill library

### Pattern 2: Progressive Complexity

```text
Level 1: Single-task skill
├── Input → Process → Output
└── No external dependencies

Level 2: Tool-using skill  
├── Uses 1-2 MCP tools
├── Handles tool failures
└── Provides fallback strategies

Level 3: Multi-step workflow
├── 3-5 sequential steps
├── Decision points and branching
└── Structured outputs

Level 4: Adaptive skill
├── Context-aware behavior
├── User preference learning
└── Integration with other skills
```

### Pattern 3: The Circuit Metaphor

Think of skills as electronic components:

- **Wires**: Tools/MCP servers (data flow)
- **Components**: Skills (processing units)
- **Power/Ground**: System prompt + rules (operating conditions)
- **Circuit topology**: Workflows (how components connect)
- **Overall device**: Capability (emergent behavior)

---

## Templates and Examples

### Basic Skill Template

```markdown
# SKILL: [Skill Name]

## Purpose
[1-2 sentences describing what this skill does and when to use it]

## When to Use
- [Specific scenarios where this skill applies]
- [Input conditions that trigger this skill]

## When NOT to Use
- [Scenarios where this skill should NOT be used]
- [Input conditions that mean this skill is inappropriate]

## Inputs
- **Required**: [List of required inputs]
- **Optional**: [List of optional inputs]
- **Assumptions**: [Environment assumptions]

## Outputs
- **Primary**: [Main output artifact]
- **Secondary**: [Additional outputs]
- **Format**: [Expected format/structure]

## Workflow
1. [First step with clear criteria]
2. [Second step with clear criteria]
3. [Continue with numbered steps]

## Constraints
- [Hard rule 1]
- [Hard rule 2]
- [Safety requirement]
- [Quality standard]

## Examples
### Example 1: [Scenario name]
**Input**: [Describe input]
**Output**: [Describe expected output]
**Notes**: [Any special considerations]

### Example 2: [Scenario name]
**Input**: [Describe input]
**Output**: [Describe expected output]
**Notes**: [Any special considerations]

## Assets
- [List of supporting files, scripts, templates]
```

### Example: Repo Recon Skill

```markdown
# SKILL: Repo Reconnaissance

## Purpose
Analyze a codebase to understand its structure, technology stack, and potential risks. Used when onboarding to a new project or assessing code quality.

## When to Use
- First time working with a repository
- Before making significant architectural changes
- When security/compliance review is needed
- When onboarding new team members

## When NOT to Use
- When you already know the codebase intimately
- When you need to make quick, isolated changes
- When time is severely constrained

## Inputs
- **Required**: Repository path or URL
- **Optional**: Focus areas (security, performance, architecture)
- **Assumptions**: Git repository with commit history

## Outputs
- **Primary**: Structured analysis report (JSON)
- **Secondary**: Risk assessment summary
- **Format**: Markdown report with sections for structure, tech stack, risks

## Workflow
1. **Structure Analysis**: Scan directory layout, identify main components
2. **Tech Stack Detection**: Analyze package files, imports, build configs
3. **Risk Assessment**: Check for secrets, deprecated dependencies, security issues
4. **Documentation Review**: Evaluate README, architecture docs, code comments
5. **Report Generation**: Compile findings into structured format

## Constraints
- NEVER execute arbitrary code found in the repository
- DO NOT modify any files during analysis
- MUST respect .gitignore and ignore patterns
- STOP if repository appears malicious or contains sensitive data

## Examples
### Example 1: New Project Onboarding
**Input**: Path to unfamiliar codebase
**Output**: Comprehensive overview report
**Notes**: Focus on understanding architecture and potential risks

### Example 2: Security Review
**Input**: Repository with focus area = "security"
**Output**: Security-focused risk assessment
**Notes**: Emphasize secrets, dependencies, and vulnerable patterns

## Assets
- tech_stack_detector.py: Script to identify technologies
- risk_scanner.py: Security and compliance checker
- report_template.md: Standard report format
```

---

## Meta-Skills for Skill Development

### 1. Skill Drafting Skill

**Purpose**: Turn messy intent into structured `SKILL.md` files

**Workflow**:

1. Extract core elements from natural language description
2. Normalize into standard skill structure
3. Identify missing information and ask clarifying questions
4. Generate complete skill specification
5. Validate against best practices

### 2. Skill Critiquing Skill

**Purpose**: Review and refine existing skill specifications

**Workflow**:

1. Analyze scope and clarity
2. Identify ambiguous steps or missing constraints
3. Check for consistency with other skills
4. Suggest improvements and refinements
5. Validate testability and composability

### 3. Skill Testing Skill

**Purpose**: Create and run evaluations for skill behavior

**Workflow**:

1. Generate test scenarios based on skill specification
2. Create expected output templates
3. Run skill against test cases
4. Compare actual vs. expected outputs
5. Report on skill reliability and edge cases

---

## Distribution and Libraries

### Library Structure

```
agent-libraries/
├── repo_doctor/                    # Your first library
│   ├── SKILL.analyze.md
│   ├── SKILL.security.md
│   ├── FLOW.onboard.yaml
│   ├── mcp_tools/ (git_search, pytest_runner)
│   └── README.md (install: copy to .agents/skills/)
├── skill_factory/
│   ├── SKILL.draft.md
│   ├── SKILL.critique.md
│   └── FLOW.build.yaml
└── README.md (compatible: Goose, Cline, Cursor, Claude)
```

### Distribution Strategies

1. **GitHub Repositories**: Version-controlled, collaborative
2. **VS Code Extensions**: Integrated with editor ecosystem
3. **Package Managers**: npm, pip, cargo for language-specific skills
4. **Community Hubs**: Shared repositories and marketplaces

### Compatibility Matrix

| Platform | Skills Support | MCP Support | Notes |
|----------|----------------|-------------|-------|
| Goose    | Native         | Yes         | Local-first, extension-based |
| Cline    | Yes            | Native      | Plan/Act modes + terminal |
| Cursor   | Yes            | Yes         | IDE-integrated |
| Claude | Yes | Yes | Cross-platform |

---

## Best Practices

### 1. Naming Conventions

- Use verb-noun pattern: "Review PR", "Generate Report"
- Be specific: "Security Review" vs. "Code Review"
- Include scope when helpful: "Frontend Component Review"

### 2. Versioning

- Include version in skill metadata
- Maintain backward compatibility when possible
- Document breaking changes clearly
- Use semantic versioning (MAJOR.MINOR.PATCH)

### 3. Documentation

- Write for both humans and LLMs
- Include clear examples with inputs/outputs
- Document assumptions and limitations
- Provide troubleshooting guidance

### 4. Testing

- Create test cases for each workflow branch
- Test with edge cases and invalid inputs
- Validate output format and content
- Test integration with other skills

### 5. Performance

- Minimize context usage in skill descriptions
- Use progressive disclosure to reduce prompt size
- Cache expensive operations when possible
- Optimize for the most common use cases

### 6. Security

- Never hardcode secrets in skills
- Validate all inputs before processing
- Use principle of least privilege for tool access
- Include security checks in skill workflows

### 7. Maintainability

- Keep skills focused and single-purpose
- Use consistent structure across all skills
- Document dependencies and assumptions
- Plan for skill evolution and deprecation

---

## Getting Started

### Step 1: Define Your First Skill

1. Identify a repetitive task or workflow
2. Break it down into clear steps
3. Identify required inputs and expected outputs
4. Write the skill using the template
5. Test with realistic scenarios

### Step 2: Build Meta-Skills

1. Create a skill drafting skill
2. Create a skill critiquing skill
3. Create a skill testing skill
4. Use these to improve your skill development process

### Step 3: Create Libraries

1. Organize related skills into libraries
2. Create workflow files to orchestrate skills
3. Package with clear documentation
4. Share with your team or community

### Step 4: Iterate and Improve

1. Gather feedback from skill usage
2. Identify common failure modes
3. Refine skill specifications
4. Add new skills based on emerging needs

---

## Conclusion

Agent Skills are a powerful way to build reusable, reliable workflows that work across different LLM platforms. By following these principles and patterns, you can create a library of skills that amplifies your productivity and enables consistent, high-quality results.

Remember: skills are about **consistency** and **reliability**. The goal is to turn your best practices into repeatable procedures that any agent can execute successfully.

Start small, build iteratively, and focus on skills that solve real problems in your workflow.
