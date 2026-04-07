---
name: specification-lifecycle-management
description: "Use when: managing specification review cycles, establishing spec expiration policies, preventing specification rot, or setting up automated lifecycle governance. Triggers: 'spec lifecycle', 'review cycle', 'spec expiration', 'spec stale', 'spec governance', 'spec maintenance', 'spec health'. NOT for: small stable specs, rapidly changing specs, or projects without governance needs."
---

# Specification Lifecycle Management

Automate specification review cycles with configurable expiration dates, accountability tracking, and health checks to prevent specification rot. This skill ensures specs stay current and maintained.

## When to Use This Skill

Use this skill when:
- Managing specification review cycles
- Establishing spec expiration policies
- Preventing specification rot
- Setting up automated lifecycle governance
- Implementing team governance requirements

Do NOT use this skill when:
- Small, stable specification sets
- Rapidly changing specifications
- Projects without governance or compliance needs

## Input Format

```yaml
lifecycle_request:
  spec_paths: array              # Specifications to manage
  review_cycle: string           # Review frequency (weekly, monthly, quarterly)
  expiration_policy: object     # Expiration rules
  notifications: object          # Alert configuration
```

## Output Format

```yaml
lifecycle_result:
  schedules: object              # Generated review schedules
  expirations: array            # Upcoming expirations
  health_scores: object         # Specification health metrics
  alerts: array                  # Generated alerts
```

## Capabilities

### 1. Review Scheduling (10 min)

- Create automated review schedules
- Configure review frequencies
- Set escalation paths

### 2. Expiration Management (10 min)

- Define expiration policies
- Track specification age
- Auto-archive expired specs

### 3. Health Scoring (10 min)

- Calculate specification health
- Identify stale or outdated specs
- Track maintenance metrics

### 4. Accountability Tracking (10 min)

- Assign ownership to specifications
- Track review completion
- Generate accountability reports

### 5. Notification System (5 min)

- Send review reminders
- Alert on expiration
- Report on overdue reviews

## Usage Examples

### Basic Usage

"Set up quarterly review cycles for my team specifications."

### Advanced Usage

"Automate spec lifecycle with expiration policies and Slack notifications for overdue reviews."

## When to Use

- Large specification repositories
- Team governance requirements
- Preventing specification rot
- Compliance and audit needs

## When NOT to Use

- Small, stable specification sets
- Rapidly changing specifications
- Individual projects without governance needs

## Configuration Options

- `review_cycle`: Frequency of reviews
- `expiration_days`: Days before expiration
- `notification_channels`: Alert destinations
- `auto_archive`: Auto-archive expired specs

## Constraints

- MUST track all specifications
- SHOULD notify before expiration
- MUST maintain review history
- SHOULD enforce accountability

## Integration Examples

- Project management: Link to task systems
- Communication: Slack/email notifications
- Audit trails: Maintain compliance records

## Dependencies

- Python 3.10+
- Scheduling libraries
- Notification integrations (Slack, email)
