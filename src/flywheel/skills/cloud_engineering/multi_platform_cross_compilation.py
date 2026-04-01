#!/usr/bin/env python3
"""
Multi-Platform Cross-Compilation Pipeline

Build system patterns for compiling a single C codebase against multiple
target architectures (x86, ARM, MIPS, PPC) using cross-compilation toolchains.

Extracted from Buildroot-style embedded Linux cross-compilation workflows.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PlatformConfig:
    """Configuration for a cross-compilation target platform."""

    def __init__(
        self,
        name: str,
        arch: str,
        cross_prefix: str,
        buildroot_path: str = "/opt/buildroot",
        endianness: str = "little",
        defines: Optional[List[str]] = None,
    ):
        self.name = name
        self.arch = arch
        self.cross_prefix = cross_prefix
        self.buildroot_path = buildroot_path
        self.endianness = endianness
        self.defines = defines or []
        self.debug_level = 2

    @property
    def gcc_bin(self) -> str:
        """Path to cross-compiler gcc."""
        return f"{self.buildroot_path}/{self.cross_prefix}-linux-gcc"

    @property
    def ar_bin(self) -> str:
        """Path to cross-compiler ar."""
        return f"{self.buildroot_path}/{self.cross_prefix}-linux-ar"

    @property
    def ranlib_bin(self) -> str:
        """Path to cross-compiler ranlib."""
        return f"{self.buildroot_path}/{self.cross_prefix}-linux-ranlib"

    @property
    def strip_bin(self) -> str:
        """Path to cross-compiler strip."""
        return f"{self.buildroot_path}/{self.cross_prefix}-linux-strip"

    def get_cflags(self) -> str:
        """Get CFLAGS for this platform."""
        defines = " ".join(f"-D{d}" for d in self.defines)
        if self.endianness == "big":
            defines += " -DFORCE_BIG_ENDIAN"
        return f"-static {defines} -DDEBUG_LEVEL={self.debug_level}"

    def get_makefile_content(self) -> str:
        """Generate Makefile-include content for this platform."""
        return f"""# Cross-compiler for {self.name} ({self.arch})
CC := {self.gcc_bin}
AR := {self.ar_bin}
RANLIB := {self.ranlib_bin}
STRIP := {self.strip_bin}

# Architecture defines
CFLAGS += {self.get_cflags()}
LDFLAGS += -static
"""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "arch": self.arch,
            "cross_prefix": self.cross_prefix,
            "endianness": self.endianness,
            "gcc_bin": self.gcc_bin,
            "defines": self.defines,
        }


# Predefined platform configurations
KNOWN_PLATFORMS = {
    "linux-x86": {
        "arch": "i386",
        "cross_prefix": "i386",
        "endianness": "little",
        "defines": ["LINUX", "_X86"],
    },
    "linux-x86_64": {
        "arch": "x86_64",
        "cross_prefix": "x86_64",
        "endianness": "little",
        "defines": ["LINUX", "_X86_64"],
    },
    "mikrotik-mips": {
        "arch": "mips",
        "cross_prefix": "mips",
        "endianness": "big",
        "defines": ["MIKROTIK", "_MIPS"],
    },
    "mikrotik-ppc": {
        "arch": "powerpc",
        "cross_prefix": "powerpc",
        "endianness": "big",
        "defines": ["MIKROTIK", "_PPC"],
    },
    "ubiquiti-mips": {
        "arch": "mips",
        "cross_prefix": "mips",
        "endianness": "big",
        "defines": ["UBIQUITI", "_MIPS"],
    },
    "avtech-arm": {
        "arch": "arm",
        "cross_prefix": "arm",
        "endianness": "little",
        "defines": ["AVTECH", "_ARM"],
    },
}


def create_platform(name: str) -> PlatformConfig:
    """Create a platform config from a known platform name."""
    config = KNOWN_PLATFORMS.get(name)
    if not config:
        raise ValueError(f"Unknown platform: {name}. Known: {list(KNOWN_PLATFORMS.keys())}")
    return PlatformConfig(
        name=name,
        arch=config["arch"],
        cross_prefix=config["cross_prefix"],
        endianness=config["endianness"],
        defines=config["defines"],
    )


def list_platforms() -> List[Dict[str, Any]]:
    """List all known platform configurations."""
    return [
        {
            "name": name,
            "arch": cfg["arch"],
            "endianness": cfg["endianness"],
            "defines": cfg["defines"],
        }
        for name, cfg in KNOWN_PLATFORMS.items()
    ]


def generate_makefile(platform_n: PlatformConfig, target: str = "all") -> str:
    """Generate a Makefile for cross-compilation."""
    platform = platform_n if isinstance(platform_n, PlatformConfig) else create_platform(platform_n)

    return f"""# Top-level Makefile for cross-compilation
# Target: {platform.name}

.PHONY: all clean server client

all: server client

server:
\t$(MAKE) -C server PLATFORM={platform.name}

client:
\t$(MAKE) -C client PLATFORM={platform.name}

clean:
\trm -f *.o
\t$(MAKE) -C server clean
\t$(MAKE) -C client clean
"""


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "list_platforms")

    if action == "list_platforms":
        platforms = list_platforms()
        return {
            "result": {"platforms": platforms, "count": len(platforms)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    elif action == "get_platform":
        name = payload.get("name", "")
        if not name:
            return {
                "result": {"error": "name required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        try:
            platform = create_platform(name)
            return {
                "result": platform.to_dict(),
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        except ValueError as e:
            return {
                "result": {"error": str(e)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    elif action == "generate_makefile":
        name = payload.get("name", "linux-x86")
        try:
            platform = create_platform(name)
            makefile = generate_makefile(platform)
            return {
                "result": {
                    "platform": name,
                    "makefile": makefile,
                },
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        except ValueError as e:
            return {
                "result": {"error": str(e)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    elif action == "generate_makefile_include":
        name = payload.get("name", "linux-x86")
        try:
            platform = create_platform(name)
            content = platform.get_makefile_content()
            return {
                "result": {
                    "platform": name,
                    "content": content,
                },
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        except ValueError as e:
            return {
                "result": {"error": str(e)},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    elif action == "add_custom_platform":
        name = payload.get("name")
        if not name:
            return {
                "result": {"error": "name, arch, cross_prefix, endianness, defines required"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }
        KNOWN_PLATFORMS[name] = {
            "arch": payload.get("arch", ""),
            "cross_prefix": payload.get("cross_prefix", ""),
            "endianness": payload.get("endianness", "little"),
            "defines": payload.get("defines", []),
        }
        return {
            "result": {"status": "added", "name": name},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


def register_skill():
    """Return skill metadata."""
    return {
        "name": "multi-platform-cross-compilation",
        "description": "Build system patterns for cross-compiling C codebases against multiple target architectures (x86, ARM, MIPS, PPC) using Buildroot toolchains",
        "version": "1.0.0",
        "domain": "CLOUD_ENGINEERING",
    }