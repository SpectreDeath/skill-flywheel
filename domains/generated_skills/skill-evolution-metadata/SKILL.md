---
name: skill-evolution-metadata
description: Use when defining SKILL.md files with evolution metadata including origin tracking, version history, trigger keywords, and quality metrics for self-evolving agent systems.
---

# SKILL.md Convention with Evolution Metadata

## Overview

Extended SKILL.md format for self-evolving skill engines. Adds evolution metadata (origin, version, triggers, quality metrics) to the standard name/description frontmatter, enabling lineage tracking and quality-gated evolution.

## Frontmatter Schema

```yaml
---
name: csv-data-validation
description: Validate CSV files for encoding, delimiter, missing values, type mismatches, and duplicates before processing.
version: 3
origin: derived           # manual | captured | derived | fixed
parent_skill: csv-reader  # parent skill ID (for derived/fixed), null for captured/manual
triggers:
  - csv
  - data validation
  - data quality
  - pandas
  - encoding detection
quality:
  applied_count: 28
  success_count: 25
  completion_rate: 0.893
  token_savings_avg: 0.459
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T14:30:00Z"
---
```

## Origin Values

| Origin | Description | Has Parent? |
|--------|-------------|-------------|
| `manual` | Human-created skill | No |
| `captured` | Auto-extracted from novel successful execution | No |
| `derived` | Auto-improved from existing skill after better pattern found | Yes |
| `fixed` | Auto-repaired after execution failure | Yes |

## Content Structure

```markdown
# Skill Name

Brief description of what this skill does.

## Instructions

Detailed implementation guidance:
1. Step-by-step process
2. Code patterns
3. Error handling

## Code Template

```python
# Reusable code pattern
def template_function():
    pass
```

## Quality Metrics

- Applied Rate: 28/35 selections (80%)
- Completion Rate: 25/28 applications (89.3%)
- Token Savings: 45.9% average
- Version History: v1 (captured) → v2 (derived, improved delimiter detection) → v3 (fixed, encoding fallback)
```

## Example: Execution Recovery Skill

```markdown
---
name: execution-recovery
description: Multi-layer execution recovery handling sandbox failures, shell errors, and file write issues with progressive fallbacks.
version: 1
origin: captured
triggers:
  - error
  - failure
  - recovery
  - fallback
  - retry
quality:
  applied_count: 28
  success_count: 24
  completion_rate: 0.857
  token_savings_avg: 0.38
---

# Execution Recovery

Handle code execution failures with targeted fixes.

## Instructions

When code execution fails:

1. **Capture the full error** including traceback
2. **Identify the failure type**: ImportError, PermissionError, TimeoutError
3. **Apply targeted fix**:
   - ImportError → pip install the missing package
   - PermissionError → change output directory to /tmp
   - TimeoutError → reduce data size or add chunking
   - MemoryError → process in batches
4. **Retry with fix applied**
5. **Log the fix** for future skill evolution
```

## Evolution Lineage Format

```markdown
## Evolution History

| Version | Mode   | Trigger                          | Change Summary                    |
|---------|--------|----------------------------------|-----------------------------------|
| v1      | CAPTURED | Novel CSV validation success    | Initial pattern extraction        |
| v2      | DERIVED | Better delimiter detection found | Added csv.Sniffer() auto-detect   |
| v3      | FIXED  | chardet ImportError on sandbox   | Added fallback: try utf-8 → latin-1 |
```

## Constraints

- MUST include `origin` field to distinguish manual from evolved skills
- MUST include `version` integer, incremented on each DERIVED/FIX
- MUST include `parent_skill` when origin is derived or fixed
- MUST include `triggers` array for hybrid BM25 + embedding search
- SHOULD include `quality` metrics for evolution gating
- Quality metrics MUST be updated after each successful/failed application
- Skills with `applied_count < 3` should not trigger DERIVED evolution (insufficient evidence)
- `completion_rate < 0.5` triggers FIX mode automatically
