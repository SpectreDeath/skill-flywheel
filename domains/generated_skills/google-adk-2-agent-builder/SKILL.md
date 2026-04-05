---
name: google-adk-2-agent-builder
description: "Use when: building AI agents with Google Agent Development Kit (ADK) 2.0, creating graph-based workflows, building multi-agent systems, or running agents with Gemini/Claude. Triggers: 'ADK', 'agent development kit', 'google adk', 'build agent', 'graph workflow', 'workflow agent', 'multi-agent', 'sequential agent', 'parallel agent', 'loop agent', 'run agent'. Requires: google-adk 2.0.0a2+. NOT for: ADK 1.x (use google-adk 1.x skills)."
---

# Google ADK 2.0 Agent Builder

Build sophisticated AI agents using Google Agent Development Kit 2.0 (Alpha). Supports graph-based workflows, collaborative agents, and dynamic workflows.

## Installation

```bash
pip install google-adk --pre
```

Verify version:
```python
import google.adk
print(google.adk.__version__)  # 2.0.0a2
```

## Core Components

### 1. LLM Agent

```python
from google.adk.agents import Agent
from pydantic import BaseModel

class CityInfo(BaseModel):
    name: str
    population: int

city_agent = Agent(
    name="city_agent",
    model="gemini-2.0-flash",
    instruction="Return a random city name. Return only the name.",
    output_schema=str,
)
```

### 2. Graph-based Workflow

```python
from google.adk import Workflow, Event
from pydantic import BaseModel

# Define agents
generator_agent = Agent(
    name="generator",
    model="gemini-2.0-flash",
    instruction="Generate a random topic.",
    output_schema=str,
)

processor_agent = Agent(
    name="processor",
    model="gemini-2.0-flash",
    input_schema=str,
    instruction="Expand this topic into a short paragraph.",
    output_schema=str,
)

# Define node functions
def route_handler(node_input: str) -> Event:
    """Route to processor."""
    return Event(route="processor")

def completion_handler(node_input: str) -> Event:
    """Final output."""
    return Event(message=f"Topic: {node_input}\nWORKFLOW COMPLETED.")

# Create workflow
root_agent = Workflow(
    name="topic_workflow",
    edges=[
        ("START", generator_agent, route_handler, processor_agent, completion_handler)
    ],
)
```

## Workflow Patterns

### Sequential Workflow

```python
from google.adk.agents import SequentialAgent

# Create sub-agents
step1 = Agent(name="step1", model="gemini-2.0-flash", instruction="First step")
step2 = Agent(name="step2", model="gemini-2.0-flash", instruction="Second step")
step3 = Agent(name="step3", model="gemini-2.0-flash", instruction="Third step")

# Sequential execution
workflow = SequentialAgent(
    name="sequential_workflow",
    sub_agents=[step1, step2, step3],
)
```

### Parallel Workflow

```python
from google.adk.agents import ParallelAgent

parallel_workflow = ParallelAgent(
    name="parallel_workflow",
    sub_agents=[
        Agent(name="task1", model="gemini-2.0-flash", instruction="Task 1"),
        Agent(name="task2", model="gemini-2.0-flash", instruction="Task 2"),
        Agent(name="task3", model="gemini-2.0-flash", instruction="Task 3"),
    ],
)
```

### Loop Workflow

```python
from google.adk.agents import LoopAgent

loop_workflow = LoopAgent(
    name="loop_workflow",
    sub_agents=[Agent(name="iterative_task", model="gemini-2.0-flash", instruction="...")],
    max_iterations=5,
)
```

### Routing Workflow with Conditional Edges

```python
def router(node_input: str) -> Event:
    """Route based on classification."""
    classification = node_input.upper()
    routes = []
    
    if "BUG" in classification:
        routes.append("bug_handler")
    if "SUPPORT" in classification:
        routes.append("support_handler")
    if "LOGISTICS" in classification:
        routes.append("logistics_handler")
    
    return Event(route=routes if routes else ["default"])

root_agent = Workflow(
    name="routing_workflow",
    edges=[
        ("START", classifier_agent, router),
        (router, {
            "bug_handler": bug_handler,
            "support_handler": support_handler,
            "logistics_handler": logistics_handler,
        }),
    ],
)
```

## Multi-Agent Systems

### Collaborative Agents (Coordinator + Subagents)

```python
from google.adk.agents import LlmAgent

# Sub-agents
researcher = LlmAgent(
    name="researcher",
    model="gemini-2.0-flash",
    instruction="Research the given topic and provide key findings.",
)

writer = LlmAgent(
    name="writer",
    model="gemini-2.0-flash",
    instruction="Write a summary based on research findings.",
)

editor = LlmAgent(
    name="editor",
    model="gemini-2.0-flash",
    instruction="Edit and improve the written content.",
)

# Coordinator
coordinator = LlmAgent(
    name="coordinator",
    model="gemini-2.0-flash",
    instruction="""You coordinate a team.
    - Use researcher to gather info
    - Use writer to create content
    - Use editor to refine
    Delegate tasks appropriately.""",
    sub_agents=[researcher, writer, editor],
)
```

