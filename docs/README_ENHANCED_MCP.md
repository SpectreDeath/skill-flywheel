# Enhanced MCP Server with Advanced Features

A production-ready Multi-Agent Orchestration Server built with FastAPI, LangChain, and CrewAI, featuring advanced performance monitoring, skill lifecycle management, and multi-agent orchestration capabilities.

## 🚀 Features

### Core Capabilities
- **Multi-Agent Orchestration**: Create and manage teams of AI agents with LangChain and CrewAI
- **Advanced Performance Monitoring**: Real-time system metrics, agent performance tracking, and health checks
- **Skill Lifecycle Management**: Auto-discovery, validation, and execution of modular skills
- **Production Deployment**: Docker support, monitoring stack, and production configuration
- **Enhanced Configuration**: YAML-based configuration with validation and environment variable support

### Advanced Features
- **Real-time Telemetry**: System metrics collection with CPU, memory, GPU, and network monitoring
- **Agent Metrics Tracking**: Success rates, execution times, and error tracking for each agent
- **Skill Auto-Discovery**: Automatic detection and loading of skills from the skills directory
- **Rate Limiting & Retry Logic**: Built-in protection against API limits and transient failures
- **Health Monitoring**: Comprehensive health checks with configurable thresholds
- **Batch API Operations**: Concurrent API calls with rate limiting and error handling
- **Data Transformation**: Flexible data mapping and transformation utilities

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Skills System](#skills-system)
- [Multi-Agent Orchestration](#multi-agent-orchestration)
- [Monitoring & Telemetry](#monitoring--telemetry)
- [Production Deployment](#production-deployment)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Docker (for containerized deployment)
- OpenAI API key (for LLM functionality)

### Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd enhanced-mcp-server
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the server**
```bash
python enhanced_mcp_server.py
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up -d
```

2. **Access the server**
- API: http://localhost:8000
- Health Check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics

## ⚙️ Configuration

The server uses a YAML configuration file (`mcp_config.yaml`) with the following sections:

### Server Configuration
```yaml
server:
  host: "0.0.0.0"
  port: 8000
  debug: false
  cors_origins: ["*"]
  max_concurrent_requests: 100
  request_timeout: 300
```

### Monitoring Configuration
```yaml
monitoring:
  enabled: true
  metrics_interval: 60
  log_level: "INFO"
  performance_thresholds:
    cpu_warning: 80.0
    memory_warning: 80.0
    response_time_warning: 5.0
```

### Agent Configuration
```yaml
agents:
  max_agents: 50
  agent_timeout: 300
  retry_attempts: 3
  parallel_execution: true
  default_llm:
    model: "gpt-3.5-turbo"
    temperature: 0.7
    max_tokens: 2000
```

### Skills Configuration
```yaml
skills:
  auto_discovery: true
  validation_enabled: true
  cache_ttl: 3600
  max_skill_size: 1048576
  skills_directory: "skills"
```

## 📚 API Reference

### Health Check
```http
GET /health
```
Returns system health status and performance metrics.

### Metrics
```http
GET /metrics
```
Returns detailed performance metrics including system stats and agent metrics.

### Skills Management

#### Discover Skills
```http
POST /skills/discover
```
Auto-discovers available skills in the skills directory.

#### Execute Skill
```http
POST /skills/execute
Content-Type: application/json

{
  "skill_name": "data_analyzer",
  "args": [],
  "kwargs": {
    "data": [...],
    "analysis_type": "comprehensive"
  }
}
```

### Agent Management

#### Create Agent
```http
POST /agents/create
Content-Type: application/json

{
  "agent_id": "data_analyst",
  "role": "Data Analyst",
  "goal": "Analyze datasets and provide insights",
  "backstory": "Expert in statistical analysis and data visualization",
  "tools": [],
  "llm_config": {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7
  }
}
```

#### Execute Agent Task
```http
POST /agents/execute
Content-Type: application/json

{
  "agent_id": "data_analyst",
  "task_description": "Analyze the sales data and identify trends",
  "context": {
    "dataset": "sales_data.csv",
    "time_period": "Q1 2024"
  }
}
```

### Crew Management

#### Create Crew
```http
POST /crews/create
Content-Type: application/json

{
  "crew_id": "analytics_team",
  "agents": ["data_analyst", "business_analyst"],
  "process": "sequential"
}
```

#### Execute Crew Task
```http
POST /crews/execute
Content-Type: application/json

{
  "crew_id": "analytics_team",
  "task_description": "Perform comprehensive business analysis",
  "context": {
    "business_domain": "e-commerce",
    "analysis_period": "last_6_months"
  }
}
```

## 🧠 Skills System

### Creating Custom Skills

Skills are Python modules placed in the `skills/` directory. Each skill should:

1. **Follow the naming convention**: `skill_name.py`
2. **Export functions**: Functions should be named after the skill
3. **Handle errors gracefully**: Use try-catch blocks for error handling
4. **Return structured data**: Use dictionaries for complex results

### Example Skill
```python
# skills/my_skill.py
import logging

logger = logging.getLogger(__name__)

def my_skill(input_data: dict, **kwargs) -> dict:
    """
    Example skill function
    
    Args:
        input_data: Input data for the skill
        **kwargs: Additional parameters
    
    Returns:
        dict: Processed result
    """
    try:
        # Process input data
        result = {
            "processed": True,
            "data": input_data,
            "metadata": kwargs
        }
        logger.info(f"Skill executed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Skill execution failed: {e}")
        return {"error": str(e)}
```

### Skill Validation

The server automatically validates skills by:
- Checking file existence and readability
- Verifying function exports
- Testing basic execution with sample data
- Monitoring execution time and success rates

## 🤖 Multi-Agent Orchestration

### Agent Creation

Agents are created with specific roles, goals, and capabilities:

```python
from enhanced_mcp_server import AgentOrchestrator

orchestrator = AgentOrchestrator(config)

# Create specialized agents
data_agent = orchestrator.create_agent(
    agent_id="data_specialist",
    role="Data Specialist",
    goal="Process and analyze data",
    backstory="Expert in data analysis and machine learning",
    tools=[data_analyzer_tool],
    llm_config={
        "model": "gpt-4",
        "temperature": 0.3
    }
)
```

### Crew Formation

Crews combine multiple agents for complex tasks:

```python
# Create a crew
analytics_crew = orchestrator.create_crew(
    crew_id="analytics_crew",
    agents=["data_specialist", "business_analyst", "report_writer"],
    process="hierarchical"  # or "sequential"
)

# Execute complex task
result = await orchestrator.execute_crew_task(
    crew_id="analytics_crew",
    task_description="Generate quarterly business report",
    context={
        "data_source": "sales_database",
        "report_format": "executive_summary"
    }
)
```

### Process Types

- **Sequential**: Agents work in sequence, passing results to the next agent
- **Hierarchical**: One agent coordinates others, suitable for complex multi-step tasks

## 📊 Monitoring & Telemetry

### System Metrics

The server collects comprehensive system metrics:
- CPU usage and load
- Memory consumption
- Disk usage
- GPU utilization (if available)
- Network connections
- Request/response statistics

### Agent Metrics

Track agent performance:
- Execution time and success rates
- Error counts and patterns
- Resource utilization per agent
- Historical performance trends

### Health Monitoring

Configurable health thresholds:
- CPU usage warnings
- Memory usage warnings
- Response time degradation
- Error rate increases

### Metrics Export

Metrics can be exported to:
- Prometheus (for Grafana dashboards)
- Custom telemetry endpoints
- Log files for analysis

## 🚢 Production Deployment

### Docker Compose Stack

The provided `docker-compose.yml` includes:
- **Enhanced MCP Server**: Main application container
- **Redis**: Caching and session storage
- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Nginx**: Reverse proxy and SSL termination

### Environment Variables

Key environment variables for production:

```bash
# API Configuration
OPENAI_API_KEY=your_openai_key
MCP_JWT_SECRET=your_jwt_secret

# Server Configuration
MCP_DEBUG=false
MCP_HOST=0.0.0.0
MCP_PORT=8000

# Monitoring
MCP_METRICS_ENABLED=true
MCP_TELEMETRY_ENDPOINT=https://your-telemetry-endpoint.com
```

### Production Best Practices

1. **Security**:
   - Use HTTPS with valid SSL certificates
   - Set strong JWT secrets
   - Implement rate limiting
   - Use environment variables for secrets

2. **Performance**:
   - Configure appropriate worker counts
   - Set up Redis for caching
   - Monitor resource usage
   - Use load balancing for high traffic

3. **Monitoring**:
   - Set up Grafana dashboards
   - Configure alerting rules
   - Monitor error rates and response times
   - Track agent performance metrics

4. **Scaling**:
   - Use horizontal scaling with multiple containers
   - Implement database connection pooling
   - Configure proper resource limits
   - Use service discovery for agent coordination

## 📖 Examples

### Basic Usage

```python
import asyncio
from enhanced_mcp_server import EnhancedMCPServer

async def main():
    # Start server
    server = EnhancedMCPServer()
    
    # Create an agent
    await server.create_agent(
        agent_id="test_agent",
        role="Test Agent",
        goal="Test agent functionality",
        backstory="Simple test agent",
        tools=[]
    )
    
    # Execute a task
    result = await server.execute_agent_task(
        agent_id="test_agent",
        task_description="Say hello world"
    )
    
    print(f"Agent result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Multi-Agent Workflow

```python
import asyncio
from enhanced_mcp_server import EnhancedMCPServer

async def multi_agent_workflow():
    server = EnhancedMCPServer()
    
    # Create specialized agents
    agents = [
        {
            "agent_id": "researcher",
            "role": "Research Agent",
            "goal": "Gather information",
            "backstory": "Expert researcher"
        },
        {
            "agent_id": "analyst",
            "role": "Analysis Agent", 
            "goal": "Analyze gathered data",
            "backstory": "Data analysis expert"
        },
        {
            "agent_id": "reporter",
            "role": "Reporting Agent",
            "goal": "Generate reports",
            "backstory": "Report generation specialist"
        }
    ]
    
    # Create agents
    for agent_config in agents:
        await server.create_agent(**agent_config)
    
    # Create crew
    await server.create_crew(
        crew_id="research_team",
        agents=["researcher", "analyst", "reporter"],
        process="sequential"
    )
    
    # Execute complex task
    result = await server.execute_crew_task(
        crew_id="research_team",
        task_description="Research market trends and generate report"
    )
    
    print(f"Research result: {result}")

if __name__ == "__main__":
    asyncio.run(multi_agent_workflow())
```

### Skill Integration

```python
import asyncio
from enhanced_mcp_server import EnhancedMCPServer

async def skill_integration():
    server = EnhancedMCPServer()
    
    # Discover available skills
    skills = await server.discover_skills()
    print(f"Available skills: {skills}")
    
    # Execute a skill
    result = await server.execute_skill(
        skill_name="data_analyzer",
        args=[],
        kwargs={
            "data": sample_data,
            "analysis_type": "comprehensive"
        }
    )
    
    print(f"Skill result: {result}")

if __name__ == "__main__":
    asyncio.run(skill_integration())
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make changes and add tests**
4. **Run linting and formatting**: `black . && flake8`
5. **Test your changes**: `pytest`
6. **Commit your changes**: `git commit -am 'Add feature'`
7. **Push to the branch**: `git push origin feature-name`
8. **Create a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team**: For the excellent framework for building LLM applications
- **CrewAI Team**: For the powerful multi-agent orchestration capabilities
- **FastAPI Team**: For the modern, fast web framework
- **OpenAI**: For the powerful language models that make this possible

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Join our Discord community
- Email us at support@example.com

## 🔗 Related Projects

- [LangChain](https://github.com/langchain-ai/langchain)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [MCP Protocol](https://github.com/modelcontextprotocol)

---

**Built with ❤️ by the Enhanced MCP Team**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-2496ED?logo=docker)](https://www.docker.com/)