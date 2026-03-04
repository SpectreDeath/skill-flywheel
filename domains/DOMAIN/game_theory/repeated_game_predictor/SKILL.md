---
Domain: GAME THEORY
Version: 1.0.0
Type: Algorithm
Category: Dynamic Strategy
Complexity: Advanced
Estimated Execution Time: 30 seconds - 3 minutes
name: repeated_game_predictor
---

# SKILL: Repeated Game Predictor


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

Analyze and optimize strategies for repeated interactions between agents where future consequences influence current decisions. This skill identifies optimal strategies for long-term cooperation, detects patterns in opponent behavior, and predicts future actions based on historical interaction data.

## When to Use

- Multi-agent systems with ongoing interactions and relationship building
- Flywheel optimization scenarios requiring long-term strategic planning
- Agent coordination requiring trust and reputation management
- Resource sharing systems with repeated allocation decisions
- Negotiation scenarios with multiple rounds and learning opportunities

## When NOT to Use

- One-shot games with no future interactions
- Single-agent optimization problems
- Scenarios where agents have no memory of past interactions
- Time-critical decisions requiring immediate action without analysis

## Inputs

- **Required**: Historical interaction data between agents
- **Required**: Payoff structures for different strategy combinations
- **Optional**: Agent discount factors for future rewards
- **Optional**: Learning rates and adaptation parameters
- **Assumptions**: Agents learn from past interactions and adapt strategies over time

## Outputs

- **Primary**: Optimal repeated game strategies with cooperation incentives
- **Secondary**: Predictive models of opponent future behavior
- **Format**: JSON structure with strategy recommendations, prediction confidence, and adaptation plans

## Capabilities

1. **Strategy Evolution**: Track how agent strategies evolve over repeated interactions
2. **Cooperation Analysis**: Identify conditions for sustained cooperation vs. defection
3. **Prediction Modeling**: Forecast opponent behavior based on historical patterns
4. **Adaptation Planning**: Design strategies that adapt to opponent learning
5. **Equilibrium Detection**: Find subgame perfect equilibria in repeated game scenarios

## Usage Examples

### Example 1: Flywheel Loop Optimization

**Context**: Repeated coordination decisions in flywheel_loop.py optimization cycles
**Input**: Historical coordination outcomes and agent performance data
**Output**: Optimal coordination strategy maximizing long-term system performance

### Example 2: Resource Sharing with Reputation

**Context**: Multiple agents repeatedly sharing computational resources
**Input**: Past resource allocation decisions and cooperation patterns
**Output**: Strategy promoting fair sharing with punishment for defection

## Input Format

- **Interaction History**: Sequence of past strategy choices and outcomes
- **Payoff Matrices**: Utility functions for different strategy combinations
- **Discount Parameters**: Agent preferences for immediate vs. future rewards
- **Learning Models**: Specifications of how agents adapt based on experience

## Output Format

```json
{
  "optimal_strategy": {
    "strategy_type": "tit_for_tat|grim_trigger|win_stay_lose_shift|adaptive",
    "parameters": {
      "cooperation_threshold": 0.8,
      "punishment_duration": 3,
      "forgiveness_probability": 0.1
    },
    "expected_payoff": value,
    "confidence_interval": [lower, upper]
  },
  "opponent_prediction": {
    "predicted_strategy": "cooperative|defensive|exploitative|random",
    "prediction_confidence": 0.85,
    "behavioral_patterns": [...],
    "adaptation_forecast": {...}
  },
  "equilibrium_analysis": {
    "subgame_perfect": true,
    "stability_metrics": {...},
    "robustness_score": 0.78
  },
  "adaptation_plan": {
    "trigger_conditions": {...},
    "response_strategies": [...],
    "monitoring_schedule": {...}
  }
}
```

## Configuration Options

- `discount_factor`: Agent preference for future vs. immediate rewards (default: 0.9)
- `learning_rate`: Speed of strategy adaptation (default: 0.1)
- `memory_length`: Number of past interactions to consider (default: 10)
- `prediction_horizon`: Number of future rounds to forecast (default: 5)
- `exploration_rate`: Probability of trying new strategies (default: 0.05)

## Constraints

- **Hard Rules**:
  - Never recommend strategies that lead to perpetual conflict
  - Always maintain computational tractability for real-time adaptation
  - Preserve agent autonomy in strategy selection
- **Safety Requirements**:
  - Validate all payoff structures for mathematical consistency
  - Handle infinite horizon scenarios with appropriate discounting
- **Quality Standards**:
  - Provide confidence intervals for all predictions
  - Include sensitivity analysis for key strategic parameters

## Error Handling

