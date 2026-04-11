---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: security-scan
---



## Description

The Security Scan skill provides an automated workflow to detect security vulnerabilities, misconfigurations, and potential threats in a codebase. It is used for security audits, compliance checks, and proactive risk mitigation.

## Usage Examples

### Basic Usage

"Run a security scan on the current project."

### Advanced Usage

"Scan for OWASP Top 10 vulnerabilities and report all high-severity issues."

## Purpose

Automatically detect security vulnerabilities, misconfigurations, and potential threats in a codebase. Used for security audits, compliance checks, and proactive risk mitigation before deployment.

## Input Format

### Security Scan Request

```yaml
security_scan_request:
  repository_path: string         # Absolute path to the repository
  standards:
    - OWASP_TOP_10
    - SOC2
    - PCI_DSS
  severity_threshold: "low|medium|high|critical"
  focus_areas:
    - secrets                     # API keys, passwords
    - dependencies                # Vulnerable packages
    - code                        # SQLi, XSS, etc.
```

## Output Format

### Security Scan Report

```yaml
security_scan_report:
  scan_timestamp: timestamp
  vulnerabilities:
    - id: string
      severity: string
      category: string
      file_path: string
      line_number: number
      description: string
      remediation: string
  
  compliance_summary:
    passed_checks: number
    failed_checks: number
    score: number                 # 0-100
```

## Implementation Notes

- **Static Analysis**: Uses standard linting and pattern matching for code-level issues.
- **Dependency Audit**: Leverages existing databases (CVE, GitHub Advisory) for package checks.
- **Secret Detection**: Uses entropy checks and known prefix signatures to detect hardcoded keys.

## When to Use

- Before deploying to production
- During security audit processes
- After major code changes or dependency updates

## When NOT to Use

- When you need manual business logic security analysis
- When the codebase contains data you shouldn't access

## Capabilities

1. **Secrets Scanning**: Detect hardcoded keys and exposed credentials.
2. **Dependency Analysis**: Identify vulnerable packages and transitive risks.
3. **Code Review**: Scan for common vulnerabilities like SQLi or XSS.
4. **Configuration Check**: Validate environment and permission settings.
5. **Report Generation**: Categorize findings by severity with specific fixes.

## Constraints

- NEVER execute or test discovered vulnerabilities
- DO NOT modify any files during scanning
- MUST respect .gitignore patterns
- STOP if unauthorized sensitive data is encountered

## Examples

### Example 1: Pre-Deployment Check

**Input**: Repository path with severity threshold = "high".
**Output**: List of critical vulnerabilities and dependency upgrade paths.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Configuration Options

- `severity_threshold`: Minimum severity to report (low, medium, high, critical).
- `standards`: Compliance standards to check against (OWASP, SOC2).

## Performance Optimization

- **Vulnerability Database Caching**: Cache recent CVE lookups to avoid redundant network calls.
- **Delta Scanning**: Only scan files changed since the last verified commit.

## Integration Examples

### Pipeline Integration

Run `security-scan` as a quality gate in `FLOW.full_cycle.yaml`.

## Best Practices

- **Specific Context**: Provide known entry points to speed up analysis.
- **Review Outputs**: Always manually verify critical recommendations before implementation.

## Troubleshooting

- **Empty Results**: Verify that the input identifiers are correct and accessible.
- **Slow Execution**: Reduce the `execution_depth` or narrowed the focus area.

## Monitoring and Metrics

- **Success Rate**: Monitored across automated cycles to ensure reliability.

## Dependencies

- **Standard Tools**: Requires base AgentSkills execution environment.
- **Python 3.10+**: For supporting scripts and automation logic.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.
