#!/usr/bin/env python3
"""Primordial - Skill Code Generator.

Turns archived skill specifications into executable code using local LLMs.
"""

import argparse
import json
import logging
import re
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Primordial:
    """Generate executable code from archived skill specifications."""

    PROMPT_TEMPLATE = """You are an expert Python developer. Generate working Python code from this skill specification.

## Name
{name}

## Description
{description}

## Purpose
{purpose}

## Workflow
{workflow}

## Examples
{examples}

## Implementation Notes
{implementation_notes}

## Constraints
{constraints}

Generate clean, working Python code that implements this skill. Include:
- Proper imports
- Class/function definitions
- Error handling
- Type hints
- Docstrings matching the skill purpose

Return ONLY Python code wrapped in ```python code blocks. Nothing else."""

    def __init__(self, archive_dir: str, output_dir: str, llm_model: str = "codellama"):
        self.archive_dir = Path(archive_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.llm_model = llm_model
        self._init_llm()

    def _init_llm(self):
        """Initialize local LLM client."""
        from .local_llm_client import LocalLLMClient

        self.llm = LocalLLMClient(model=self.llm_model)
        logger.info(f"Initialized LLM: {self.llm_model}")

    def extract_section(self, content: str, section: str) -> str:
        """Extract a section from skill markdown."""
        pattern = rf"## {section}\s*\n(.*?)(?=## |\Z)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def parse_skill(self, skill_path: Path) -> dict[str, Any]:
        """Parse a skill file into structured data."""
        content = skill_path.read_text(encoding="utf-8")

        # Extract frontmatter
        name = ""
        description = ""
        for line in content.split("\n"):
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            if line.startswith("description:"):
                description = line.split(":", 1)[1].strip()
                break

        return {
            "name": name or skill_path.parent.name,
            "description": description,
            "purpose": self.extract_section(content, "Purpose"),
            "workflow": self.extract_section(content, "Workflow"),
            "examples": self.extract_section(content, "Examples"),
            "implementation_notes": self.extract_section(
                content, "Implementation Notes"
            ),
            "constraints": self.extract_section(content, "Constraints"),
            "content": content,
        }

    def build_prompt(self, skill_data: dict[str, Any]) -> str:
        """Build generation prompt from skill data."""
        return self.PROMPT_TEMPLATE.format(
            name=skill_data.get("name", "Unknown"),
            description=skill_data.get("description", ""),
            purpose=skill_data.get("purpose", ""),
            workflow=skill_data.get("workflow", ""),
            examples=skill_data.get("examples", ""),
            implementation_notes=skill_data.get("implementation_notes", ""),
            constraints=skill_data.get("constraints", ""),
        )

    def generate(self, skill_path: Path) -> str | None:
        """Generate code for a single skill."""
        logger.info(f"Processing: {skill_path.parent.name}")

        skill_data = self.parse_skill(skill_path)
        prompt = self.build_prompt(skill_data)

        try:
            response = self.llm.generate(prompt)
            return self._extract_code(response)
        except Exception as e:
            logger.error(f"Failed to generate: {e}")
            return None

    def _extract_code(self, response: str) -> str | None:
        """Extract code block from LLM response."""
        match = re.search(r"```python\n(.*?)```", response, re.DOTALL)
        return match.group(1).strip() if match else response

    def process_archive(self, domains: list[str] | None = None) -> int:
        """Process all archived skills."""
        processed = 0

        for domain_dir in self.archive_dir.iterdir():
            if not domain_dir.is_dir():
                continue
            if domains and domain_dir.name not in domains:
                continue
            if domain_dir.name.startswith("ARCHIVED"):
                continue

            output_domain = self.output_dir / domain_dir.name
            output_domain.mkdir(exist_ok=True)

            for skill_dir in domain_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    continue

                code = self.generate(skill_file)
                if code:
                    output_file = output_domain / f"{skill_dir.name}.py"
                    output_file.write_text(code, encoding="utf-8")
                    logger.info(f"  Generated: {output_file.name}")
                    processed += 1

        return processed


def main():
    parser = argparse.ArgumentParser(description="Primordial - Skill Code Generator")
    parser.add_argument(
        "--archive", default="../domains/ARCHIVED_LOW_VALUE", help="Archive directory"
    )
    parser.add_argument(
        "--output", default="../generated_skills", help="Output directory"
    )
    parser.add_argument("--domains", nargs="*", help="Specific domains to process")
    parser.add_argument("--model", default="codellama", help="LLM model")
    args = parser.parse_args()

    archive_dir = Path(__file__).parent / args.archive
    output_dir = Path(__file__).parent / args.output

    print("Primordial - Skill Code Generator")
    print(f"Archive: {archive_dir}")
    print(f"Output: {output_dir}")

    generator = Primordial(str(archive_dir), str(output_dir), args.model)
    count = generator.process_archive(args.domains)

    print(f"\nGenerated {count} skills!")


if __name__ == "__main__":
    main()
