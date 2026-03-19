---
Domain: COGNITIVE_SKILLS
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Thinking Skills
Estimated Execution Time: 5-30 minutes
name: convergent-thinking
Source: community
Source_File: wikipedia-vertical-convergent-thinking
---

## Purpose

Provides a comprehensive framework for analytical problem-solving, logical reasoning, and finding the single best answer to problems. Derived from Vertical thinking (Edward de Bono) and Convergent thinking (Joy Paul Guilford).

## Description

Convergent thinking is a cognitive approach that focuses on finding the single best solution to a problem through systematic, logical analysis. Unlike divergent thinking which generates multiple possibilities, convergent thinking narrows down to the most correct answer using rational assessment, evidence-based evaluation, and sequential reasoning. This skill encompasses 13 sub-skills that enable systematic analytical thinking.

## Examples

### Example 1: Problem-Solving Workflow

**Input**: A complex technical problem with multiple potential causes
**Output**: Systematic identification of root cause with evidence-based justification
**Use Case**: Debugging, troubleshooting, decision-making

### Example 2: Decision Selection

**Input**: Multiple solution options with trade-offs
**Output**: Weighted evaluation selecting optimal choice
**Use Case**: Business decisions, technical architecture choices

### Example 3: Knowledge Application

**Input**: Domain problem requiring existing knowledge
**Output**: Synthesized solution combining known information
**Use Case**: Research, analysis, academic problem-solving

## Implementation Notes

- **Origin**: Edward de Bono (Vertical thinking, 1970), Joy Paul Guilford (Convergent thinking)
- **Key Principle**: Selection by exclusion - work within frame of reference, throw out irrelevant
- **Complementary**: Use with divergent thinking for creative problem-solving
- **Application**: Best for problems with existing solutions that need to be elucidated

## Capabilities

- **Logical Reasoning**: Apply rational assessment to draw correct inferences
- **Sequential Problem-Solving**: Move from problem to solution in logical steps
- **Critical Evaluation**: Apply standards and probabilities to make judgments
- **Analytical Thinking**: Systematically break down problems to find optimal solutions
- **Decision Making**: Weigh alternatives and select best solution based on criteria
- **Knowledge Synthesis**: Combine existing knowledge to form coherent solutions
- **Information Retrieval**: Efficiently recall and apply stored information
- **Fact-Based Assessment**: Evaluate using evidence rather than intuition
- **Accuracy and Speed**: Focus on correct answers efficiently under time pressure
- **Focused Selection**: Filter irrelevant information, work within relevant frame
- **Depth of Understanding**: Build detailed logical justifications
- **Conclusive Thinking**: Reach definitive, unambiguous answers
- **Technique Application**: Apply proven methods and standard procedures

## Usage Examples

### Logical Reasoning Template

```
PREMISE 1: [Known fact]
PREMISE 2: [Known fact]
LOGICAL RULE: [Syllogism, implication, etc.]
CONCLUSION: [Derived statement]
```

### Sequential Problem-Solving Framework

```
STEP 1: Understand the Problem
        - What is given?
        - What is required?
        - What constraints exist?

STEP 2: Devise a Plan
        - What approach applies?
        - What is the first action?

STEP 3: Execute the Plan
        - Show each step explicitly
        - Verify before proceeding

STEP 4: Review the Solution
        - Does answer satisfy problem?
        - Are there edge cases?
```

### Decision Matrix

```
| Criterion   | Weight | Option A | Option B |
|-------------|--------|----------|----------|
| Cost        | 30%    | 4        | 3        |
| Speed       | 25%    | 3        | 5        |
| Reliability | 25%    | 5        | 4        |
| Features    | 20%    | 4        | 3        |
| TOTAL       | 100%   | 3.7      | 3.75     |
```

## Input Format

```yaml
thinking_task:
  type: "problem-solving|decision|analysis|evaluation"
  problem: "description of the problem"
  constraints:
    - "constraint 1"
    - "constraint 2"
  available_information:
    fact_1: "relevant fact"
    fact_2: "relevant fact"
  criteria:
    - "success criterion 1"
    - "success criterion 2"
```

## Output Format

```yaml
thinking_result:
  approach: "convergent"
  solution: "the selected answer"
  confidence: "HIGH|MEDIUM|LOW"
  justification:
    - "logical step 1"
    - "logical step 2"
  alternatives_considered:
    - "alternative 1 (rejected because...)"
    - "alternative 2 (rejected because...)"
  limitations:
    - "limitation 1"
```

## Configuration Options

### Thinking Style Profiles

```yaml
profiles:
  analytical:
    focus: "depth over breadth"
    approach: "sequential"
    verification: "rigorous"
  
  practical:
    focus: "solution over theory"
    approach: "incremental"
    verification: "sufficient"
  
  academic:
    focus: "precision over speed"
    approach: "thorough"
    verification: "exhaustive"
```

## Error Handling

```yaml
thinking_failures:
  insufficient_information:
    detection: "cannot reach conclusion with available data"
    recovery: "switch to information retrieval mode"
  
  analysis_paralysis:
    detection: "excessive time on single option"
    recovery: "apply time-boxed decision rule"
  
  bias_引入:
    detection: "conclusion precedes evidence"
    recovery: "restart with evidence-first approach"
```

## Best Practices

1. **Define Frame First**: Know what you're focusing on before filtering
2. **Verify Each Step**: Check each inference before proceeding to next
3. **Quantify When Possible**: Use numbers, percentages, probabilities
4. **Document Rationale**: Record why each choice was made
5. **Acknowledge Uncertainty**: State confidence levels explicitly

## Troubleshooting

### Common Issues

1. **Premature Closure**: Jumping to conclusions without sufficient analysis
   - Fix: Apply sequential framework rigorously

2. **Analysis Paralysis**: Overthinking leading to no decision
   - Fix: Set time limits per decision stage

3. **Ignoring Evidence**: Letting bias override facts
   - Fix: Apply fact-based assessment checklist

4. **False Precision**: Claiming more certainty than warranted
   - Fix: Explicitly state confidence levels

## Dependencies

- **Information Sources**: Access to relevant data and knowledge bases
- **Validation Tools**: Methods for verifying conclusions
- **Time Resources**: Sufficient time for thorough analysis (when accuracy matters)

## Version History

- **1.0.0**: Initial release with 13 convergent thinking sub-skills

## Constraints

- MUST verify each step before proceeding to next
- MUST state confidence level with conclusions
- SHOULD consider alternative explanations before finalizing
- MUST NOT commit to conclusion without sufficient evidence
- SHOULD document reasoning for future reference
