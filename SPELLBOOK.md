# SPELLBOOK

> Your guide to invoking skills and combining them for powerful results.

This document serves as both a skill index and recipe book for the Skill Flywheel. Part 1 lists all available skills with their **triggers** (what activates them). Part 2 shows recipes - skill combinations that achieve specific outcomes.

---

## Part 1: Skill Index

**How to read**: Each skill shows its domain, description, and the trigger phrases that activate it. Include any of these phrases in your input to invoke the skill.

---

### SPECIFICATION_ENGINEERING

Domain for specification-driven development skills.

- **specification-validation-framework**: Implement automated testing and validation for specifications
  - **Triggers**: `validate spec`, `spec validation`, `spec quality`, `test spec`, `validate specification`, `spec completeness`

- **specification-traceability**: Establish requirement-to-implementation traceability
  - **Triggers**: `traceability`, `trace requirements`, `requirement trace`, `impact analysis`, `trace matrix`

- **executable-spec-harness**: Convert specifications into automated tests
  - **Triggers**: `spec to test`, `executable spec`, `contract testing`, `spec test`, `generate tests from spec`, `test from specification`

- **spec-regression-monitoring**: Track specification drift and detect breaking changes
  - **Triggers**: `spec regression`, `breaking changes`, `backward compatibility`, `spec drift`, `spec version`, `version comparison`, `spec monitoring`

- **spec-evolution-engine**: Manage spec versioning with backward compatibility
  - **Triggers**: `spec evolution`, `version upgrade`, `migration`, `backward compatibility`, `deprecation`, `semver`, `breaking changes`

- **specification-lifecycle-management**: Automated spec review cycles and expiration
  - **Triggers**: `spec lifecycle`, `review cycle`, `spec expiration`, `spec stale`, `spec governance`, `spec maintenance`, `spec health`

- **spec-contract-authoring**: Author executable specifications (OpenAPI, JSON Schema)
  - **Triggers**: `executable spec`, `contract first`, `API spec`, `machine readable spec`, `spec as test`, `documentation as code`

- **spec-to-task-decomposition**: Break specs into actionable implementation tasks
  - **Triggers**: `break down spec`, `spec to task`, `task from spec`, `decompose requirements`, `implementation plan`, `effort estimation`, `work breakdown`

- **spec-guardrail-enforcement**: Enforce spec compliance during implementation
  - **Triggers**: `enforce spec`, `spec compliance`, `validate implementation`, `spec gate`, `spec violation`, `compliance check`

---

### skill_validation

Domain for validating AgentSkills repository.

- **skill-spec-validator**: Validate AgentSkills directory structure and SKILL.md compliance
  - **Triggers**: `validate skills`, `skill spec`, `directory structure`, `validate structure`, `compliance check`, `auto fix`

- **frontmatter-validator**: Validate YAML frontmatter in SKILL.md files
  - **Triggers**: `frontmatter`, `validate yaml`, `validate metadata`, `fix frontmatter`, `required fields`, `metadata validation`

- **naming-convention-checker**: Enforce consistent naming conventions
  - **Triggers**: `naming`, `convention`, `file name`, `validate naming`, `fix naming`, `naming violation`

- **dependency-analyzer**: Analyze skill dependencies and detect circular refs
  - **Triggers**: `dependency`, `circular dependency`, `dependency graph`, `analyze dependencies`, `dependency visualization`, `dependency audit`

- **format-compliance-tester**: Test format compliance against AgentSkills spec
  - **Triggers**: `format compliance`, `test compliance`, `validate format`, `section completeness`, `compliance report`, `quality check`

---

### orchestration

Domain for skill orchestration, chaining, routing, and workflow management.

- **task-skill-router**: Map user tasks to optimal skills
  - **Triggers**: `route task`, `skill routing`, `task mapping`, `select skill`, `match task to skill`, `skill selection`

- **skill-recommendation**: Recommend relevant skills based on queries
  - **Triggers**: `recommend skill`, `skill suggestion`, `find skills`, `skill relevance`, `similar skills`, `skill match`

- **multi-skill-chaining-engine**: Chain multiple skills in sequence or parallel
  - **Triggers**: `chain skills`, `skill pipeline`, `skill sequence`, `orchestrate skills`, `skill workflow`, `multi-skill`

---

### SECURITY_RESEARCH

Domain for security research and offensive security skills.

- **secrets-management-detection**: Scan for hardcoded secrets
  - **Triggers**: `secrets detection`, `secret scanning`, `credential detection`, `secrets management`, `secret rotation`, `hardcoded secrets`

- **pentesting-workflow-automation**: Automated penetration testing
  - **Triggers**: `pentest`, `penetration testing`, `security scan`, `vulnerability assessment`, `ethical hacking`, `security testing`

---

