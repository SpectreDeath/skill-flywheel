---
Domain: FORENSICS
Version: 1.0.0
Type: Algorithm
Category: Evidence Management
Complexity: Advanced
Estimated Execution Time: 2-5 minutes
name: chain_of_custody_tracker
---

# SKILL: Chain of Custody Tracker

## Purpose

Maintain forensic-grade audit trails for all skill artifacts, evidence, and modifications within the agent ecosystem. This skill ensures evidence integrity, prevents tampering, and provides complete traceability for forensic investigations and compliance audits.

## When to Use

- Tracking evidence collection and handling in forensic investigations
- Maintaining audit trails for skill modifications and deployments
- Ensuring compliance with forensic standards (NIST, ISO)
- Investigating evidence tampering or integrity violations
- Auditing skill lifecycle from creation to retirement

## When NOT to Use

- Simple operations with no compliance requirements
- Emergency situations requiring immediate action over documentation
- Systems where audit trails are not legally or operationally required
- When evidence integrity is not a concern

## Inputs

- **Required**: Evidence artifacts and their metadata
- **Required**: Handler identification and timestamps
- **Required**: Storage location and access logs
- **Optional**: Chain of custody violation reports
- **Optional**: Evidence integrity verification results
- **Assumptions**: All evidence can be digitally tracked, handlers are authenticated, timestamps are reliable

## Outputs

- **Primary**: Complete chain of custody documentation with cryptographic verification
- **Secondary**: Tamper detection reports and integrity violation alerts
- **Tertiary**: Compliance audit reports and evidence validation certificates
- **Format**: JSON structure with evidence logs, handler chains, and integrity proofs

## Capabilities

1. **Evidence Tracking**: Complete lifecycle tracking from collection to disposal
2. **Tamper Detection**: Cryptographic verification of evidence integrity
3. **Handler Authentication**: Secure identification and authorization of evidence handlers
4. **Audit Trail Generation**: Comprehensive logs for compliance and legal requirements
5. **Violation Detection**: Real-time alerts for chain of custody breaches

## Usage Examples

### Example 1: Skill Modification Audit

**Context**: Investigating unauthorized changes to critical authentication skill
**Input**: 
```
Evidence: skill files, modification timestamps, handler logs
Chain of custody: 15 handlers over 30 days
Integrity checks: SHA-256 hashes, digital signatures
```
**Output**: Complete audit trail showing unauthorized access and modification details

### Example 2: Forensic Evidence Collection

**Context**: Collecting evidence after system compromise
**Input**: Compromised files, system logs, network captures
**Output**: Chain of custody documentation for legal proceedings

## Input Format

- **Evidence Metadata**: File paths, hashes, creation/modification times
- **Handler Information**: User IDs, authentication tokens, access permissions
- **Storage Details**: Location paths, access controls, backup information
- **Integrity Data**: Cryptographic hashes, digital signatures, verification timestamps

## Output Format

```json
{
  "evidence_chain": {
    "evidence_id": "skill_auth_v2.1.0",
    "collection_details": {
      "timestamp": "2026-03-03T14:30:00Z",
      "collector": "system_admin_001",
      "collection_method": "automated_backup",
      "integrity_hash": "sha256:abc123...",
      "storage_location": "/evidence/chain_of_custody/2026/03/03/"
    },
    "handler_chain": [
      {
        "handler_id": "system_admin_001",
        "action": "collected",
        "timestamp": "2026-03-03T14:30:00Z",
        "integrity_verified": true,
        "digital_signature": "sig_abc123..."
      },
      {
        "handler_id": "security_analyst_007",
        "action": "analyzed",
        "timestamp": "2026-03-03T15:45:00Z",
        "integrity_verified": true,
        "analysis_notes": "No signs of tampering detected"
      }
    ],
    "current_status": {
      "location": "/evidence/secure_storage/chain_of_custody/2026/03/03/",
      "integrity_verified": true,
      "access_control": "role_based",
      "retention_policy": "7_years"
    }
  },
  "integrity_verification": {
    "hash_algorithm": "SHA-256",
    "verification_timestamp": "2026-03-03T16:00:00Z",
    "verification_result": "PASS",
    "tamper_detection": "NONE",
    "integrity_score": 1.0
  },
  "compliance_report": {
    "nist_compliance": true,
    "iso_compliance": true,
    "audit_trail_complete": true,
    "handler_authentication_valid": true,
    "storage_security_valid": true
  }
}
```

## Configuration Options

- `integrity_algorithm`: SHA-256, SHA-512, BLAKE3 (default: SHA-256)
- `verification_frequency`: real_time, hourly, daily (default: real_time)
- `tamper_detection_level`: strict, moderate, lenient (default: strict)
- `audit_trail_format`: json, xml, csv (default: json)
- `retention_period`: days, months, years (default: 7 years)

## Constraints

- **Hard Rules**: 
  - Never allow evidence modification without proper authorization
  - Always maintain cryptographic integrity verification
  - Preserve original evidence in immutable storage
- **Safety Requirements**: 
  - Implement multi-factor authentication for evidence access
  - Use encrypted storage for all sensitive evidence
  - Maintain backup copies in geographically separate locations
