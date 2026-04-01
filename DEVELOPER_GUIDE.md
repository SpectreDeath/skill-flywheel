# Skill Flywheel Developer Guide

Welcome to the Skill Flywheel development team! This guide covers contributing to a **unified MCP server** with 531+ skills.

## Architecture Overview

The Skill Flywheel uses a **unified server** — a single FastAPI application (`src/flywheel/server/unified_server.py`) that consolidates:
- **Skill Discovery** (SQLite-backed search and listing)
- **Skill Execution** (dynamic Python module loading)
- **ML Optimization** (predictive loading, resource adaptive scaling)

### Core Components

| Component | Location | Description |
|-----------|----------|-------------|
| EnhancedSkillManager | `src/flywheel/core/skills.py` | Dynamic lazy loading, module caching |
| AdvancedCache | `src/flywheel/core/cache.py` | LRU cache, per-module config |
| TelemetryManager | `src/flywheel/core/telemetry.py` | Prometheus metrics |
| MLModelManager | `src/flywheel/core/ml_models.py` | ML predictions for skill loading |
| ResourceOptimizer | `src/flywheel/core/resource_optimizer.py` | Resource adaptive scaling |
| ContainerManager | `src/flywheel/core/containers.py` | Docker orchestration |

## Prerequisites

- Python 3.11+
- pip or uv
- SQLite (built-in to Python)

## Quick Start

### 1. Clone and Install

```bash
git clone <repository-url>
cd skill-flywheel
pip install -r requirements.txt
```

### 2. Start the Server

```bash
python -m src.flywheel.server.unified_server
```

### 3. Verify Installation

```bash
curl http://localhost:8000/health
```

## Skill Module Requirements

Every skill must follow this format:

```python
#!/usr/bin/env python3
"""Skill description"""

import logging
from datetime import datetime
from typing import Any, Dict

logger = logging.getLogger(__name__)

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "default")
    try:
        # Business logic here
        result = {"status": "success", "data": "..."}
        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in skill_name: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "skill-name",
        "description": "What this skill does",
        "version": "1.0.0",
        "domain": "DOMAIN_NAME",
    }
```

### Key Requirements Checklist

- [x] `async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]`
- [x] `from datetime import datetime` import
- [x] Return format: `{"result": ..., "metadata": {"action": ..., "timestamp": ...}}`
- [x] `try/except` error handling with `logger.error()`
- [x] `register_skill()` function returning metadata

## Creating New Skills

### From Command Line

```bash
python scripts/scaffold_skill.py my_skill DOMAIN --description "What it does" --actions "process:Process data" "analyze:Analyze data"
```

### From SKILL.md Spec

```bash
python scripts/scaffold_skill.py --from-spec domains/ML_AI/SKILL.tutorial-name/SKILL.md
```

### Validate Skills

```bash
python scripts/validate_skill.py src/flywheel/skills --recursive
```

## Running Tests

```bash
# All tests
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_claw_code_skills.py -v

# With coverage
python -m pytest tests/ --cov=src -v
```

## Linting

```bash
ruff check .
python -m mypy src/ --ignore-missing-imports
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server health |
| `/health` | GET | Detailed health with telemetry |
| `/skills` | GET | List skills (filter by domain, paginate) |
| `/skills/search` | GET | Search by name/description/keywords |
| `/domains` | GET | List domains and counts |
| `/skills/execute` | POST | Execute a skill by name |
| `/metrics` | GET | Performance metrics |
| `/skills/optimize` | POST | Run optimization |

## Database

```bash
sqlite3 data/skill_registry.db

# List skills
SELECT name, domain, status FROM skills ORDER BY domain LIMIT 10;

# Search skills
SELECT name, domain FROM skills WHERE name LIKE '%search%';
```

## Pipeline: Spec → Code → Test

1. **Spec** (`domains/`) — SKILL.md defines requirements
2. **Scaffold** (`scripts/scaffold_skill.py`) — Generates Python module
3. **Validate** (`scripts/validate_skill.py`) — Checks format compliance
4. **Implement** — Developer fills in business logic
5. **Test** — pytest tests verify behavior
6. **Register** — Skill added to `data/skill_registry.db`

## Security

- Never commit secrets to version control
- Use `.env` for local development (already in `.gitignore`)
- Run safety checks before deploying:
  ```bash
  pip install safety bandit
  safety check
  bandit -r src/
  ```

## Known Issues

- **Windows junction failures**: Some skills may fail to load on Windows due to symlink/junction issues. This is Windows-specific and resolves on Linux CI.
- **OpenClaw/NemoClaw**: 5 platform-specific modules without `invoke()` — by design, excluded from fix runs.
- **Format compliance**: 94% of skills pass validation (501/531). The remaining 30 have minor issues.

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run linting: `ruff check .`
4. Run tests: `python -m pytest tests/ -v`
5. Validate skills: `python scripts/validate_skill.py src/flywheel/skills --recursive`
6. Commit with conventional commits
7. Push and create PR