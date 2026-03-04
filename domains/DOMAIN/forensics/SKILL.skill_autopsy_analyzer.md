---
Domain: FORENSICS
Version: 1.0.0
Type: Algorithm
Category: Post-Mortem Analysis
Complexity: Advanced
Estimated Execution Time: 3-8 minutes
name: skill_autopsy_analyzer
---

# SKILL: Skill Autopsy Analyzer

## Purpose

Perform comprehensive post-mortem analysis of failed or underperforming skills to determine root causes, identify patterns, and extract lessons for future skill development. This skill applies forensic pathology principles to skill ecosystems for systematic failure analysis and improvement recommendations.

## When to Use

- Investigating skill failures and performance degradation
- Analyzing skill lifecycle termination and retirement reasons
- Identifying systemic issues in skill development practices
- Learning from skill failures to improve future development
- Investigating skill interactions that led to system failures

## When NOT to Use

- For skills that are currently functioning properly
- When immediate skill replacement is needed over analysis
- For trivial failures with obvious causes
- When time constraints prevent thorough investigation

## Inputs

- **Required**: Failed skill artifacts and execution logs
- **Required**: Performance metrics and error reports
- **Required**: Skill interaction and dependency data
- **Optional**: Development history and version control data
- **Optional**: User feedback and usage patterns
- **Assumptions**: Skill failures can be systematically analyzed, logs contain sufficient detail, dependencies are traceable

## Outputs

- **Primary**: Comprehensive autopsy report with cause of death analysis
- **Secondary**: Pattern recognition report identifying systemic issues
- **Tertiary**: Improvement recommendations and preventive measures
- **Format**: JSON structure with findings, analysis, and actionable recommendations

## Capabilities

1. **Failure Analysis**: Systematic investigation of skill failure causes
2. **Pattern Recognition**: Identify recurring failure patterns across skills
3. **Dependency Analysis**: Trace failure propagation through skill networks
4. **Performance Forensics**: Analyze performance degradation over time
5. **Lessons Learned**: Extract actionable insights for future development

## Usage Examples

### Example 1: Authentication Skill Failure

**Context**: Critical authentication skill failed during peak usage
**Input**: 
```
Failed skill: auth_manager_v3.2.1
Error logs: 1500+ error entries over 2 hours
Performance data: Response time increased 300% before failure
Dependencies: 12 dependent skills affected
```
**Output**: Autopsy report identifying memory leak as root cause with prevention recommendations

### Example 2: System-Wide Performance Degradation

**Context**: Multiple skills showing performance issues over time
**Input**: Performance metrics, dependency graphs, usage patterns
**Output**: Pattern analysis revealing cascading performance failures

## Input Format

- **Skill Artifacts**: Source code, configuration files, deployment manifests
- **Execution Logs**: Error messages, stack traces, performance metrics
- **Interaction Data**: Dependency graphs, call patterns, resource usage
- **Context Information**: Development history, deployment timeline, user feedback

## Output Format

```json
{
  "autopsy_report": {
    "skill_id": "auth_manager_v3.2.1",
    "failure_timestamp": "2026-03-03T14:30:00Z",
    "failure_type": "catastrophic",
    "cause_of_death": {
      "primary_cause": "memory_leak",
      "secondary_cause": "resource_exhaustion",
      "contributing_factors": [
        "increased_load",
        "insufficient_monitoring",
        "lack_of_circuit_breaker"
      ]
    },
    "timeline_analysis": {
      "onset": "2026-03-03T12:00:00Z",
      "progression": "gradual_performance_degradation",
      "failure_point": "2026-03-03T14:30:00Z",
      "duration": "2.5_hours"
    },
    "impact_assessment": {
      "affected_skills": 12,
      "user_impact": "high",
      "system_impact": "critical",
      "financial_impact": "estimated_50000_usd"
    }
  },
  "pattern_analysis": {
    "failure_patterns": [
      {
        "pattern": "memory_leak_in_long_running_skills",
        "frequency": "3_occurrences_in_6_months",
        "affected_skills": ["auth_manager", "data_processor", "cache_service"],
        "common_factors": ["lack_of_memory_monitoring", "insufficient_cleanup"]
      }
    ],
    "systemic_issues": [
      "inadequate_performance_monitoring",
      "missing_circuit_breakers",
      "insufficient_load_testing"
    ]
  },
  "improvement_recommendations": [
    {
      "priority": "high",
      "recommendation": "Implement memory monitoring and alerts",
      "implementation": "Add memory usage metrics and automated alerts",
      "expected_impact": "prevent_future_memory_leaks"
    },
    {
      "priority": "medium",
      "recommendation": "Add circuit breakers to critical skills",
      "implementation": "Implement circuit breaker pattern for auth_manager",
      "expected_impact": "prevent_cascading_failures"
    },
    {
      "priority": "low",
      "recommendation": "Improve load testing procedures",
      "implementation": "Add comprehensive load testing to CI/CD pipeline",
      "expected_impact": "identify_performance_issues_earlier"
    }
  ],
  "lessons_learned": [
    "Memory leaks in long-running skills require proactive monitoring",
    "Circuit breakers are essential for preventing cascading failures",
    "Performance testing should include memory usage analysis"
  ]
}
```

## Configuration Options

- `analysis_depth`: shallow, medium, deep (default: deep)
- `pattern_recognition_window`: 30_days, 90_days, 1_year (default: 90_days)
- `impact_assessment_level`: basic, detailed, comprehensive (default: detailed)
- `recommendation_priority`: all, high_only, critical_only (default: all)
- `chaos_injection_level`: none, light, heavy (default: light)

## Constraints

- **Hard Rules**: 
  - Never modify original skill artifacts during analysis
  - Always preserve evidence for potential legal proceedings
  - Maintain objectivity in failure analysis