## Tool Integration

### Function Tools

```python
from google.adk.tools import FunctionTool

def calculate(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def search_web(query: str) -> str:
    """Search the web."""
    # Implementation
    return f"Results for: {query}"

calculator_tool = FunctionTool(func=calculate)
search_tool = FunctionTool(func=search_web)

agent = Agent(
    name="tool_agent",
    model="gemini-2.0-flash",
    instruction="Use tools when needed.",
    tools=[calculator_tool, search_tool],
)
```

### MCP Tools

```python
from google.adk.tools import McpTool

mcp_tool = McpTool(
    tool_name="mcp-server-name",
    server_url="http://localhost:8000",
)

agent = Agent(
    name="mcp_agent",
    model="gemini-2.0-flash",
    instruction="...",
    tools=[mcp_tool],
)
```

### OpenAPI Tools

```python
from google.adk.tools import OpenApiTool

openapi_tool = OpenApiTool(
    name="weather_api",
    spec_path="weather_openapi.yaml",
)

agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash",
    tools=[openapi_tool],
)
```

## Running Agents

### Command Line

```bash
# Serve web interface
adk web

# Run in terminal
adk run agent_module

# Run API server
adk serve
```

### Programmatic

```python
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

async def run_agent():
    # Create session service
    session_service = InMemorySessionService()
    
    # Create runner
    runner = Runner(
        app_name="my_app",
        agent=root_agent,
        session_service=session_service,
    )
    
    # Run agent
    async for event in runner.run_async(user_id="user1", session_id="session1"):
        if event.is_final_response():
            print(f"Response: {event.content}")
        
asyncio.run(run_agent())
```

## Supported Models

```python
from google.adk.models import Gemini, Claude, Ollama, LiteLlm

# Gemini (default)
agent = Agent(model="gemini-2.0-flash")
agent = Agent(model="gemini-2.5-pro")

# Claude via Anthropic
agent = Agent(
    model="claude-3-5-sonnet-20241022",
    provider=Claude(anthropic_api_key="sk-...")
)

# Ollama (local)
agent = Agent(
    model="llama3",
    provider=Ollama(model="llama3", base_url="http://localhost:11434")
)

# LiteLLM (unified)
agent = Agent(
    model="gpt-4",
    provider=LiteLlm(model="openai/gpt-4")
)
```

## Context & Memory

### Session State

```python
from google.adk.agents import Context

async def tool_func(context: Context):
    # Access state
    state = context.state
    state["counter"] = state.get("counter", 0) + 1
    
    # Modify state
    return {"result": f"Count: {state['counter']}"}
```

### Memory

```python
from google.adk.memory import InMemoryMemoryService

memory_service = InMemoryMemoryService()

runner = Runner(
    app_name="app",
    agent=agent,
    memory_service=memory_service,
)
```

## Artifacts

```python
from google.adk.artifacts import InMemoryArtifactService

artifact_service = InMemoryArtifactService()

# Save artifact
context.save_artifact(key="data", artifact=my_data)

# Load artifact
artifact = context.load_artifact(key="data")
```

## Callbacks

```python
async def before_model_callback(context, request):
    """Called before model call."""
    print(f"Calling model: {request.model}")
    return request

async def after_model_callback(context, response):
    """Called after model response."""
    print(f"Got response: {response.text}")
    return response

agent = Agent(
    name="callback_agent",
    model="gemini-2.0-flash",
    instruction="...",
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
)
```

## Configuration

### RunConfig

```python
from google.adk.agents import RunConfig

config = RunConfig(
    max_llm_calls=50,
    streaming_mode=True,
    response_modalities=["text", "audio"],
)
```

### App Configuration

```python
from google.adk.apps import App

app = App(
    name="my_app",
    root_agent=root_agent,
    plugins=[LoggingPlugin()],
)
```

## Deployment

### Local Web Interface

```bash
adk web --port 8000
```

### API Server

```bash
adk serve --port 8000
```

### Google Cloud Run (production)

```yaml
# cloudrun.yaml
runtime: python311
entrypoint: adk serve
```

## Known Limitations (Alpha)

- Live Streaming not compatible with graph-based workflows
- Some third-party integrations may not work
- Do NOT mix ADK 2.0 and ADK 1.0 data storage

## Constraints

- MUST use Python 3.11+
- SHOULD use virtual environments (ADK 2.0 is alpha)
- MUST NOT share storage with ADK 1.0 projects
- SHOULD test thoroughly before production use
- MAY cause breaking changes in future versions