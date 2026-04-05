---
name: skillsmp-skill-gap-discoverer
description: "Use when: identifying missing capabilities in SkillsMP, discovering gaps in available skills for specific tasks, analyzing coverage, or recommending new skills to create. Triggers: 'find gaps', 'missing skills', 'coverage analysis', 'recommend skill', 'identify gaps'. Works with skillsmp-api-client."
---

# SkillsMP Skill Gap Discoverer

Analyzes SkillsMP to identify capability gaps, discovers areas where no suitable skills exist, and recommends new skill creation.

## Dependencies

- Requires `skillsmp-api-client` skill
- Works with `skillsmp-skill-learner` for pattern analysis

## Core Workflow

```
Task/Goal Input
    |
    v
Analyze Available Skills (search SkillsMP)
    |
    v
Identify Gaps (no skill or poor skill coverage)
    |
    v
Rate Gap Severity (critical, high, medium, low)
    |
    v
Recommend Solutions (create skill, combine, extend)
    |
    v
Output Gap Report with Recommendations
```

## Gap Detection Algorithm

```python
class GapDetector:
    def __init__(self, client: SkillsMPClient):
        self.client = client
        self.min_acceptable_score = 0.3
        
    def find_gaps(self, task: str) -> List[Gap]:
        """Find capability gaps for a given task."""
        
        # 1. Get all potentially relevant skills
        related_skills = self.client.search(q=task, limit=50)
        ai_skills = self.client.ai_search(q=f"how to {task}")
        
        all_skills = self.merge_results(related_skills, ai_skills)
        
        # 2. Score each skill for the task
        scored_skills = []
        for skill in all_skills:
            score = self.score_skill_for_task(skill, task)
            scored_skills.append((skill, score))
        
        # 3. Identify gaps
        gaps = []
        
        # No skills found
        if not scored_skills:
            gaps.append(Gap(
                type="no_skills",
                severity="critical",
                task=task,
                message="No skills found for this task"
            ))
        
        # Low quality skills
        low_quality = [s for s, score in scored_skills if score < self.min_acceptable_score]
        if low_quality and scored_skills:
            gaps.append(Gap(
                type="insufficient_quality",
                severity="high",
                task=task,
                existing_skills=low_quality,
                message=f"Found {len(low_quality)} skills but none meet quality threshold"
            ))
        
        # Missing sub-capabilities
        sub_tasks = self.decompose_task(task)
        for sub_task in sub_tasks:
            if not self.has_coverage(sub_task, scored_skills):
                gaps.append(Gap(
                    type="missing_sub_capability",
                    severity="medium",
                    task=sub_task,
                    message=f"Missing capability for: {sub_task}"
                ))
        
        return gaps
    
    def score_skill_for_task(self, skill: Skill, task: str) -> float:
        """Score how well a skill matches a task (0-1)."""
        
        # Text similarity
        text_score = self.similarity(skill.description, task)
        
        # Star quality
        star_score = min(skill.stars / 100, 1.0)
        
        # Recency
        recency_score = self.age_score(skill.updated_at)
        
        return (text_score * 0.6 + star_score * 0.3 + recency_score * 0.1)
    
    def has_coverage(self, sub_task: str, scored_skills: List) -> bool:
        """Check if any skill adequately covers a sub-task."""
        for skill, score in scored_skills:
            if score >= self.min_acceptable_score:
                return True
        return False
```

## Gap Severity Classification

```python
class GapSeverity:
    CRITICAL = "critical"  # No solution exists, blocks major functionality
    HIGH = "high"         # Poor solution exists, significant improvement needed
    MEDIUM = "medium"     # Some coverage but gaps in capability
    LOW = "low"           # Minor improvements possible
    
    @staticmethod
    def classify(gap: Gap, task_importance: float) -> str:
        """Classify severity based on gap type and task importance."""
        
        if gap.type == "no_skills":
            return GapSeverity.CRITICAL if task_importance > 0.7 else GapSeverity.HIGH
        
        if gap.type == "insufficient_quality":
            return GapSeverity.HIGH
        
        if gap.type == "missing_sub_capability":
            return GapSeverity.MEDIUM
        
        return GapSeverity.LOW
```

## Gap Report Generation

