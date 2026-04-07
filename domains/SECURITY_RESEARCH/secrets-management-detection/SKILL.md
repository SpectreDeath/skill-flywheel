---
name: secrets-management-detection
description: "Use when: scanning for hardcoded secrets, detecting exposed credentials, managing secrets securely, implementing secret rotation, or integrating secrets management into CI/CD. Triggers: 'secrets detection', 'secret scanning', 'credential detection', 'secrets management', 'secret rotation', 'hardcoded secrets'. NOT for: when secrets are already externalized, development only without production, or when using external secret managers only."
---

# Secrets Management & Detection

Comprehensive secrets detection, management, and secure storage across the development lifecycle. This skill scans for hardcoded secrets, provides secure storage solutions, and integrates with workflows.

## When to Use This Skill

Use this skill when:
- Scanning for hardcoded secrets in code
- Detecting exposed credentials
- Implementing secrets management
- Setting up secret rotation
- Integrating secrets into CI/CD
- Preventing secrets exposure

Do NOT use this skill when:
- Secrets already externalized
- Development only without production
- Using external secret managers only
- No code scanning needed

## Input Format

```yaml
secrets_request:
  scan_path: string              # Path to scan
  scan_type: string              # full, quick, incremental
  secrets_types: array           # Types of secrets to find
  remediation: boolean           # Provide fixes
```

## Output Format

```yaml
secrets_result:
  detected_secrets: array        # Secrets found
  risk_assessment: object        # Risk levels
  remediation: array             # Fix suggestions
  compliance_status: object    # Compliance impact
```

## Capabilities

### 1. Secret Scanning (15 min)

- Scan source code for secrets
- Detect API keys, tokens, passwords
- Find hardcoded credentials
- Identify config file leaks

### 2. Pattern Detection (10 min)

- Recognize secret patterns
- Detect various secret types
- Identify custom secrets
- Reduce false positives

### 3. Risk Assessment (10 min)

- Evaluate secret severity
- Assess exposure scope
- Determine remediation priority
- Flag compliance issues

### 4. Remediation Guidance (15 min)

- Suggest secret externalization
- Recommend secret managers
- Provide migration paths
- Generate fix scripts

### 5. Integration Setup (15 min)

- Integrate with CI/CD pipelines
- Set up pre-commit hooks
- Configure secret scanners
- Enable alerting

## Usage Examples

### Basic Usage

"Scan for secrets in this codebase."

### Advanced Usage

"Full secret scan with remediation and CI/CD integration."

## Configuration Options

- `scan_type`: full, quick, incremental
- `secret_types`: Types to detect
- `exclusions`: Paths to skip
- `severity_threshold`: Min severity to report

## Constraints

- MUST detect all common secret types
- SHOULD minimize false positives
- MUST provide remediation guidance
- SHOULD integrate with existing tools

## Integration Examples

- CI/CD: Block commits with secrets
- Pre-commit: Scan before push
- IDE: Real-time scanning
- Secret managers: Migrate to vault

## Dependencies

- Python 3.10+
- Secret scanning tools (trufflehog, gitleaks)
- Regex pattern libraries