- **Quality Standards**: 
  - Provide 100% audit trail coverage
  - Ensure all timestamps are synchronized and verifiable
  - Maintain evidence integrity throughout entire lifecycle

## Error Handling

- **Integrity Violations**: Immediate alerts and evidence isolation
- **Authentication Failures**: Block access and log security incident
- **Storage Failures**: Automatic failover to backup storage locations
- **Timestamp Discrepancies**: Flag for manual review and correction

## Performance Optimization

- **Hash Caching**: Cache frequently accessed integrity hashes
- **Parallel Verification**: Verify multiple evidence items concurrently
- **Incremental Updates**: Update only changed portions of chain of custody
- **Compression**: Compress audit trail data while maintaining integrity

## Integration Examples

### With Agent Ecosystem
```python
# Integrate chain of custody into skill management
custody_tracker = ChainOfCustodyTracker()
evidence_log = custody_tracker.track_evidence(
    evidence_id="skill_auth_v2.1.0",
    handler_id="system_admin_001",
    action="modified"
)
```

### With MCP Server
```python
@tool(name="chain_of_custody_tracker")
def track_evidence_chain(evidence_id: str, handler_id: str, action: str) -> dict:
    tracker = ChainOfCustodyTracker()
    return tracker.track_evidence(evidence_id, handler_id, action)
```

## Best Practices

- **Immediate Documentation**: Record all evidence handling actions in real-time
- **Cryptographic Verification**: Use strong cryptographic algorithms for integrity
- **Role-Based Access**: Implement strict access controls based on roles
- **Regular Audits**: Conduct periodic audits of chain of custody procedures
- **Training**: Ensure all handlers are trained in proper evidence handling

## Troubleshooting

- **Missing Handler Information**: Implement fallback authentication mechanisms
- **Timestamp Synchronization**: Use NTP servers for accurate timekeeping
- **Storage Space Issues**: Implement automated archiving and compression
- **Integrity Check Failures**: Investigate and document all integrity violations

## Monitoring and Metrics

- **Chain of Custody Completeness**: Percentage of evidence with complete audit trails
- **Integrity Violation Rate**: Number of integrity violations per time period
- **Handler Compliance**: Percentage of handlers following proper procedures
- **Evidence Access Patterns**: Frequency and patterns of evidence access
- **Storage Utilization**: Disk space usage for evidence storage

## Dependencies

- **Required Skills**: Cryptography, digital forensics, audit trail management
- **Required Tools**: Python with hashlib, digital signature libraries, secure storage
- **Required Files**: Evidence metadata schemas, handler authentication data, storage configurations

## Version History

- **1.0.0**: Initial release with core chain of custody tracking and integrity verification
- **1.1.0**: Added real-time tamper detection and automated compliance reporting
- **1.2.0**: Integrated with MCP server for seamless evidence tracking

## License

MIT

## Description

The Chain of Custody Tracker skill implements forensic-grade evidence management for agent skill ecosystems. By maintaining complete audit trails and cryptographic integrity verification, this skill ensures that all evidence remains admissible and trustworthy throughout its entire lifecycle.

The skill applies NIST and ISO forensic standards to track every interaction with evidence, from initial collection through analysis, storage, and eventual disposal. It provides real-time tamper detection, automated compliance reporting, and comprehensive audit trails that meet legal and regulatory requirements.

This skill is essential for maintaining the integrity of forensic investigations, ensuring compliance with industry standards, and providing defensible evidence handling procedures in complex agent ecosystems.

## Workflow

1. **Evidence Collection**: Capture evidence with cryptographic hashes and metadata
2. **Handler Authentication**: Verify handler identity and authorization
3. **Chain Documentation**: Record all handling actions with timestamps
4. **Integrity Verification**: Continuously verify evidence integrity
5. **Tamper Detection**: Alert on any integrity violations or unauthorized access
6. **Compliance Reporting**: Generate audit reports for legal and regulatory requirements

## Examples

### Example 1: Security Incident Investigation
**Scenario**: Investigating unauthorized access to critical system files
**Process**: Track all evidence collection, analysis, and storage with complete audit trails
**Result**: Defensible evidence suitable for legal proceedings and compliance audits

### Example 2: Skill Lifecycle Audit
**Scenario**: Auditing changes to authentication skills over 6 months
**Process**: Review complete chain of custody for all skill modifications
**Result**: Comprehensive audit trail showing all changes and responsible parties

## Asset Dependencies

- **Scripts**: custody_tracker_core.py, integrity_verifier.py, audit_generator.py
- **Templates**: evidence_metadata_schema.json, handler_auth_schema.json
- **Reference Data**: NIST forensic standards, ISO compliance requirements
- **Tools**: Python hashlib, digital signature libraries, secure storage systems

## Ralph Wiggum Chaos Integration

This skill includes Ralph Wiggum-style chaotic creativity injection:

- **Unexpected Evidence Sources**: Discover evidence in unconventional locations
- **Creative Chain Building**: Build unexpected connections between evidence items
- **Chaos-Driven Verification**: Use entropy to detect subtle integrity violations
- **Randomized Audit Patterns**: Apply unpredictable audit schedules to catch violations

The chaos engine enhances traditional chain of custody procedures by introducing creative approaches to evidence discovery and verification while maintaining strict forensic standards.