# Context Hub Provider Skill

## Overview

The Context Hub Provider skill wraps the `chub` CLI tool to provide autonomous skill synthesis capabilities for the Strategy & Analysis domain. This skill enables integration with the context-hub system for managing and analyzing skills within the MCP ecosystem.

## Features

- **Context Hub Integration**: Wraps the `chub` CLI tool for seamless integration
- **Strategy & Analysis Focus**: Specialized for strategy and analysis workflows
- **Autonomous Skill Synthesis**: Create and synthesize new skills based on requirements
- **Context Analysis**: Analyze context data using context-hub capabilities
- **MCP Integration**: Full integration with MCP server v3 infrastructure

## Prerequisites

- Python 3.8 or higher
- `chub` CLI tool installed and accessible
- MCP server v3 infrastructure running

## Installation

1. Ensure the `chub` CLI tool is installed and accessible in your PATH
2. The skill uses only built-in Python modules, no additional dependencies required
3. Register the skill with your MCP server

## Configuration

The skill is configured via `config.json` with the following key settings:

```json
{
  "domain": "strategy_analysis",
  "chub_cli": {
    "search_paths": [
      "chub",
      "/usr/local/bin/chub",
      "/usr/bin/chub",
      "context-hub/cli/chub"
    ]
  },
  "performance": {
    "max_concurrent_operations": 3,
    "cache_results": true,
    "cache_ttl": 300
  }
}
```

## Functions

### get_context_hub_info()
Get information about the context hub system.

**Parameters**: None
**Returns**: System information and status

### list_skills(domain)
List available skills in the context hub.

**Parameters**:
- `domain` (optional): Domain to filter skills (defaults to "strategy_analysis")

**Returns**: List of available skills with metadata

### create_skill(skill_name, skill_description, skill_type)
Create a new skill in the context hub.

**Parameters**:
- `skill_name`: Name of the skill
- `skill_description`: Description of the skill
- `skill_type`: Type of skill (defaults to "analysis")

**Returns**: Creation status and skill details

### analyze_context(context_data)
Analyze context data using the context hub.

**Parameters**:
- `context_data`: Dictionary containing context to analyze

**Returns**: Analysis results and insights

### synthesize_skills(requirements)
Synthesize new skills based on requirements.

**Parameters**:
- `requirements`: List of skill requirements

**Returns**: Synthesized skills and recommendations

## Usage Examples

### Basic Usage

```python
from skills.context_hub_provider.skill import ContextHubProvider

# Initialize the provider
provider = ContextHubProvider()

# Check if chub CLI is available
if provider.is_available():
    # Get context hub information
    info = provider.get_context_hub_info()
    print(f"Context Hub Status: {info}")
    
    # List skills in strategy analysis domain
    skills = provider.list_skills("strategy_analysis")
    print(f"Available Skills: {skills['count']}")
    
    # Create a new skill
    result = provider.create_skill(
        "competitive_analysis",
        "Analyze competitive landscape and market positioning",
        "analysis"
    )
    print(f"Skill Created: {result['status']}")
```

### MCP Integration

```python
from skills.context_hub_provider.skill import execute_function

# Execute functions through MCP
result = execute_function("list_skills", {"domain": "strategy_analysis"})
print(result)

# Analyze context data
context_data = {
    "market_trends": ["AI", "ML", "Automation"],
    "competitors": ["Company A", "Company B"],
    "timeframe": "Q1 2024"
}

analysis = execute_function("analyze_context", {"context_data": context_data})
print(analysis)
```

## Error Handling

The skill includes comprehensive error handling:

- **Timeout Handling**: Configurable timeouts for all operations
- **Retry Logic**: Automatic retries for transient failures
- **Graceful Degradation**: Fallback parsing for non-standard output
- **Input Validation**: Sanitization of all inputs
- **Logging**: Detailed logging for debugging and monitoring

## Performance Considerations

- **Caching**: Results are cached for 5 minutes by default
- **Concurrent Operations**: Maximum 3 concurrent operations
- **Memory Limits**: 256MB memory limit per operation
- **Timeouts**: Configurable timeouts per function

## Security

- **Input Validation**: All inputs are validated and sanitized
- **Shell Command Safety**: No shell commands are executed directly
- **Input Size Limits**: Maximum 1MB input size
- **Output Sanitization**: All outputs are sanitized

## Troubleshooting

### chub CLI Not Found

If the `chub` CLI is not found:

1. Check if `chub` is installed: `chub --version`
2. Verify it's in your PATH
3. Update `config.json` with the correct path
4. Ensure proper permissions

### Permission Errors

If you encounter permission errors:

1. Check file permissions on the `chub` executable
2. Ensure the skill has read/write access to log files
3. Verify MCP server permissions

### Timeout Issues

If operations timeout:

1. Check `chub` CLI responsiveness
2. Increase timeout values in `config.json`
3. Monitor system resources
4. Check network connectivity (if applicable)

## Development

### Testing

Run the skill directly to test functionality:

```bash
cd skills/context_hub_provider
python skill.py
```

### Adding New Functions

To add new functions:

1. Implement the function in `ContextHubProvider` class
2. Add function metadata to `register_skill()`
3. Add function handler to `execute_function()`
4. Update `config.json` with timeouts and retry settings

### Contributing

1. Follow the existing code style and patterns
2. Add comprehensive error handling
3. Include logging for debugging
4. Update documentation for new features
5. Test thoroughly before submitting

## Integration with MCP Server

The skill integrates with MCP server v3 through:

1. **Function Registration**: Automatic registration of available functions
2. **Parameter Validation**: Built-in parameter validation and type checking
3. **Error Reporting**: Structured error reporting for MCP clients
4. **Performance Monitoring**: Built-in performance metrics and monitoring

## License

MIT License - See LICENSE file for details.

## Support

For support and questions:

1. Check the troubleshooting section above
2. Review the logs in `context_hub_provider.log`
3. Verify MCP server configuration
4. Ensure `chub` CLI is properly installed and configured