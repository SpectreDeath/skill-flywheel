# Containerized MCP Architecture (agent-skills-mcp)

This plan outlines the refactoring of the "Skill Flywheel" empire into an enterprise-grade, multi-container MCP architecture. This design ensures domain isolation, scalability, and enterprise-grade auditability.

## User Review Required

> [!IMPORTANT]
> **Breaking Change**: The repository structure will be reorganized. Scripts previously located in the root will move to `src/`.
> **Network Requirement**: Users will need Docker/Docker Compose installed locally to run the full stack.
> **Compliance**: Telemetry is now centralized in a shared volume `/app/telemetry` for cross-container auditing.

## Proposed Changes

### [Component] Repository Structure

Reorganize the root directory to separate domain data from service logic and deployment configuration.

#### [MODIFY] [.](file:///d:/Skill%20Flywheel)

- Move `mcp_server.py`, `discovery_service.py`, `registry_search.py`, `reindex_skills.py` to `src/core`.
- Move `Dockerfile` to `deploy/container/`.
- Update `docker-compose.yml` in root to point to new paths.
- Keep `domains/` as the source of truth for skill definitions.

### [Component] Core Infrastructure

#### [MODIFY] [mcp_server.py](file:///d:/Skill%20Flywheel/mcp_server.py)

- Update paths to use relative imports or environment-based pathing.
- Enhance logging to include container ID and server name for better audit trails.

#### [MODIFY] [discovery_service.py](file:///d:/Skill%20Flywheel/discovery_service.py)

- Replace static placeholders with logic that queries `skill_registry.json` to find which server hosts a specific skill.

### [Component] Orchestration

#### [MODIFY] [docker-compose.yml](file:///d:/Skill%20Flywheel/docker-compose.yml)

- Add health checks for each service.
- Use a shared read-only volume for `domains/` and `skill_registry.json`.
- Use a shared write-only volume for `telemetry/`.
- Standardize on `mcp-network` bridge.

## Verification Plan

### Automated Tests

- **Startup Check**: Run `docker compose up -d` and verify all 10 containers (9 servers + 1 discovery) reach `healthy` state.
- **Discovery Validation**: Query the Discovery Service at `http://localhost:8000` to ensure it lists all 9 endpoints.
- **Cross-Domain Routing**: Use an MCP client to call a tool in the `SecurityServer` (8002) and verify telemetry is logged correctly.

### Manual Verification

- **Compliance Audit Simulation**: Verify that calling a skill in `mcp-security` creates a log entry in the shared telemetry volume that includes `server: SecurityServer`.
- **Zero-Downtime Test**: Run `docker compose restart mcp-devops` and verify that the `DiscoveryService` still responds while the DevOps server is cycling.
