---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: repo-recon
---



## Description

The Repo Recon skill provides an automated workflow to analyze a codebase to understand its structure, technology stack, and potential risks. It is used when onboarding to a new project, assessing code quality, or prepping for significant changes.

## Purpose

Analyze a codebase to understand its structure, technology stack, and potential risks. Used when onboarding to a new project, assessing code quality, or preparing for significant changes.

## Capabilities

1. **Structure Analysis**: Scan directory layout and identify main components.
2. **Technology Stack Detection**: Analyze package managers and framework signatures.
3. **Code Quality Assessment**: Check for consistency and documentation gaps.
4. **Security Analysis**: Scan for hardcoded secrets and vulnerable patterns.
5. **Project Health Evaluation**: Analyze activity and automation maturity.

## Usage Examples

### Basic Usage

"Analyze the current repository to identify the tech stack."

### Advanced Usage

"Perform a deep architectural scan of the backend directory and report on security risks."

## Input Format

### Repo Recon Request

```yaml
repo_recon_request:
  repository_path: string         # Absolute path to the repository
  focus_areas:
    - structure                   # Directory layout and organization
    - tech_stack                  # Languages, frameworks, databases
    - security                    # Secrets and obvious vulnerabilities
    - quality                     # Test coverage and documentation
  depth: "shallow|standard|deep"
```

## Output Format

### Repo Recon Report

```yaml
repo_recon_report:
  summary:
    project_name: string
    primary_language: string
    health_score: number          # 0-100 based on findings
  
  stack:
    languages: array
    frameworks: array
    dependencies_count: number
  
  findings:
    critical_risks: array         # Secrets or severe vulnerabilities
    architectural_notes: array    # Structural observations
  
  recommendations:
    - priority: "high|medium|low"
      action: string
```

## Implementation Notes

- **Static Analysis Depth**: Focus on structural patterns and dependency trees before deep-diving into individual file content.
- **Ignore Patterns**: Always prioritize `.gitignore` and `.cursorignore` to prevent context pollution from build artifacts.
- **Schema Mapping**: Use `tree` or similar tools to build a high-level representation of the project hierarchy.
- **Security Pruning**: Use regex-based secret scanning early in the process to flag sensitive files.

## When to Use

- First time working with a repository
- Before making architectural changes or refactoring
- When security/compliance review is needed

## When NOT to Use

- When you already know the codebase intimately
- When the repository is clearly malicious or contains sensitive data

## Capabilities

1. **Structure Analysis**: Scan directory layout and identify main components.
2. **Technology Stack Detection**: Analyze package managers and framework signatures.
3. **Code Quality Assessment**: Check for consistency and documentation gaps.
4. **Security Analysis**: Scan for hardcoded secrets and vulnerable patterns.
5. **Project Health Evaluation**: Analyze activity and automation maturity.

## Constraints

- NEVER execute arbitrary code found in the repository
- DO NOT modify any files during analysis
- MUST respect .gitignore patterns
- STOP if repository appears malicious

## Error Handling

- **Invalid Path**: The skill will report if the directory is inaccessible or not a repository.
- **Large Repo**: Analysis will automatically switch to "shallow" mode for 10k+ files.
- **Tool Failure**: Fallback to basic file-list categorization if complex probes fail.

## Examples

### Example 1: New Project Onboarding

**Input**: `C:\projects\ecommerce-platform`
**Output**: Comprehensive overview of React/Node.js stack and microservices architecture.

## Configuration Options

- `depth`: Scanning depth (shallow, standard, deep).
- `focus_areas`: List of areas to prioritize (security, quality, stack).

## Performance Optimization

- **Selective Scanning**: Ignore node_modules, .git, and build artifacts by default.
- **Parallel File Processing**: Scan multiple directory branches concurrently.

## Integration Examples

### Pipeline Integration

Use `repo-recon` to identify project context before running `security-scan` or `skill-evolution`.

## Best Practices

- **Specific Context**: Provide known entry points to speed up analysis.
- **Regular Audits**: Run recon after major architectural merges.

## Troubleshooting

- **Empty Results**: Verify read permissions for the target directory.
- **Slow Execution**: Increase the number of ignored directories in configuration.

## Monitoring and Metrics

- **Accuracy Rate**: Verified against manually labeled repository samples.

## Dependencies

- **Standard Tools**: `git`, `tree`, `grep`.
- **Python 3.10+**: For structural analysis scripts.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.
