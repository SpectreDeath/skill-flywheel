---
name: chain-of-thought-reasoning
description: Step-by-step logical reasoning skill for solving complex problems through explicit intermediate steps
metadata:
  updated-on: "2026-03-18"
  source: community
  tags: "reasoning,logic,problem-solving,thinking,chain-of-thought"
---

# Chain of Thought Reasoning

Build solutions by articulating each intermediate step explicitly.

## Problem Solving Template

```
PROBLEM: [statement of the problem]

STEP 1 - Understanding:
- What is given?
- What is required?
- What constraints exist?

STEP 2 - Plan:
- What approach applies?
- What is the first action?
- What comes next?

STEP 3 - Execute:
- [Show each calculation/reasoning step]
- Verify each step before proceeding

STEP 4 - Verify:
- Does the answer satisfy the problem?
- Are there edge cases?
- Can the result be cross-checked?
```

## Mathematical Reasoning

```
Given: 2x + 5 = 17
Find: x

Step 1: Subtract 5 from both sides
        2x + 5 - 5 = 17 - 5
        2x = 12

Step 2: Divide both sides by 2
        2x / 2 = 12 / 2
        x = 6

Step 3: Verify
        2(6) + 5 = 12 + 5 = 17 ✓
```

## Algorithmic Reasoning

```
Problem: Find if a string has all unique characters.

Step 1 - Clarify:
- "Unique" means no character repeats
- ASCII or Unicode?
- Empty string? Single char?

Step 2 - Approach Options:
A) Brute force: O(n²) - compare every pair
B) Hash set: O(n) - track seen characters
C) Bit vector: O(n) - for limited charset

Step 3 - Choose and implement (Option B):
```
function hasUniqueChars(s):
    seen = new Set()
    for each char in s:
        if char in seen:
            return false
        seen.add(char)
    return true
```

Step 4 - Test:
- "hello" → false (l repeats)
- "world" → true
- "" → true (vacuous)
```

## Causal Chain Reasoning

```
Problem: Why did the API request fail?

Step 1 - Observation:
- HTTP 500 error returned
- Response time: 2.3s

Step 2 - Possible causes:
- Server crashed
- Database timeout
- Invalid request format
- Resource exhaustion

Step 3 - Check each:
- Server status: healthy ✓
- Database: connection pool exhausted
- Request format: valid JSON ✓

Step 4 - Root cause:
Database connection pool was exhausted due to 
unclosed connections in the retry logic.

Step 5 - Fix verification:
Applied connection pooling fix → requests succeed
```

## Code Example: CoT Prompt Template

```python
CHAIN_OF_THOUGHT_PROMPT = """
Solve this problem step by step. For each step:
1. State what you're doing
2. Show the reasoning
3. Explain why it's correct

Problem: {problem}

Begin with "Step 1:" and continue until reaching a solution.
After solving, verify your answer.
"""
```

## Best Practices

- **Explicit over implicit**: Show work, don't skip steps
- **Verify each step**: Check before moving forward  
- **Track dependencies**: Know what assumptions each step relies on
- **Handle branches**: If-then paths need separate tracking
- **Document failures**: When stuck, explain why and try alternatives

## Anti-Patterns to Avoid

- Jumping to conclusions
- Skipping "obvious" steps
- Not verifying intermediate results
- Mixing multiple reasoning chains
- Ignoring constraints or edge cases