- **Safety Requirements**: 
  - Isolate failed skills before analysis to prevent further damage
  - Use read-only access to production artifacts
  - Document all analysis procedures for reproducibility
- **Quality Standards**: 
  - Provide root cause analysis, not just symptoms
  - Include actionable recommendations with implementation guidance
  - Identify both immediate fixes and long-term improvements

## Error Handling

- **Incomplete Logs**: Use statistical inference to fill gaps in analysis
- **Corrupted Artifacts**: Implement artifact recovery and reconstruction
- **Missing Dependencies**: Flag for manual investigation and documentation
- **Analysis Conflicts**: Provide multiple hypotheses with confidence levels

## Performance Optimization

- **Parallel Analysis**: Analyze multiple failure aspects concurrently
- **Incremental Processing**: Process large log files in chunks
- **Caching**: Cache analysis results for similar failure patterns
- **Compression**: Compress large artifact files during analysis

## Integration Examples

### With Agent Ecosystem
```python
# Integrate autopsy analysis into skill management
autopsy_analyzer = SkillAutopsyAnalyzer()
analysis_report = autopsy_analyzer.analyze_failure(
    failed_skill="auth_manager_v3.2.1",
    analysis_depth="deep"
)
```

### With MCP Server
```python
@tool(name="skill_autopsy_analyzer")
def analyze_skill_failure(skill_id: str, analysis_depth: str = "deep") -> dict:
    analyzer = SkillAutopsyAnalyzer()
    return analyzer.analyze_failure(skill_id, analysis_depth)
```

## Best Practices

- **Comprehensive Documentation**: Document all analysis steps and findings
- **Root Cause Focus**: Go beyond symptoms to identify underlying causes
- **Pattern Recognition**: Look for recurring issues across multiple failures
- **Actionable Recommendations**: Provide specific, implementable suggestions
- **Continuous Learning**: Update analysis procedures based on new findings

## Troubleshooting

- **Insufficient Data**: Implement data collection improvements for future analysis
- **Complex Dependencies**: Use dependency visualization tools for clarity
- **Conflicting Evidence**: Document all hypotheses with supporting evidence
- **Analysis Overload**: Prioritize analysis based on impact and frequency

## Monitoring and Metrics

- **Analysis Coverage**: Percentage of failures subjected to autopsy analysis
- **Root Cause Accuracy**: Success rate of identified root causes
- **Recommendation Implementation**: Percentage of recommendations actually implemented
- **Pattern Detection Rate**: Number of systemic issues identified per analysis period
- **Analysis Turnaround Time**: Time from failure to complete analysis

## Dependencies

- **Required Skills**: Forensic analysis, system diagnostics, pattern recognition
- **Required Tools**: Python with analysis libraries, log parsing tools, visualization
- **Required Files**: Skill artifacts, execution logs, dependency graphs, performance metrics

## Version History

- **1.0.0**: Initial release with core autopsy analysis and pattern recognition
- **1.1.0**: Added Ralph Wiggum chaos integration for creative failure analysis
- **1.2.0**: Integrated real-time monitoring and automated failure detection

## License

MIT

## Description

The Skill Autopsy Analyzer skill applies forensic pathology principles to failed skills within agent ecosystems. By conducting systematic post-mortem analysis, this skill identifies root causes of failures, recognizes patterns across multiple incidents, and extracts actionable lessons for improving future skill development.

The skill implements advanced analysis algorithms to examine skill artifacts, execution logs, and performance data to determine the exact cause of failure. It goes beyond simple error identification to provide comprehensive understanding of failure mechanisms and their systemic implications.

This skill transforms reactive failure response into proactive improvement by systematically learning from each failure and preventing similar issues in the future. It's essential for maintaining high reliability and continuous improvement in complex agent ecosystems.

## Workflow

1. **Failure Collection**: Gather all relevant artifacts and data from failed skill
2. **Evidence Preservation**: Secure and document all evidence for analysis
3. **Systematic Analysis**: Examine failure from multiple angles (code, logs, dependencies)
4. **Root Cause Identification**: Determine primary and contributing causes
5. **Pattern Recognition**: Identify systemic issues and recurring problems
6. **Recommendation Generation**: Create actionable improvement suggestions
7. **Knowledge Integration**: Update organizational knowledge base with lessons learned

## Examples

### Example 1: Database Connection Failure
**Scenario**: Database connection skill failed during high-traffic period
**Process**: Analyze connection patterns, error logs, and resource usage
**Result**: Identified connection pool exhaustion as root cause, implemented connection pooling improvements

### Example 2: Cascading System Failure
**Scenario**: Single skill failure caused system-wide outage
**Process**: Trace failure propagation through dependency network
**Result**: Discovered missing circuit breakers, implemented comprehensive failure isolation

## Asset Dependencies

- **Scripts**: autopsy_analyzer_core.py, pattern_recognizer.py, recommendation_engine.py
- **Templates**: failure_analysis_schema.json, autopsy_report_template.json
- **Reference Data**: Failure pattern databases, best practice guidelines
- **Tools**: Python analysis libraries, log parsing tools, dependency visualization

## Ralph Wiggum Chaos Integration

This skill includes Ralph Wiggum-style chaotic creativity injection:

- **Unexpected Failure Scenarios**: Discover failure modes through chaotic simulation
- **Creative Root Cause Analysis**: Use entropy to identify non-obvious failure causes
- **Chaos-Driven Pattern Recognition**: Apply randomization to find hidden failure patterns
- **Randomized Investigation Paths**: Explore failure analysis from unexpected angles

The chaos engine enhances traditional autopsy analysis by introducing creative approaches to failure investigation while maintaining scientific rigor and accuracy.