- **Insufficient Data**: Return detailed analysis of data requirements with suggestions for data collection
- **Convergence Issues**: Implement alternative prediction algorithms with performance warnings
- **Strategy Instability**: Detect and warn about strategies prone to oscillation or chaos
- **Computational Limits**: Scale down prediction horizon with user notification

## Performance Optimization

- **Incremental Learning**: Update predictions incrementally rather than recomputing from scratch
- **Pattern Recognition**: Use machine learning techniques to identify behavioral patterns
- **Caching**: Store frequently accessed strategy evaluations and prediction models
- **Parallel Processing**: Distribute prediction calculations across available computational resources

## Integration Examples

### With flywheel_loop.py
```python
# Integrate repeated game analysis into flywheel optimization
long_term_strategy = repeated_game_predictor.optimize_coordination(
    interaction_history=coordination_log,
    payoff_structure=performance_metrics,
    discount_factor=adaptive_discount
)
```

### With MCP Server
```python
# Register as MCP tool for repeated game analysis
@tool(name="repeated_game_predictor")
def analyze_repeated_interactions(history: list, payoffs: dict) -> dict:
    return repeated_game_predictor.predict(history, payoffs)
```

## Best Practices

- **Data Quality**: Ensure historical interaction data is accurate and complete
- **Strategy Validation**: Test recommended strategies against alternative approaches
- **Adaptation Monitoring**: Continuously monitor strategy effectiveness and adjust as needed
- **Communication**: Clearly explain strategic recommendations to all participating agents

## Troubleshooting

- **Strategy Oscillation**: Implement damping mechanisms and longer memory windows
- **Prediction Drift**: Regularly recalibrate prediction models with new data
- **Cooperation Breakdown**: Design more robust punishment and forgiveness mechanisms
- **Computational Complexity**: Use approximation methods for large-scale repeated games

## Monitoring and Metrics

- **Strategy Performance**: Track actual vs. predicted outcomes over time
- **Cooperation Levels**: Monitor frequency and stability of cooperative behavior
- **Prediction Accuracy**: Measure forecast accuracy for opponent behavior
- **System Stability**: Assess overall system performance and conflict frequency

## Dependencies

- **Required Skills**: Repeated game theory, machine learning, time series analysis
- **Required Tools**: Python with machine learning libraries, optimization frameworks
- **Required Files**: Interaction history templates, payoff structure schemas, prediction model frameworks

## Version History

- **1.0.0**: Initial release with core repeated game analysis capabilities
- **1.1.0**: Added machine learning-based prediction and adaptation planning
- **1.2.0**: Integrated with MCP server and real-time strategy monitoring

## License

MIT

## Description

The Repeated Game Predictor skill provides sophisticated analysis capabilities for ongoing multi-agent interactions where future consequences influence current decisions. It combines classical repeated game theory with modern machine learning techniques to identify optimal strategies that promote long-term cooperation while protecting against exploitation. This is particularly valuable in flywheel optimization, resource sharing systems, and any scenario involving repeated coordination decisions.

The skill implements advanced algorithms for strategy evolution analysis, cooperation detection, and behavioral prediction. It provides comprehensive adaptation planning and equilibrium analysis to ensure strategies remain effective as opponents learn and adapt over time.

## Workflow

1. **History Analysis**: Analyze historical interaction data for patterns and trends
2. **Strategy Evaluation**: Assess effectiveness of different repeated game strategies
3. **Prediction Modeling**: Build models to forecast opponent future behavior
4. **Optimization**: Identify optimal strategies balancing cooperation and self-protection
5. **Adaptation Planning**: Design strategies that can adapt to opponent learning
6. **Monitoring Setup**: Establish metrics for ongoing strategy performance evaluation

## Examples

### Example 1: Flywheel Coordination Optimization
**Input**: Historical coordination decisions and performance outcomes in flywheel_loop.py
**Process**: Analyze patterns in coordination effectiveness and opponent behavior
**Output**: Optimal coordination strategy maximizing long-term system performance

### Example 2: Resource Sharing with Learning
**Input**: Past resource allocation decisions and cooperation patterns among agents
**Process**: Identify conditions for sustained cooperation and optimal punishment strategies
**Output**: Strategy promoting fair sharing with adaptive response to defection

## Asset Dependencies

- **Scripts**: repeated_game_core.py, prediction_model.py, adaptation_planner.py
- **Templates**: interaction_history_template.json, payoff_structure_schema.json, prediction_framework.json
- **Reference Data**: Repeated game algorithms, machine learning benchmarks, equilibrium analysis methods
- **Tools**: Python machine learning libraries, optimization frameworks, MCP server integration