### META_SKILL_DISCOVERY

Domain for discovering and analyzing skills.

- **domain-analysis-and-remediation**: Analyze domain directories for quality issues
  - **Triggers**: `analyze domain`, `domain analysis`, `skill remediation`, `fix skills`, `evaluate skills`, `domain refresh`, `clean up domain`

- **skill-analyzer**: Analyze existing skill to understand capabilities
  - **Triggers**: `analyze skill`, `what does this skill do`, `skill review`, `evaluate skill`, `skill analysis`, `understand skill`, `skill capability`, `can this skill`

- **context-offloading**: Save and retrieve context across sessions
  - **Triggers**: `save context`, `remember`, `memory`, `prior context`, `load history`, `session memory`, `project memory`

---

### XAI_EXPLAINABILITY

Domain for explainable AI skills.

- **shapiq-explainability-pipeline**: Build SHAP-IQ explainability pipelines
  - **Triggers**: `SHAP-IQ`, `Shapley interactions`, `feature interactions`, `pairwise effects`, `explainability pipeline`, `XAI`

- **xai-plotly-visualization**: Create interactive Plotly XAI visualizations
  - **Triggers**: `SHAP plot`, `feature importance`, `interaction heatmap`, `waterfall plot`, `explainability`, `XAI visualization`

---

### PRODUCTION_OPERATIONS

Domain for production-grade skill operations.

- **skill-evolution-metadata**: Track skill evolution metadata
  - **Triggers**: `skill metadata`, `evolution tracking`, `version history`, `origin tracking`, `skill quality`

- **self-evolving-skill-engine**: Build self-evolving AI agent systems
  - **Triggers**: `self-evolving`, `skill evolution`, `auto-improve`, `skill repair`, `pattern capture`, `evolution modes`

---

### SKILLSMP_ECOSYSTEM

Domain for SkillsMP (Skill Marketplace) integration.

- **skillsmp-master**: Master skill for all SkillsMP operations
  - **Triggers**: `skillsmp`, `skill marketplace`, `AI skills`, `agent skills`, `find skills`, `learn skills`, `orchestrate`

---

### logic

Domain for logic programming and formal methods.

- **design-pattern-recommender**: Recommend design patterns for problems
  - **Triggers**: `design pattern`, `recommend pattern`, `which pattern`, `pattern selection`, `architectural pattern`, `refactor pattern`

- **tla-plus-specification**: Write TLA+ formal specifications
  - **Triggers**: `TLA+`, `formal specification`, `model checking`, `temporal logic`, `formal verification`, `PlusCal`

---

### DATABASE_ENGINEERING

Domain for database development skills.

- **database-architect**: Design database schemas and architecture
  - **Triggers**: `database`, `SQL`, `schema`, `PostgreSQL`, `MongoDB`, `query`, `migration`, `index`, `connection pool`, `repository pattern`, `ORM`, `EF Core`, `postgres`

- **sql-optimization-patterns**: Optimize SQL queries and performance
  - **Triggers**: `SQL optimization`, `slow query`, `EXPLAIN`, `index`, `performance`, `database`, `optimize`, `execution plan`

---

### DEVOPS

Domain for DevOps and infrastructure.

- **deployment-patterns**: CI/CD pipelines and deployment strategies
  - **Triggers**: `deploy`, `deployment`, `CI/CD`, `pipeline`, `Docker`, `containerize`, `release`, `rollback`, `health check`, `production ready`

---

### DATA_ENGINEERING

Domain for data pipeline development.

- **data-pipeline-orchestrator**: Build and orchestrate data pipelines
  - **Triggers**: `ETL`, `data pipeline`, `extract transform load`, `airflow`, `schedule`, `batch`, `data sync`, `data migration`, `data warehouse`, `dbt`

- **web-scraper-agent**: Web scraping and data extraction
  - **Triggers**: `scrape`, `crawl`, `extract data`, `web fetch`, `parse html`, `get prices`, `monitor website`, `apify`, `firecrawl`, `crawlee`

---

### LLM_INTEGRATION

Domain for LLM integration skills.

- **llm-agent-integration**: Integrate LLMs with agents
  - **Triggers**: `LLM`, `Claude`, `OpenAI`, `GPT`, `Gemini`, `prompt`, `embedding`, `RAG`, `tool use`, `function calling`, `streaming`, `AI agent`, `chat completion`

- **google-adk-2-agent-builder**: Build agents with Google ADK 2.0
  - **Triggers**: `ADK`, `agent development kit`, `google adk`, `build agent`, `graph workflow`, `workflow agent`, `multi-agent`, `sequential agent`, `parallel agent`, `loop agent`, `run agent`

---

### SOFTWARE_TESTING

Domain for testing skills.

