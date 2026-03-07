# Skill Flywheel: Enterprise-Grade Multi-Container MCP Architecture

Skill Flywheel is a production-ready, highly scalable Model Context Protocol (MCP) ecosystem. It features a distributed architecture of 9 specialized domain servers orchestrated through a central Discovery Service, providing isolation, horizontal scaling, and built-in regulatory compliance auditing.

## 🏗️ Architecture Overview

The system is organized into logical domain groups, each running in its own isolated container:

- **Discovery Service** (Port 8000): Central registry and routing engine.
- **Orchestration** (Port 8001): Core empire management and meta-skills.
- **Security** (Port 8002): Application security, forensics, and osint.
- **Data & AI** (Port 8003): ML/AI research, data engineering, and ethics.
- **DevOps** (Port 8004): Cloud, database, and infrastructure engineering.
- **Engineering** (Port 8005): Specification engineering and formal methods.
- **UX & Mobile** (Port 8006): Frontend and mobile development.
- **Advanced** (Port 8007): Quantum computing, Web3, and complex algorithms.
- **Strategy** (Port 8008): Strategy analysis, epidemiology, and game theory.
- **Agent R&D** (Port 8009): AI agent development and autonomous evolution.

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- [Docker Compose](https://docs.docker.com/compose/install/) (included with Docker Desktop).

### Deployment

1. Clone the repository.
2. Run the orchestration stack:

   ```bash
   docker compose up -d
   ```

3. Verify the status:

   ```bash
   docker compose ps
   ```

## 🔍 Service Discovery

The **Discovery Service** acts as the entry point for the entire empire. Use it to find which server hosts a specific skill.

### Discovery Tools

- `list_available_services`: Returns all active MCP endpoints and their domain coverage.
- `find_domain_for_skill`: Maps a skill name (e.g., `repo-recon`) to its specific container endpoint.

## 🛡️ Operational Compliance & Telemetry

Every transaction within the ecosystem is logged to a centralized telemetry volume. This ensures all agent actions are auditable and compliant with operational standards. Logs are located at `./telemetry/usage_log.jsonl`.

## ♿ Accessibility & API Resiliency

Skill Flywheel is designed to be functional even without paid API keys. Core services and tools (including Skill Enrichment and Agent Orchestration) verify the presence of `GEMINI_API_KEY` or `OPENAI_API_KEY` and gracefully disable dependent features if they are missing, providing clear feedback instead of system failures.

## 📁 Repository Structure

- `/src/core`: Shared MCP implementation and registry logic.
- `/src/discovery`: Routing and discovery service logic.
- `/domains`: Repository of 513+ specialized skills.
- `/docs/analysis`: Architecture and ecosystem analysis reports.
- `/docs/guides`: User and deployment guides.
- `/tests`: Comprehensive test suites.
- `/telemetry`: Persistent audit logs.
- `/deploy`: Containerization artifacts.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
