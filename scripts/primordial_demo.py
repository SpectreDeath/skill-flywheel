#!/usr/bin/env python3
"""Test Primordial with mock LLM."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from primordial import Primordial
from primordial.mock_llm import MockLLMClient


# Monkey-patch to use mock
class TestPrimordial(Primordial):
    def _init_llm(self):
        logger = logging.getLogger(__name__)
        self.llm = MockLLMClient(model="mock")
        logger.info("Using MOCK LLM for testing")


import logging

logging.basicConfig(level=logging.INFO)


def main():
    script_dir = Path(__file__).parent.parent
    archive_dir = script_dir / "domains/ARCHIVED_LOW_VALUE"
    output_dir = script_dir / "generated_skills"

    print("""
╔═══════════════════════════════════════════════════╗
║        PRIMORDIAL - TEST MODE                      ║
╚═══════════════════════════════════════════════════╝
    """)

    # Create test instance
    generator = TestPrimordial(
        archive_dir=str(archive_dir), output_dir=str(output_dir), llm_model="mock"
    )

    # Process just ML_AI domain, limit 2 skills
    print("Processing ML_AI domain (2 skills)...")

    skills = list((archive_dir / "ML_AI").glob("SKILL.*"))
    count = 0
    for skill_dir in skills[:2]:
        code = generator.generate(skill_dir / "SKILL.md")
        if code:
            output_file = output_dir / "ML_AI" / f"{skill_dir.name}.py"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(code)
            print(f"  Generated: {output_file.name}")
            count += 1

    print(f"""
╔═══════════════════════════════════════════════════╗
║                  COMPLETE!                       ║
║  Skills Generated: {count:<30} ║
║  Output: {output_dir:<35} ║
╚═══════════════════════════════════════════════════╝
    """)

    # Show result
    print("\n=== Generated Code Sample ===")
    sample = list((output_dir / "ML_AI").glob("*.py"))
    if sample:
        print(sample[0].read_text()[:500])


if __name__ == "__main__":
    main()
