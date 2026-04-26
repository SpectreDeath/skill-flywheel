#!/usr/bin/env python3
"""
Behavioral Profiles

Pre-configured sets of behavioral guidelines for different contexts.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class BehavioralProfile:
    """Configuration for behavioral guidelines."""

    name: str
    description: str
    constraints: List[str]
    settings: Dict[str, Any] = field(default_factory=dict)
    min_score: float = 0.7  # Minimum quality score to pass

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "constraints": self.constraints,
            "settings": self.settings,
            "min_score": self.min_score,
        }


# Predefined behavioral profiles
KARPATHY_STRICT = BehavioralProfile(
    name="karpathy_strict",
    description=(
        "Full Karpathy guidelines - all principles enforced strictly. "
        "For production-critical or safety-sensitive work."
    ),
    constraints=["simplicity", "assumptions", "surgical", "goals"],
    settings={
        "max_complexity": 8,
        "require_assumptions": True,
        "require_isolation_check": True,
        "require_success_criteria": True,
        "max_change_ratio": 0.05,
        "max_lines_changed": 30,
        "max_critical_assumptions": 1,
    },
    min_score=0.85,
)

KARPATHY_BALANCED = BehavioralProfile(
    name="karpathy_balanced",
    description=(
        "Karpathy guidelines - balanced strictness. "
        "Recommended for most engineering work."
    ),
    constraints=["simplicity", "assumptions", "goals"],
    settings={
        "max_complexity": 15,
        "require_assumptions": True,
        "require_isolation_check": False,
        "require_success_criteria": True,
        "max_change_ratio": 0.10,
        "max_lines_changed": 50,
        "max_critical_assumptions": 3,
    },
    min_score=0.7,
)

KARPATHY_MINIMAL = BehavioralProfile(
    name="karpathy_minimal",
    description=(
        "Karpathy core principles - simplicity and goals only. "
        "For rapid prototyping or exploratory work."
    ),
    constraints=["simplicity", "goals"],
    settings={
        "max_complexity": 20,
        "require_assumptions": False,
        "require_isolation_check": False,
        "require_success_criteria": True,
        "max_change_ratio": 0.15,
        "max_lines_changed": 100,
        "max_critical_assumptions": 5,
    },
    min_score=0.5,
)

PRODUCTION_CRITICAL = BehavioralProfile(
    name="production_critical",
    description=(
        "Maximum quality enforcement - all checks with strict thresholds. "
        "For production deployments, security-sensitive, or reliability-critical work."
    ),
    constraints=["simplicity", "assumptions", "surgical", "goals"],
    settings={
        "max_complexity": 5,
        "require_assumptions": True,
        "require_isolation_check": True,
        "require_success_criteria": True,
        "max_change_ratio": 0.03,
        "max_lines_changed": 20,
        "max_critical_assumptions": 0,
        "require_formal_verification": True,
    },
    min_score=0.95,
)

RAPID_PROTOTYPE = BehavioralProfile(
    name="rapid_prototype",
    description=(
        "Minimal guidelines - goals only. "
        "For quick experiments, proofs of concept, or throwaway code."
    ),
    constraints=["goals"],
    settings={
        "max_complexity": 50,
        "require_assumptions": False,
        "require_isolation_check": False,
        "require_success_criteria": True,
        "max_change_ratio": 0.30,
        "max_lines_changed": 500,
        "max_critical_assumptions": 10,
    },
    min_score=0.3,
)

# Registry of available profiles
BEHAVIORAL_PROFILES: Dict[str, BehavioralProfile] = {
    "karpathy_strict": KARPATHY_STRICT,
    "karpathy_balanced": KARPATHY_BALANCED,
    "karpathy_minimal": KARPATHY_MINIMAL,
    "production_critical": PRODUCTION_CRITICAL,
    "rapid_prototype": RAPID_PROTOTYPE,
}


def get_profile(name: str) -> BehavioralProfile:
    """
    Get a behavioral profile by name.

    Args:
        name: Profile name

    Returns:
        BehavioralProfile instance

    Raises:
        ValueError: If profile not found
    """
    if name not in BEHAVIORAL_PROFILES:
        available = ", ".join(sorted(BEHAVIORAL_PROFILES.keys()))
        raise ValueError(
            f"Unknown behavioral profile: '{name}'. "
            f"Available profiles: {available}"
        )
    return BEHAVIORAL_PROFILES[name]


def list_profiles() -> List[str]:
    """
    List all available behavioral profile names.

    Returns:
        List of profile names
    """
    return sorted(BEHAVIORAL_PROFILES.keys())


def get_default_profile() -> BehavioralProfile:
    """
    Get the default behavioral profile.

    Returns:
        Default profile (karpathy_balanced)
    """
    return get_profile("karpathy_balanced")
