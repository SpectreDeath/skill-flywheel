# Quick Start Guide - Enhanced MCP Server

Get up and running with the Enhanced MCP Server in minutes!

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11+
- pip (Python package manager)
- Optional: Docker (for containerized deployment)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd enhanced-mcp-server

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

Copy the example configuration and customize if needed:

```bash
cp mcp_config.yaml mcp_config.yaml
```

For basic usage, no configuration changes are needed. For production, set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### 4. Start the Server

```bash
python enhanced_mcp_server.py
```

The server will start on `http://localhost:8000`

### 5. Verify Installation

Open your browser and visit: http://localhost:8000/health

You should see a JSON response with system health status.

## 🧪 Try It Out

### Test with cURL

```bash
# Health check
curl http://localhost:8000/health

# Discover skills
curl -X POST http://localhost:8000/skills/discover

# Execute a skill
curl -X POST http://localhost:8000/skills/execute \
  -H "Content-Type: application/json" \
  -d '{
    "skill_name": "data_analyzer",
    "args": [],
    "kwargs": {
      "data": [{"value": 1}, {"value": 2}, {"value": 3}],
      "analysis_type": "basic"
    }
  }'
```

### Test with Python

```python
import requests
import json

# Test health check
response = requests.get("http://localhost:8000/health")
print("Health:", response.json())

# Test skill discovery
response = requests.post("http://localhost:8000/skills/discover")
print("Skills:", response.json())

# Test skill execution
payload = {
    "skill_name": "data_analyzer",
    "args": [],
    "kwargs": {
        "data": [{"age": 25, "score": 85}, {"age": 30, "score": 90}],
        "analysis_type": "comprehensive"
    }
}
response = requests.post("http://localhost:8000/skills/execute", json=payload)
print("Skill result:", response.json())
```

### Run the Test Suite

```bash
python test_enhanced_server.py
```

This will run comprehensive tests and show you all the features in action.

## 🐳 Docker Deployment

### Quick Docker Start

```bash
# Build and start all services
docker-compose up -d

# Check if services are running
docker-compose ps

# View logs
docker-compose logs -f enhanced-mcp-server
```

### Docker Services

- **enhanced-mcp-server**: Main application (port 8000)
- **redis**: Caching (port 6379)
- **prometheus**: Metrics (port 9090)
- **grafana**: Dashboards (port 3000, admin/admin)
- **nginx**: Reverse proxy (ports 80/443)

### Access Services

- **API**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📊 Monitoring

### View Metrics

```bash
# Get system metrics
curl http://localhost:8000/metrics
```

### Grafana Dashboards

1. Open http://localhost:3000
2. Login with admin/admin
3. Import dashboards from `monitoring/grafana/dashboards/`

### Prometheus Metrics

Visit http://localhost:9090 to view raw metrics and set up alerts.

## 🤖 Multi-Agent Examples

### Create Your First Agent

```python
import requests

# Create an agent
payload = {
    "agent_id": "my_analyst",
    "role": "Data Analyst",
    "goal": "Analyze data and provide insights",
    "backstory": "Expert in data analysis",
    "tools": [],
    "llm_config": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7
    }
}

response = requests.post("http://localhost:8000/agents/create", json=payload)
print("Agent created:", response.json())
```

### Execute Agent Task

```python
# Execute a task
payload = {
    "agent_id": "my_analyst",
    "task_description": "Analyze this data: [1, 2, 3, 4, 5]",
    "context": {"analysis_type": "basic"}
}

response = requests.post("http://localhost:8000/agents/execute", json=payload)
print("Task result:", response.json())
```

### Create a Crew

```python
# Create a crew
payload = {
    "crew_id": "my_team",
    "agents": ["my_analyst"],
    "process": "sequential"
}

response = requests.post("http://localhost:8000/crews/create", json=payload)
print("Crew created:", response.json())
```

## 🧠 Creating Custom Skills

### 1. Create a Skill File

Create `skills/my_custom_skill.py`:

```python
import logging

logger = logging.getLogger(__name__)

def my_custom_skill(input_data: dict, **kwargs) -> dict:
    """
    Custom skill that processes input data
    
    Args:
        input_data: Input data to process
        **kwargs: Additional parameters
    
    Returns:
        dict: Processing result
    """
    try:
        # Your custom logic here
        result = {
            "processed": True,
            "input": input_data,
            "output": f"Processed: {input_data}",
            "metadata": kwargs
        }
        logger.info(f"Custom skill executed: {result}")
        return result
    except Exception as e:
        logger.error(f"Custom skill failed: {e}")
        return {"error": str(e)}
```

### 2. Discover and Use the Skill

```python
# Discover skills
response = requests.post("http://localhost:8000/skills/discover")
print("Available skills:", response.json())

# Execute your custom skill
payload = {
    "skill_name": "my_custom_skill",
    "args": [],
    "kwargs": {
        "input_data": {"message": "Hello World"},
        "custom_param": "test"
    }
}

response = requests.post("http://localhost:8000/skills/execute", json=payload)
print("Custom skill result:", response.json())
```

## 🔧 Configuration Options

### Basic Configuration

Edit `mcp_config.yaml`:

```yaml
server:
  port: 8000
  debug: false

monitoring:
  enabled: true
  metrics_interval: 60

skills:
  auto_discovery: true
  validation_enabled: true
```

### Environment Variables

```bash
# API Configuration
export OPENAI_API_KEY="your-api-key"
export MCP_JWT_SECRET="your-jwt-secret"

# Server Configuration
export MCP_DEBUG=false
export MCP_HOST=0.0.0.0
export MCP_PORT=8000
```

## 🚨 Troubleshooting

### Server Won't Start

1. **Check Python version**: `python --version` (needs 3.11+)
2. **Check dependencies**: `pip install -r requirements.txt`
3. **Check port availability**: `netstat -an | grep 8000`
4. **Check logs**: Look at console output for error messages

### Docker Issues

1. **Check Docker**: `docker --version`
2. **Check Docker Compose**: `docker-compose --version`
3. **Clean up**: `docker-compose down && docker-compose up -d`
4. **Check logs**: `docker-compose logs enhanced-mcp-server`

### API Not Responding

1. **Check server status**: `curl http://localhost:8000/`
2. **Check health**: `curl http://localhost:8000/health`
3. **Check firewall**: Ensure port 8000 is not blocked
4. **Check configuration**: Verify `mcp_config.yaml`

### Skill Not Found

1. **Check skills directory**: Ensure `skills/` directory exists
2. **Check file naming**: Skill files must be `skill_name.py`
3. **Check function export**: Function must be named after the skill
4. **Rediscover skills**: POST to `/skills/discover`

## 📚 Next Steps

1. **Explore API**: Visit http://localhost:8000/docs for interactive API docs
2. **Create Skills**: Add custom skills to the `skills/` directory
3. **Set up Monitoring**: Configure Grafana dashboards
4. **Production Deployment**: Use Docker Compose for production
5. **Multi-Agent Workflows**: Create complex agent teams
6. **Custom Tools**: Build specialized tools for your use case

## 🆘 Getting Help

- **Documentation**: See `README_ENHANCED_MCP.md`
- **Issues**: Create GitHub issues for bugs
- **Examples**: Check `test_enhanced_server.py` for usage examples
- **Community**: Join our Discord for support

## 🎉 You're Ready!

The Enhanced MCP Server is now running and ready to power your multi-agent applications. Explore the API, create custom skills, and build amazing AI workflows!

---

**Happy Building! 🚀**