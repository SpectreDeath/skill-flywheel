---
name: continuous-learning
description: "Use when: automatically extracting reusable patterns from AI agent sessions and saving them as learned skills for future use, building a personal knowledge base from project work, or creating on-demand capabilities from code patterns. Triggers: 'learn from this', 'extract pattern', 'save this as skill', 'create skill from', 'remember this', 'build knowledge base', 'on-demand capability'. NOT for: one-off tasks that don't need reuse, or when pattern is already well-documented."
---

# Continuous Learning

Automatically extract reusable patterns from AI agent sessions and save them as learned skills for future use. Builds a personal knowledge base from project work.

## When to Use This Skill

Use this skill when:
- You discover a useful pattern during development
- User asks to "learn from this" or "extract pattern"
- You want to save a solution for future reuse
- Building on-demand capabilities from code patterns
- Creating personal skill library from project work

Do NOT use when:
- One-off tasks that don't need reuse
- Pattern is already well-documented in existing skills
- Simple information that doesn't warrant a full skill
- Time-sensitive tasks where extraction would delay work

## Pattern Discovery

The skill analyzes session work to identify:

### Extractable Patterns
- Reusable code snippets that solve recurring problems
- Configuration patterns for tools/frameworks
- Testing strategies that worked well
- Error handling approaches
- API integration patterns
- Workflow sequences that achieved goals

### Quality Indicators
- Pattern solved a non-trivial problem
- Pattern could apply to other projects
- Pattern required research or experimentation to discover
- Pattern documentation would save future time

## Pattern Extraction Process

### 1. Identify Candidate
Analyze current work for extractable patterns:
- What problem did this solve?
- How would someone else apply this?
- Does this pattern generalize?

### 2. Document Pattern
Create skill documentation including:
- **When to use**: Trigger conditions and use cases
- **When NOT to use**: Exclusions and limitations
- **How it works**: Step-by-step process
- **Examples**: Concrete usage examples
- **Dependencies**: Required tools/libraries
- **Variations**: Different implementations

### 3. Store in Skill Library
Save to organized location:
- Domain-specific skills → appropriate domain folder
- General patterns → GENERAL/ or META_SKILL_DISCOVERY/
- Include metadata for discovery

### 4. Verify Reusability
Test that extracted pattern:
- Works in isolation from original context
- Has clear input/output contract
- Includes necessary dependencies
- Can be invoked independently

## Skill Template Structure

```markdown
---
name: [pattern-name]
description: "Use when: [primary use cases] Triggers: [keywords] NOT for: [exclusions]"
---

# [Pattern Name]

[Brief description of what this pattern does]

## When to Use

- Use when: [specific conditions]
- Don't use when: [limitations]

## How It Works

[Step-by-step process]

## Examples

[Code examples, commands, or workflows]

## Dependencies

[List of required tools, libraries, or configurations]

## Variations

[Alternative implementations if applicable]
```

## Learning Hooks

The skill operates through observation hooks that detect learning opportunities:

### Automatic Detection
- User explicitly requests learning
- Repeated similar tasks detected
- Complex problem solved elegantly
- Useful code pattern created

### Manual Trigger
- Developer marks code as "learnable"
- Comment or marker indicates reusable pattern
- Explicit "save this" command

## Version Considerations

Patterns evolve over time:
- Track pattern version
- Note when pattern was learned
- Update when better approaches discovered
- Mark deprecated patterns

## Constraints

- Each pattern should be self-contained
- Patterns must include all necessary context
- Avoid patterns that depend on specific project state
- Document any external dependencies clearly
- Pattern should be testable/verifiable
