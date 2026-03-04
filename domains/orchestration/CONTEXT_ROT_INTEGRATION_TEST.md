# Context Rot Detection Skills Integration Test

## Overview

This document provides comprehensive integration testing for the 4 new context rot detection skills within your orchestration container ecosystem. The skills integrate seamlessly with your existing 9 orchestration skills to provide comprehensive conversation health management.

## Skills Created

### 1. SKILL.context_rot_detector
- **Purpose**: Real-time detection of context rot symptoms
- **Integration**: Works with Empire Health Monitor for health scoring
- **Key Metrics**: Token pressure, U-shape bias, recency bias, semantic drift, confidence fabrication, needle miss rates

### 2. SKILL.context_health_analyzer  
- **Purpose**: Deep context health analysis and diagnostics
- **Integration**: Uses Multi-Skill Chaining Engine for complex workflows
- **Key Capabilities**: Embedding drift analysis, needle-in-haystack testing, trend analysis, recovery planning

### 3. SKILL.context_pruning_engine
- **Purpose**: Intelligent context optimization and cleanup
- **Integration**: Works with MCP Load Balancer for resource optimization
- **Key Features**: Irrelevant turn removal, essential bracketing, citation preservation, coherence maintenance

### 4. SKILL.conversation_reset_optimizer
- **Purpose**: Strategic conversation resets with minimal information loss
- **Integration**: Coordinates with Skill Team Assembler for fresh context building
- **Key Capabilities**: Reset timing optimization, summary preservation, gradual rebuilding, cross-domain coordination

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION CONTAINER                      │
├─────────────────────────────────────────────────────────────────┤
│  Context Rot Detection Skills (NEW)                             │
│  ├── context_rot_detector      ──┐                              │
│  ├── context_health_analyzer   ──┤                              │
│  ├── context_pruning_engine    ──┤  Empire Health Monitor       │
│  └── conversation_reset_optimizer ─┘                              │
├─────────────────────────────────────────────────────────────────┤
│  Existing Orchestration Skills                                  │
│  ├── autonomous_mission_planner                                 │
│  ├── cross_domain_workflow_orchestrator                         │
│  ├── domain_portfolio_manager                                   │
│  ├── empire_health_monitor                                      │
│  ├── mcp_load_balancer                                          │
│  ├── multi_skill_chaining_engine                                │
│  ├── ralph_chaos_wildcard                                       │
│  └── skill_team_assembler                                       │
└─────────────────────────────────────────────────────────────────┘
```

## MCP Server Integration

### Server Configuration

```yaml
# Add to your mcp_config.json
{
  "servers": {
    "context_rot_detection": {
      "url": "mcp://localhost:8001/context_rot_detector",
      "skills": ["context_rot_detector", "context_health_analyzer", "context_pruning_engine", "conversation_reset_optimizer"],
      "integration_points": [
        "empire_health_monitor",
        "mcp_load_balancer", 
        "multi_skill_chaining_engine",
        "skill_team_assembler"
      ]
    }
  }
}
```

### Docker Integration

```dockerfile
# Add to your orchestration container Dockerfile
FROM your-base-image

# Install context rot detection skills
COPY domains/orchestration/SKILL.context_rot_detector /app/skills/context_rot_detector
COPY domains/orchestration/SKILL.context_health_analyzer /app/skills/context_health_analyzer  
COPY domains/orchestration/SKILL.context_pruning_engine /app/skills/context_pruning_engine
COPY domains/orchestration/SKILL.conversation_reset_optimizer /app/skills/conversation_reset_optimizer

# Expose MCP server port
EXPOSE 8001

# Start MCP server with context rot detection
CMD ["python", "-m", "mcp_server", "--port", "8001", "--skills", "context_rot_detection"]
```

## Integration Test Scenarios

### Test 1: Basic Context Rot Detection Flow

```yaml
test_scenario: "Basic Context Rot Detection"
description: "Test end-to-end context rot detection and response"

