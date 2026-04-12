#!/usr/bin/env python3
"""CLI for Primordial skill code generator."""

import argparse
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Primordial - Generate executable code from archived skills"
    )
    parser.add_argument(
        "--archive",
        default="../domains/ARCHIVED_LOW_VALUE",
        help="Path to archived skills directory",
    )
    parser.add_argument(
        "--output",
        default="../generated_skills",
        help="Output directory for generated code",
    )
    parser.add_argument(
        "--domains", nargs="+", help="Specific domains to process (default: all)"
    )
    parser.add_argument("--model", default="codellama", help="Local LLM model name")
    parser.add_argument(
        "--limit", type=int, default=0, help="Limit number of skills to process"
    )
    args = parser.parse_args()

    # Resolve paths relative to this file
    script_dir = Path(__file__).parent
    archive_dir = script_dir / args.archive
    output_dir = script_dir / args.output

    print(f"""
╔═══════════════════════════════════════════════════╗
║          PRIMORDIAL - Skill Code Generator       ║
║                                                   ║
║  Archive: {archive_dir.name:<42} ║
║  Output: {output_dir.name:<42} ║
║  Model:  {args.model:<42} ║
╚═══════════════════════════════════════════════════╝
    """)

    from primordial import Primordial

    # Initialize generator
    primordial = Primordial(
        archive_dir=str(archive_dir), output_dir=str(output_dir), llm_model=args.model
    )

    # Process skills
    if args.limit > 0:
        logger.info(f"Processing limited to {args.limit} skills...")

    skills_generated = primordial.process_archive(args.domains)

    print(f"""
╔═══════════════════════════════════════════════════╗
║                  COMPLETE!                       ║
║                                                   ║
║  Skills Generated: {skills_generated:<30} ║
║  Output Directory: {output_dir:<35} ║
╚═══════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
