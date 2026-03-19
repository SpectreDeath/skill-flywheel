# Skill Flywheel

A unified skill registry with 345+ specialized skills for AI agent development.

## 🚀 Quick Start

```bash
# Start the discovery service
uvicorn src.server.discovery_service:app --reload

# Verify status
curl http://localhost:8000/health
```

## 📁 Repository Structure

- `/src/core`: Shared logic and specialized core components.
- `/src/discovery`: Routing and discovery service.
- `/src/skills/`: Python skill modules organized by domain.
- `/domains`: SKILL.md specifications organized by domain.
- `/data`: SQLite skill registry and backlog.
- `/docs`: Comprehensive documentation index.
- `/tests`: Automated test suites.

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
- **SQLite Registry**: Skills stored in `data/skill_registry.db`
- **Python Modules**: Skills implemented as modules in `src/skills/`
- **SKILL.md Specs**: Domain-driven specifications in `domains/`

## 📜 License

Licensed under the MIT License.
