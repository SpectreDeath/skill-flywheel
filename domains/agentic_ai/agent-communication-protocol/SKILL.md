---
name: agent-communication-protocol
description: "Use when: designing agent communication, implementing message protocols, building agent messaging, setting up inter-agent communication, or creating agent APIs. Triggers: 'agent communication', 'message protocol', 'inter-agent', 'agent messaging', 'agent API', 'communication protocol'. NOT for: single agents without communication, when direct calls are sufficient, or when no agent coordination needed."
---

# Agent Communication Protocol

Designs and implements communication protocols for multi-agent systems. This skill creates message formats, protocols, and communication infrastructure.

## When to Use This Skill

Use this skill when:
- Designing agent communication
- Implementing message protocols
- Building agent messaging systems
- Setting up inter-agent communication
- Creating agent APIs

Do NOT use this skill when:
- Single agents without communication
- Direct calls sufficient
- No agent coordination needed
- Simple request-response

## Input Format

```yaml
protocol_request:
  num_agents: number             # Number of communicating agents
  communication_style: string    # sync, async, event-driven
  message_format: string         # JSON, proto, custom
  protocol_type: string          # request-response, pub-sub, streaming
```

## Output Format

```yaml
protocol_result:
  protocol_spec: object           # Complete protocol spec
  message_schemas: object         # Message format definitions
  implementation_code: string    # Generated code
  examples: array                # Usage examples
```

## Capabilities

### 1. Protocol Design (15 min)

- Design message formats
- Define message types
- Create protocol states
- Specify error handling

### 2. Message Schema (15 min)

- Define message structures
- Create validation rules
- Handle versioning
- Add type safety

### 3. Transport Layer (15 min)

- Select transport (HTTP, WebSocket, message queue)
- Implement connection management
- Handle reconnection
- Add encryption

### 4. Implementation (20 min)

- Generate protocol code
- Implement message handling
- Add error handling
- Create utilities

### 5. Testing (10 min)

- Test message handling
- Verify protocol compliance
- Test error cases
- Benchmark performance

## Usage Examples

### Basic Usage

"Design agent communication protocol."

### Advanced Usage

"Async pub-sub protocol with JSON messages."

## Configuration Options

- `transport`: HTTP, WebSocket, gRPC, message-queue
- `message_format`: JSON, Protobuf, Avro
- `delivery`: at-least-once, exactly-once
- `security`: TLS, encryption

## Constraints

- MUST define clear message formats
- SHOULD handle failures gracefully
- MUST be extensible
- SHOULD support versioning

## Integration Examples

- LangGraph: Add communication
- Custom agents: Implement protocols
- Message queues: Connect agents
- gRPC: Generate protobufs

## Dependencies

- Python 3.10+
- Protocol libraries
- Message queues
- Serialization
