#!/usr/bin/env python3
"""Test the two new skills."""
import sys
import os
import asyncio
from pathlib import Path

sys.path.insert(0, os.getcwd() + '/src')

# Ensure __init__.py files exist
Path('src/flywheel/skills/CLOUD_ENGINEERING/__init__.py').parent.mkdir(parents=True, exist_ok=True)
Path('src/flywheel/skills/DATA_ENGINEERING/__init__.py').touch(exist_ok=True)
Path('src/flywheel/skills/CLOUD_ENGINEERING/__init__.py').touch(exist_ok=True)

async def main():
    from flywheel.skills.CLOUD_ENGINEERING.multi_platform_cross_compilation import invoke as xcompile
    from flywheel.skills.DATA_ENGINEERING.operational_deliverables import invoke as deliverables

    r1 = await xcompile({"action": "list_platforms"})
    print("Multi-platform Cross-compilation:", r1["result"]["count"], "platforms")

    r2 = await xcompile({"action": "get_platform", "name": "mikrotik-mips"})
    print("  mikrotik-mips:", r2["result"]["arch"], r2["result"]["endianness"])

    r3 = await deliverables({"action": "list_artifacts"})
    print("Operational Deliverables:", r3["result"])

    print()
    print("Both new skills tested successfully!")

if __name__ == "__main__":
    asyncio.run(main())