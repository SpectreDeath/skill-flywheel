# Skill Flywheel

A unified skill registry with 528+ specialized skills for AI agent development.

## 🚀 Quick Start

```bash
# Start the discovery service
uvicorn src.server.discovery_service:app --reload

# Verify status
curl http://localhost:8000/health
```

## 📁 Repository Structure

- `/src/flywheel/core`: Shared logic and specialized core components.
- `/src/flywheel/server`: Discovery service and MCP server.
- `/src/skills/`: Legacy Python skill modules (deprecated - use domains/).
- `/domains`: **Canonical** SKILL.md specifications organized by domain.
- `/data`: SQLite skill registry and JSON indexes.
- `/docs`: Comprehensive documentation index.
- `/tests`: Automated test suites.
- `/skills`: Runtime Python skill modules.

## 📚 Skill Domains

| Domain | Description |
|--------|-------------|
| AI_AGENT_DEVELOPMENT | AI agent frameworks and implementations |
| ALGO_PATTERNS | Algorithm design patterns |
| APPLICATION_SECURITY | Security vulnerability assessment |
| CLOUD_ENGINEERING | Distributed systems |
| COGNITIVE_SKILLS | Thinking and reasoning skills |
| DATABASE_ENGINEERING | Database design and optimization |
| DATA_ENGINEERING | Data pipelines and processing |
| DEVOPS | CI/CD and infrastructure |
| FRONTEND | Frontend development |
| GAME_DEV | Game development |
| ML_AI | Machine learning and AI |
| MCP_TOOLS | Model Context Protocol tools |
| MODEL_ORCHESTRATION | Model routing and selection |
| ORCHESTRATION | Workflow orchestration |
| QUANTUM_COMPUTING | Quantum algorithms |
| SECURITY_ENGINEERING | Security engineering |
| And more... | 24 total domains |

## 🔍 Key Features

- **Single FastAPI Service**: Discovery service runs on port 8000
- **JSON Registry**: Skills indexed in `skill_registry.json` (built from `domains/`)
- **SKILL.md Specs**: Domain-driven specifications in `domains/` (canonical source)
- **Python Modules**: Runtime skills in `skills/` directory

## 📜 License

Licensed under the MIT License.
