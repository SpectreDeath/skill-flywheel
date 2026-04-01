---
name: cold-warm-transition
description: Use when implementing cold-start vs warm-start execution comparison in AI agent systems, measuring how skill reuse reduces token costs and execution time on subsequent similar tasks.
---

# Cold-Start to Warm-Start Transition

## Overview

Execution pattern that distinguishes between cold-start (no matching skills, full LLM reasoning) and warm-start (skill reuse, reduced reasoning). Measures token savings, execution time reduction, and quality improvement across the transition.

## Cold-Start Execution

```python
async def cold_start_execute(task, model="gpt-4o-mini"):
    """No skills available -- full reasoning from scratch."""
    messages = [
        {"role": "system", "content": "You are a coding assistant. Write complete, working code."},
        {"role": "user", "content": task}
    ]

    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=1500
    )

    return {
        "tokens": response.usage.total_tokens,
        "response": response.choices[0].message.content,
        "skills_used": 0,
        "type": "cold"
    }
```

## Warm-Start Execution

```python
async def warm_start_execute(task, matched_skills, model="gpt-4o-mini"):
    """Skills found -- inject patterns, reduce reasoning."""
    skill_context = format_skills_for_prompt(matched_skills)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a coding assistant with access to pre-evolved skills. "
                "Reuse the provided skill patterns to write efficient code. "
                "Only add what's missing -- don't re-derive what the skill provides.\n\n"
                f"{skill_context}"
            )
        },
        {"role": "user", "content": task}
    ]

    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=1000  # Lower max due to skill context
    )

    return {
        "tokens": response.usage.total_tokens,
        "response": response.choices[0].message.content,
        "skills_used": len(matched_skills),
        "type": "warm"
    }
```

## Token Savings Measurement

```python
def measure_savings(cold_result, warm_result):
    cold_tokens = cold_result["tokens"]
    warm_tokens = warm_result["tokens"]
    savings = cold_tokens - warm_tokens
    savings_pct = (savings / cold_tokens) * 100

    return {
        "cold_tokens": cold_tokens,
        "warm_tokens": warm_tokens,
        "savings_absolute": savings,
        "savings_percent": savings_pct,
        "cold_response_len": len(cold_result["response"]),
        "warm_response_len": len(warm_result["response"]),
        "quality_delta": None  # Measured separately via evaluation
    }
```

## Skill Context Formatting

```python
def format_skills_for_prompt(skills):
    """Format matched skills into LLM context."""
    parts = []
    for skill in skills:
        parts.append(
            f"## Available Skill: {skill['name']} "
            f"(v{skill['version']}, evolved from {skill['applied_count']} executions)\n\n"
            f"{skill['summary']}\n\n"
            f"Template:\n```python\n{skill['code_template']}\n```"
        )
    return "\n\n".join(parts)
```

## Benchmark Reference (GDPVal)

```
Category                  | P1 Income | P2 Income | Token Reduction
--------------------------|-----------|-----------|----------------
Documents & Correspondence|    71%    |    74%    |     -56%
Compliance & Forms        |    51%    |    70%    |     -51%
Media Production          |    53%    |    58%    |     -46%
Engineering               |    70%    |    78%    |     -43%
Spreadsheets              |    63%    |    70%    |     -37%
Strategy & Analysis       |    88%    |    89%    |     -32%
-------------------------------------------------
Overall                   |    --     |    --     |   -45.9% avg
```

## Constraints

- MUST measure both cold and warm on the same task for valid comparison
- MUST use lower `max_tokens` for warm-start (skill context replaces generated code)
- MUST track token counts from `response.usage` not text length
- SHOULD run N>=5 trials for statistical significance
- MUST format skill context as structured sections (not raw dumps)
- SHOULD use `gpt-4o-mini` or equivalent for cost-effective benchmarking
- MUST report savings as both absolute tokens and percentage
- Quality should be measured separately (task completion rate, not just token count)
