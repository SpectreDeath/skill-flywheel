#!/usr/bin/env python3
r"""
Generate Skill Flywheel skills from the AI Tutorial library.

Scans D:\GitHub\AI-Tutorial-Codes-Included-main, categorizes each tutorial,
and produces a SKILL.md file under the appropriate domain directory.
"""

import re
import textwrap
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
TUTORIAL_ROOT = Path(r"D:\GitHub\AI-Tutorial-Codes-Included-main")
WORKSPACE_ROOT = Path(__file__).parent.parent.parent
DOMAINS_DIR = WORKSPACE_ROOT / "domains"

# ── Category → Domain mapping ─────────────────────────────────────────────
CATEGORY_DOMAIN_MAP = {
    "AI Agents Codes": "AI_AGENT_DEVELOPMENT",
    "Agentic AI Codes": "agentic_ai",
    "Agentic Workflows": "agentic_ai",
    "Agentic AI Memory": "agentic_ai",
    "Agent Communication Protocol": "mcp_tools",
    "MCP Codes": "mcp_tools",
    "MCP_Tutorial_Server": "mcp_tools",
    "RAG": "ML_AI",
    "Computer Vision": "ML_AI",
    "Deep Learning": "ML_AI",
    "LLM Projects": "ML_AI",
    "LLM Evaluation": "ML_AI",
    "MLFlow for LLM Evaluation": "ML_AI",
    "Reinforcement learning": "ML_AI",
    "Federated Learning": "ML_AI",
    "Voice AI": "ML_AI",
    "Prompt Optimization": "ML_AI",
    "Robotics": "ML_AI",
    "Data Science": "DATA_ENGINEERING",
    "Distributed Systems": "CLOUD_ENGINEERING",
    "Security": "APPLICATION_SECURITY",
    "Adversarial Attacks": "APPLICATION_SECURITY",
    "Quantum Computing": "QUANTUM_COMPUTING",
    "GPT-5": "ML_AI",
    "SHAP-IQ": "ML_AI",
    "Mirascope": "ML_AI",
    "MiniMax": "ML_AI",
    "OAuth 2.1 for MCP Servers": "APPLICATION_SECURITY",
    "A2A_Simple_Agent": "AI_AGENT_DEVELOPMENT",
}

# Domain for standalone files in the root of the tutorial repo
STANDALONE_DOMAIN_KEYWORDS = {
    "agent": "AI_AGENT_DEVELOPMENT",
    "agentic": "agentic_ai",
    "mcp": "mcp_tools",
    "rag": "ML_AI",
    "llm": "ML_AI",
    "gemini": "ML_AI",
    "security": "APPLICATION_SECURITY",
    "scrape": "DATA_ENGINEERING",
    "data": "DATA_ENGINEERING",
    "quantum": "QUANTUM_COMPUTING",
    "voice": "ML_AI",
    "speech": "ML_AI",
    "crew": "agentic_ai",
    "langgraph": "agentic_ai",
    "langchain": "ML_AI",
    "autogen": "AI_AGENT_DEVELOPMENT",
    "mistral": "ML_AI",
    "graph": "ML_AI",
    "research": "ML_AI",
    "workflow": "agentic_ai",
}


# ── Complexity heuristics ──────────────────────────────────────────────────
def estimate_complexity(file_size_bytes: int) -> str:
    if file_size_bytes < 15000:
        return "Medium"
    elif file_size_bytes < 60000:
        return "High"
    return "Very High"


# ── Name helpers ───────────────────────────────────────────────────────────
def filename_to_skill_name(filename: str) -> str:
    """Convert a filename like 'Advanced_PEER_MultiAgent_Tutorial_Marktechpost.ipynb' to 'advanced-peer-multiagent-tutorial'."""
    name = Path(filename).stem
    # Strip common suffixes
    for suffix in ["_Marktechpost", "_marktechpost", "_Marktechpost2", " (1)", " (2)"]:
        name = name.replace(suffix, "")
    # Convert to kebab-case
    name = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-").lower()
    # Collapse repeated hyphens
    name = re.sub(r"-+", "-", name)
    return name


