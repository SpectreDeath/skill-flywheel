---
Domain: EPIDEMIOLOGY
Version: 1.0.0
Type: Algorithm
Category: Dependency Mapping
Complexity: Advanced
Estimated Execution Time: 3-7 minutes
name: contact_tracing_engine
---

# SKILL: Contact Tracing Engine


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

Map and analyze skill dependencies and interactions within agent ecosystems using epidemiological contact tracing principles. This skill identifies transmission pathways, super-spreader skills, and potential failure cascades to enable proactive risk management and optimized skill deployment strategies.

## When to Use

- Analyzing skill dependency networks for risk assessment
- Identifying critical skills that could cause system-wide failures
- Tracing skill interaction patterns and influence chains
- Optimizing skill isolation strategies during system maintenance
- Investigating skill performance degradation root causes

## When NOT to Use

- Simple systems with minimal skill interactions
- When immediate tactical fixes are needed over systemic analysis
- Systems with complete skill isolation (no dependencies)
- Time-critical emergency situations requiring immediate action

## Inputs

- **Required**: Skill dependency graph and interaction logs
- **Required**: Agent skill usage patterns and frequency data
- **Required**: Historical failure and performance incident data
- **Optional**: Skill execution timing and resource consumption metrics
- **Optional**: Agent trust and collaboration networks
- **Assumptions**: Skills interact through defined interfaces, dependencies can be traced, failure patterns are detectable

## Outputs

- **Primary**: Contact tracing map showing skill interaction pathways
- **Secondary**: Risk assessment with super-spreader skill identification
- **Tertiary**: Quarantine and isolation recommendations for high-risk scenarios
- **Format**: JSON structure with dependency graphs, risk scores, and intervention strategies

## Capabilities

1. **Transmission Pathway Analysis**: Map how skills influence and depend on each other
2. **Super-Spreader Identification**: Identify skills with disproportionate ecosystem impact
3. **Failure Cascade Prediction**: Model potential domino effects from skill failures
4. **Contact Network Visualization**: Generate interactive dependency graphs
5. **Risk-Based Quarantine**: Recommend isolation strategies for high-risk skills

## Usage Examples

### Example 1: System Maintenance Planning

**Context**: Planning maintenance window for critical authentication skill
**Input**: 
```
Dependency graph: 150 skills, 450 dependencies
Super-spreader skills: auth_manager (affects 89% of ecosystem)
Historical failure data: 12 incidents in past 6 months
```
**Output**: Quarantine strategy minimizing system impact during maintenance

### Example 2: Performance Degradation Investigation

**Context**: Investigating root cause of system-wide performance issues
**Input**: Performance logs, skill execution patterns, dependency chains
**Output**: Contact tracing report identifying source skill and affected downstream skills

## Input Format

- **Dependency Graph**: JSON object with skill nodes and directed edges
- **Interaction Logs**: Time-series data of skill calls and dependencies
- **Performance Metrics**: Response times, error rates, resource usage per skill
- **Failure Incidents**: Historical data on skill failures and their impacts

## Output Format

```json
{
  "contact_map": {
    "nodes": [
      {"id": "auth_manager", "type": "super_spreader", "risk_score": 0.95},
      {"id": "data_processor", "type": "connector", "risk_score": 0.65}
    ],
    "edges": [
      {"source": "auth_manager", "target": "data_processor", "weight": 0.8},
      {"source": "data_processor", "target": "report_generator", "weight": 0.3}
    ]
  },
  "risk_assessment": {
    "super_spreaders": ["auth_manager", "config_loader"],
    "vulnerable_skills": ["report_generator", "notification_service"],
    "cascade_risk": 0.72,
    "isolation_recommendations": [
      {
        "skill": "auth_manager",
        "quarantine_strategy": "blue_green_deployment",
        "impact_reduction": 0.85
      }
    ]
  },
  "intervention_timeline": [
    {
      "phase": "detection",
      "skills_affected": 15,
      "time_to_isolate": "2 minutes"
    },
    {
      "phase": "containment", 
      "skills_affected": 45,
      "time_to_isolate": "15 minutes"
    }
  ]
}
```

## Configuration Options

- `trace_depth`: Maximum dependency chain depth to analyze (default: 5)
- `risk_threshold`: Minimum risk score for intervention (default: 0.7)
- `time_window`: Historical data window for analysis (default: 30 days)
- `isolation_strategy`: aggressive, moderate, or conservative (default: moderate)
- `visualization_enabled`: Generate interactive graphs (default: true)

## Constraints

- **Hard Rules**: 
  - Never isolate skills critical for system operation
  - Maintain minimum service availability during interventions
  - Preserve skill execution order where dependencies exist
- **Safety Requirements**: 
  - Validate isolation strategies before implementation
  - Monitor for unintended side effects during quarantine
  - Maintain rollback capabilities for all interventions
