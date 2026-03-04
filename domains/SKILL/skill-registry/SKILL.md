---
Domain: SKILL
Version: 1.0.0
Complexity: Low
Type: Tool
Category: Discovery
Estimated Execution Time: 50ms - 1 second
name: skill-registry
---

# SKILL: Skill Registry


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

The Skill Registry provides a centralized mechanism for discovering and searching the AgentSkills library. It allows agents to find the most relevant skill for a specific task using metadata, tags, and semantic descriptions.

## When to Use

- You are unsure which skill to use for a user request
- You need to see the full capabilities of the library
- You want to perform a gap analysis on existing skills
- You're building an automated pipeline and need to select a tool dynamically

## When NOT to Use

- You already know the exact skill needed
- The task is highly specific and unlikely to be covered by existing skills
- You are strictly following a predefined sequence in a `FLOW` file

## Inputs

- **Required**: Search query or task description
- **Optional**: Category filter (e.g., Security, Database, Game Dev)
- **Optional**: Complexity threshold
- **Optional**: Output format (JSON/Markdown)

## Outputs

- **Primary**: List of matching skills with relevance scores
- **Secondary**: Detailed metadata for the top-matched skill
- **Format**: Structured table or JSON object

## Capabilities

1. **Metadata Search**: Search across `name`, `Domain`, `Category`, and `Purpose` fields.
2. **Tag Filtering**: Filter results by technology stack or process type.
3. **Relevance Ranking**: Order skills by how well they match the query intent.
4. **Tool Info Extraction**: Provide immediate access to the matched skill's description and usage examples.

## Workflow

1. **Receive Request**: Parse the user's intent and target domain.
2. **Scan Registry**: Execute `registry_search.py` against the `skills/` directory.
3. **Filter Results**: Apply any optional constraints (e.g., complexity).
4. **Rank & Select**: Return the top 3-5 most relevant skills.
5. **Present Findings**: Format the results for easy agent consumption.

## Constraints

- NEVER suggest skills that don't exist in the local `skills/` directory.
- MUST respect the `agentskills.io` specification for metadata fields.
- SHOULD provide a fallback "No skill found" message if relevance scores are low.

## Examples

### Example 1: General Help

**Input**: "How do I optimize a database?"
**Output**:

1. `database-optimization-guide` (Relevance: 0.95)
2. `sql-query-profiler` (Relevance: 0.82)

### Example 2: Specific Domain

**Input**: "Query: 'Smart contract audit', Category: 'WEB3'"
**Output**:

1. `smart-contract-audit` (Relevance: 1.0)

## Configuration Options

- `registry_path`: Path to the root of the skills directory.
- `max_results`: Maximum number of skills to return in a search.

## Error Handling

- **Index Missing**: The tool will attempt to rebuild the index if it is out of date or missing.
- **Search Timeout**: Complex regex searches will be limited to 5 seconds.

## Performance Optimization

- **Caching**: The registry index is stored as `registry_index.json` to avoid rescanning on every call.

## Integration Examples

Used by the `find_skill` MCP tool to provide real-time discovery for AI agents.

## Best Practices

- Use specific keywords like "performance", "security", or "refactor" for better matching.

## Troubleshooting

- **No results**: Try removing filters or broadening the query terms.

## Monitoring and Metrics

- **Search Success Rate**: Logs how often a search results in a selected skill.

## Dependencies

- `registry_search.py`: The underlying search engine script.

## Version History

- **1.0.0**: Initial release for Phase 8.

## License

MIT


## Description

The Skill Registry skill provides an automated workflow to address the skill registry provides a centralized mechanism for discovering and searching the agentskills library. it allows agents to find the most relevant skill for a specific task using metadata, tags, and semantic descriptions.. It is designed to be highly modular and integrates seamlessly into larger agentic pipelines.

## Usage Examples

### Basic Usage
'Use skill-registry to analyze my current project context.'

### Advanced Usage
'Run skill-registry with focus on high-priority optimization targets.'

## Input Format

- **Query**: Natural language request or specific target identifier.
- **Context**: (Optional) Relevant file paths or metadata.
- **Options**: Custom parameters for execution depth.

## Output Format

- **Report**: A structured summary of findings and actions.
- **Artifacts**: (Optional) Generated files or updated configurations.
- **Status**: Success/Failure metrics with detailed logs.