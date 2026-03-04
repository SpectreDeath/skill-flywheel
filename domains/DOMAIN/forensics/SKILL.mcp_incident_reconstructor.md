---
Domain: FORENSICS
Version: 1.0.0
Type: Algorithm
Category: Incident Investigation
Complexity: Advanced
Estimated Execution Time: 5-15 minutes
name: mcp_incident_reconstructor
---

# SKILL: MCP Incident Reconstructor

## Purpose

Reconstruct and analyze MCP server incidents, crashes, and failures using forensic techniques to determine root causes, timeline reconstruction, and preventive measures. This skill specializes in MCP-specific failure analysis and system recovery strategies.

## When to Use

- Investigating MCP server crashes and unexpected shutdowns
- Analyzing MCP communication failures and protocol violations
- Reconstructing timeline of events leading to MCP incidents
- Investigating MCP security breaches and unauthorized access
- Analyzing MCP performance degradation and resource exhaustion

## When NOT to Use

- For minor MCP configuration issues that are easily resolved
- When immediate MCP restart is needed over investigation
- For MCP maintenance activities with known procedures
- When MCP logs are completely unavailable or corrupted

## Inputs

- **Required**: MCP server logs and error reports
- **Required**: System resource usage and performance metrics
- **Required**: MCP protocol communication logs
- **Optional**: MCP configuration files and version information
- **Optional**: Network traffic analysis and security logs
- **Assumptions**: MCP logs contain sufficient detail, system timestamps are synchronized, network logs are available

## Outputs

- **Primary**: Complete incident reconstruction with timeline and root cause analysis
- **Secondary**: MCP-specific failure pattern identification and classification
- **Tertiary**: Recovery procedures and preventive measures for MCP systems
- **Format**: JSON structure with incident timeline, analysis, and MCP-specific recommendations

## Capabilities

1. **MCP Protocol Analysis**: Deep analysis of MCP communication protocols and violations
2. **Timeline Reconstruction**: Precise reconstruction of events leading to MCP incidents
3. **Resource Analysis**: Analysis of system resource usage and exhaustion patterns
4. **Security Investigation**: Investigation of MCP security breaches and unauthorized access
5. **Recovery Planning**: Development of MCP-specific recovery and prevention strategies

## Usage Examples

### Example 1: MCP Server Crash Investigation

**Context**: MCP server crashed during high-traffic period causing system-wide outage
**Input**: 
```
MCP logs: 5000+ entries over 4 hours before crash
Resource metrics: CPU 95%, Memory 98%, Disk I/O saturated
Protocol logs: 150 protocol violations detected
Network traffic: 10x normal load detected
```
**Output**: Complete incident reconstruction identifying resource exhaustion as root cause

### Example 2: MCP Security Breach

**Context**: Unauthorized access detected through MCP server
**Input**: Authentication logs, network traffic, protocol violations
**Output**: Security breach timeline and attack vector analysis

## Input Format

- **MCP Logs**: Server logs, error messages, protocol communication logs
- **System Metrics**: CPU, memory, disk, network usage over time
- **Configuration Data**: MCP version, configuration files, security settings
- **Network Data**: Traffic patterns, connection logs, security events

## Output Format