steps:
  1. Start long conversation (100+ messages)
  2. context_rot_detector monitors for symptoms
  3. Detect token pressure > 80% and recency bias
  4. Trigger context_health_analyzer for deep analysis
  5. Generate health report with rot_score = 0.45
  6. Recommend context_pruning_engine with moderate strategy
  7. Execute pruning with 35% compression, 92% information retention
  8. Verify conversation quality improvement

expected_outcome:
  - rot_score decreases from 0.45 to 0.25
  - conversation performance improves
  - no critical information lost
  - user experience maintained
```

### Test 2: Cross-Domain Conversation Recovery

```yaml
test_scenario: "Cross-Domain Conversation Recovery"
description: "Test conversation reset across multiple domains"

steps:
  1. Start complex conversation spanning 4 domains
  2. Simulate severe context rot (rot_score = 0.85)
  3. context_health_analyzer identifies cross-domain issues
  4. conversation_reset_optimizer coordinates reset
  5. Skill Team Assembler builds fresh team for each domain
  6. Execute coordinated reset with 95% information preservation
  7. Rebuild conversation across all domains
  8. Validate cross-domain consistency

expected_outcome:
  - All domains synchronized after reset
  - Information preservation > 90%
  - Conversation coherence maintained
  - Cross-domain dependencies preserved
```

### Test 3: Real-time Monitoring Integration

```yaml
test_scenario: "Real-time Monitoring Integration"
description: "Test integration with Empire Health Monitor"

steps:
  1. Start Empire Health Monitor
  2. Begin conversation with context rot detection enabled
  3. Monitor real-time health metrics
  4. context_rot_detector sends alerts to health monitor
  5. Health monitor aggregates context health with empire health
  6. Display unified health dashboard
  7. Test alert escalation for critical context rot
  8. Verify coordinated response across skills

expected_outcome:
  - Unified health scoring (empire + context)
  - Real-time alert integration
  - Coordinated skill response
  - Comprehensive health dashboard
```

### Test 4: Performance Optimization Integration

```yaml
test_scenario: "Performance Optimization Integration"
description: "Test integration with MCP Load Balancer"

steps:
  1. Configure MCP Load Balancer with context awareness
  2. Start multiple concurrent conversations
  3. context_rot_detector identifies high-load conversations
  4. MCP Load Balancer redistributes load based on context health
  5. context_pruning_engine optimizes context for better performance
  6. Monitor resource utilization and response times
  7. Test load balancing during conversation resets
  8. Verify performance improvements

expected_outcome:
  - Optimized resource allocation
  - Improved response times
  - Balanced load distribution
  - Efficient context management
```

## Integration Points Verification

### Empire Health Monitor Integration

```yaml
integration_points:
  health_data_sharing:
    - context_rot_detector → empire_health_monitor: real-time metrics
    - context_health_analyzer → empire_health_monitor: comprehensive reports
    - conversation_reset_optimizer → empire_health_monitor: recovery validation
  
  alert_forwarding:
    - context_rot_detector alerts → empire_health_monitor dashboard
    - critical context rot → empire health alerts
    - recovery success → health score updates
  
  coordinated_optimization:
    - unified health scoring
    - cross-skill optimization triggers
    - comprehensive health recommendations
```

### MCP Load Balancer Integration

```yaml
integration_points:
  context_load_distribution:
    - context_pruning_engine → mcp_load_balancer: optimized context
    - conversation_reset_optimizer → mcp_load_balancer: fresh context routing
    - context_rot_detector → mcp_load_balancer: health-aware load distribution
  
  performance_optimization:
    - context-aware skill routing
    - resource allocation based on conversation health
    - load balancing during context operations
```

### Multi-Skill Chaining Engine Integration

```yaml
integration_points:
  complex_analysis_workflows:
    - context_health_analyzer → multi_skill_chaining_engine: complex analysis chains
    - coordinated skill execution for deep analysis
    - result aggregation across multiple skills
  
  performance_optimization:
    - coordinated execution timing
    - resource sharing between context skills
    - optimized workflow execution
