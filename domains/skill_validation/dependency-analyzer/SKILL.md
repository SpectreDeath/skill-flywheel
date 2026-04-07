---
name: dependency-analyzer
description: "Use when: analyzing dependencies between skills, detecting circular dependencies, verifying dependency completeness, or visualizing dependency graphs. Triggers: 'dependency', 'circular dependency', 'dependency graph', 'analyze dependencies', 'dependency visualization', 'dependency audit'. NOT for: structure validation, naming checks, or content validation."
---

# Dependency Analyzer

Analyzes and validates dependencies between skills. This tool detects circular dependencies, verifies completeness, and generates visualizations.

## When to Use This Skill

Use this skill when:
- Analyzing dependencies between skills
- Detecting circular dependencies
- Verifying dependency completeness
- Creating dependency visualizations
- Assessing skill modularity

Do NOT use this skill when:
- Validating directory structure (use skill-spec-validator)
- Checking naming conventions (use naming-convention-checker)
- Validating content (use format-compliance-tester)

## Input Format

```yaml
analysis_request:
  root_path: string              # Path to skills directory
  detect_circular: boolean       # Detect circular deps
  visualize: boolean             # Generate graph
  depth_limit: number           # Max dependency depth
```

## Output Format

```yaml
analysis_result:
  status: "pass" | "fail"
  dependency_graph: object       # Full dependency map
  circular_deps: array           # Circular dependencies
  missing_deps: array           # Missing dependencies
  orphan_skills: array          # Skills with no deps
  visualization: string          # Graphviz if requested
```

## Capabilities

### 1. Dependency Graph Analysis (10 min)

- Map all skill dependencies
- Build dependency tree
- Identify direct/indirect deps
- Calculate dependency depth

### 2. Circular Dependency Detection (10 min)

- Detect circular references
- Trace cycle paths
- Identify problematic cycles
- Suggest break points

### 3. Dependency Completeness (10 min)

- Find missing dependencies
- Identify broken references
- Verify optional vs required
- Check version compatibility

### 4. Modularity Assessment (5 min)

- Identify orphan skills
- Measure coupling
- Calculate cohesion
- Flag tight coupling

### 5. Visualization Generation (10 min)

- Generate Graphviz diagrams
- Create dependency tables
- Export to DOT/PNG
- Highlight critical paths

## Usage Examples

### Basic Usage

"Analyze dependencies in the skills repository."

### Advanced Usage

"Run dependency analysis with circular detection and graphviz visualization."

## Configuration Options

- `detect_circular`: Find circular deps
- `visualize`: Generate diagrams
- `depth_limit`: Max traversal depth
- `format`: Output format (json, dot, png)

## Constraints

- MUST detect all circular dependencies
- SHOULD identify missing refs
- MUST build accurate dependency graph
- SHOULD provide visualizations

## Integration Examples

- CI/CD: Check in pipeline
- Pre-merge: Validate before PR
- Audits: Regular dependency reviews

## Dependencies

- Python 3.10+
- graphviz for visualization
- networkx for graph analysis
- json for output
