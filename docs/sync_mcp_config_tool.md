# sync_mcp_config Tool Documentation

## Overview

The `sync_mcp_config` tool is a powerful utility within the Discovery Service that automatically synchronizes MCP (Model Context Protocol) configuration files with the current service topology. This tool ensures that your MCP infrastructure remains consistent and up-to-date as your skill registry evolves.

## Purpose

The tool addresses several key challenges in MCP infrastructure management:

1. **Configuration Drift**: Automatically keeps MCP config files in sync with the actual service topology
2. **Service Discovery**: Dynamically maps skills to their appropriate domain services
3. **Infrastructure as Code**: Generates and maintains docker-compose.yml files for containerized deployments
4. **Backup and Recovery**: Creates timestamped backups before making any changes
5. **Validation**: Ensures configuration files are valid and consistent

## Features

### Core Functionality

- **Registry Synchronization**: Reads from `skill_registry.json` and maps skills to domain services
- **Service Configuration**: Generates service definitions for all configured domain services
- **Skill Routing**: Creates routing tables that map skills to their hosting services
- **Docker Compose Generation**: Produces complete docker-compose.yml files for container orchestration
- **Backup Management**: Creates timestamped backups before overwriting existing files

### Safety Mechanisms

- **Atomic Operations**: All file operations are atomic to prevent partial updates
- **Backup Creation**: Automatic backup creation with timestamp suffixes
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Validation**: Validates registry file existence before proceeding

## Usage

### As an MCP Tool

The tool is available as an MCP tool within the Discovery Service:

```python
# The tool is automatically registered with the MCP server
# and can be called by MCP clients

result = await sync_mcp_config()
```

### Command Line Interface

While primarily designed as an MCP tool, the functionality can be tested using the provided test script:

```bash
python test_sync_tool.py
```

## Configuration

### Environment Variables

The tool uses the following environment variables to determine file paths:

- `REGISTRY_FILE`: Path to the skill registry file (default: `/app/skill_registry.json`)
- `MCP_CONFIG_FILE`: Path to the MCP configuration file (default: `/app/mcp_config.json`)
- `DOCKER_COMPOSE_FILE`: Path to the docker-compose.yml file (default: `/app/docker-compose.yml`)

### Service Configuration

The tool uses predefined service groups and port mappings:

```python
SERVICE_GROUPS = {
    "orchestration": ["orchestration", "skill_registry", "SKILL", "META_SKILL_DISCOVERY", "meta_agent_enhancement", "FLOW", "TEMPLATES", "agent_evolution"],
    "security": ["APPLICATION_SECURITY", "security_engineering", "skill_validation", "DEVSECOPS", "forensics", "osint_collector"],
    # ... other service groups
}

DOMAIN_PORT_MAP = {
    "orchestration": 8001,
    "security": 8002,
    "data-ai": 8003,
    # ... other port mappings
}
```

## Output Files

### MCP Configuration (`mcp_config.json`)

The generated MCP configuration includes:

```json
{
  "version": "1.0.0",
  "generated_at": "2026-03-09T17:06:19.123Z",
  "services": {
    "orchestration": {
      "name": "mcp-orchestration",
      "type": "http",
      "url": "http://mcp-orchestration:8001",
      "health_check": "http://mcp-orchestration:8001/health",
      "domains": ["orchestration", "skill_registry", ...],
      "status": "active"
    }
  },
  "skills": {
    "test-skill-1": {
      "service": "orchestration",
      "endpoint": "http://mcp-orchestration:8001",
      "domain": "orchestration",
      "status": "routed"
    }
  },
  "routing": {
    "test-skill-1": {
      "service": "orchestration",
      "endpoint": "http://mcp-orchestration:8001",
      "priority": 1
    }
  }
}
```

### Docker Compose (`docker-compose.yml`)

The generated docker-compose.yml includes:

```yaml
version: "3.8"
services:
  mcp-orchestration:
    image: skill-flywheel/mcp-orchestration:latest
    ports:
      - "8001:8001"
    networks:
      - mcp-network
    environment:
      - PORT=8001
      - REGISTRY_FILE=/app/skill_registry.json
      - MCP_CONFIG_FILE=/app/mcp_config.json
    volumes:
      - "./skill_registry.json:/app/skill_registry.json"
      - "./mcp_config.json:/app/mcp_config.json"
    restart: unless-stopped

  mcp-discovery:
    image: skill-flywheel/mcp-discovery:latest
    ports:
      - "8000:8000"
    networks:
      - mcp-network
    environment:
      - PORT=8000
      - REGISTRY_FILE=/app/skill_registry.json
      - MCP_CONFIG_FILE=/app/mcp_config.json
      - DOCKER_COMPOSE_FILE=/app/docker-compose.yml
    volumes:
      - "./skill_registry.json:/app/skill_registry.json"
      - "./mcp_config.json:/app/mcp_config.json"
      - "./docker-compose.yml:/app/docker-compose.yml"
    restart: unless-stopped

networks:
  mcp-network:
    driver: bridge
```

## Return Values

The tool returns a structured result object:

```python
{
    "status": "success",  # or "error"
    "message": "MCP configuration synchronized successfully",
    "files": {
        "mcp_config": "/app/mcp_config.json",
        "docker_compose": "/app/docker-compose.yml",
        "backup_config": "/app/mcp_config.json.20260309_170619.bak",
        "backup_compose": "/app/docker-compose.yml.20260309_170619.bak"
    },
    "services_configured": 11,
    "skills_routed": 25
}
```

## Error Handling

The tool provides comprehensive error handling:

```python
{
    "status": "error",
    "message": "Failed to synchronize MCP configuration: Registry file not found",
    "error_details": "Registry file not found at /app/skill_registry.json"
}
```

Common error scenarios:

1. **Missing Registry File**: When `skill_registry.json` doesn't exist
2. **File Write Errors**: When unable to write configuration files
3. **YAML Generation Errors**: When docker-compose.yml generation fails
4. **Backup Creation Errors**: When unable to create backup files

## Integration

### With Discovery Service

The tool is automatically registered as an MCP tool when the Discovery Service starts:

```python
@mcp.tool()
async def sync_mcp_config():
    # Implementation
```

### With CI/CD Pipelines

The tool can be integrated into CI/CD pipelines to automatically update MCP configurations:

```yaml
# Example GitHub Actions step
- name: Sync MCP Configuration
  run: |
    python -c "from discovery_service import sync_mcp_config; import asyncio; asyncio.run(sync_mcp_config())"
```

### With Monitoring Systems

The tool's output can be integrated with monitoring systems to track configuration changes:

```python
result = await sync_mcp_config()
if result["status"] == "success":
    # Log successful sync
    logger.info(f"MCP config synced: {result['files']}")
else:
    # Alert on failure
    alert_system.send(f"MCP sync failed: {result['message']}")
```

## Best Practices

1. **Regular Synchronization**: Run the tool regularly to keep configurations in sync
2. **Backup Management**: Implement backup retention policies for generated backup files
3. **Validation**: Always validate the generated configuration files before deployment
4. **Monitoring**: Monitor sync operations for failures or inconsistencies
5. **Testing**: Test configuration changes in development environments before production

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the service has write permissions to the configuration directory
2. **Registry Not Found**: Verify the `REGISTRY_FILE` environment variable points to the correct location
3. **YAML Syntax Errors**: Check the generated docker-compose.yml for syntax issues
4. **Service Conflicts**: Ensure port mappings don't conflict with existing services

### Debugging

Enable debug logging to troubleshoot issues:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Testing

Use the provided test script to validate functionality:

```bash
python test_sync_tool.py
```

## Future Enhancements

Potential future improvements:

1. **Incremental Updates**: Only update changed services/skills
2. **Validation Hooks**: Add custom validation for generated configurations
3. **Rollback Mechanism**: Automatic rollback on deployment failures
4. **Multi-Environment Support**: Support for different environments (dev, staging, prod)
5. **Configuration Templates**: Support for custom docker-compose templates