- **tdd-workflow**: Test-driven development workflow
  - **Triggers**: `TDD`, `test driven`, `write tests first`, `red green refactor`, `test coverage`, `unit test`, `integration test`

- **comprehensive-testing-harness**: Full testing framework
  - **Triggers**: `test`, `pytest`, `unit test`, `integration test`, `e2e`, `coverage`, `expect`, `assert`, `mock`, `fixture`, `playwright`, `vitest`, `jest`, `debug test`, `test failure`

---

### EMBEDDED_SYSTEMS

Domain for embedded systems development.

- **multi-platform-cross-compilation**: Cross-compile for multiple architectures
  - **Triggers**: `cross-compile`, `multi-arch`, `Buildroot`, `ARM toolchain`, `embedded build`

---

### FRONTEND

Domain for frontend development.

- **frontend-development**: Full frontend development (React/Vue/Angular)
  - **Triggers**: `frontend`, `react`, `vue`, `angular`, `component`, `state management`, `responsive`, `UI`, `web development`

---

### COGNITIVE_SKILLS

Domain for cognitive thinking skills.

- **belief-revision**: Update beliefs based on evidence
  - **Triggers**: `belief revision`, `update beliefs`, `Bayesian update`, `evidence-based`, `epistemic`, `belief update`

---

<!-- Add new skills above this line -->

---

## Part 2: Recipes

Recipes combine multiple skills to achieve specific outcomes. Each recipe shows the skills used, input/output format, and steps.

---

### Recipe 1: Security Audit Combo

**Description**: Complete codebase security review scanning for secrets and vulnerabilities.

**Skills Used**:
- secrets-management-detection
- security-scan

**Input**:
```yaml
scan_request:
  target_path: string
  scan_depth: "full" | "quick"
  include_secrets: true
  include_vulnerabilities: true
```

**Output**:
```yaml
audit_result:
  secrets_found: array
  vulnerabilities: array
  risk_score: number
  recommendations: array
```

**Steps**:
1. Invoke `secrets-management-detection` to scan for hardcoded secrets
2. Use output to inform `security-scan` scope
3. Run `security-scan` for vulnerability assessment
4. Combine results into comprehensive audit report

---

### Recipe 2: Spec-to-Test Pipeline

**Description**: Generate and execute tests directly from specification documents.

**Skills Used**:
- spec-contract-authoring
- executable-spec-harness

**Input**:
```yaml
pipeline_input:
  spec_path: string
  target_framework: "pytest" | "jest" | "junit"
  test_types: ["unit", "integration"]
```

**Output**:
```yaml
pipeline_output:
  generated_tests: array
  test_files: array
  execution_results: object
  coverage_report: object
```

**Steps**:
1. Use `spec-contract-authoring` to create machine-readable spec (OpenAPI/JSON Schema)
2. Feed spec to `executable-spec-harness` to generate test code
3. Execute generated tests
4. Report coverage and results

---

### Recipe 3: Multi-Agent Setup

**Description**: Create a working multi-agent system with task routing and chaining.

**Skills Used**:
- task-skill-router
- multi-skill-chaining-engine

**Input**:
```yaml
setup_input:
  agent_count: number
  agent_roles: array
  communication_mode: "sync" | "async"
```

**Output**:
```yaml
setup_output:
  agent_configs: array
  routing_logic: object
  execution_pipeline: object
  ready_to_run: boolean
```

**Steps**:
1. Define agent roles and types
2. Use `task-skill-router` to create routing logic
3. Use `multi-skill-chaining-engine` to build execution pipeline
4. Output combined configuration for running agents

---

### Recipe 4: Domain Analysis

**Description**: Complete health assessment of a skill domain with remediation.

**Skills Used**:
- domain-analysis-and-remediation
- skill-analyzer

**Input**:
```yaml
analysis_input:
  domain_path: string
  scan_depth: "quick" | "medium" | "thorough"
  fix_mode: boolean
```

**Output**:
```yaml
analysis_output:
  domain_status: object
  issues_found: array
  skills_evaluated: object
  implemented_skills: array
  recommendations: array
```

**Steps**:
1. Run `domain-analysis-and-remediation` to scan domain
2. For each issue found, use `skill-analyzer` to understand existing skills
3. Implement fixes for high-value missing skills
4. Generate final health report

---

### Recipe 5: XAI Analysis Pipeline

**Description**: Interactive SHAP-IQ analysis with visualization.

**Skills Used**:
- shapiq-explainability-pipeline
- xai-plotly-visualization

**Input**:
```yaml
xai_input:
  model: object
  data: array
  interaction_level: number
  visualization_type: "heatmap" | "waterfall" | "bar"
```

**Output**:
```yaml
xai_output:
  shapley_values: object
  interactions: object
  visualizations: array
  interpretation: string
```

