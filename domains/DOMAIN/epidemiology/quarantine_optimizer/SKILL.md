---
Domain: EPIDEMIOLOGY
Version: 1.0.0
Type: Algorithm
Category: Fault Isolation
Complexity: Advanced
Estimated Execution Time: 2-6 minutes
name: quarantine_optimizer
---

# SKILL: Quarantine Optimizer


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

Optimize MCP tool quarantine strategies in agent ecosystems using epidemiological isolation principles. This skill analyzes fault propagation patterns, identifies optimal isolation boundaries, and implements targeted quarantine measures to prevent system-wide failures while maintaining operational continuity.

## When to Use

- Implementing fault isolation for malfunctioning MCP tools
- Designing quarantine strategies for system maintenance windows
- Analyzing fault propagation patterns in agent tool ecosystems
- Optimizing isolation boundaries to minimize operational impact
- Managing cascading failure scenarios in distributed agent systems

## When NOT to Use

- Single-tool systems with no interdependencies
- Emergency situations requiring immediate full system shutdown
- When quarantine would cause more damage than the fault itself
- Systems with complete tool isolation already in place

## Inputs

- **Required**: MCP tool dependency graph and fault propagation patterns
- **Required**: Current system state and tool health metrics
- **Required**: Operational impact data for different quarantine scenarios
- **Optional**: Historical fault isolation effectiveness data
- **Optional**: Agent workload distribution and critical path analysis
- **Assumptions**: Faults can propagate through tool dependencies, quarantine boundaries can be defined, operational impact can be quantified

## Outputs

- **Primary**: Optimized quarantine strategy with isolation boundaries
- **Secondary**: Fault containment probability and operational impact assessment
- **Tertiary**: Quarantine implementation timeline and rollback procedures
- **Format**: JSON structure with quarantine plans, impact analysis, and implementation procedures

## Capabilities

1. **Fault Propagation Analysis**: Map how failures spread through MCP tool dependencies
2. **Quarantine Boundary Optimization**: Identify minimal isolation zones for maximum protection
3. **Impact Assessment**: Quantify operational consequences of different quarantine strategies
4. **Containment Probability**: Calculate likelihood of successful fault isolation
5. **Rollback Planning**: Develop procedures for safe quarantine termination

## Usage Examples

### Example 1: Malfunctioning Tool Isolation

**Context**: Isolating faulty authentication tool affecting 200-agent system
**Input**: 
```
Fault propagation: 15 tools affected in 3 dependency layers
Critical operations: 45% of system functions dependent on affected tools
Quarantine options: partial (layer 1), moderate (layers 1-2), full (all layers)
```
**Output**: Optimized quarantine strategy isolating 60% of fault with only 15% operational impact

### Example 2: Maintenance Window Planning

**Context**: Planning system maintenance requiring temporary tool isolation
**Input**: Maintenance requirements, tool dependencies, critical operation timing
**Output**: Quarantine schedule minimizing disruption to critical workflows

## Input Format

- **Dependency Graph**: JSON object with tool nodes and fault propagation edges
- **Health Metrics**: Current tool status, fault indicators, and performance data
- **Impact Data**: Operational consequences of isolating different tool groups
- **Historical Data**: Past quarantine effectiveness and fault patterns

## Output Format

```json
{
  "quarantine_strategy": {
    "isolation_boundaries": [
      {
        "boundary_id": "zone_1",
        "tools_included": ["auth_manager", "session_handler"],
        "fault_containment_probability": 0.85,
        "operational_impact": 0.15
      },
      {
        "boundary_id": "zone_2", 
        "tools_included": ["data_processor", "cache_manager"],
        "fault_containment_probability": 0.92,
        "operational_impact": 0.08
      }
    ],
    "optimization_target": "minimal_impact_with_max_containment",
    "strategy_effectiveness": 0.88
  },
  "implementation_timeline": [
    {
      "phase": "detection",
      "duration": "30 seconds",
      "actions": ["monitor_fault_signals", "identify_affected_tools"]
    },
    {
      "phase": "isolation",
      "duration": "2 minutes", 
      "actions": ["activate_quarantine_zones", "redirect_traffic"]
    },
    {
      "phase": "stabilization",
      "duration": "10 minutes",
      "actions": ["monitor_containment", "adjust_boundaries"]
    }
  ],
  "rollback_procedures": [
    {
      "step": 1,
      "action": "verify_fault_resolution",
      "criteria": "no_fault_signals_for_5_minutes",
      "rollback_time": "immediate"
    },
    {
      "step": 2,
      "action": "gradual_tool_reactivation",
      "criteria": "monitor_performance_metrics",
      "rollback_time": "5_minutes"
    }
  ],
  "risk_assessment": {
    "containment_failure_probability": 0.08,
    "operational_disruption_score": 0.15,
    "recovery_time_estimate": "15 minutes",
    "recommendations": ["staggered_reactivation", "enhanced_monitoring"]
  }
}
```

## Configuration Options

- `optimization_strategy`: minimal_impact, maximum_containment, or balanced (default: balanced)
- `quarantine_speed`: aggressive, moderate, or conservative (default: moderate)
- `impact_threshold`: Maximum acceptable operational impact (default: 0.25)
- `containment_target`: Minimum fault containment probability (default: 0.80)
- `rollback_automation`: Enable automatic rollback procedures (default: true)

