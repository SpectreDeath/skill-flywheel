---
name: design-pattern-recommender
description: "Use when: recommending design patterns for code, selecting appropriate patterns for problems, analyzing architectural needs, or suggesting refactoring approaches. Triggers: 'design pattern', 'recommend pattern', 'which pattern', 'pattern selection', 'architectural pattern', 'refactor pattern'. NOT for: when pattern is already chosen, simple code without architecture, or when antipatterns are the issue."
---

# Design Pattern Recommender

Recommends appropriate design patterns based on problem characteristics, constraints, and requirements. This analyzer suggests patterns from creational, structural, and behavioral categories.

## When to Use This Skill

Use this skill when:
- Recommending design patterns for code
- Selecting appropriate patterns for problems
- Analyzing architectural needs
- Suggesting refactoring approaches
- Understanding pattern trade-offs

Do NOT use this skill when:
- Pattern already chosen
- Simple code without architecture
- Antipatterns are the issue
- No architectural concern

## Input Format

```yaml
recommendation_request:
  problem_description: string    # Problem to solve
  constraints: array              # Technical constraints
  language: string              # Programming language
  existing_code: string         # Current implementation (optional)
```

## Output Format

```yaml
recommendation_result:
  recommended_patterns: array     # Suggested patterns
  analysis: object               # Why each fits
  trade_offs: object             # Pros/cons
  implementation_guide: string  # How to apply
```

## Capabilities

### 1. Problem Analysis (10 min)

- Analyze problem requirements
- Identify object relationships
- Determine behavioral needs
- Assess complexity

### 2. Pattern Matching (15 min)

- Match problem to pattern categories
- Score pattern fit
- Consider constraints
- Filter inappropriate patterns

### 3. Trade-off Analysis (10 min)

- Evaluate pros/cons
- Consider maintenance impact
- Assess learning curve
- Measure complexity increase

### 4. Implementation Guidance (15 min)

- Provide pattern structure
- Show code examples
- Explain variations
- Suggest application steps

### 5. Refactoring Planning (10 min)

- Plan migration from current code
- Identify change scope
- Estimate effort
- Handle dependencies

## Usage Examples

### Basic Usage

"What design pattern fits this problem?"

### Advanced Usage

"Recommend patterns with trade-off analysis and implementation guide."

## Configuration Options

- `pattern_categories`: Which to consider
- `language`: Target language
- `include_antipatterns`: Flag bad approaches
- `detail_level`: Summary or detailed

## Constraints

- MUST explain why pattern fits
- SHOULD provide examples
- MUST consider constraints
- SHOULD warn about over-engineering

## Integration Examples

- Code reviews: Suggest patterns
- Refactoring: Plan improvements
- Architecture: Select patterns
- Mentoring: Teach patterns

## Dependencies

- Python 3.10+
- Pattern catalogs
- Code analysis tools
