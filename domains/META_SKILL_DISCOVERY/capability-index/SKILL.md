---
name: capability-index
description: "Use when: building capability indexes, indexing skill capabilities, searching by capability, or mapping skills to capabilities. Triggers: 'capability index', 'skill index', 'capability search', 'map skills', 'index capabilities', 'capability mapping'. NOT for: simple skill lists, when skills are self-describing, or when no search capability needed."
---

# Capability Index

Builds and maintains indexes of skill capabilities for efficient search and discovery. This skill maps skills to capabilities and enables capability-based retrieval.

## When to Use This Skill

Use this skill when:
- Building capability indexes
- Indexing skill capabilities
- Searching by capability
- Mapping skills to capabilities
- Creating capability directories

Do NOT use this skill when:
- Simple skill lists
- Skills are self-describing
- No search capability needed
- Manual lookup sufficient

## Input Format

```yaml
index_request:
  skills: array                  # Skills to index
  capability_taxonomy: object   # Capability categories
  index_type: string            # How to index
  search_requirements: object  # Search needs
```

## Output Format

```yaml
index_result:
  capability_map: object        # Skill-to-capability mapping
  index_structure: object        # Index organization
  search_interface: object      # How to query
  coverage: object             # Coverage metrics
```

## Capabilities

### 1. Capability Extraction (15 min)

- Analyze skill descriptions
- Extract capability keywords
- Categorize capabilities
- Build taxonomy

### 2. Index Building (15 min)

- Create index structure
- Map skills to capabilities
- Build search structures
- Enable fast lookup

### 3. Search Implementation (10 min)

- Implement search interface
- Handle capability queries
- Support fuzzy matching
- Rank results

### 4. Maintenance (10 min)

- Update index as skills change
- Handle skill additions
- Remove deprecated entries
- Maintain consistency

### 5. Analytics (10 min)

- Analyze capability coverage
- Identify gaps
- Suggest new skills
- Track usage

## Usage Examples

### Basic Usage

"Build a capability index for these skills."

### Advanced Usage

"Create searchable index with taxonomy and analytics."

## Configuration Options

- `index_type`: inverted, hierarchical, graph
- `update_frequency`: How often to refresh
- `search_type`: keyword, semantic, hybrid
- `taxonomy_source`: Custom or auto-generated

## Constraints

- MUST support fast lookup
- SHOULD handle skill changes
- MUST maintain accuracy
- SHOULD enable flexible search

## Integration Examples

- Skill registries: Enable search
- Agent systems: Find skills
- Self-service: Capability lookup
- Planning: Gap analysis

## Dependencies

- Python 3.10+
- Search libraries
- Indexing structures
