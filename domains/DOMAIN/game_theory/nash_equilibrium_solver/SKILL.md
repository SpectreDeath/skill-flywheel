---
Domain: GAME THEORY
Version: 1.0.0
Type: Algorithm
Category: Strategic Analysis
Complexity: Advanced
Estimated Execution Time: 1-5 minutes
name: nash_equilibrium_solver
---

# SKILL: Nash Equilibrium Solver


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

Solve complex multi-agent coordination problems by finding Nash equilibria in strategic interactions. This skill analyzes payoff matrices, identifies stable strategy combinations, and provides actionable recommendations for optimal agent behavior in competitive and cooperative scenarios.

## When to Use

- Multi-agent systems with conflicting objectives
- Resource allocation conflicts between agents
- Strategic decision-making under uncertainty
- Validation gate conflicts requiring compromise solutions
- MCP tool selection optimization scenarios

## When NOT to Use

- Single-agent decision problems
- Scenarios with clear hierarchical authority
- Time-critical situations requiring immediate action
- When agents have identical, non-conflicting goals

## Inputs

- **Required**: Payoff matrix or strategic interaction description
- **Required**: Agent strategy sets and preferences
- **Optional**: Risk tolerance parameters
- **Optional**: Historical interaction data
- **Assumptions**: Rational agents with well-defined preferences

## Outputs

- **Primary**: Nash equilibrium identification with stability analysis
- **Secondary**: Alternative equilibrium candidates ranked by robustness
- **Format**: JSON structure with equilibrium strategies, payoffs, and confidence intervals

## Capabilities

1. **Equilibrium Detection**: Identify pure and mixed strategy Nash equilibria
2. **Stability Analysis**: Assess equilibrium robustness to parameter changes
3. **Multi-Agent Coordination**: Handle 2-10 agent strategic interactions
4. **Payoff Optimization**: Recommend strategy adjustments for improved outcomes
5. **Conflict Resolution**: Provide compromise solutions for validation gate conflicts

## Usage Examples

### Example 1: MCP Tool Allocation Conflict

**Context**: Two agents competing for limited MCP tool resources
**Input**: 
```
Agent A: {Tool1: 8, Tool2: 5, Tool3: 3}
Agent B: {Tool1: 4, Tool2: 7, Tool3: 6}
```
**Output**: Nash equilibrium showing optimal tool allocation strategy

### Example 2: Validation Gate Coordination

**Context**: Multiple agents with conflicting validation priorities
**Input**: Validation requirements with priority weights
**Output**: Equilibrium strategy balancing all validation needs

## Input Format

- **Payoff Matrix**: JSON object with agent strategies and corresponding utilities
- **Strategy Sets**: Array of available actions for each agent
- **Preferences**: Weighted importance of different outcomes
- **Constraints**: Hard limits on strategy combinations

## Output Format

```json
{
  "equilibria": [
    {
      "type": "pure|mixed",
      "strategies": {"agent1": "strategy", "agent2": "strategy"},
      "payoffs": {"agent1": value, "agent2": value},
      "stability": "high|medium|low",
      "confidence": 0.95
    }
  ],
  "recommendations": [
    "Strategy adjustment suggestions",
    "Alternative equilibrium analysis"
  ]
}
```

## Configuration Options

- `max_agents`: Maximum number of agents to analyze (default: 10)
- `precision`: Numerical precision for mixed strategy calculations (default: 0.001)
- `iterations`: Maximum iterations for convergence (default: 1000)
- `risk_tolerance`: Agent risk preferences (default: risk-neutral)

## Constraints

- **Hard Rules**: 
  - Never recommend strategies that violate system constraints
  - Always maintain computational tractability for real-time use
  - Preserve agent autonomy in strategy selection
- **Safety Requirements**: 
  - Validate all input matrices for mathematical consistency
  - Handle degenerate cases gracefully
- **Quality Standards**: 
  - Provide confidence intervals for all equilibrium claims
  - Include sensitivity analysis for key parameters

## Error Handling

