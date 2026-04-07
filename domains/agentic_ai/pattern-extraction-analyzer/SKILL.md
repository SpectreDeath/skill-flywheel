---
name: pattern-extraction-analyzer
description: "Use when: extracting patterns from tutorials, analyzing code patterns, identifying agent patterns, finding common implementations, or learning from existing codebases. Triggers: 'pattern extraction', 'extract patterns', 'analyze patterns', 'tutorial analysis', 'code patterns', 'pattern discovery'. NOT for: when patterns are already known, simple code without patterns, or manual pattern identification."
---

# Pattern Extraction Analyzer

Extracts and analyzes patterns from tutorials, code examples, and documentation. This skill identifies reusable patterns, architectural approaches, and implementation strategies.

## When to Use This Skill

Use this skill when:
- Extracting patterns from tutorials
- Analyzing code patterns
- Identifying agent patterns
- Finding common implementations
- Learning from existing codebases

Do NOT use this skill when:
- Patterns already known
- Simple code without patterns
- Manual pattern identification preferred
- No tutorial content available

## Input Format

```yaml
extraction_request:
  source_content: string         # Tutorial or code to analyze
  pattern_type: string            # Type of patterns to find
  analysis_depth: string          # Shallow, medium, deep
  output_format: string           # How to present findings
```

## Output Format

```yaml
extraction_result:
  patterns_found: array           # Extracted patterns
  pattern_details: object         # Each pattern's details
  implementation_examples: array # Code examples
  recommendations: array         # How to apply patterns
```

## Capabilities

### 1. Content Parsing (10 min)

- Parse tutorial content
- Extract code examples
- Identify explanatory sections
- Handle various formats

### 2. Pattern Detection (20 min)

- Find recurring patterns
- Identify architectural approaches
- Detect implementation strategies
- Recognize anti-patterns

### 3. Classification (10 min)

- Categorize patterns (creational, structural, behavioral)
- Group by domain
- Rank by importance
- Assess complexity

### 4. Example Extraction (15 min)

- Pull code examples
- Identify key implementations
- Extract configuration
- Gather usage patterns

### 5. Documentation (10 min)

- Document findings
- Create pattern guide
- Generate implementation notes
- Provide usage recommendations

## Usage Examples

### Basic Usage

"Extract patterns from this tutorial."

### Advanced Usage

"Deep analysis of patterns with implementation examples."

## Configuration Options

- `analysis_depth`: shallow, medium, deep
- `pattern_categories`: What types to find
- `output_format`: structured, narrative, code
- `min_occurrences`: How common to be a pattern

## Constraints

- MUST extract accurate patterns
- SHOULD provide implementation guidance
- MUST handle various content formats
- SHOULD flag anti-patterns

## Integration Examples

- Tutorial harvesting: Extract from docs
- Agent design: Learn from examples
- Code generation: Apply patterns
- Learning: Create pattern libraries

## Dependencies

- Python 3.10+
- Code parsing libraries
- NLP for pattern detection
- Documentation generators
