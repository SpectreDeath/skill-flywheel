---
name: skill-recommendation
description: "Use when: recommending skills for user queries, building skill recommendation engines, analyzing skill relevance, or suggesting skill combinations. Triggers: 'recommend skill', 'skill suggestion', 'find skills', 'skill relevance', 'similar skills', 'skill match'. NOT for: when exact skill is known, simple direct lookups, or when all skills are equally applicable."
---

# Skill Recommendation

Recommends relevant skills based on user queries, context, or task requirements. This engine analyzes skill descriptions, matches against requirements, and provides ranked recommendations.

## When to Use This Skill

Use this skill when:
- Recommending skills for user queries
- Building skill recommendation engines
- Analyzing skill relevance
- Suggesting skill combinations
- Discovering new capabilities

Do NOT use this skill when:
- Exact skill is known
- Simple direct lookups
- All skills are equally applicable
- Pre-defined skill sets

## Input Format

```yaml
recommendation_request:
  query: string                  # User query or task
  context: object                # Context (domain, user, etc.)
  available_skills: array       # Skills to consider
  num_recommendations: number   # Max recommendations
  include_reasoning: boolean   # Explain recommendations
```

## Output Format

```yaml
recommendation_result:
  recommendations: array          # Ranked skill recommendations
  relevance_scores: object       # Score for each skill
  reasoning: string              # Why these were recommended
  alternatives: array           # Fallback suggestions
```

## Capabilities

### 1. Query Analysis (10 min)

- Parse user query
- Extract key terms and intent
- Identify domain constraints
- Determine skill requirements

### 2. Skill Indexing (15 min)

- Analyze skill descriptions
- Extract capability keywords
- Build skill embeddings
- Create relevance index

### 3. Matching & Scoring (10 min)

- Match query to skill capabilities
- Calculate relevance scores
- Rank by match quality
- Filter by constraints

### 4. Explanation Generation (5 min)

- Generate reasoning for recommendations
- Highlight matched capabilities
- Explain relevance factors
- Provide usage context

### 5. Recommendation Refinement (10 min)

- Consider skill combinations
- Suggest complementary skills
- Account for dependencies
- Optimize for task completion

## Usage Examples

### Basic Usage

"Recommend skills for this user query."

### Advanced Usage

"Get skill recommendations with reasoning and alternatives."

## Configuration Options

- `num_recommendations`: Max skills to recommend
- `include_reasoning`: Explain selections
- `similarity_threshold`: Minimum match score
- `consider_chains`: Suggest skill combinations

## Constraints

- MUST provide relevance scores
- SHOULD explain recommendations
- MUST handle no-match gracefully
- SHOULD suggest alternatives

## Integration Examples

- Skill registries: Power search
- Chatbots: Suggest capabilities
- Agent systems: Skill discovery
- Onboarding: Guide new users

## Dependencies

- Python 3.10+
- Text embedding libraries
- Similarity scoring
- Search indexing