- **Invalid Matrix**: Return detailed error description with suggested fixes
- **No Equilibrium**: Provide alternative solution concepts (Pareto optimality, etc.)
- **Convergence Issues**: Implement fallback algorithms with performance warnings
- **Memory Limits**: Scale down problem size with user notification

## Performance Optimization

- **Matrix Compression**: Use sparse matrix representations for large strategy spaces
- **Parallel Processing**: Distribute equilibrium calculations across available cores
- **Caching**: Store frequently accessed equilibrium solutions
- **Incremental Updates**: Update solutions when only minor parameter changes occur

## Integration Examples

### With flywheel_loop.py
```python
# Integrate Nash equilibrium analysis into flywheel optimization
equilibrium = nash_solver.analyze_coordination_conflicts(
    agent_strategies=current_strategies,
    payoff_matrix=performance_metrics
)
```

### With MCP Server
```python
# Register as MCP tool for real-time equilibrium analysis
@tool(name="nash_equilibrium_solver")
def solve_nash_equilibrium(payoff_matrix: dict) -> dict:
    return nash_solver.solve(payoff_matrix)
```

## Best Practices

- **Model Validation**: Always validate payoff matrices with domain experts
- **Sensitivity Analysis**: Test equilibrium stability under parameter variations
- **Communication**: Clearly explain equilibrium concepts to non-expert users
- **Documentation**: Maintain detailed records of strategic assumptions

## Troubleshooting

- **No Pure Strategy Equilibrium**: Check for mixed strategy solutions
- **Multiple Equilibria**: Use refinement concepts (trembling hand, subgame perfection)
- **Computational Complexity**: Consider approximate methods for large strategy spaces
- **Convergence Issues**: Verify matrix properties and adjust numerical parameters

## Monitoring and Metrics

- **Solution Quality**: Measure equilibrium stability and robustness
- **Computational Performance**: Track convergence time and memory usage
- **User Satisfaction**: Monitor adoption and effectiveness of recommendations
- **System Integration**: Verify seamless operation with existing workflows

## Dependencies

- **Required Skills**: Basic game theory understanding, matrix operations
- **Required Tools**: Python with numpy/scipy, optimization libraries
- **Required Files**: Payoff matrix templates, strategy definition schemas

## Version History

- **1.0.0**: Initial release with core Nash equilibrium detection
- **1.1.0**: Added mixed strategy support and stability analysis
- **1.2.0**: Integrated with MCP server and flywheel_loop.py

## License

MIT

## Description

The Nash Equilibrium Solver skill provides automated analysis of strategic interactions between multiple agents. It identifies stable strategy combinations where no agent can improve their outcome by unilaterally changing their strategy. This is particularly valuable in multi-agent systems where coordination conflicts arise, such as MCP tool allocation, validation gate coordination, and resource management scenarios.

The skill implements advanced algorithms for detecting both pure and mixed strategy Nash equilibria, providing confidence intervals and stability analysis for all solutions. It integrates seamlessly with the existing Skill Flywheel infrastructure, offering real-time strategic analysis capabilities.

## Workflow

1. **Input Validation**: Verify payoff matrix structure and agent strategy definitions
2. **Equilibrium Detection**: Apply mathematical algorithms to find Nash equilibria
3. **Stability Analysis**: Assess solution robustness to parameter changes
4. **Recommendation Generation**: Provide actionable strategy suggestions
5. **Output Formatting**: Deliver results in structured JSON format

## Examples

### Example 1: Resource Allocation
**Input**: Two agents competing for three resources with different valuations
**Process**: Analyze payoff matrix for equilibrium strategies
**Output**: Optimal allocation strategy with 95% confidence interval

### Example 2: Validation Coordination
**Input**: Multiple validation requirements with conflicting priorities
**Process**: Identify equilibrium validation strategy
**Output**: Balanced validation approach maximizing overall system quality

## Asset Dependencies

- **Scripts**: nash_solver_core.py, matrix_validator.py, equilibrium_analyzer.py
- **Templates**: payoff_matrix_template.json, strategy_definition_schema.json
- **Reference Data**: Game theory solution algorithms, optimization benchmarks
- **Tools**: Python scipy/numpy, optimization libraries, MCP server integration