- **Quality Standards**: 
  - Provide confidence intervals for risk assessments
  - Include alternative intervention strategies
  - Document assumptions and limitations

## Error Handling

- **Incomplete Dependency Data**: Use probabilistic inference for missing connections
- **Circular Dependencies**: Detect and flag cycles with suggested resolution strategies
- **Data Quality Issues**: Implement data validation and cleaning procedures
- **Model Uncertainty**: Provide conservative estimates when confidence is low

## Performance Optimization

- **Graph Algorithms**: Use efficient algorithms for large-scale dependency analysis
- **Incremental Updates**: Update contact maps as new interaction data arrives
- **Caching**: Store frequently accessed dependency paths and risk calculations
- **Parallel Processing**: Analyze multiple skill chains concurrently

## Integration Examples

### With Agent Ecosystem
```python
# Integrate contact tracing into skill management
tracer = ContactTracingEngine()
risk_map = tracer.analyze_dependencies(
    skill_graph=current_dependencies,
    interaction_logs=recent_activity
)
```

### With MCP Server
```python
@tool(name="contact_tracing_engine")
def trace_skill_dependencies(dependency_graph: dict, risk_threshold: float = 0.7) -> dict:
    tracer = ContactTracingEngine()
    return tracer.trace_dependencies(dependency_graph, risk_threshold)
```

## Best Practices

- **Continuous Monitoring**: Update contact maps in real-time as skills interact
- **Risk-Based Prioritization**: Focus on high-impact skills first
- **Collaborative Analysis**: Involve skill owners in tracing and intervention planning
- **Documentation**: Maintain clear records of dependency relationships and changes
- **Testing**: Validate isolation strategies in staging environments

## Troubleshooting

- **Missing Dependencies**: Use statistical inference to estimate unknown connections
- **Performance Issues**: Optimize graph traversal algorithms for large ecosystems
- **False Positives**: Implement validation procedures for risk assessments
- **Stale Data**: Establish data freshness requirements and monitoring

## Monitoring and Metrics

- **Contact Rate**: Number of skill interactions per time period
- **Transmission Probability**: Likelihood of failure propagation between skills
- **Isolation Effectiveness**: Success rate of quarantine interventions
- **Ecosystem Resilience**: System recovery time after skill failures
- **False Positive Rate**: Accuracy of risk predictions

## Dependencies

- **Required Skills**: Graph theory, dependency analysis, risk assessment
- **Required Tools**: Python with networkx, graph visualization libraries, time-series analysis
- **Required Files**: Skill dependency definitions, interaction logs, performance metrics

## Version History

- **1.0.0**: Initial release with core contact tracing and risk assessment
- **1.1.0**: Added super-spreader detection and quarantine strategies
- **1.2.0**: Integrated real-time monitoring and predictive analytics

## License

MIT

## Description

The Contact Tracing Engine skill applies epidemiological contact tracing principles to agent skill ecosystems. By mapping how skills interact, depend on, and influence each other, this skill enables proactive identification of potential failure points and optimization of skill deployment strategies.

The skill implements advanced graph analysis algorithms to identify super-spreader skills (those with disproportionate ecosystem impact), trace transmission pathways for failures or performance issues, and recommend targeted quarantine strategies. This approach is particularly valuable in complex agent ecosystems where understanding interdependencies is crucial for maintaining system reliability and performance.

This skill transforms reactive incident response into proactive risk management by providing early warning systems and strategic intervention capabilities.

## Workflow

1. **Data Collection**: Gather skill dependency graphs and interaction logs
2. **Network Analysis**: Identify critical nodes, super-spreaders, and transmission paths
3. **Risk Assessment**: Calculate failure probabilities and impact assessments
4. **Intervention Planning**: Develop quarantine and isolation strategies
5. **Implementation**: Execute targeted interventions with monitoring
6. **Validation**: Measure intervention effectiveness and update models

## Examples

### Example 1: Critical Infrastructure Protection
**Scenario**: Protecting financial transaction processing from skill failures
**Process**: Map all dependencies, identify super-spreader skills, implement targeted monitoring
**Result**: 90% reduction in cascading failures, faster incident response

### Example 2: Development Environment Optimization
**Scenario**: Optimizing CI/CD pipeline skill dependencies
**Process**: Trace build and deployment skill interactions, identify bottlenecks
**Result**: 40% faster pipeline execution, improved reliability

## Asset Dependencies

- **Scripts**: contact_tracer_core.py, dependency_analyzer.py, risk_calculator.py
- **Templates**: dependency_graph_schema.json, interaction_log_format.json
- **Reference Data**: Graph theory algorithms, epidemiological modeling techniques
- **Tools**: Python networkx, graph visualization, time-series analysis libraries