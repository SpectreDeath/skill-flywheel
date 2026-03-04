---
Domain: FORENSICS
Version: 1.0.0
Type: Algorithm
Category: Root Cause Analysis
Complexity: Advanced
Estimated Execution Time: 4-12 minutes
name: failure_root_causer
---

# SKILL: Failure Root Causer

## Purpose

Perform comprehensive root cause analysis of skill failures using advanced forensic techniques and Ralph Wiggum-style chaotic creativity. This skill identifies underlying causes, contributing factors, and systemic issues that lead to failures in agent ecosystems.

## When to Use

- Investigating complex skill failures with multiple contributing factors
- Analyzing systemic issues that cause recurring failures
- Performing root cause analysis for critical system failures
- Identifying hidden patterns and correlations in failure data
- Investigating Ralph Wiggum-style chaotic failures and unexpected outcomes

## When NOT to Use

- For simple failures with obvious single causes
- When immediate tactical fixes are needed over root cause analysis
- For failures that are easily resolved without investigation
- When failure data is completely unavailable or corrupted

## Inputs

- **Required**: Failure event data and error logs
- **Required**: System state information at failure time
- **Required**: Skill interaction and dependency data
- **Optional**: Historical failure patterns and trend analysis
- **Optional**: User feedback and operational context
- **Assumptions**: Failure data contains sufficient detail, system state is accurately captured, dependencies are traceable

## Outputs

- **Primary**: Comprehensive root cause analysis with primary and contributing factors
- **Secondary**: Systemic issue identification and pattern recognition
- **Tertiary**: Preventive measures and improvement recommendations
- **Format**: JSON structure with root cause analysis, contributing factors, and actionable recommendations

## Capabilities

1. **Deep Root Cause Analysis**: Identify underlying causes beyond surface symptoms
2. **Systemic Issue Detection**: Identify systemic problems causing multiple failures
3. **Pattern Recognition**: Recognize failure patterns and correlations
4. **Chaos Analysis**: Analyze Ralph Wiggum-style chaotic and unexpected failures
5. **Prevention Strategy Development**: Develop comprehensive prevention strategies

## Usage Examples

### Example 1: Complex System Failure

**Context**: Multiple skills failed simultaneously during peak load
**Input**: 
```
Failure events: 25 skills failed over 15 minutes
System state: CPU 98%, Memory 95%, Network congestion
Dependencies: 150 inter-skill dependencies affected
Contributing factors: Load spike, resource exhaustion, cascading failures
```
**Output**: Root cause analysis identifying resource exhaustion as primary cause with cascading failure patterns

### Example 2: Recurring Performance Issues

**Context**: Performance degradation recurring weekly with unknown cause
**Input**: Performance metrics, failure logs, usage patterns, dependency graphs
**Output**: Root cause analysis identifying memory leak patterns and preventive measures

## Input Format

- **Failure Data**: Error messages, stack traces, failure timestamps, affected components
- **System State**: Resource usage, performance metrics, system configuration at failure time
- **Dependency Data**: Skill interaction graphs, dependency chains, communication patterns
- **Context Data**: User activity, external factors, operational conditions

## Output Format

