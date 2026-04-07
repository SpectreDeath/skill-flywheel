# Skill Flywheel

A unified MCP server with 839+ specialized skills for AI agent development, all running on a single FastAPI service.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Start the unified server
python -m src.flywheel.server.unified_server

# Verify status
curl http://localhost:8000/health
```

## 📁 Repository Structure

- `/src/flywheel/server/unified_server.py`: **Main entry point** — FastAPI server with discovery, execution, and optimization
- `/src/flywheel/core/`: Components (SkillManager, Cache, Telemetry, ML, ResourceOptimizer)
- `/src/flywheel/evolution/`: Darwinian evolution system for skill genome optimization
- `/src/flywheel/skills/`: 839+ Python skill modules across 32 domains
- `/domains/`: SKILL.md specifications organized by domain — source material for skill generation
- `/data/`: SQLite registry (`skill_registry.db`), backlog tracking, and skill index
- `/scripts/`: `scaffold_skill.py` (generate skills), `validate_skill.py` (format checking), `evolution_cli.py` (skill evolution)
- `/docs/`: Architecture and developer documentation
- `/tests/`: Automated test suites (320 tests, all passing)

## 📁 Skill Domains (32)

| Domain | Description |
|--------|-------------|
| discovered | Auto-discovered skills |
| ML_AI | Machine learning and AI |
| AI_AGENT_DEVELOPMENT | AI agent frameworks and implementations |
| agentic_ai | Agentic AI patterns |
| APPLICATION_SECURITY | Security vulnerability assessment |
| DATA_ENGINEERING | Data pipelines and processing |
| orchestration | Workflow orchestration |
| mcp_tools | MCP tool integrations |
| WEB3 | Decentralized finance and layer 2 scaling |
| SPECIFICATION_ENGINEERING | PRD generation, API design |
| GAME_DEV | Game development |
| DATABASE_ENGINEERING | Database architecture and SQL |
| model_orchestration | Model routing and selection |
| CLOUD_ENGINEERING | Distributed systems, Buildroot cross-compilation |
| skill_registry | Skill registry and auto-evolution |
| ARCHIVED | Archived skills |
| skill_validation | Format compliance and naming conventions |
| security_engineering | Security engineering |
| search_algorithms | A*, genetic algorithms, simulated annealing |
| probabilistic_models | Bayesian models and probabilistic programming |
| mobile_development | Cross-platform architecture |
| meta_agent_enhancement | Agent enhancement patterns |
| logic_programming | Logic programming |
| logic | Logic and reasoning |
| formal_methods | Formal verification methods |
| epistemology | Knowledge representation |
| agent_evolution | Agent evolution |
| FRONTEND | Frontend development |
| ALGO_PATTERNS | Algorithm design patterns |
| DEVOPS | CI/CD and infrastructure |
| META_SKILL_DISCOVERY | Skill discovery and indexing |
| QUANTUM_COMPUTING | Quantum algorithms |

## 🔍 Key Features

- **Unified FastAPI Server**: Single port 8000 for discovery, execution, and metrics
- **SQLite Registry**: Skills registered in `data/skill_registry.db`
- **Lazy Loading**: Modules loaded on-demand, cached after 10+ hits
- **ML Optimization**: Predictive loading and resource adaptive scaling
- **Prometheus Telemetry**: Request counters, duration metrics
- **Skill Scaffold**: `scripts/scaffold_skill.py` generates properly formatted skills from CLI args or SKILL.md specs
- **Format Validation**: `scripts/validate_skill.py` checks skills match the required format

## 📖 API Endpoints

### Discovery
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server health |
| `/health` | GET | Detailed health with telemetry status |
| `/skills` | GET | List all skills (filter by domain, paginate) |
| `/skills/search` | GET | Search skills by name/description |
| `/domains` | GET | List domains and skill counts |

### Execution
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/skills/execute` | POST | Execute a skill by name |

### Optimization
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/metrics` | GET | System performance metrics |
| `/skills/optimize` | POST | Trigger ML optimization and predictive preloading |
| `/skills/predict` | GET | Predict usage probability for a skill |
| `/skills/preload` | GET | Get skills recommended for preloading |

### Evolution
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/skills/evolve` | POST | Trigger skill evolution for a group |
| `/skills/evolve/groups` | GET | List available evolvable skill groups |

### Orchestration
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/skills/orchestrate` | POST | Orchestrate multi-agent workflows (AutoGen, LangChain, LangGraph, CrewAI) |

### Security
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/skills/scan` | POST | Scan a skill for security vulnerabilities |
| `/skills/scan/all` | GET | Scan all skills for security vulnerabilities |
| `/security/summary` | GET | Get security monitoring summary |

## 🛠️ Development

### Creating New Skills

```bash
# From CLI
python scripts/scaffold_skill.py my_skill DOMAIN --description "Description"

# From SKILL.md spec
python scripts/scaffold_skill.py --from-spec domains/ML_AI/SKILL.name/SKILL.md

# Validate
python scripts/validate_skill.py src/flywheel/skills --recursive

# Test
python -m pytest tests/ -v
```

## 📜 License

Licensed under the MIT License.
