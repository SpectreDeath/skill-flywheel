# Skill Flywheel Deployment Guide

## Overview

The Skill Flywheel is a comprehensive AgentSkills ecosystem with 234+ specialized skills across 9 domains, designed to work with MCP (Model Context Protocol) servers for LLM agent enhancement.

## Quick Start

### Option 1: Docker Deployment (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Skill-Flywheel

# Build and start all services
docker compose up -d

# Verify services are running
docker ps
```

### Option 2: Direct Python Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Start individual MCP servers
python src/core/mcp_server.py  # Discovery service
python src/core/mcp_server.py  # Orchestration server
python src/core/mcp_server.py  # Security server
# ... etc for each domain
```

## Architecture

### MCP Server Structure

The ecosystem uses 9 specialized MCP servers:

1. **Discovery Server** (Port 8000) - Skill discovery and indexing
2. **Orchestration Server** (Port 8001) - Multi-skill coordination
3. **Security Server** (Port 8002) - Security and compliance
4. **Data/AI Server** (Port 8003) - ML/AI and data engineering
5. **DevOps Server** (Port 8004) - Infrastructure and deployment
6. **Engineering Server** (Port 8005) - Formal methods and specifications
7. **UX/Mobile Server** (Port 8006) - Frontend and mobile development
8. **Advanced Server** (Port 8007) - Quantum computing and advanced algorithms
9. **Strategy Server** (Port 8008) - Game theory and strategic analysis

### Domain Organization

- **AI_AGENT_DEVELOPMENT** - Agent evolution and enhancement
- **APPLICATION_SECURITY** - Security scanning and compliance
- **CLOUD_ENGINEERING** - Cloud infrastructure and deployment
- **DATA_ENGINEERING** - Data pipelines and ML workflows
- **DEVSECOPS** - Security integration and DevOps
- **EDGE_COMPUTING** - Edge deployment and optimization
- **EPIDEMIOLOGY** - Data analysis and modeling
- **FORENSICS** - Security analysis and investigation
- **GAME_THEORY** - Strategic decision making
- **OSINT_COLLECTOR** - Open source intelligence
- **QUANTUM_COMPUTING** - Quantum algorithms and optimization
- **STRATEGY_ANALYSIS** - Business and technical strategy

## Configuration

### Environment Variables

Each MCP server can be configured with:

```bash
# Server configuration
MCP_SERVER_NAME=OrchestrationServer
PORT=8001
MCP_TRANSPORT=http

# Domain filtering
MCP_DOMAINS=orchestration,skill_registry,META_SKILL_DISCOVERY

# File paths
REGISTRY_FILE=/app/skill_registry.json
SKILLS_DIR=/app/domains
TELEMETRY_LOG=/app/telemetry/usage_log.jsonl
```

### Docker Compose Configuration

The `docker-compose.yml` file defines all services with:

- Port mappings for each domain server
- Volume mounts for skills and telemetry
- Health checks for service monitoring
- Network isolation for security

## Integration with LLM Agents

### MCP Client Setup

```python
from mcp.client import MCPClient

# Connect to the discovery server
client = MCPClient("http://localhost:8000")

# Discover available skills
skills = client.list_tools()

# Execute a skill
result = client.call_tool("skill_repo_recon", {"repository_path": "/path/to/repo"})
```

### Agent Integration Examples

#### Claude Code Integration

```yaml
# .claude/commands/skill_flywheel.yaml
name: skill_flywheel
description: Execute AgentSkills from the Skill Flywheel
mcpServers:
  discovery:
    url: http://localhost:8000
  orchestration:
    url: http://localhost:8001
  security:
    url: http://localhost:8002
```

#### Cursor IDE Integration

```json
// .cursor/rules/mcp_config.json
{
  "mcpServers": {
    "discovery": {
      "url": "http://localhost:8000"
    },
    "orchestration": {
      "url": "http://localhost:8001"
    }
  }
}
```

## Monitoring and Telemetry

### Telemetry Collection

The system automatically collects:

- Skill execution metrics
- Performance data
- Error rates and patterns
- Usage statistics

### Monitoring Dashboard

```bash
# View telemetry logs
tail -f telemetry/usage_log.jsonl

# Monitor service health
docker compose ps

# Check service logs
docker compose logs -f
```

## Troubleshooting

### Common Issues

1. **Docker Desktop not running**
   ```bash
   # Start Docker Desktop
   net start com.docker.service
   ```

2. **Port conflicts**
   ```bash
   # Check port usage
   netstat -an | grep 8000
   
   # Change ports in docker-compose.yml
   ```

3. **Missing skill registry**
   ```bash
   # Rebuild the registry
   python docs/audit/reindex_skills.py
   ```

### Debug Mode

```bash
# Enable debug logging
export DEBUG=1
docker compose up

# View detailed logs
docker compose logs --tail=100 -f
```

## Security Considerations

### Network Security

- Use HTTPS for production deployments
- Implement authentication for MCP endpoints
- Use network isolation between services

### Data Security

- Encrypt telemetry data at rest
- Implement access controls for skill execution
- Regular security audits of skill content

### Compliance

- Follow SOC 2 Type II requirements
- Implement data retention policies
- Regular vulnerability assessments

## Performance Optimization

### Caching Strategies

- Implement skill result caching
- Use CDN for static skill content
- Optimize skill registry queries

### Scaling

- Use load balancers for high traffic
- Implement horizontal scaling for MCP servers
- Monitor resource usage and scale accordingly

## Development Workflow

### Adding New Skills

1. Create skill directory in appropriate domain
2. Write SKILL.md following the template
3. Update skill registry
4. Test with MCP server
5. Deploy to production

### Testing Skills

```bash
# Run skill tests
python -m pytest tests/

# Validate skill format
python docs/audit/skill-spec-validator.py

# Test MCP integration
python tests/test_mcp_integration.py
```

## Production Deployment

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-flywheel
spec:
  replicas: 3
  selector:
    matchLabels:
      app: skill-flywheel
  template:
    metadata:
      labels:
        app: skill-flywheel
    spec:
      containers:
      - name: discovery
        image: skillflywheel/discovery:latest
        ports:
        - containerPort: 8000
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Skill Flywheel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build and deploy
      run: |
        docker compose build
        docker compose push
        kubectl apply -f k8s/
```

## Support and Maintenance

### Regular Maintenance

- Update skill content regularly
- Monitor service health
- Review and update security configurations
- Optimize performance based on usage patterns

### Support Channels

- Documentation: docs/
- Issues: GitHub Issues
- Community: Discord/Slack channels
- Email: support@skillflywheel.com

## Conclusion

The Skill Flywheel provides a robust, scalable platform for enhancing LLM agents with specialized skills. Whether deploying locally for development or in production with Kubernetes, the system offers comprehensive tooling for skill management, execution, and monitoring.

For more information, see the individual domain documentation and implementation guides in the docs/ directory.