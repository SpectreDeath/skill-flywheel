---
Domain: GAME THEORY
Version: 1.0.0
Type: Algorithm
Category: Information Asymmetry
Complexity: Advanced
Estimated Execution Time: 2-8 minutes
name: signaling_equilibrium_detector
---

# SKILL: Signaling Equilibrium Detector


## Implementation Notes
Content for ## Implementation Notes section to be added based on the specific skill requirements.

## Purpose

Analyze and optimize information signaling in multi-agent systems where agents possess private information and must communicate strategically. This skill identifies optimal signaling strategies, detects equilibrium in signaling games, and designs mechanisms to prevent information asymmetry problems in agent interactions.

## When to Use

- Multi-agent scenarios with asymmetric information and strategic communication
- Registry search ranking optimization through strategic signaling
- Agent reputation and capability signaling in coordination scenarios
- Negotiation scenarios with hidden preferences or constraints
- Resource allocation with incomplete information about agent capabilities

## When NOT to Use

- Complete information scenarios where all agents have identical knowledge
- Single-agent optimization problems
- Scenarios with no strategic communication or signaling
- Time-critical decisions requiring immediate action without analysis

## Inputs

- **Required**: Agent private information and signaling capabilities
- **Required**: Receiver preferences and information processing models
- **Optional**: Historical signaling behavior and reputation data
- **Optional**: Cost structures for different signaling strategies
- **Assumptions**: Rational agents optimizing signaling strategies based on receiver responses

## Outputs

- **Primary**: Signaling equilibrium analysis with optimal strategy recommendations
- **Secondary**: Information asymmetry quantification and mitigation strategies
- **Format**: JSON structure with signaling strategies, equilibrium analysis, and communication optimization

## Capabilities

1. **Equilibrium Detection**: Identify separating, pooling, and semi-separating equilibria in signaling games
2. **Strategy Optimization**: Compute optimal signaling strategies for senders and receivers
3. **Information Design**: Design communication protocols that minimize information asymmetry
4. **Reputation Analysis**: Analyze how signaling affects agent reputation and future interactions
5. **Manipulation Prevention**: Detect and prevent strategic misinformation in signaling

## Usage Examples

### Example 1: Registry Search Ranking Optimization

**Context**: Agents strategically signaling capabilities to improve registry search rankings
**Input**: Agent capability profiles and search algorithm preferences
**Output**: Optimal signaling strategy balancing truthfulness and competitive advantage

### Example 2: Capability Signaling in Coordination

**Context**: Agents signaling their capabilities to coordinate effectively
**Input**: Private capability information and coordination requirements
**Output**: Signaling equilibrium ensuring efficient task allocation

## Input Format

- **Private Information**: Agent characteristics, capabilities, or preferences not publicly known
- **Signaling Options**: Available communication methods and their costs
- **Receiver Models**: How other agents interpret and respond to signals
- **Cost Structures**: Resource costs associated with different signaling strategies

## Output Format

```json
{
  "signaling_equilibrium": {
    "equilibrium_type": "separating|pooling|semi_separating",
    "sender_strategies": {
      "agent1": {"signal": "strategy", "cost": value, "benefit": value},
      "agent2": {"signal": "strategy", "cost": value, "benefit": value}
    },
    "receiver_strategies": {
      "interpretation_rules": {...},
      "response_strategies": {...}
    },
    "equilibrium_stability": 0.85
  },
  "information_asymmetry": {
    "asymmetry_level": "low|medium|high",
    "mitigation_strategies": [...],
    "efficiency_loss": value
  },
  "signaling_optimization": {
    "optimal_signals": {...},
    "cost_benefit_analysis": {...},
    "reputation_impact": {...}
  },
  "manipulation_detection": {
    "misinformation_risk": "low|medium|high",
    "detection_signals": [...],
    "prevention_recommendations": [...]
  }
}
```

## Configuration Options

- `signal_cost_weight`: Importance of signaling costs vs. benefits (default: 0.5)
- `reputation_decay`: Rate at which reputation effects diminish over time (default: 0.1)
- `equilibrium_tolerance`: Numerical precision for equilibrium detection (default: 0.001)
- `signaling_frequency`: How often agents can send signals (default: continuous)
- `receiver_rationality`: Assumed rationality level of signal receivers (default: 0.9)

## Constraints

- **Hard Rules**:
  - Never recommend signaling strategies that violate truthfulness constraints
  - Always maintain computational tractability for real-time signaling
  - Preserve privacy when designing signaling mechanisms
- **Safety Requirements**:
  - Validate all signaling cost structures for mathematical consistency
  - Handle zero-cost signaling scenarios with appropriate constraints
- **Quality Standards**:
  - Provide stability analysis for all detected equilibria
  - Include manipulation detection and prevention measures

