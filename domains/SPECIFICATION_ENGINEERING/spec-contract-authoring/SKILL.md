---
name: spec-contract-authoring
description: "Use when: authoring executable specifications that serve as both documentation and tests, creating machine-readable specs (OpenAPI, JSON Schema) from requirements, or implementing contract-first development. Triggers: 'executable spec', 'contract first', 'API spec', 'machine readable spec', 'spec as test', 'documentation as code'. NOT for: simple internal docs, early exploration phases, or when specs won't be executed/validated."
---

# Spec Contract Authoring

Author executable specifications that serve as both documentation and tests. This skill creates machine-readable specifications that can be validated and tested programmatically.

## When to Use This Skill

Use this skill when:
- Authoring specifications that need to be executable as tests
- Creating machine-readable specs (OpenAPI, JSON Schema, GraphQL)
- Implementing contract-first development approaches
- Generating documentation from code contracts
- Building consumer-driven contracts for APIs

Do NOT use this skill when:
- Simple internal documentation only
- Early exploration phases with high uncertainty
- Specifications won't be executed or validated
- Team lacks tooling for spec execution

## Input Format

```yaml
contract_request:
  name: string                  # Contract/API name
  domain: string                # Business domain
  requirements: array           # Functional requirements
  data_models: array            # Data model definitions
  integrations: array           # Integration points
  format: string               # Target format (openapi, json-schema, graphql)
```

## Output Format

```yaml
contract_result:
  specification: object         # Generated specification
  schema_files: array          # Schema definition files
  documentation: object        # Generated documentation
  test_scaffolding: object     # Test templates
```

## Capabilities

### 1. Contract Design (15 min)

- Define API endpoints and operations
- Design request/response schemas
- Specify error handling and status codes
- Define authentication requirements

### 2. Schema Generation (15 min)

- Generate JSON Schema for data models
- Create OpenAPI/Swagger specifications
- Build GraphQL type definitions
- Define validation rules

### 3. Documentation Generation (10 min)

- Generate human-readable documentation
- Create usage examples
- Build API reference guides
- Export to common formats (MD, HTML)

### 4. Test Scaffolding (15 min)

- Generate test templates from contracts
- Create sample test data
- Build contract validation tests
- Define success criteria

### 5. Validation Rules (10 min)

- Define input validation constraints
- Specify business rule validations
- Create custom validation functions
- Document validation expectations

## Usage Examples

### Basic Usage

"Create an OpenAPI specification for my user management API."

### Advanced Usage

"Generate executable contract with JSON Schema, OpenAPI docs, and pytest test scaffolding."

## Configuration Options

- `format`: Target specification format
- `version`: API version (for versioning)
- `style`: REST, GraphQL, or gRPC
- `validation`: Include validation rules

## Constraints

- MUST generate machine-readable specs
- SHOULD include test scaffolding
- MUST document all fields and parameters
- SHOULD provide examples

## Integration Examples

- API frameworks: Generate from specs (FastAPI, Express)
- Testing: Execute specs as tests
- Documentation: Publish auto-generated docs
- Code generation: Generate client/server stubs

## Dependencies

- Python 3.10+
- OpenAPI generators
- Schema validation libraries
- Documentation generators