```json
{
  "incident_reconstruction": {
    "mcp_server_id": "mcp_server_001",
    "incident_type": "catastrophic_crash",
    "timeline": {
      "normal_operation": "2026-03-03T10:00:00Z",
      "anomaly_detection": "2026-03-03T13:30:00Z",
      "escalation_period": "2026-03-03T13:30:00Z - 2026-03-03T13:55:00Z",
      "crash_time": "2026-03-03T13:55:00Z",
      "detection_time": "2026-03-03T13:56:00Z",
      "response_time": "2026-03-03T13:58:00Z"
    },
    "root_cause_analysis": {
      "primary_cause": "resource_exhaustion",
      "secondary_cause": "protocol_violation_accumulation",
      "contributing_factors": [
        "increased_load",
        "insufficient_monitoring",
        "missing_circuit_breakers"
      ],
      "mcp_specific_factors": [
        "protocol_buffer_overflow",
        "connection_pool_exhaustion",
        "message_queue_backlog"
      ]
    },
    "impact_assessment": {
      "affected_agents": 150,
      "downtime_duration": "45_minutes",
      "data_loss": "minimal",
      "system_impact": "critical"
    }
  },
  "mcp_failure_patterns": {
    "pattern_type": "resource_exhaustion",
    "frequency": "2_occurrences_in_3_months",
    "common_triggers": [
      "traffic_spikes",
      "memory_leaks",
      "connection_leaks"
    ],
    "mcp_vulnerabilities": [
      "insufficient_resource_limits",
      "missing_backpressure_mechanisms",
      "inadequate_monitoring"
    ]
  },
  "recovery_procedures": {
    "immediate_actions": [
      {
        "action": "restart_mcp_server",
        "priority": "critical",
        "time_to_execute": "2_minutes",
        "success_rate": "95%"
      },
      {
        "action": "clear_message_queues",
        "priority": "high",
        "time_to_execute": "1_minute",
        "success_rate": "100%"
      }
    ],
    "preventive_measures": [
      {
        "measure": "implement_resource_limits",
        "priority": "high",
        "implementation_time": "1_week",
        "expected_impact": "prevent_resource_exhaustion"
      },
      {
        "measure": "add_backpressure_mechanisms",
        "priority": "medium",
        "implementation_time": "2_weeks",
        "expected_impact": "prevent_queue_backlog"
      }
    ]
  },
  "mcp_security_analysis": {
    "security_incidents": "none_detected",
    "vulnerability_assessment": "medium_risk",
    "authentication_issues": "none",
    "protocol_compliance": "95%_compliant"
  }
}
```

## Configuration Options

- `reconstruction_depth`: basic, detailed, forensic (default: detailed)
- `timeline_precision`: seconds, milliseconds, microseconds (default: milliseconds)
- `pattern_analysis_window`: 1_week, 1_month, 3_months (default: 1_month)
- `security_analysis_level`: basic, detailed, comprehensive (default: detailed)
- `chaos_injection_level`: none, light, heavy (default: light)

## Constraints

- **Hard Rules**: 
  - Never modify MCP configuration during incident analysis
  - Always preserve MCP logs and evidence for investigation
  - Maintain MCP service isolation during analysis
- **Safety Requirements**: 
  - Use read-only access to MCP logs and configurations
  - Implement proper MCP service isolation procedures
  - Document all analysis procedures for compliance
- **Quality Standards**: 
  - Provide MCP-specific root cause analysis
  - Include protocol-specific failure patterns
  - Generate actionable recovery procedures

## Error Handling

- **Incomplete MCP Logs**: Use statistical inference and pattern matching
- **Corrupted Protocol Data**: Implement data recovery and reconstruction
- **Missing Network Logs**: Flag for manual investigation and documentation
- **Analysis Conflicts**: Provide multiple hypotheses with confidence levels

## Performance Optimization

- **Log Processing**: Use efficient parsing algorithms for large MCP log files
- **Timeline Analysis**: Implement optimized timeline reconstruction algorithms
- **Pattern Recognition**: Use machine learning for MCP-specific pattern detection
- **Resource Analysis**: Implement real-time resource usage analysis

## Integration Examples

### With Agent Ecosystem
```python
# Integrate MCP incident analysis into system monitoring
mcp_reconstructor = MCPIncidentReconstructor()
incident_report = mcp_reconstructor.analyze_incident(
    mcp_server_id="mcp_server_001",
    analysis_depth="forensic"
)
```

### With MCP Server
```python
@tool(name="mcp_incident_reconstructor")
def reconstruct_mcp_incident(mcp_server_id: str, analysis_depth: str = "detailed") -> dict:
    reconstructor = MCPIncidentReconstructor()
    return reconstructor.analyze_incident(mcp_server_id, analysis_depth)
```

## Best Practices

