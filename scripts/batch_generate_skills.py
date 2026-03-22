"""
Batch skill generator - processes all NOT_IMPLEMENTED skills from backlog
"""

import asyncio
import json
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from skills.skill_management.tutorial_skill_generator import (
    parse_skill_md,
    generate_tutorial_skill_code,
    save_skill_module,
    verify_module_import,
    register_skill_in_db,
    update_backlog_status,
    SKILLS_ROOT,
    DOMAINS_ROOT,
    REGISTRY_DB_PATH,
    BACKLOG_PATH,
)


def get_not_implemented_skills():
    """Load all NOT_IMPLEMENTED skills from backlog."""
    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)
    return [s for s in backlog if s.get("status") == "NOT_IMPLEMENTED"]


def group_by_domain(skills):
    """Group skills by domain."""
    domains = {}
    for skill in skills:
        domain = skill.get("domain", "UNKNOWN")
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(skill)
    return domains


def find_skill_md_path(domain, skill_name):
    """Find the SKILL.md file path for a skill."""
    path_variations = [
        os.path.join(
            DOMAINS_ROOT, domain.upper(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(
            DOMAINS_ROOT, domain.lower(), "SKILL.{}".format(skill_name), "SKILL.md"
        ),
        os.path.join(DOMAINS_ROOT, domain, "SKILL.{}".format(skill_name), "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain.upper(), skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain.lower(), skill_name, "SKILL.md"),
        os.path.join(DOMAINS_ROOT, domain, skill_name, "SKILL.md"),
    ]

    for path in path_variations:
        if os.path.exists(path):
            return path

    for d in [domain.upper(), domain.lower(), domain]:
        domain_path = os.path.join(DOMAINS_ROOT, d)
        if os.path.exists(domain_path):
            for item in os.listdir(domain_path):
                if (
                    item.lower() == "SKILL.{}".format(skill_name).lower()
                    or item.lower() == skill_name.lower()
                ):
                    potential = os.path.join(domain_path, item, "SKILL.md")
                    if os.path.exists(potential):
                        return potential
    return None


async def process_skill(skill, fix_attempted=False):
    """Process a single skill - generate, verify, register."""
    skill_id = skill.get("skill_id")
    skill_name = skill.get("name")
    domain = skill.get("domain")

    logger.info("Processing: {} ({})".format(skill_name, domain))

    skill_md_path = find_skill_md_path(domain, skill_name)
    if not skill_md_path:
        logger.warning("SKILL.md not found for: {} in {}".format(skill_name, domain))
        return {
            "status": "skipped",
            "reason": "SKILL.md not found",
            "skill": skill_name,
        }

    try:
        metadata = parse_skill_md(skill_md_path)
    except Exception as e:
        logger.error("Failed to parse SKILL.md for {}: {}".format(skill_name, str(e)))
        return {
            "status": "skipped",
            "reason": "Parse error: " + str(e),
            "skill": skill_name,
        }

    version = metadata.get("version", "1.0.0")

    try:
        code = generate_tutorial_skill_code(skill_name, domain, metadata, skill_id)
        generated_path = save_skill_module(domain, skill_name, code, overwrite=True)
    except FileExistsError:
        logger.info("Skill file already exists: {}".format(skill_name))
        return {"status": "skipped", "reason": "File exists", "skill": skill_name}
    except Exception as e:
        logger.error("Failed to generate code for {}: {}".format(skill_name, str(e)))
        if not fix_attempted:
            return {"status": "retry", "skill": skill_name, "error": str(e)}
        return {
            "status": "skipped",
            "reason": "Generation error: " + str(e),
            "skill": skill_name,
        }

    try:
        verify_module_import(generated_path)
    except Exception as e:
        logger.error("Import verification failed for {}: {}".format(skill_name, str(e)))
        if os.path.exists(generated_path):
            os.remove(generated_path)
        if not fix_attempted:
            return {"status": "retry", "skill": skill_name, "error": str(e)}
        return {
            "status": "skipped",
            "reason": "Import error: " + str(e),
            "skill": skill_name,
        }

    try:
        register_skill_in_db(
            domain=domain,
            skill_name=skill_name,
            module_path=generated_path,
            skill_id=skill_id,
            version=version,
            description=metadata.get("description"),
        )
    except Exception as e:
        logger.error("Registration failed for {}: {}".format(skill_name, str(e)))
        return {
            "status": "skipped",
            "reason": "Registration error: " + str(e),
            "skill": skill_name,
        }

    update_backlog_status(skill_id)
    logger.info("Successfully processed: {}".format(skill_name))
    return {"status": "implemented", "skill": skill_name, "skill_id": skill_id}


async def process_domain(domain_name, skills):
    """Process all skills in a single domain."""
    logger.info("=" * 60)
    logger.info("Processing domain: {} ({} skills)".format(domain_name, len(skills)))
    logger.info("=" * 60)

    implemented = 0
    skipped = 0

    for i, skill in enumerate(skills):
        logger.info("Progress: {}/{}".format(i + 1, len(skills)))

        result = await process_skill(skill)

        if result["status"] == "implemented":
            implemented += 1
        elif result["status"] == "retry":
            logger.info("Retrying: {}".format(result["skill"]))
            retry_result = await process_skill(skill, fix_attempted=True)
            if retry_result["status"] == "implemented":
                implemented += 1
            else:
                skipped += 1
                logger.warning(
                    "Skipped after retry: {} - {}".format(
                        result["skill"], retry_result.get("reason", "unknown")
                    )
                )
        else:
            skipped += 1
            logger.warning(
                "Skipped: {} - {}".format(
                    result["skill"], result.get("reason", "unknown")
                )
            )

    logger.info(
        "Domain {} complete: {} implemented, {} skipped".format(
            domain_name, implemented, skipped
        )
    )
    return {"implemented": implemented, "skipped": skipped}


async def main():
    """Main entry point."""
    logger.info("Loading backlog...")
    skills = get_not_implemented_skills()
    logger.info("Found {} NOT_IMPLEMENTED skills".format(len(skills)))

    domains = group_by_domain(skills)
    logger.info("Domains to process: {}".format(len(domains)))

    total_implemented = 0
    total_skipped = 0

    for domain_name in sorted(domains.keys()):
        domain_skills = domains[domain_name]
        result = await process_domain(domain_name, domain_skills)
        total_implemented += result["implemented"]
        total_skipped += result["skipped"]

        logger.info("Committing domain: {}".format(domain_name))

    logger.info("=" * 60)
    logger.info("FINAL TOTALS")
    logger.info("=" * 60)
    logger.info("Implemented: {}".format(total_implemented))
    logger.info("Skipped: {}".format(total_skipped))

    import sqlite3

    conn = sqlite3.connect(REGISTRY_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM skills")
    count = cursor.fetchone()[0]
    conn.close()
    logger.info("Final registry total: {}".format(count))

    return {
        "implemented": total_implemented,
        "skipped": total_skipped,
        "final_count": count,
    }


if __name__ == "__main__":
    asyncio.run(main())