```json
{
  "root_cause_analysis": {
    "failure_id": "system_failure_2026_03_03_001",
    "failure_type": "cascading_system_failure",
    "primary_cause": {
      "cause_type": "resource_exhaustion",
      "description": "Memory exhaustion due to unbounded cache growth",
      "confidence_level": 0.95,
      "evidence": [
        "memory_usage_98_percent",
        "cache_size_unbounded_growth",
        "gc_pressure_high"
      ]
    },
    "contributing_factors": [
      {
        "factor_type": "load_spike",
        "description": "Unexpected 300% increase in user traffic",
        "contribution_level": 0.7,
        "evidence": ["traffic_spike_detected", "request_rate_increase"]
      },
      {
        "factor_type": "missing_circuit_breaker",
        "description": "No circuit breaker protection for cache operations",
        "contribution_level": 0.6,
        "evidence": ["no_circuit_breaker_found", "cache_operations_unprotected"]
      },
      {
        "factor_type": "insufficient_monitoring",
        "description": "Memory usage alerts not configured",
        "contribution_level": 0.4,
        "evidence": ["no_memory_alerts", "monitoring_gaps_detected"]
      }
    ],
    "systemic_issues": [
      {
        "issue_type": "resource_management",
        "description": "Inadequate resource management across multiple skills",
        "severity": "high",
        "frequency": "recurring",
        "impact": "system_wide"
      },
      {
        "issue_type": "monitoring_gaps",
        "description": "Missing monitoring for critical resource metrics",
        "severity": "medium",
        "frequency": "systemic",
        "impact": "preventive_failure"
      }
    ]
  },
  "chaos_analysis": {
    "chaos_factors": [
      {
        "factor": "ralph_wiggum_effect",
        "description": "Unexpected interaction between unrelated skills",
        "chaos_level": 0.8,
        "pattern": "unintended_skill_interaction"
      },
      {
        "factor": "butterfly_effect",
        "description": "Small configuration change causing large system impact",
        "chaos_level": 0.6,
        "pattern": "configuration_sensitivity"
      }
    ],
    "chaos_patterns": [
      "unintended_skill_coupling",
      "configuration_sensitivity",
      "load_distribution_anomalies"
    ],
    "chaos_mitigation": [
      {
        "strategy": "skill_isolation",
        "priority": "high",
        "implementation": "Implement strict skill isolation boundaries",
        "expected_impact": "reduce_chaos_propagation"
      },
      {
        "strategy": "configuration_validation",
        "priority": "medium",
        "implementation": "Add comprehensive configuration validation",
        "expected_impact": "prevent_butterfly_effects"
      }
    ]
  },
  "prevention_strategies": [
    {
      "strategy_type": "immediate",
      "priority": "critical",
      "strategy": "Implement memory limits and monitoring",
      "implementation": "Add memory usage limits and real-time monitoring",
      "expected_impact": "prevent_resource_exhaustion",
      "implementation_time": "1_week"
    },
    {
      "strategy_type": "medium_term",
      "priority": "high",
      "strategy": "Add circuit breakers to critical operations",
      "implementation": "Implement circuit breaker pattern for cache operations",
      "expected_impact": "prevent_cascading_failures",
      "implementation_time": "2_weeks"
    },
    {
      "strategy_type": "long_term",
      "priority": "medium",
      "strategy": "Improve system observability",
      "implementation": "Enhance monitoring and alerting systems",
      "expected_impact": "early_failure_detection",
      "implementation_time": "1_month"
    }
  ],
  "improvement_recommendations": [
    {
      "recommendation": "Implement comprehensive resource management",
      "priority": "high",
      "details": "Add resource limits, monitoring, and automatic scaling",
      "expected_outcome": "prevent_resource_exhaustion_failures"
    },
    {
      "recommendation": "Enhance skill isolation mechanisms",
      "priority": "medium",
      "details": "Implement strict boundaries between skill interactions",
      "expected_outcome": "reduce_chaos_propagation"
    },
    {
      "recommendation": "Improve failure detection and response",
      "priority": "medium",
      "details": "Add real-time failure detection and automated response",
      "expected_outcome": "reduce_failure_impact_and_duration"
    }
  ]
}
```

## Configuration Options

- `analysis_depth`: shallow, medium, deep (default: deep)
- `chaos_detection_level`: basic, advanced, expert (default: advanced)
- `pattern_recognition_window`: 1_week, 1_month, 3_months (default: 1_month)
- `prevention_strategy_focus`: immediate, balanced, comprehensive (default: balanced)
- `chaos_injection_level`: none, light, heavy (default: heavy)

## Constraints

- **Hard Rules**: 
  - Never stop at surface-level causes, always dig deeper
  - Always consider multiple contributing factors
  - Maintain objectivity in root cause identification
- **Safety Requirements**: 
  - Document all analysis assumptions and limitations
  - Use evidence-based reasoning for all conclusions
  - Consider both technical and operational factors
- **Quality Standards**: 
  - Provide actionable root cause analysis
  - Include both immediate and systemic solutions
  - Identify patterns for future prevention

## Error Handling

- **Incomplete Failure Data**: Use statistical inference and pattern matching
- **Conflicting Evidence**: Provide multiple hypotheses with confidence levels
- **Missing System State**: Flag for manual investigation and data collection
- **Analysis Uncertainty**: Document uncertainty levels and recommend verification

## Performance Optimization

- **Parallel Analysis**: Analyze multiple failure aspects concurrently
- **Incremental Processing**: Process large failure datasets in chunks
- **Caching**: Cache analysis results for similar failure patterns
- **Pattern Recognition**: Use machine learning for failure pattern detection

## Integration Examples

### With Agent Ecosystem
```python
# Integrate root cause analysis into failure response
root_causer = FailureRootCauser()
analysis_report = root_causer.analyze_failure(
    failure_id="system_failure_2026_03_03_001",
    analysis_depth="deep"
)
```

