---
name: self-evolving-skill-engine
description: Use when building self-evolving AI agent systems that automatically capture, repair, and improve reusable skill patterns from task executions, with SQLite persistence and three evolution modes (FIX, DERIVED, CAPTURED).
---

# Self-Evolving Skill Engine Architecture

## Overview

Architecture pattern for agents that learn from every task execution. Skills are not static configuration -- they evolve through three modes, persist in SQLite, and auto-trigger repair/improvement based on execution outcomes.

## Evolution Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| **FIX** | Tool/API breakage detected | Auto-repairs skills when external dependencies change (e.g., library API update, sandbox policy change) |
| **DERIVED** | Better pattern found | Improves existing skill when a more efficient or reliable approach is discovered during execution |
| **CAPTURED** | Novel task completed | Extracts new reusable skill from a successful task execution that had no prior skill match |

## Architecture

```
[Task Input]
     |
[Skill Search] -- BM25 + embedding hybrid ranking
     |
  ┌──┤ Match found? ├──┐
  │                     │
 YES                    NO (cold start)
  │                     │
[Skill Reuse]      [Full LLM reasoning]
  │                     │
[Execute + Track]  [Execute + Track]
  │                     │
  └──┬──────────────────┘
     |
[Post-Execution Analysis]
     |
  ┌──┤ Outcome? ├──┐
  │                 │
 Success          Failure
  │                 │
[CAPTURED mode]  [FIX mode]
  │                 │
[Store new skill] [Repair skill]
  │                 │
[Compare to       [Retry with
 existing]         fix]
  │                 │
[DERIVED mode     [Store fixed
 if better]        version]
  │
[SQLite + SKILL.md]
```

## Skill Search (Hybrid BM25 + Embedding)

```python
# Combines keyword matching (BM25) with semantic similarity (embeddings)
# for robust skill discovery

async def search_skills(query, top_k=5):
    # BM25: exact keyword matching (fast, handles jargon)
    bm25_results = bm25_index.search(query, top_k=top_k*2)

    # Embedding: semantic similarity (handles paraphrasing)
    embedding_results = embedding_index.search(
        embed(query), top_k=top_k*2
    )

    # Reciprocal rank fusion
    return reciprocal_rank_fusion(bm25_results, embedding_results, top_k)
```

## SQLite Persistence Schema

```sql
-- Core skill storage
CREATE TABLE skills (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    version INTEGER DEFAULT 1,
    origin TEXT,              -- 'manual', 'captured', 'derived', 'fixed'
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    applied_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    token_savings REAL DEFAULT 0.0
);

-- Skill evolution lineage
CREATE TABLE skill_evolution (
    id INTEGER PRIMARY KEY,
    skill_id TEXT REFERENCES skills(id),
    parent_skill_id TEXT,     -- NULL for CAPTURED, parent for DERIVED/FIX
    evolution_mode TEXT,      -- 'FIX', 'DERIVED', 'CAPTURED'
    trigger_event TEXT,
    diff_summary TEXT,
    evolved_at TIMESTAMP
);

-- Trigger configuration
CREATE TABLE triggers (
    skill_id TEXT REFERENCES skills(id),
    trigger_keyword TEXT
);
```

## Quality Metrics Tracking

```python
# Per-skill metrics updated after each execution
skill_metrics = {
    'applied_rate': applied_count / search_hits,  # How often selected
    'completion_rate': success_count / applied_count,  # How often succeeds
    'effective_rate': token_savings / applied_count,  # Avg savings per use
    'version': 1,  # Incremented on DERIVED/FIX
}
```

## Three Automatic Triggers

1. **Execution failure** → FIX mode: detect what broke, patch the skill, retry
2. **Better pattern discovered** → DERIVED mode: compare new approach to existing skill, upgrade if better
3. **Novel successful execution** → CAPTURED mode: extract pattern, store as new skill

## Constraints

- MUST persist skills in both SQLite (metadata/indexing) and SKILL.md files (content/human-readable)
- MUST track parent_skill_id for evolution lineage (enables rollback and auditing)
- MUST increment version on DERIVED/FIX (never modify in place)
- MUST track applied_count and success_count for quality gating
- SHOULD use hybrid BM25 + embedding search (neither alone is sufficient)
- MUST NOT auto-evolve skills with applied_count < 3 (insufficient evidence)
- SHOULD cap version depth to prevent runaway evolution
- ALWAYS log trigger_event in skill_evolution table for debugging