**Steps**:
1. Use `shapiq-explainability-pipeline` to compute SHAP-IQ values
2. Pass results to `xai-plotly-visualization` for interactive charts
3. Generate combined report with values and visuals

---

### Recipe 6: Test-Driven Development Workflow

**Description**: Full test coverage implementation using TDD methodology.

**Skills Used**:
- tdd-workflow
- comprehensive-testing-harness

**Input**:
```yaml
tdd_input:
  feature_spec: string
  coverage_target: number
  test_types: ["unit", "integration", "e2e"]
```

**Output**:
```yaml
tdd_output:
  test_files: array
  coverage_report: object
  passed_tests: number
  failed_tests: number
```

**Steps**:
1. Use `tdd-workflow` to drive development with tests
2. Leverage `comprehensive-testing-harness` for framework setup
3. Achieve target coverage
4. Generate coverage report

---

### Recipe 7: Skill Evolution System

**Description**: Self-improving skill system with metadata tracking.

**Skills Used**:
- skill-evolution-metadata
- self-evolving-skill-engine

**Input**:
```yaml
evolution_input:
  skills_path: string
  enable_auto_improve: boolean
  track_metrics: boolean
```

**Output**:
```yaml
evolution_output:
  metadata_schema: object
  evolution_history: array
  improved_skills: array
  metrics: object
```

**Steps**:
1. Use `skill-evolution-metadata` to define metadata schema
2. Initialize `self-evolving-skill-engine` with schema
3. Run task executions and capture patterns
4. Review evolution history and improvements

---

### Recipe 8: API Specification Lifecycle

**Description**: Complete API spec management from authoring to monitoring.

**Skills Used**:
- spec-contract-authoring
- spec-evolution-engine
- spec-regression-monitoring

**Input**:
```yaml
lifecycle_input:
  api_name: string
  version: string
  spec_type: "openapi" | "json-schema"
```

**Output**:
```yaml
lifecycle_output:
  specification: object
  version_history: array
  breaking_changes: array
  migration_guide: object
```

**Steps**:
1. Author initial spec with `spec-contract-authoring`
2. Manage evolution with `spec-evolution-engine`
3. Monitor for regressions using `spec-regression-monitoring`
4. Generate migration documentation

---

### Recipe 9: LLM Agent with RAG

**Description**: Build complete LLM agent with RAG knowledge retrieval.

**Skills Used**:
- llm-agent-integration
- data-pipeline-orchestrator
- executable-spec-harness

**Input**:
```yaml
agent_input:
  knowledge_sources: array
  llm_provider: string
  capabilities: array
```

**Output**:
```yaml
agent_output:
  agent_config: object
  rag_pipeline: object
  test_results: object
  ready_to_deploy: boolean
```

**Steps**:
1. Use `data-pipeline-orchestrator` to build RAG pipeline from knowledge sources
2. Integrate with `llm-agent-integration` for LLM capabilities
3. Validate with `executable-spec-harness` against spec
4. Output deployment-ready agent

---

### Recipe 10: Database Performance Optimization

**Description**: End-to-end database optimization from schema to queries.

**Skills Used**:
- database-architect
- sql-optimization-patterns

**Input**:
```yaml
db_input:
  schema_requirements: object
  existing_queries: array
  performance_targets: object
```

**Output**:
```yaml
db_output:
  schema_design: object
  optimized_queries: array
  index_recommendations: array
  performance_report: object
```

**Steps**:
1. Use `database-architect` to design optimal schema
2. Analyze existing queries with `sql-optimization-patterns`
3. Apply optimizations and create indexes
4. Generate performance report

---

### Recipe 11: Context-Aware Workflow

**Description**: Enable agents to maintain context across sessions for better continuity.

**Skills Used**:
- context-offloading
- skill-analyzer

**Input**:
```yaml
workflow_input:
  project_path: string
  current_task: string
  enable_memory: boolean
```

**Output**:
```yaml
workflow_output:
  prior_context: array
  relevant_decisions: array
  session_continuity: boolean
  memory_saved: boolean
```

**Steps**:
1. Use `context-offloading` to query for relevant prior context
2. Use `skill-analyzer` to understand current project skills
3. Combine context with current task
4. Save new decisions and notes back with `context-offloading`

---

<!-- Add new recipes above this line -->

---

## Maintenance

To add new skills to the SPELLBOOK:

1. Find the skill in its domain directory
2. Copy the `name` and `description` from frontmatter
3. Extract 2 example phrases from the "Triggers" in description
4. Add to appropriate domain section in Part 1

To add new recipes:

1. Define the recipe with Description, Skills Used, Input, Output, Steps
2. Add to Part 2 following the template format
3. Use skills that exist in Part 1

---

*Last updated: 2026-04-07*
*This SPELLBOOK is designed to be updated as skills and recipes are added or discovered.*