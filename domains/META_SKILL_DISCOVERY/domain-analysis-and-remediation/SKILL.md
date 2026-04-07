---
name: domain-analysis-and-remediation
description: "Use when: analyzing domain directories for quality issues, identifying placeholder or underdeveloped skills, evaluating skill value and potential, implementing missing skills, or refreshing stale domains. Triggers: 'analyze domain', 'domain analysis', 'skill remediation', 'fix skills', 'evaluate skills', 'domain refresh', 'clean up domain'. NOT for: when domains are healthy, when no issues are suspected, or when manual review is preferred."
---

# Domain Analysis and Remediation

Analyzes domain directories to identify quality issues, evaluates skill value, and implements fixes for underdeveloped or placeholder skills. This meta-skill refreshes stale domains.

## When to Use This Skill

Use this skill when:
- Analyzing domain directories for quality issues
- Identifying placeholder or underdeveloped skills
- Evaluating skill value and potential
- Implementing missing skills
- Refreshing stale domains
- Cleaning up duplicate/archived skills

Do NOT use this skill when:
- Domains are healthy
- No issues suspected
- Manual review preferred
- All skills are properly implemented

## Input Format

```yaml
analysis_request:
  domain_path: string             # Path to domain to analyze
  scan_depth: string              # quick, medium, thorough
  fix_mode: boolean              # Whether to fix issues
  create_missing: boolean        # Implement missing skills
```

## Output Format

```yaml
analysis_result:
  domain_status: object          # Health assessment
  issues_found: array             # Problems identified
  skills_evaluated: object       # Value assessments
  implemented_skills: array      # New skills created
  cleaned_up: object             # What was removed/fixed
  recommendations: array          # Further actions
```

## Capabilities

### 1. Domain Scanning (15 min)

- List all skills in domain
- Check for README
- Identify file structure issues
- Find duplicate or archived versions

### 2. Skill Quality Assessment (20 min)

- Read skill contents
- Identify placeholder content ("To be provided dynamically")
- Check quality metrics (applied_count, completion_rate)
- Evaluate implementation completeness

### 3. Value Evaluation (15 min)

- Categorize skills by value (high, medium, low)
- Identify skills worth reviving
- Flag skills for removal
- Assess feasibility of implementation

### 4. Skill Implementation (30+ min)

- Create proper SKILL.md files
- Follow flywheel format standards
- Include triggers and NOT for clauses
- Add Input/Output schemas
- Write capabilities sections

### 5. Documentation & Cleanup (15 min)

- Update domain README
- Remove duplicate/archived skills
- Clean up old reports
- Document changes

## Usage Examples

### Basic Usage

"Analyze this domain and identify issues."

### Advanced Usage

"Full analysis with skill implementation and cleanup."

## Process Steps

1. **Scan Domain**
   - List all files and subdirectories
   - Check for README.md
   - Identify naming patterns used

2. **Read Sample Skills**
   - Check implementation status
   - Look for placeholder text
   - Evaluate completeness

3. **Categorize Issues**
   - Placeholders (no implementation)
   - Duplicates (archived versions)
   - Format issues (old naming patterns)
   - Missing skills (referenced but not present)

4. **Evaluate Value**
   - High: Real use cases, feasible to implement
   - Medium: Niche but valuable
   - Low: Impractical or redundant

5. **Implement Fixes**
   - Create high-value skills in proper format
   - Update documentation
   - Remove archived placeholders

6. **Verify Format**
   - Follow SKILL.md template
   - Include frontmatter with name/description
   - Add triggers + NOT for clauses
   - Include Input/Output schemas

## Configuration Options

- `scan_depth`: quick (readmes), medium (samples), thorough (all)
- `fix_mode`: Just report or actually fix
- `create_missing`: Implement identified gaps
- `remove_duplicates`: Clean up archived skills

## Constraints

- MUST follow flywheel skill format
- SHOULD prioritize high-value skills
- MUST verify new skills are complete
- SHOULD document changes

## Integration Examples

- Domain audits: Regular health checks
- Onboarding: Analyze new domains
- Refactoring: Improve existing domains
- Quality: Maintain skill standards

## Dependencies

- Python 3.10+ (for file operations)
- Glob for file finding
- Read for content analysis
- Write for creating skills
