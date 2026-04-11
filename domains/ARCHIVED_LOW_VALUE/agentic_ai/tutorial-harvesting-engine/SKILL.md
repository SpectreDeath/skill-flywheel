---
name: tutorial-harvesting-engine
description: "Use when: harvesting tutorials, extracting knowledge from docs, gathering implementation guides, collecting code examples, or building knowledge bases from tutorials. Triggers: 'tutorial harvesting', 'extract from docs', 'collect tutorials', 'knowledge extraction', 'doc parsing', 'tutorial extraction'. NOT for: when content is already structured, simple content copy, or when manual documentation is preferred."
---

# Tutorial Harvesting Engine

Harvests and extracts knowledge from tutorials, documentation, and code examples. This skill builds structured knowledge bases from unstructured tutorial content.

## When to Use This Skill

Use this skill when:
- Harvesting tutorials
- Extracting knowledge from docs
- Gathering implementation guides
- Collecting code examples
- Building knowledge bases from tutorials

Do NOT use this skill when:
- Content already structured
- Simple content copy
- Manual documentation preferred
- No knowledge extraction needed

## Input Format

```yaml
harvesting_request:
  sources: array                 # URLs, files, or directories
  extraction_type: string         # Full, code-only, concepts
  format_output: string           # How to structure output
  filter_criteria: object        # What to include/exclude
```

## Output Format

```yaml
harvesting_result:
  extracted_knowledge: object     # Structured knowledge
  code_examples: array            # Code snippets found
  concepts: array                 # Key concepts extracted
  metadata: object                # Source metadata
  knowledge_base: string         # Formatted knowledge base
```

## Capabilities

### 1. Source Discovery (10 min)

- Find tutorial sources
- Handle various formats (MD, HTML, PDF)
- Navigate documentation sites
- Discover related content

### 2. Content Extraction (15 min)

- Parse tutorial content
- Extract code blocks
- Identify key concepts
- Handle formatting

### 3. Knowledge Structuring (15 min)

- Organize extracted content
- Create knowledge structures
- Build concept maps
- Link related ideas

### 4. Code Processing (15 min)

- Extract code examples
- Identify language and framework
- Clean and format code
- Add context

### 5. Knowledge Base Generation (10 min)

- Build searchable knowledge base
- Create index structures
- Add metadata
- Format for consumption

## Usage Examples

### Basic Usage

"Harvest tutorials from these sources."

### Advanced Usage

"Full extraction with code examples and knowledge base."

## Configuration Options

- `extraction_type`: full, code-only, concepts-only
- `output_format`: markdown, JSON, database
- `include_metadata`: Add source info
- `language_filter`: Limit to specific languages

## Constraints

- MUST handle various formats
- SHOULD extract accurate code
- MUST maintain context
- SHOULD handle failures gracefully

## Integration Examples

- Knowledge bases: Build from tutorials
- Agent training: Extract training data
- Documentation: Auto-generate docs
- Search: Create searchable index

## Dependencies

- Python 3.10+
- HTML parsers
- PDF extractors
- Code highlighting
