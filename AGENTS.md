# Skill Flywheel - Agent Instructions

This file provides context for AI agents working on the Skill Flywheel project.

## Project Overview

- **Version**: MCP Server v3 unified
- **Skills**: 839+ specialized skills across 32 domains
- **Architecture**: FastAPI with lazy loading

## Key Commands

`ash
# Start server
python -m src.flywheel.server.unified_server

# Find orphaned skills
python scripts/find_orphaned_skills.py

# Validate skills
python scripts/validate_skill.py src/flywheel/skills/<domain>/

# Scaffold new skill
python scripts/scaffold_skill.py <skill-name> <domain>
`

## Important Notes

- Skills are in src/flywheel/skills/<domain>/
- Skill specs are in domains/<domain>/
- Always run validate_skill.py after creating new skills
- Use find_orphaned_skills.py to find skills needing implementations

## Code Style

- Run ruff check before committing
- Target Python 3.11+
- Use async/await pattern for skills