```

### Skill Team Assembler Integration

```yaml
integration_points:
  fresh_context_building:
    - conversation_reset_optimizer → skill_team_assembler: team coordination
    - fresh team assembly for reset conversations
    - cross-domain team building
    - team lead assignment based on context needs
```

## Test Execution Commands

### Basic Integration Test

```bash
# Start context rot detection MCP server
python -m mcp_server --port 8001 --skills context_rot_detection

# Test basic detection flow
curl -X POST http://localhost:8001/context_rot_detector \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": [...],
    "current_token_count": 12000,
    "max_context_window": 16000
  }'

# Test health analysis
curl -X POST http://localhost:8001/context_health_analyzer \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test_conversation",
    "analysis_scope": "comprehensive"
  }'
```

### Performance Test

```bash
# Test context pruning performance
curl -X POST http://localhost:8001/context_pruning_engine \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_history": [...],
    "pruning_strategy": "moderate",
    "preservation_requirements": ["key_decisions"]
  }'

# Test conversation reset
curl -X POST http://localhost:8001/conversation_reset_optimizer \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test_conversation",
    "current_state": "severe_context_rot",
    "reset_strategy": "gradual_rebuilding"
  }'
```

## Success Criteria

### Functional Requirements

- [ ] All 4 context rot detection skills integrate seamlessly with existing orchestration skills
- [ ] Real-time context rot detection with < 2 second response time
- [ ] Comprehensive health analysis with > 90% accuracy
- [ ] Context pruning with > 85% information retention
- [ ] Conversation reset with > 90% success rate
- [ ] Cross-domain coordination working correctly
- [ ] Integration with Empire Health Monitor successful
- [ ] MCP Load Balancer integration optimized
- [ ] Multi-Skill Chaining Engine coordination working
- [ ] Skill Team Assembler integration successful

### Performance Requirements

- [ ] Context rot detection latency < 2 seconds
- [ ] Health analysis completion < 5 minutes
- [ ] Context pruning completion < 3 minutes
- [ ] Conversation reset completion < 8 minutes
- [ ] Resource usage optimized for long conversations
- [ ] Scalability to 1000+ message conversations
- [ ] Concurrent conversation handling

### Integration Requirements

- [ ] MCP server communication working
- [ ] Skill registry integration successful
- [ ] Data format compatibility maintained
- [ ] Error handling and recovery working
- [ ] Debug mode functionality operational
- [ ] Monitoring and metrics integration complete

## Troubleshooting Guide

### Common Integration Issues

1. **MCP Server Connection Failures**
   - Check port availability (8001)
   - Verify skill registration
   - Check network connectivity

2. **Data Format Incompatibility**
   - Validate YAML/JSON formats
   - Check field naming conventions
   - Verify data types and constraints

3. **Performance Degradation**
   - Monitor resource usage
   - Check for memory leaks
   - Optimize analysis algorithms

4. **Integration Timeouts**
   - Increase timeout values
   - Check network latency
   - Optimize skill execution

### Debug Commands

```bash
# Check MCP server status
curl http://localhost:8001/health

# Test skill connectivity
curl http://localhost:8001/skills

# Check integration logs
tail -f /var/log/mcp_server.log

# Monitor performance metrics
curl http://localhost:8001/metrics
```

## Conclusion

The 4 context rot detection skills provide comprehensive conversation health management for your 234-skill empire. They integrate seamlessly with your existing orchestration infrastructure to provide:

- **Real-time monitoring** of conversation quality
- **Intelligent optimization** of context usage
- **Strategic recovery** from context degradation
- **Cross-domain coordination** for complex conversations
- **Performance optimization** through resource management

These skills will significantly enhance your MCP container's ability to maintain high-quality, long-running conversations, especially valuable for FDA compliance chats and other critical multi-turn interactions.