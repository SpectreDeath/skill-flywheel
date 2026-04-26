#!/usr/bin/env python3
"""Documentation Generator - Auto-generates CLAUDE.md, CURSOR.md."""

from typing import Dict, Any, List, Optional
from datetime import datetime


class ClaudeMDGenerator:
    """Generate CLAUDE.md from skill and behavioral configuration."""

    def generate(self, profile_name: str = "karpathy_balanced",
                 skills: Optional[List[Dict[str, Any]]] = None,
                 project_name: str = "Project") -> str:
        from flywheel.behavioral.profiles import get_profile
        profile = get_profile(profile_name)
        content = self._header(project_name)
        content += self._introduction(profile)
        content += self._profile_section(profile)
        if skills:
            content += self._skills_section(skills)
        content += self._usage_examples()
        content += self._installation()
        content += self._footer()
        return content

    def _header(self, project_name: str) -> str:
        return f"""# Karpathy-Inspired Guidelines for {project_name}

---

"""

    def _introduction(self, profile: Any) -> str:
        return f"""## Overview

This project follows the **{profile.name}** behavioral guidelines.

**Description:** {profile.description}

### The Problem
> "The models make wrong assumptions and overcomplicate code."

### The Solution
| Principle | Addresses |
|-----------|-----------|
| Think Before Coding | Wrong assumptions |
| Simplicity First | Overcomplication |
| Surgical Changes | Orthogonal edits |
| Goal-Driven Execution | Tests-first, verifiable goals |

---

"""

    def _profile_section(self, profile: Any) -> str:
        settings = ""
        for k, v in profile.settings.items():
            settings += f"- **{k}**: {v}\n"
        return f"""## Active Profile: {profile.name}

**Description:** {profile.description}

**Constraints:** {", ".join(profile.constraints)}

**Configuration:**
{settings}
**Minimum Quality Score:** {profile.min_score:.0%}

---

"""

    def _skills_section(self, skills: List[Dict[str, Any]]) -> str:
        content = "## Available Skills\n\n"
        for skill in skills:
            content += f"### {skill.get('name', 'Unknown')}\n"
            content += f"**Domain:** {skill.get('domain', 'N/A')}\n"
            content += f"**Description:** {skill.get('description', 'N/A')}\n"
            content += f"**Version:** {skill.get('version', 'N/A')}\n\n"
        return content

    def _usage_examples(self) -> str:
        return """## Usage Examples

```markdown
## Task
Add input validation for the user registration form.

## Success Criteria
1. All required fields validated
2. Tests cover all scenarios

## Approach
- Keep changes surgical
- State assumptions explicitly
```

---

"""

    def _installation(self) -> str:
        return """## Installation

```python
from flywheel.behavioral.orchestrator import BehavioralOrchestrator

result = orchestrator.invoke(
    skill_name="sat-solver-optimization",
    payload=your_payload,
    profile="karpathy_balanced"
)
```

---

"""

    def _footer(self) -> str:
        generated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""## How to Know It's Working
- Fewer unnecessary changes
- Code is simple
- Questions before implementation

*Generated on {generated}*
"""


class CursorRuleGenerator:
    """Generate Cursor rules from skill definitions."""

    def generate(self, profile_name: str = "karpathy_balanced",
                 skills: Optional[List[Dict[str, Any]]] = None,
                 project_name: str = "Project") -> str:
        from flywheel.behavioral.profiles import get_profile
        profile = get_profile(profile_name)
        content = f"# Karpathy Guidelines for {project_name}\n\n"
        content += "## Behavioral Rules\n\n"
        content += "1. **Think Before Coding**: State assumptions\n"
        content += "2. **Simplicity First**: Minimum code\n"
        content += "3. **Surgical Changes**: Touch only what's needed\n"
        content += "4. **Goal-Driven Execution**: Verify success criteria\n\n"
        if skills:
            content += "### Available Skills\n"
            for skill in skills:
                content += f"- **{skill.get('name')}**: {skill.get('description')}\n"
        return content