```python
def generate_gap_report(gaps: List[Gap]) -> GapReport:
    """Generate structured gap report with recommendations."""
    
    report = GapReport(
        summary=f"Found {len(gaps)} gaps",
        critical=[g for g in gaps if g.severity == "critical"],
        high=[g for g in gaps if g.severity == "high"],
        medium=[g for g in gaps if g.severity == "medium"],
        low=[g for g in gaps if g.severity == "low"],
        recommendations=[]
    )
    
    # Generate recommendations for each gap
    for gap in gaps:
        recommendation = generate_recommendation(gap)
        report.recommendations.append(recommendation)
    
    return report
```

## Recommendation Types

For each gap, recommend one of:

```python
class Recommendation:
    CREATE_NEW = "create_new"      # Build new skill from scratch
    EXTEND_EXISTING = "extend"      # Add capabilities to existing skill
    COMBINE_SKILLS = "combine"     # Merge multiple partial skills
    IMPORT_EXTERNAL = "import"     # Import from external source
    USE_ALTERNATIVE = "alternative" # Use different approach/technology

def generate_recommendation(gap: Gap) -> Recommendation:
    """Generate best recommendation for gap."""
    
    if gap.type == "no_skills":
        # Could create new or import
        return Recommendation(
            type=Recommendation.CREATE_NEW,
            priority=gap.severity,
            description="Create new skill to fill gap",
            approach="Analyze similar skills in related domains, adapt patterns"
        )
    
    elif gap.type == "insufficient_quality":
        # Extend existing or create better version
        return Recommendation(
            type=Recommendation.EXTEND_EXISTING,
            priority=gap.severity,
            description="Improve existing skill or create enhanced version",
            approach="Add error handling, better documentation, more features"
        )
    
    # etc.
```

## Usage Example

```python
# Analyze a complex task for gaps
detector = GapDetector(client)

# Check for data pipeline capabilities
gaps = detector.find_gaps("real-time data pipeline with ETL")

report = generate_gap_report(gaps)

print("=== Gap Report ===")
print(f"Total gaps: {len(gaps)}")
print(f"Critical: {len(report.critical)}")
print(f"High: {len(report.high)}")

print("\n=== Recommendations ===")
for rec in report.recommendations:
    print(f"- [{rec.type}] {rec.description}")
    print(f"  Priority: {rec.priority}")
    print(f"  Approach: {rec.approach}")
```

## Domain-Wide Analysis

For strategic planning, analyze gaps across domains:

```python
def analyze_domain_gaps(client: SkillsMPClient, domains: List[str]) -> DomainGapAnalysis:
    """Analyze gaps across multiple domains."""
    
    domain_gaps = {}
    
    for domain in domains:
        # Get representative tasks for domain
        tasks = get_representative_tasks(domain)
        
        domain_gaps[domain] = []
        for task in tasks:
            gaps = find_gaps(task)
            domain_gaps[domain].extend(gaps)
    
    # Aggregate and prioritize
    return DomainGapAnalysis(
        total_gaps=sum(len(g) for g in domain_gaps.values()),
        gaps_by_domain=domain_gaps,
        highest_priority=list(sorted(
            all_gaps, key=lambda g: g.severity
        ))[:10]  # Top 10 gaps
    )
```

## Gap Tracking Over Time

Maintain gap history to track progress:

```python
class GapTracker:
    def __init__(self):
        self.gaps = []  # Historical gaps
        self.resolutions = []  # How gaps were resolved
        
    def record_gap(self, gap: Gap):
        gap.id = generate_id()
        gap.discovered_at = datetime.now()
        self.gaps.append(gap)
        
    def mark_resolved(self, gap_id: str, resolution: str):
        gap = self.find(gap_id)
        gap.resolved_at = datetime.now()
        gap.resolution = resolution
        self.resolutions.append(Resolution(gap_id, resolution))
        
    def get_resolved_count(self) -> int:
        return len([g for g in self.gaps if g.resolved_at])
    
    def get_trending_gaps(self) -> List[str]:
        """Find gaps that appear repeatedly across tasks."""
        # Count gap patterns
        gap_types = Counter(g.type for g in self.gaps)
        return [t for t, count in gap_types.most_common() if count > 3]
```

## Constraints

- MUST verify gaps with multiple search strategies
- SHOULD consider task importance when rating severity
- MUST provide actionable recommendations
- SHOULD track gap resolution over time
- MAY combine gap analysis with skill generation (use with skill-learner)
- SHOULD prioritize critical gaps first
- MUST handle case where gap is actually unsolvable (external dependency)