## Constraints

- **Hard Rules**: 
  - Never quarantine tools critical for system survival
  - Maintain minimum service levels during quarantine operations
  - Preserve data integrity and transaction consistency
- **Safety Requirements**: 
  - Validate quarantine boundaries before implementation
  - Monitor for unintended side effects during isolation
  - Maintain communication channels during quarantine
- **Quality Standards**: 
  - Provide confidence intervals for containment probabilities
  - Include alternative quarantine strategies
  - Document rollback procedures and recovery timelines

## Error Handling

- **Incomplete Dependency Data**: Use probabilistic inference for unknown fault propagation paths
- **Real-time Fault Changes**: Implement adaptive quarantine boundary adjustments
- **Quarantine Failure**: Activate emergency containment procedures
- **System Instability**: Implement conservative fallback isolation strategies

## Performance Optimization

- **Graph Analysis**: Use efficient algorithms for large-scale dependency analysis
- **Real-time Monitoring**: Implement streaming fault detection and quarantine activation
- **Parallel Processing**: Analyze multiple quarantine scenarios concurrently
- **Caching**: Store frequently accessed quarantine patterns and impact calculations

## Integration Examples

### With Agent Ecosystem
```python
# Integrate quarantine optimization into fault management
quarantine_optimizer = QuarantineOptimizer()
isolation_plan = quarantine_optimizer.optimize_quarantine(
    fault_tools=affected_tools,
    dependency_graph=tool_dependencies
)
```

### With MCP Server
```python
@tool(name="quarantine_optimizer")
def optimize_mcp_quarantine(fault_data: dict, impact_threshold: float = 0.25) -> dict:
    optimizer = QuarantineOptimizer()
    return optimizer.optimize_quarantine(fault_data, impact_threshold)
```

## Best Practices

- **Proactive Monitoring**: Implement continuous fault detection and early warning systems
- **Gradual Implementation**: Test quarantine boundaries incrementally
- **Communication**: Maintain clear communication during quarantine operations
- **Documentation**: Record all quarantine decisions and their outcomes
- **Testing**: Validate quarantine strategies in staging environments

## Troubleshooting

- **Incomplete Containment**: Analyze fault propagation paths and adjust boundaries
- **Excessive Impact**: Optimize quarantine scope to reduce operational disruption
- **Rollback Failures**: Review rollback procedures and implement manual overrides
- **False Positives**: Improve fault detection accuracy to reduce unnecessary quarantines

## Monitoring and Metrics

- **Containment Success Rate**: Percentage of faults successfully isolated
- **Operational Impact**: Measured disruption during quarantine operations
- **Recovery Time**: Time to restore normal operations after quarantine
- **False Positive Rate**: Percentage of unnecessary quarantines
- **System Stability**: Overall system performance during and after quarantine

## Dependencies

- **Required Skills**: Fault analysis, system architecture, operational management
- **Required Tools**: Python with graph analysis libraries, real-time monitoring systems
- **Required Files**: Tool dependency definitions, fault propagation patterns, impact metrics

## Version History

- **1.0.0**: Initial release with core quarantine optimization and fault analysis
- **1.1.0**: Added real-time monitoring and adaptive quarantine boundaries
- **1.2.0**: Integrated automated rollback procedures and impact minimization

## License

MIT

## Description

The Quarantine Optimizer skill applies epidemiological isolation principles to MCP tool fault management in agent ecosystems. By analyzing how faults propagate through tool dependencies and implementing targeted quarantine measures, this skill enables proactive fault containment while minimizing operational disruption.

The skill implements advanced graph analysis algorithms to identify optimal isolation boundaries, calculate containment probabilities, and develop implementation strategies. It helps system administrators respond to tool failures with surgical precision, preventing cascading failures while maintaining critical system functions.

This approach transforms reactive fault response into proactive containment management, providing systematic procedures for isolating problematic tools while preserving system functionality and performance.

## Workflow

1. **Fault Detection**: Monitor MCP tools for fault indicators and propagation patterns
2. **Dependency Analysis**: Map tool relationships and potential fault spread paths
3. **Quarantine Planning**: Design optimal isolation boundaries and implementation strategies
4. **Impact Assessment**: Quantify operational consequences of different quarantine approaches
5. **Implementation**: Execute quarantine with real-time monitoring and adjustment
6. **Recovery**: Implement rollback procedures and restore normal operations

## Examples

### Example 1: Distributed System Fault Containment
**Scenario**: Containing database connection fault in 500-agent distributed system
**Process**: Analyze connection dependencies, implement targeted quarantine zones
**Result**: 95% fault containment with only 10% operational impact

### Example 2: Development Environment Maintenance
**Scenario**: Isolating testing tools during critical production maintenance
**Process**: Plan quarantine boundaries to minimize development disruption
**Result**: 100% production stability with 20% development impact

## Asset Dependencies

- **Scripts**: quarantine_planner.py, fault_analyzer.py, impact_calculator.py
- **Templates**: dependency_graph_schema.json, quarantine_plan_template.json
- **Reference Data**: Fault propagation algorithms, quarantine optimization techniques
- **Tools**: Python graph libraries, real-time monitoring systems, MCP server integration