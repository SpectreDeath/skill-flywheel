---
Domain: META_SKILL_DISCOVERY
Version: 1.0.0
Type: Process
Category: Library Management
Complexity: Medium
Estimated Execution Time: 30s - 1m
name: skill-proximity-search
---

# SKILL: skill-proximity-search


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Description

Analyzes the semantic relationship between a user request and the available skills in the library, identifying "close-match" skills that might be applicable even if keywords don't match exactly.

## Purpose

Improves skill discovery by going beyond literal keyword matching, helping agents find the most relevant tools for a task.

## Capabilities

1. **Semantic Mapping**: Uses vector embeddings or conceptual proximity to relate tasks to skills.
2. **Threshold Tuning**: Adjusts the strictness of the search to broaden or narrow results.
3. **Cross-Domain Linking**: Identifies relevant skills in unrelated domains.

## Usage Examples

"Find skills similar to `repo-recon` but for data files."

## Input Format

```json
{
  "query": "string",
  "proximity_limit": "float"
}
```

## Output Format

```markdown
### Proximity Search Results
- **Recommended Skill**: [name] (Proximity: 0.95)
- **Rationale**: [text]
```

## Configuration Options

- `include_experimental`: Boolean to search the EXPERIMENTAL folder.

## Constraints

- MUST prioritize verified skills over self-generated variants.

## Examples

### Example 1: Finding an alternative

**Input**: "Database optimization"
**Output**: `query-performance-optimization` and `database-sharding-plan`.

## Error Handling

- **No Matches Found**: Sugests relaxing the `proximity_limit`.

## Performance Optimization

- **Cached Embeddings**: Stores skill summaries in an index for fast lookup.

## Integration Examples

Integrated into the `mcp_server.py` as a fallback for the `find_skill` tool.

## Best Practices

- Use specific technical terms in the query for better accuracy.

## Troubleshooting

- **Irrelevant Matches**: Check the `Domain` filters.

## Monitoring and Metrics

- **Discovery Hit Rate**: Percentage of times a recommended skill is successfully used.

## Dependencies

- `registry_search.py`

## Version History

- 1.0.0: Initial release.

## License

MIT License
