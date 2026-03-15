# Agent Skills Library 🚀

**Universal extensions for Goose, Cline, Cursor, Claude**  
*Level up any coding agent without subscriptions. Portable skills that work across models.*

> Copy → Drop → Use. No setup. No lock-in.

![Version](https://img.shields.io/badge/version-1.0-blue)
⭐ **Star if useful** - helps free agents everywhere

## 🔥 One Command Wonder

```bash
cp -r skills/ .agents/skills/ && echo "Run FLOW.onboard.yaml"
```

**That's it.** Your free agent is now enterprise-grade.

## Quick Start (2 minutes)

### 1. Install
```bash
# Copy skills to your agent's skills directory
cp -r skills/ ~/.agents/skills/          # For Cline
cp -r skills/ ~/.goose/skills/           # For Goose  
cp -r skills/ ~/.cursor/skills/          # For Cursor
cp -r skills/ ~/.claude/skills/          # For Claude
```

### 2. Use Immediately
```text
"Run SKILL.repo_recon.md on this repository and give me a summary."
"Execute FLOW.onboard.yaml on this project and report the results."
"Use SKILL.security_scan.md to check for security issues in the src/ directory."
```

### 3. Advanced Workflows
```text
"First run SKILL.repo_recon.md, then use SKILL.skill_drafting.md to create a refactoring plan based on the findings."
"Run FLOW.quality_audit.yaml and create a prioritized improvement roadmap."
```

## Why This Exists

Free agents lack structure. This library gives them:
- **Meta-skills** to build more skills
- **Repo skills** for onboarding/analysis 
- **Templates** that enforce quality
- **Zero vendor lock-in** - files work everywhere

## What You Get

### 🎯 **Meta-Skills (Force Multipliers)**
- **skill_drafting**: Transform messy intent into structured skills
- **skill_critiquing**: Review and refine existing skills
- **skill_template**: Standard structure for consistency

### 📁 **Repository & Onboarding Skills**
- **repo_recon**: Analyze codebase structure and tech stack
- **security_scan**: Detect security vulnerabilities and risks
- **test_survey**: Assess test coverage and quality
- **deps_audit**: Audit dependencies for health and security

### 🔧 **Code Quality Skills**
- **refactor_plan**: Develop safe refactoring strategies
- **perf_audit**: Identify performance bottlenecks
- **api_design**: Review and improve API design

### 🔄 **Automated Pipelines**
- **FLOW.onboard.yaml**: Complete new project onboarding workflow
- **FLOW.quality_audit.yaml**: Comprehensive code quality assessment
- **FLOW.skill_pipeline.yaml**: Meta-skill development workflow

## Real-World Example

Point any coding agent at a fresh repo and run `FLOW.onboard` to get structure, risk, tests, and dependency insights in one pass:

```text
User: "Run FLOW.onboard.yaml on this repository and summarize results in 3 bullet points per step."
Agent: [Executes onboarding pipeline]
Agent: "Here's your onboarding summary:
- **Structure Analysis**: React frontend, Node.js backend, PostgreSQL database
- **Security Scan**: 2 critical issues found, 5 medium-risk dependencies
- **Test Coverage**: 65% coverage, integration tests need expansion
- **Dependencies**: 3 packages need security updates
- **Next Steps**: 1) Fix security issues, 2) Update dependencies, 3) Add more tests"
```

## Overview

Agent Skills are modular, reusable workflows that turn messy, variable user tasks into well-scoped, repeatable procedures. This library provides:

- **Meta-Skills**: Skills for creating and improving other skills
- **Example Skills**: Demonstrations of best practices
- **Templates**: Standardized structures for new skills
- **Documentation**: Guidelines and patterns for skill development

## Quick Start

### For Users

1. Copy skills to your agent's skills directory (e.g., `.agents/skills/`, `.claude/skills/`)
2. Most agents will auto-discover skills in standard locations
3. Use skills by name in your prompts: "Use the repo_recon skill to analyze this codebase"

### For Developers

1. Use `skill_template.md` as a starting point for new skills
2. Follow the principles in `Agent_Skills_Development_Guide.md`
3. Test skills with realistic scenarios before sharing
4. Contribute improvements and new skills

## Skill Categories

### Meta-Skills

Skills that help you create and improve other skills:

- `SKILL.skill_drafting.md` - Turn messy intent into structured skills
- `SKILL.skill_critiquing.md` - Review and refine existing skills

### Example Skills

Demonstrations of best practices:

- `SKILL.repo_recon.md` - Analyze codebases for structure and risks

### Templates

Standardized structures:

- `skill_template.md` - Complete template for new skills

## Supported Platforms

These skills work across multiple agent platforms:

| Platform | Skills Support | MCP Support | Notes |
|----------|----------------|-------------|-------|
| Goose | Native | Yes | Local-first, extension-based |
| Cline | Yes | Native | Plan/Act modes + terminal |
| Cursor | Yes | Yes | IDE-integrated |
| Claude | Yes | Yes | Cross-platform |
| Any LLM with file access | Yes | No | Skills work without MCP |

## Development Guidelines

### Naming Conventions

- Use verb-noun pattern: `repo_recon`, `skill_drafting`
- Be specific: `security_review` vs `code_review`
- Include scope when helpful: `frontend_component_review`

### Structure Requirements

Every skill should include:

1. Clear purpose and scope
2. When to use / when NOT to use
3. Well-defined inputs and outputs
4. Step-by-step workflow
5. Explicit constraints and guardrails
6. Examples and edge cases
7. Asset dependencies

### Quality Standards

- Skills must be testable with clear success criteria
- Steps must be finite and bounded
- Constraints must be explicit and enforceable
- Examples must be realistic and helpful
- Documentation must be clear for both humans and LLMs

## Contributing

### Adding New Skills

1. Use `skill_template.md` as your starting point
2. Follow the principles in `Agent_Skills_Development_Guide.md`
3. Test thoroughly with realistic scenarios
4. Include clear examples and edge cases
5. Document all dependencies and assumptions

### Improving Existing Skills

1. Use `SKILL.skill_critiquing.md` to review the skill
2. Identify specific areas for improvement
3. Suggest concrete changes
4. Test improvements before submitting

### Best Practices for Contributors

- Keep skills focused and single-purpose
- Use consistent structure across all skills
- Document dependencies and assumptions clearly
- Plan for skill evolution and deprecation
- Consider composability with other skills

## Usage Examples

### Basic Usage

```text
"Use the repo_recon skill to analyze this codebase and identify potential security risks."
```

### With Parameters

```text
"Run the repo_recon skill on the /src directory with focus on performance issues."
```

### Chaining Skills

```text
"First use skill_drafting to create a new skill, then use skill_critiquing to review it."
```

## Troubleshooting

### Common Issues

- **Skill not found**: Ensure skill is in the correct directory for your agent
- **Missing dependencies**: Check the Assets section for required tools
- **Unclear results**: Review the skill's examples and constraints
- **Performance issues**: Check the Testing section for optimization guidance

### Debug Mode

Most skills support a debug mode for detailed logging:

```text
"Run repo_recon in debug mode to see detailed analysis steps."
```

### Getting Help

1. Check the skill's Troubleshooting section
2. Review the skill's examples and constraints
3. Use `SKILL.skill_critiquing.md` to identify issues
4. Consult `Agent_Skills_Development_Guide.md` for best practices

## License

This library is provided under the MIT License. See individual skill files for specific licensing information.

## Related Resources

- [Agent_Skills_Development_Guide.md](../Agent_Skills_Development_Guide.md) - Comprehensive guide to skill development
- [RL4 Documentation](../.rl4/) - Reasoning Layer 4 integration
- [MCP Documentation](https://mcp.dev) - Model Context Protocol for tool integration

## Community

Join the conversation about Agent Skills:

- Share your skills and templates
- Request new skills or improvements
- Discuss best practices and patterns
- Contribute to the ecosystem

Happy skill building! 🚀
