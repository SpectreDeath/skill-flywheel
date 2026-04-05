---
name: token-savings-measurement
description: "Use when: measuring and reporting token savings from skill reuse in AI agent systems, comparing cold-start vs warm-start execution costs. Triggers: 'token savings', 'cost measurement', 'skill reuse metrics', 'execution cost', 'warm start', 'cold start'. NOT for: latency measurement (use performance skills), or when token counting is unavailable."
---

# Token Savings Measurement Framework

## Overview

Structured framework for measuring the economic impact of skill reuse in AI agent systems. Compares cold-start (no skills) vs warm-start (skill injection) execution, tracking token counts, response quality, and cost savings.

## Measurement Pipeline

```
[Same Task]
     |
  ┌──┴──┐
  │     │
Cold   Warm
Start  Start
  │     │
Tokens Tokens
  │     │
  └──┬──┘
     |
[Savings Calculator]
     |
[Report]
```

## Implementation

```python
from openai import OpenAI
import time

def measure_cold_warm(task, skill_context, model="gpt-4o-mini"):
    client = OpenAI()

    # Cold start: no skill context
    cold_messages = [
        {"role": "system", "content": "You are a coding assistant. Write complete, working code."},
        {"role": "user", "content": task}
    ]

    cold_start = time.time()
    cold_response = client.chat.completions.create(
        model=model, messages=cold_messages, max_tokens=1500
    )
    cold_time = time.time() - cold_start

    # Warm start: with skill context
    warm_messages = [
        {
            "role": "system",
            "content": (
                "You are a coding assistant with access to pre-evolved skills. "
                "Reuse the provided skill patterns to write efficient code.\n\n"
                f"{skill_context}"
            )
        },
        {"role": "user", "content": task}
    ]

    warm_start = time.time()
    warm_response = client.chat.completions.create(
        model=model, messages=warm_messages, max_tokens=1000
    )
    warm_time = time.time() - warm_start

    return compute_savings(cold_response, warm_response, cold_time, warm_time)
```

## Savings Computation

```python
def compute_savings(cold_resp, warm_resp, cold_time, warm_time):
    cold_tok = cold_resp.usage.total_tokens
    warm_tok = warm_resp.usage.total_tokens

    return {
        "cold_tokens": cold_tok,
        "warm_tokens": warm_tok,
        "savings_tokens": cold_tok - warm_tok,
        "savings_percent": ((cold_tok - warm_tok) / cold_tok) * 100,
        "cold_time_s": cold_time,
        "warm_time_s": warm_time,
        "time_savings_percent": ((cold_time - warm_time) / cold_time) * 100,
        "cold_response_chars": len(cold_resp.choices[0].message.content),
        "warm_response_chars": len(warm_resp.choices[0].message.content),
        "cold_prompt_tokens": cold_resp.usage.prompt_tokens,
        "warm_prompt_tokens": warm_resp.usage.prompt_tokens,
        "cold_completion_tokens": cold_resp.usage.completion_tokens,
        "warm_completion_tokens": warm_resp.usage.completion_tokens,
    }
```

## Report Formatting

```python
def print_savings_report(metrics):
    print(f"{'Metric':<30} {'Cold':>10} {'Warm':>10} {'Savings':>10}")
    print("-" * 65)
    print(f"{'Total Tokens':<30} {metrics['cold_tokens']:>10} {metrics['warm_tokens']:>10} {metrics['savings_percent']:>9.1f}%")
    print(f"{'Prompt Tokens':<30} {metrics['cold_prompt_tokens']:>10} {metrics['warm_prompt_tokens']:>10}")
    print(f"{'Completion Tokens':<30} {metrics['cold_completion_tokens']:>10} {metrics['warm_completion_tokens']:>10}")
    print(f"{'Response Length (chars)':<30} {metrics['cold_response_chars']:>10} {metrics['warm_response_chars']:>10}")
    print(f"{'Execution Time (s)':<30} {metrics['cold_time_s']:>10.1f} {metrics['warm_time_s']:>10.1f} {metrics['time_savings_percent']:>9.1f}%")
```

## Batch Benchmarking

```python
def benchmark_dataset(tasks_with_skills, model="gpt-4o-mini", trials=3):
    """Run cold/warm comparison across multiple tasks."""
    results = []
    for task, skill_ctx in tasks_with_skills:
        trial_results = []
        for t in range(trials):
            r = measure_cold_warm(task, skill_ctx, model)
            trial_results.append(r)
        # Average across trials
        avg = average_results(trial_results)
        avg["task"] = task[:50]
        results.append(avg)

    # Aggregate
    total_cold = sum(r["cold_tokens"] for r in results)
    total_warm = sum(r["warm_tokens"] for r in results)
    print(f"\nOverall: {total_cold} → {total_warm} tokens "
          f"({((total_cold-total_warm)/total_cold)*100:.1f}% savings)")
    return results
```

## Budget-Aware Cost Estimation

```python
# gpt-4o-mini pricing (as of 2026)
COST_PER_1K_INPUT = 0.00015
COST_PER_1K_OUTPUT = 0.0006

def estimate_cost_savings(metrics, runs_per_day=100):
    cold_cost = (metrics['cold_prompt_tokens'] * COST_PER_1K_INPUT / 1000 +
                 metrics['cold_completion_tokens'] * COST_PER_1K_OUTPUT / 1000)
    warm_cost = (metrics['warm_prompt_tokens'] * COST_PER_1K_INPUT / 1000 +
                 metrics['warm_completion_tokens'] * COST_PER_1K_OUTPUT / 1000)
    daily_savings = (cold_cost - warm_cost) * runs_per_day
    return {"per_run_savings": cold_cost - warm_cost, "daily_savings": daily_savings}
```

## Constraints

- MUST use the same task for both cold and warm comparison
- MUST use `response.usage.total_tokens` for accurate counts (not text length estimation)
- MUST run multiple trials (>=3) and average for statistical reliability
- MUST set lower `max_tokens` for warm-start (skill context replaces reasoning)
- SHOULD report both prompt and completion token breakdowns
- SHOULD estimate monetary cost for business justification
- MUST use the same model for both cold and warm (changing models invalidates comparison)