- **Comprehensive Log Collection**: Gather all relevant MCP logs and system data
- **Protocol-Specific Analysis**: Focus on MCP protocol violations and patterns
- **Timeline Accuracy**: Ensure precise timestamp synchronization and accuracy
- **Root Cause Focus**: Identify underlying causes, not just symptoms
- **Recovery Planning**: Develop specific MCP recovery and prevention strategies

## Troubleshooting

- **Insufficient MCP Logs**: Implement improved MCP logging and monitoring
- **Complex Protocol Analysis**: Use protocol visualization and analysis tools
- **Conflicting Evidence**: Document all hypotheses with supporting evidence
- **Analysis Overload**: Prioritize analysis based on impact and frequency

## Monitoring and Metrics

- **MCP Incident Detection Rate**: Percentage of MCP incidents detected automatically
- **Analysis Accuracy**: Success rate of identified root causes
- **Recovery Time**: Time from MCP incident to complete recovery
- **Pattern Recognition Rate**: Number of MCP-specific patterns identified
- **Prevention Success Rate**: Percentage of prevented MCP incidents

## Dependencies

- **Required Skills**: MCP protocol analysis, system forensics, network analysis
- **Required Tools**: Python with MCP analysis libraries, log parsing tools, network analysis
- **Required Files**: MCP logs, system metrics, protocol specifications, configuration files

## Version History

- **1.0.0**: Initial release with core MCP incident reconstruction and analysis
- **1.1.0**: Added Ralph Wiggum chaos integration for creative incident analysis
- **1.2.0**: Integrated real-time MCP monitoring and automated incident detection

## License

MIT

## Description

The MCP Incident Reconstructor skill specializes in forensic analysis of MCP server incidents, crashes, and failures. By applying advanced analysis techniques to MCP-specific protocols and system data, this skill provides comprehensive incident reconstruction and root cause analysis.

The skill implements specialized algorithms for analyzing MCP communication protocols, system resource usage patterns, and security events. It goes beyond simple error identification to provide deep understanding of MCP failure mechanisms and their prevention.

This skill is essential for maintaining high reliability and security in MCP-based agent ecosystems, providing the tools needed to systematically investigate and prevent MCP incidents.

## Workflow

1. **Incident Detection**: Identify and document MCP server incidents
2. **Evidence Collection**: Gather all relevant MCP logs and system data
3. **Timeline Reconstruction**: Reconstruct precise timeline of events
4. **Protocol Analysis**: Analyze MCP protocol violations and communication issues
5. **Root Cause Identification**: Determine primary and contributing causes
6. **Pattern Recognition**: Identify MCP-specific failure patterns
7. **Recovery Planning**: Develop MCP-specific recovery and prevention strategies

## Examples

### Example 1: MCP Protocol Violation Investigation
**Scenario**: Multiple MCP protocol violations detected causing system instability
**Process**: Analyze protocol logs, identify violation patterns, trace root cause
**Result**: Discovered configuration mismatch, implemented protocol compliance improvements

### Example 2: MCP Resource Exhaustion
**Scenario**: MCP server crashed due to resource exhaustion during peak load
**Process**: Analyze resource usage patterns, identify bottlenecks, trace escalation
**Result**: Implemented resource limits and backpressure mechanisms, prevented future incidents

## Asset Dependencies

- **Scripts**: mcp_reconstructor_core.py, protocol_analyzer.py, timeline_builder.py
- **Templates**: mcp_incident_schema.json, protocol_analysis_template.json
- **Reference Data**: MCP protocol specifications, failure pattern databases
- **Tools**: Python MCP analysis libraries, log parsing tools, network analysis tools

## Ralph Wiggum Chaos Integration

This skill includes Ralph Wiggum-style chaotic creativity injection:

- **Unexpected MCP Failure Scenarios**: Discover failure modes through chaotic MCP simulation
- **Creative Protocol Analysis**: Use entropy to identify non-obvious protocol violations
- **Chaos-Driven Timeline Reconstruction**: Apply randomization to find hidden incident patterns
- **Randomized Investigation Paths**: Explore MCP incidents from unexpected angles

The chaos engine enhances traditional MCP incident analysis by introducing creative approaches to incident investigation while maintaining MCP-specific technical accuracy.