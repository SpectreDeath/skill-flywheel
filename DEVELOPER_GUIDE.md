# Developer Guide

Welcome to the Skill Flywheel development team! This guide will help you get started with the project.

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Git
- (Optional) OpenAI API key for advanced features

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd skill-flywheel
```

### 2. Create Environment Configuration

```bash
cp .env.example .env
# Edit .env with your actual API keys
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
# Using Docker (recommended)
docker-compose up -d

# Or directly with Python
python -m uvicorn src.server.discovery_service:app --reload
```

### 5. Verify Installation

Visit: http://localhost:8000/health

## Project Structure

```
skill-flywheel/
├── src/
│   ├── core/              # Shared core components
│   │   ├── skills.py      # Skill management
│   │   ├── telemetry.py   # Monitoring & metrics
│   │   └── ...
│   ├── server/            # API servers
│   │   ├── discovery_service.py  # Main API
│   │   └── enhanced_mcp_server_v3.py
│   ├── skills/            # Skill implementations
│   │   ├── *.py          # Individual skills
│   │   └── domain_folders/
│   └── ...
├── domains/               # Skill definitions (SKILL.md)
├── data/                  # Database and models
├── tests/                 # Test suite
└── docs/                 # Documentation
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_mcp_server_fix.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Linting & Type Checking

```bash
# Run Ruff linter
ruff check .

# Run MyPy type checker
mypy src/ --ignore-missing-imports
```

## Common Development Tasks

### Adding a New Skill

1. Create a new Python file in `src/skills/`
2. Implement the skill function with proper docstrings
3. Add `invoke()` and `register_skill()` functions
4. Register the skill in the database (if using SQLite registry)

Example:
```python
def my_skill(param: str) -> dict:
    """Skill description"""
    return {"status": "success", "result": param}

def invoke(payload: dict) -> dict:
    return {"result": my_skill(**payload)}

def register_skill():
    return {
        "name": "my-skill",
        "description": "My new skill",
        "version": "1.0.0",
        "domain": "GENERAL"
    }
```

### Adding a New Domain

1. Create directory: `domains/YOUR_DOMAIN/`
2. Add SKILL.md files for each skill
3. Skills will be auto-discovered

### Database Operations

```bash
# Open SQLite database
sqlite3 data/skill_registry.db

# List tables
.schema

# Query skills
SELECT name, domain, health_status FROM skills LIMIT 10;
```

## Troubleshooting

### Server Won't Start

1. Check if port 8000 is available
2. Verify database exists: `ls data/skill_registry.db`
3. Check logs: `docker-compose logs`

### Import Errors

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=.
```

### Test Failures

```bash
# Run tests with verbose output
pytest tests/ -v --tb=long

# Run specific test
pytest tests/test_mcp_server_fix.py::TestServerConfig::test_default_config -v
```

## Security Notes

- Never commit secrets to version control
- Use `.env` for local development (already in `.gitignore`)
- Run the security scanner before deploying:
  ```bash
  bandit -r src/
  safety check
  ```

## Contributing

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Run linting: `ruff check .`
4. Run tests: `pytest tests/`
5. Commit with conventional commits
6. Push and create PR

## Additional Resources

- [API Documentation](http://localhost:8000/docs)
- [Architecture Overview](README.md)
- [Skill Index](domains/SKILL_INDEX.md)
