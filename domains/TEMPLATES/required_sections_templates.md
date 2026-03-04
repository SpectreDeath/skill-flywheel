# Required Sections Templates for Agent Skills

This document provides standardized templates for the four required sections that must be present in all skill files.

## 1. Purpose Section Template

```markdown
## Purpose
[Clear, concise description of what this skill accomplishes and why it exists. Should be 1-3 sentences that explain the primary objective and value proposition of the skill.]
```

**Guidelines:**
- Keep it concise (1-3 sentences)
- Focus on the "why" rather than the "what"
- Explain the value proposition
- Use clear, non-technical language when possible
- Avoid implementation details

**Examples:**
- "Comprehensive CI/CD pipeline development and automation workflows for modern DevOps practices, including containerization, infrastructure as code, and deployment strategies."
- "Automatically identifies and extracts design patterns, algorithmic patterns, and architectural patterns from existing codebases."

## 2. Examples Section Template

```markdown
## Examples

### Example 1: [Descriptive Title]
**Input**: [Clear description of input or trigger]
**Output**: [Clear description of expected output or result]
**Use Case**: [When and why this example is applicable]

### Example 2: [Descriptive Title]
**Input**: [Clear description of input or trigger]
**Output**: [Clear description of expected output or result]
**Use Case**: [When and why this example is applicable]

[Add more examples as needed, typically 2-4 per skill]
```

**Guidelines:**
- Provide 2-4 concrete examples
- Use descriptive titles for each example
- Clearly specify input and output for each example
- Include use case context
- Examples should cover different scenarios or variations
- Use realistic, practical scenarios

## 3. Implementation Notes Section Template

```markdown
## Implementation Notes
[Detailed technical information about how this skill should be implemented, including:
- Key technical considerations
- Dependencies and prerequisites
- Performance considerations
- Integration requirements
- Best practices for implementation
- Common pitfalls to avoid]
```

**Guidelines:**
- Focus on technical implementation details
- Include dependencies, prerequisites, and requirements
- Address performance, scalability, and integration concerns
- Provide best practices and guidelines
- Mention common implementation challenges
- Keep it actionable and practical

**Structure Options:**
- Bullet points for quick reference
- Numbered steps for procedural information
- Subsections for different aspects (Dependencies, Performance, Integration, etc.)

## 4. Constraints Section Template

```markdown
## Constraints
- **NEVER** [specific prohibition that must never be violated]
- **ALWAYS** [mandatory requirement that must always be followed]
- **MUST** [critical requirement for successful implementation]
- **SHOULD** [strong recommendation for best results]
- **MUST NOT** [explicit prohibition of specific actions]
```

**Guidelines:**
- Use clear, imperative language
- Focus on hard constraints and requirements
- Include both positive requirements (what TO do) and negative constraints (what NOT to do)
- Prioritize the most critical constraints
- Use standard constraint keywords (NEVER, ALWAYS, MUST, SHOULD, MUST NOT)
- Keep constraints actionable and testable

**Common Constraint Categories:**
- Security constraints
- Performance requirements
- Compatibility requirements
- Resource limitations
- Behavioral requirements
- Integration constraints

## Usage Guidelines

### For Auto-Generated Skills
- Use template placeholders that can be filled programmatically
- Maintain consistency across similar skill types
- Include domain-specific constraints and requirements
- Provide realistic examples based on the skill's purpose

### For Manually Created Skills
- Extract information from existing detailed content
- Preserve technical depth while adding structure
- Ensure examples reflect actual use cases
- Validate constraints against existing implementation

### Quality Assurance
- All sections must be present in every skill file
- Content should be specific to the skill's domain and purpose
- Examples should be practical and testable
- Constraints should be enforceable and meaningful
- Templates should be adapted to fit the skill's context

## Template Adaptation Guidelines

### Domain-Specific Adaptations

**Technical Skills (ALGO_PATTERNS, DATABASE_ENGINEERING, etc.):**
- More technical language acceptable in Purpose
- Examples should include code snippets or technical scenarios
- Implementation Notes should be detailed and specific
- Constraints should focus on technical requirements

**Process Skills (DEVOPS, APPLICATION_SECURITY, etc.):**
- Focus on workflows and procedures in Purpose
- Examples should describe process scenarios
- Implementation Notes should cover organizational aspects
- Constraints should include compliance and governance requirements

**Conceptual Skills (EPISTEMOLOGY, LOGIC, etc.):**
- Theoretical context acceptable in Purpose
- Examples should illustrate conceptual applications
- Implementation Notes should cover methodological considerations
- Constraints should focus on logical consistency and validity

### Skill Complexity Adaptations

**Simple Skills (1-2 core functions):**
- Purpose: 1-2 sentences
- Examples: 2-3 examples
- Implementation Notes: 3-5 bullet points
- Constraints: 3-5 items

**Complex Skills (3+ core functions or multi-step processes):**
- Purpose: 2-3 sentences
- Examples: 3-5 examples
- Implementation Notes: 5-8 bullet points or structured subsections
- Constraints: 5-8 items

**Expert-Level Skills (specialized or advanced capabilities):**
- Purpose: 2-3 sentences with technical context
- Examples: 4-6 examples including edge cases
- Implementation Notes: Detailed technical guidance with subsections
- Constraints: 6-10 items including advanced requirements