def filename_to_title(filename: str) -> str:
    """Convert a filename to a human-readable title."""
    name = Path(filename).stem
    for suffix in ["_Marktechpost", "_marktechpost", "_Marktechpost2", " (1)", " (2)"]:
        name = name.replace(suffix, "")
    # Replace underscores with spaces
    name = name.replace("_", " ").replace("-", " ")
    # Title-case
    return name.strip()


def infer_domain_for_standalone(filename: str) -> str:
    """Infer domain for standalone files based on keyword matching."""
    lower = filename.lower()
    for keyword, domain in STANDALONE_DOMAIN_KEYWORDS.items():
        if keyword in lower:
            return domain
    return "ML_AI"  # Default


def extract_category_from_title(title: str) -> str:
    """Extract a short category label from the title."""
    lower = title.lower()
    if "rag" in lower or "retrieval" in lower:
        return "Retrieval Augmented Generation"
    if "agent" in lower and "multi" in lower:
        return "Multi-Agent Systems"
    if "agent" in lower:
        return "AI Agents"
    if "memory" in lower:
        return "Agent Memory"
    if "mcp" in lower or "model context protocol" in lower:
        return "Model Context Protocol"
    if "security" in lower or "adversarial" in lower or "attack" in lower:
        return "AI Security"
    if "workflow" in lower:
        return "Agentic Workflows"
    if "vision" in lower or "cnn" in lower or "image" in lower:
        return "Computer Vision"
    if "voice" in lower or "speech" in lower:
        return "Voice AI"
    if "quantum" in lower:
        return "Quantum Computing"
    if "reinforcement" in lower or "rl " in lower:
        return "Reinforcement Learning"
    if "federated" in lower:
        return "Federated Learning"
    if "distributed" in lower:
        return "Distributed Systems"
    if "data" in lower or "dashboard" in lower or "analytics" in lower:
        return "Data Engineering"
    if "llm" in lower or "language model" in lower:
        return "Large Language Models"
    if "deep learning" in lower or "transformer" in lower:
        return "Deep Learning"
    return "AI/ML Engineering"


# ── Skill content generation ──────────────────────────────────────────────
def generate_skill_content(
    skill_name: str,
    title: str,
    domain: str,
    category: str,
    complexity: str,
    source_file: str,
    source_category: str,
) -> str:
    """Generate a complete SKILL.md from tutorial metadata."""

    # Build implementation notes based on file type
    file_ext = Path(source_file).suffix
    if file_ext == ".ipynb":
        impl_type = "Jupyter Notebook tutorial"
        deps = "Jupyter, Python 3.10+, and domain-specific libraries (see notebook imports)"
    else:
        impl_type = "Python script tutorial"
        deps = "Python 3.10+ and domain-specific libraries (see script imports)"

    content = textwrap.dedent(f"""\
    ---
    Domain: {domain}
    Version: 1.0.0
    Complexity: {complexity}
    Type: Tutorial
    Category: {category}
    name: {skill_name}
    Source: AI-Tutorial-Codes-Included
    Source_File: {source_file}
    ---

    ## Purpose

    Teaches agents how to implement {title} patterns and techniques. Derived from a production-grade {impl_type} covering real-world {category.lower()} implementation strategies.

    ## Description

    This skill encapsulates the knowledge and implementation patterns from the "{title}" tutorial. It provides a structured guide for building, configuring, and deploying {category.lower()} solutions. The tutorial source covers end-to-end implementation with working code examples, making this skill immediately actionable for agent-driven development.

    ## Workflow

    1. **Understand Requirements**: Analyze the target use case and determine which {category.lower()} patterns apply.
    2. **Environment Setup**: Install required dependencies and configure the development environment.
    3. **Core Implementation**: Follow the tutorial's step-by-step implementation to build the primary components.
    4. **Integration**: Connect the implementation with existing systems and services.
    5. **Testing & Validation**: Verify the implementation against expected outputs and edge cases.
    6. **Optimization**: Apply performance tuning and resource optimization techniques from the tutorial.

    ## Examples

    ### Example 1: Basic Implementation
    **Input**: A request to implement {title.lower()} from scratch.
    **Output**: A working implementation following the tutorial's architecture and best practices.
    **Use Case**: When an agent needs to build a new {category.lower()} component for a project.

    ### Example 2: Integration with Existing System
    **Input**: An existing codebase that needs {category.lower()} capabilities added.
    **Output**: Modified codebase with the tutorial's patterns integrated and tested.
    **Use Case**: When extending an existing system with new {category.lower()} features.

    ### Example 3: Debugging & Troubleshooting
    **Input**: A broken or underperforming {category.lower()} implementation.
    **Output**: Diagnosed issues and applied fixes based on the tutorial's error handling patterns.
    **Use Case**: When an agent encounters failures in {category.lower()} workflows.

    ## Implementation Notes

    - **Source**: `{source_file}` from the AI-Tutorial-Codes-Included library
    - **Type**: {impl_type}
    - **Dependencies**: {deps}
    - **Category Source**: {source_category}
    - Follow the tutorial's import structure exactly to avoid dependency conflicts
    - Pay attention to API key and credential management patterns in the source
    - The tutorial may reference external services; ensure connectivity before execution
    - Review the tutorial's error handling patterns for production hardening

    ## Constraints

    - **MUST** install all dependencies listed in the tutorial before execution
    - **MUST** handle API keys and secrets via environment variables, never hardcode
    - **MUST** validate all external service connections before initiating workflows
    - **NEVER** skip the testing and validation steps outlined in the tutorial
    - **SHOULD** adapt the tutorial's examples to the specific project context
    - **MUST NOT** expose sensitive data in logs or outputs during execution
    """)
    return content