## Error Handling

- **Invalid Signaling Costs**: Return detailed error description with cost structure validation
- **No Equilibrium Found**: Provide alternative equilibrium concepts and approximation methods
- **Convergence Issues**: Implement alternative detection algorithms with performance warnings
- **Computational Limits**: Scale down signaling complexity with user notification

## Performance Optimization

- **Incremental Analysis**: Update equilibrium analysis incrementally as new signals are sent
- **Pattern Recognition**: Use machine learning to identify signaling patterns and trends
- **Caching**: Store frequently accessed equilibrium calculations and signaling strategies
- **Parallel Processing**: Distribute equilibrium detection across available computational resources

## Integration Examples

### With registry_search.py
```python
# Integrate signaling analysis into registry search optimization
optimal_signaling = signaling_detector.optimize_registry_signaling(
    agent_capabilities=agent_profiles,
    search_preferences=search_algorithm_weights,
    signaling_costs=communication_costs
)
```

### With MCP Server
```python
# Register as MCP tool for signaling analysis
@tool(name="signaling_equilibrium_detector")
def analyze_signaling_game(private_info: dict, signals: dict) -> dict:
    return signaling_detector.analyze(private_info, signals)
```

## Best Practices

- **Truthfulness Balance**: Design signaling strategies that balance competitive advantage with truthfulness
- **Reputation Management**: Consider long-term reputation effects when optimizing signaling
- **Cost Awareness**: Always account for signaling costs in strategy optimization
- **Manipulation Prevention**: Implement monitoring systems for strategic misinformation

## Troubleshooting

- **Pooling Equilibria**: Address situations where all agents send identical signals
- **Separating Equilibria**: Handle scenarios where signals perfectly reveal private information
- **Semi-separating Equilibria**: Manage partial information revelation through signaling
- **Computational Complexity**: Use approximation methods for large-scale signaling games

## Monitoring and Metrics

- **Signaling Efficiency**: Measure how well signals convey intended information
- **Equilibrium Stability**: Track stability of detected signaling equilibria over time
- **Information Asymmetry**: Monitor reduction in information gaps through signaling
- **Manipulation Detection**: Assess effectiveness of misinformation prevention measures

## Dependencies

- **Required Skills**: Signaling game theory, information economics, optimization algorithms
- **Required Tools**: Python with optimization libraries, game theory frameworks
- **Required Files**: Signaling strategy templates, equilibrium detection schemas, manipulation prevention frameworks

## Version History

- **1.0.0**: Initial release with core signaling equilibrium detection capabilities
- **1.1.0**: Added reputation analysis and manipulation detection features
- **1.2.0**: Integrated with MCP server and real-time signaling monitoring

## License

MIT

## Description

The Signaling Equilibrium Detector skill provides sophisticated analysis capabilities for strategic communication in multi-agent systems with asymmetric information. It identifies optimal signaling strategies that balance truthfulness with competitive advantage while detecting and preventing strategic manipulation. This is particularly valuable in registry search optimization, agent coordination, and any scenario involving strategic information disclosure.

The skill implements advanced algorithms from signaling game theory, including equilibrium detection, strategy optimization, and manipulation prevention. It provides comprehensive analysis of information asymmetry and designs communication protocols that minimize strategic misinformation while maximizing coordination efficiency.

## Workflow

1. **Information Analysis**: Analyze private information distribution and signaling capabilities
2. **Equilibrium Detection**: Identify separating, pooling, and semi-separating equilibria
3. **Strategy Optimization**: Compute optimal signaling strategies for senders and receivers
4. **Cost-Benefit Analysis**: Evaluate signaling strategies based on costs and benefits
5. **Manipulation Detection**: Monitor for strategic misinformation and implement prevention measures
6. **Communication Design**: Design protocols that optimize information flow while preventing manipulation

## Examples

### Example 1: Registry Search Optimization
**Input**: Agent capability profiles and search algorithm preferences
**Process**: Analyze optimal signaling strategies balancing truthfulness and ranking improvement
**Output**: Signaling equilibrium ensuring efficient search results with minimal manipulation

### Example 2: Capability Signaling in Coordination
**Input**: Private capability information and coordination requirements
**Process**: Design signaling strategies that enable efficient task allocation
**Output**: Equilibrium signaling protocol maximizing coordination efficiency

## Asset Dependencies

- **Scripts**: signaling_core.py, equilibrium_detector.py, manipulation_preventer.py
- **Templates**: signaling_strategy_template.json, equilibrium_schema.json, prevention_framework.json
- **Reference Data**: Signaling game algorithms, information economics benchmarks, manipulation detection methods
- **Tools**: Python optimization libraries, game theory frameworks, MCP server integration