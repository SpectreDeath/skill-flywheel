# Primordial - Skill Code Generator

Converts archived skill specifications into executable Python code using local LLMs.

## Purpose

The archived skills in Skill Flywheel are excellent knowledge bases but not directly executable. Primordial bridges this gap by:

1. **Parsing** archived SKILL.md files
2. **Extracting** key sections (Purpose, Workflow, Examples, Implementation Notes)
3. **Feeding** to a local LLM (Ollama/LM Studio)
4. **Generating** clean, working Python code

## Installation

```bash
# Requires requests
pip install requests

# Requires local LLM (Ollama recommended)
# ollama pull codellama
```

## Usage

```bash
# Process all archived skills
python run.py

# Process specific domains
python run.py --domains ML_AI AI_AGENT_DEVELOPMENT

# Limit processing
python run.py --limit 10

# Use different model
python run.py --model llama2
```

## Output

Generated skills are saved to `../generated_skills/`:

```
generated_skills/
├── ML_AI/
│   ├── a-coding-guide-to-acp-systems.py
│   └── ...
├── AI_AGENT_DEVELOPMENT/
│   └── ...
└── ...
```

## Requirements

- Local LLM running (Ollama, LM Studio, etc.)
- Python 3.10+
- requests library

## How It Works

1. Parses SKILL.md using regex extraction
2. Builds prompt with skill metadata and requirements
3. Calls local LLM API
4. Extracts code from response
5. Saves as .py file

## Supported LLM APIs

- **Ollama** (localhost:11434) - Default
- **LM Studio** (localhost:1234)
- Any OpenAI-compatible API

Set via `LLM_BASE_URL` environment variable or `--base-url` flag.