### With MCP Server
```python
@tool(name="failure_root_causer")
def analyze_failure_root_cause(failure_id: str, analysis_depth: str = "medium") -> dict:
    causer = FailureRootCauser()
    return causer.analyze_failure(failure_id, analysis_depth)
```

## Best Practices

- **Comprehensive Investigation**: Always investigate beyond surface symptoms
- **Multiple Perspectives**: Consider technical, operational, and systemic factors
- **Evidence-Based Analysis**: Base conclusions on concrete evidence and data
- **Pattern Recognition**: Look for recurring patterns and systemic issues
- **Actionable Recommendations**: Provide specific, implementable solutions

## Troubleshooting

- **Insufficient Data**: Implement improved data collection for future analysis
- **Complex Dependencies**: Use dependency visualization and analysis tools
- **Conflicting Evidence**: Document all hypotheses with supporting evidence
- **Analysis Overload**: Prioritize analysis based on impact and frequency

## Monitoring and Metrics

- **Root Cause Accuracy**: Success rate of identified root causes
- **Analysis Coverage**: Percentage of failures subjected to root cause analysis
- **Prevention Success Rate**: Percentage of prevented failures through implemented recommendations
- **Pattern Detection Rate**: Number of systemic issues identified per analysis period
- **Analysis Turnaround Time**: Time from failure to complete root cause analysis

## Dependencies

- **Required Skills**: Root cause analysis, system diagnostics, pattern recognition
- **Required Tools**: Python with analysis libraries, log parsing tools, visualization
- **Required Files**: Failure logs, system metrics, dependency graphs, performance data

## Version History

- **1.0.0**: Initial release with core root cause analysis and pattern recognition
- **1.1.0**: Added Ralph Wiggum chaos integration for creative failure analysis
- **1.2.0**: Integrated real-time monitoring and automated failure detection

## License

MIT

## Description

The Failure Root Causer skill specializes in comprehensive root cause analysis of skill failures using advanced forensic techniques and Ralph Wiggum-style chaotic creativity. By applying systematic analysis methods and chaos-driven investigation, this skill identifies underlying causes, contributing factors, and systemic issues that lead to failures in agent ecosystems.

The skill implements specialized algorithms for analyzing failure patterns, identifying root causes, and recognizing systemic issues. It goes beyond simple error identification to provide deep understanding of failure mechanisms and their prevention.

This skill is essential for maintaining high reliability and continuous improvement in complex agent ecosystems, providing the tools needed to systematically investigate and prevent failures through comprehensive root cause analysis.

## Workflow

1. **Failure Assessment**: Assess failure scope, impact, and available data
2. **Evidence Collection**: Gather all relevant failure data and system information
3. **Root Cause Analysis**: Apply systematic analysis to identify underlying causes
4. **Pattern Recognition**: Identify recurring patterns and systemic issues
5. **Chaos Analysis**: Analyze Ralph Wiggum-style chaotic and unexpected factors
6. **Prevention Strategy**: Develop comprehensive prevention and improvement strategies
7. **Knowledge Integration**: Update organizational knowledge with lessons learned

## Examples

### Example 1: Memory Leak Investigation
**Scenario**: Gradual performance degradation over weeks with unknown cause
**Process**: Analyze memory usage patterns, identify leak sources, trace root cause
**Result**: Discovered memory leak in caching layer, implemented memory management improvements

### Example 2: Cascading Failure Analysis
**Scenario**: Single skill failure caused system-wide outage
**Process**: Trace failure propagation, identify root cause and contributing factors
**Result**: Identified missing circuit breakers and resource management issues, implemented comprehensive prevention measures

## Asset Dependencies

- **Scripts**: root_cause_analyzer_core.py, pattern_detector.py, prevention_planner.py
- **Templates**: root_cause_analysis_schema.json, prevention_strategy_template.json
- **Reference Data**: Failure pattern databases, root cause analysis methodologies
- **Tools**: Python analysis libraries, log parsing tools, dependency visualization

## Ralph Wiggum Chaos Integration

This skill includes Ralph Wiggum-style chaotic creativity injection:

- **Unexpected Root Causes**: Discover root causes through chaotic failure simulation
- **Creative Pattern Analysis**: Use entropy to identify non-obvious failure patterns
- **Chaos-Driven Investigation**: Apply randomization to find hidden contributing factors
- **Randomized Analysis Paths**: Explore root cause analysis from unexpected angles

The chaos engine enhances traditional root cause analysis by introducing creative approaches to failure investigation while maintaining scientific rigor and accuracy.