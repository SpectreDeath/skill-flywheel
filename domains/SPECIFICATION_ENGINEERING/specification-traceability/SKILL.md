---
name: specification-traceability
description: "Use when: establishing requirement-to-implementation traceability, tracking spec changes across development lifecycle, ensuring compliance with traceability requirements, or generating traceability matrices. Triggers: 'traceability', 'trace requirements', 'requirement trace', 'impact analysis', 'trace matrix'. NOT for: simple linear requirements, projects without compliance needs, or rapid prototypes with volatile requirements."
---

# Specification Traceability

Implement comprehensive requirement traceability from initial concepts through implementation, testing, and deployment. This skill ensures complete visibility of specification impact with automated tracking.

## When to Use This Skill

Use this skill when:
- Establishing requirement-to-implementation traceability
- Tracking spec changes across development lifecycle
- Ensuring compliance with traceability requirements
- Generating traceability matrices for audits
- Performing impact analysis on spec changes

Do NOT use this skill when:
- Simple, linear requirements without dependencies
- Projects without compliance or audit requirements
- Rapid prototypes with volatile requirements

## Input Format

```yaml
traceability_request:
  spec_path: string              # Path to specification document
  artifacts: array               # Implementation artifacts to link
  relationships: array           # Custom relationship types
  format: string                 # Output format (matrix, graph, table)
```

## Output Format

```yaml
traceability_result:
  matrix: object                 # Traceability matrix
  relationships: array           # All tracked relationships
  impact_analysis: object        # Impact assessment
  coverage: object               # Traceability coverage metrics
```

## Capabilities

### 1. Requirements Inventory (10 min)

- Catalog all requirements from specifications
- Classify by type, priority, and criticality
- Assign unique identifiers for tracking

### 2. Relationship Mapping (15 min)

- Link requirements to code implementations
- Map to test cases and validation
- Connect to documentation sections

### 3. Impact Analysis (10 min)

- Track downstream impact of changes
- Identify affected components
- Assess change risk

### 4. Coverage Reporting (5 min)

- Generate traceability coverage reports
- Identify gaps in traceability
- Calculate completeness metrics

### 5. Change Propagation (10 min)

- Track requirement changes through system
- Update related artifacts
- Maintain audit trail

## Usage Examples

### Basic Usage

"Create traceability matrix linking requirements to code."

### Advanced Usage

"Generate full traceability with impact analysis for proposed spec changes."

## When to Use

- Regulatory compliance requires requirement traceability
- Complex projects with interdependent requirements
- Auditing and change management processes
- Quality assurance validation

## When NOT to Use

- Simple, linear requirements
- Projects without compliance requirements
- Rapid prototypes with volatile requirements
- Small teams with informal tracking

## Configuration Options

- `relationship_types`: Custom relationship definitions
- `auto_link`: Automatically detect relationships
- `depth`: Traceability depth (shallow, deep, full)
- `format`: Output format preference

## Constraints

- MUST maintain bidirectional traceability
- SHOULD track all acceptance criteria
- MUST include change history
- SHOULD support automated detection

## Integration Examples

- Issue trackers: Link requirements to tickets
- Version control: Track implementation changes
- Test management: Connect tests to requirements

## Dependencies

- Python 3.10+
- Graph libraries for relationship visualization
- Optional: Integration with project management tools
