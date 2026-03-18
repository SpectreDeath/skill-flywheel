# Skill Flywheel Architecture

## System Overview

```mermaid
graph TB
    subgraph External Clients
        CLI[CLI Tools]
        API[API Consumers]
        WEB[Web Applications]
    end

    subgraph "Skill Flywheel (Port 8000)"
        DISCOVERY[Discovery Service<br/>Central Registry]
        API_GW[API Gateway<br/>Request Routing]
    end

    subgraph "Domain Servers"
        ORCH[Orchestration<br/>Port 8001]
        SECURITY[Security<br/>Port 8002]
        DATA_AI[Data & AI<br/>Port 8003]
        DEVOPS[DevOps<br/>Port 8004]
        ENGINEERING[Engineering<br/>Port 8005]
        UX[UX & Mobile<br/>Port 8006]
        ADVANCED[Advanced<br/>Port 8007]
        STRATEGY[Strategy<br/>Port 8008]
        AGENT[Agent R&D<br/>Port 8009]
    end

    subgraph Data Layer
        REGISTRY[(SQLite<br/>skill_registry.db)]
        SKILLS[SKILL.md<br/>Definitions]
    end

    CLI --> DISCOVERY
    API --> DISCOVERY
    WEB --> DISCOVERY
    
    DISCOVERY --> API_GW
    API_GW --> ORCH
    API_GW --> SECURITY
    API_GW --> DATA_AI
    API_GW --> DEVOPS
    API_GW --> ENGINEERING
    API_GW --> UX
    API_GW --> ADVANCED
    API_GW --> STRATEGY
    API_GW --> AGENT
    
    DISCOVERY --> REGISTRY
    DISCOVERY --> SKILLS
```

## Component Architecture

```mermaid
graph LR
    subgraph "Discovery Service"
        HEALTH[Health Check]
        DISCOVER[Skill Discovery]
        INVOKE[Skill Invocation]
        METRICS[Metrics]
    end
    
    subgraph "Skill Manager"
        LOADER[Dynamic Loader]
        CACHE[Module Cache]
        TELEMETRY[Telemetry]
    end
    
    subgraph "Database"
        DB[(SQLite)]
        INDEX[Skill Index]
    end
    
    HEALTH --> LOADER
    DISCOVER --> LOADER
    INVOKE --> LOADER
    LOADER --> CACHE
    CACHE --> TELEMETRY
    TELEMETRY --> DB
    LOADER --> INDEX
```

## Skill Structure

```mermaid
classDiagram
    class Skill {
        +name: str
        +description: str
        +version: str
        +domain: str
        +status: SkillStatus
    }
    
    class InvokePayload {
        +args: list
        +kwargs: dict
    }
    
    Skill --> InvokePayload : invokes
```

## Data Flow

```mermaid
sequenceDiagram
    participant Client
    participant Discovery
    participant Loader
    participant Cache
    participant Skill
    
    Client->>Discovery: POST /skills/{id}/invoke
    Discovery->>Loader: Load skill module
    Loader->>Cache: Check cache
    alt Cache miss
        Cache-->>Loader: Not found
        Loader->>Loader: Import module
        Loader->>Cache: Store in cache
    else Cache hit
        Cache-->>Loader: Return cached
    end
    Loader->>Skill: Execute function
    Skill-->>Client: Return result
```

## Technology Stack

| Component | Technology |
|-----------|------------|
| API Server | FastAPI + Uvicorn |
| Database | SQLite |
| Container | Docker |
| Orchestration | Docker Compose |
| Monitoring | Prometheus |
| ML Models | scikit-learn, PyTorch |

## Directory Structure

```
skill-flywheel/
├── src/
│   ├── core/           # Shared core components
│   │   ├── skills.py
│   │   ├── telemetry.py
│   │   ├── cache.py
│   │   └── ...
│   ├── server/        # API servers
│   │   ├── discovery_service.py
│   │   └── enhanced_mcp_server_v3.py
│   └── skills/        # Skill implementations
│       ├── clustering/
│       ├── game_theory/
│       ├── epistemology/
│       └── ...
├── domains/           # SKILL.md definitions
├── data/             # Database & models
├── tests/            # Test suite
└── .github/         # CI/CD workflows
```