# ── Main generation logic ─────────────────────────────────────────────────
def collect_tutorials() -> list:
    """Walk the tutorial library and collect all tutorial files with metadata."""
    tutorials = []

    for item in sorted(TUTORIAL_ROOT.iterdir()):
        if item.name.startswith(".") or item.name == "README.md":
            continue

        if item.is_dir():
            category_name = item.name
            domain = CATEGORY_DOMAIN_MAP.get(category_name)
            if not domain:
                # Try keyword inference
                domain = infer_domain_for_standalone(category_name)

            for sub_item in sorted(item.rglob("*")):
                if sub_item.suffix in (
                    ".ipynb",
                    ".py",
                ) and not sub_item.name.startswith("."):
                    tutorials.append(
                        {
                            "file": sub_item,
                            "category": category_name,
                            "domain": domain,
                            "size": sub_item.stat().st_size,
                        }
                    )

        elif item.suffix in (".ipynb", ".py"):
            domain = infer_domain_for_standalone(item.name)
            tutorials.append(
                {
                    "file": item,
                    "category": "Standalone",
                    "domain": domain,
                    "size": item.stat().st_size,
                }
            )

    return tutorials


def generate_all_skills():
    """Generate SKILL.md files for all tutorials."""
    tutorials = collect_tutorials()
    print(f"Discovered {len(tutorials)} tutorial files.")

    generated = 0
    skipped = 0
    seen_names = set()

    for tut in tutorials:
        skill_name = filename_to_skill_name(tut["file"].name)

        # De-duplicate names
        if skill_name in seen_names:
            skipped += 1
            continue
        seen_names.add(skill_name)

        title = filename_to_title(tut["file"].name)
        domain = tut["domain"]
        category = extract_category_from_title(title)
        complexity = estimate_complexity(tut["size"])
        source_file = tut["file"].name
        source_category = tut["category"]

        # Create the skill directory
        skill_dir = DOMAINS_DIR / domain / f"SKILL.{skill_name}"
        skill_dir.mkdir(parents=True, exist_ok=True)
        skill_path = skill_dir / "SKILL.md"

        # Don't overwrite existing skills
        if skill_path.exists():
            skipped += 1
            continue

        content = generate_skill_content(
            skill_name,
            title,
            domain,
            category,
            complexity,
            source_file,
            source_category,
        )

        with open(skill_path, "w", encoding="utf-8") as f:
            f.write(content)

        generated += 1
        print(f"  [{generated:3d}] {domain}/{skill_name}")

    print(
        f"\nGeneration complete: {generated} skills created, {skipped} skipped (duplicates or existing)."
    )
    return generated


if __name__ == "__main__":
    generate_all_skills()
