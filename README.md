# Skill Flywheel

Enterprise-Grade Multi-Container MCP Architecture with 345+ specialized skills.

## 🏗️ Architecture
A distributed ecosystem of 9 domain-specific servers orchestrated by a central Discovery Service.
- **Discovery Service**: Central registry and routing (Port 8000).
- **Domains**: Orchestration, Security, Data & AI, DevOps, Engineering, UX & Mobile, Advanced, Strategy, Agent R&D.

## 🚀 Quick Start
```bash
# Start the orchestration stack
docker compose up -d

# Verify status
docker compose ps
```
Visit http://localhost:8000/health to verify.

## 🔍 Key Features
- **Scalable Discovery**: Dynamically routes requests across containers.
- **Operational Compliance**: Centralized telemetry and auditing.
- **Resilient Connectivity**: Graceful degradation without paid API keys.
- **Advanced Core**: ML-driven optimization and automated security scanning.

## 📁 Repository Structure
- `/src/core`: Shared logic and specialized core components.
- `/src/discovery`: Routing and discovery service.
- `/domains`: Repository of specialized skills.
- `/docs`: Comprehensive documentation index.
- `/tests`: Automated test suites.

## 📚 Documentation
For detailed guides and architecture deep dives, see the [Documentation Index](docs/README.md).

## 📜 License
Licensed under the MIT License.
