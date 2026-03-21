# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-03-21

### Added
- Comprehensive software quality audit report
- CI/CD pipeline with linting and testing
- pytest-cov integration for coverage reporting
- Safety dependency scanning
- CONTRIBUTING.md with contribution guidelines
- CODEOWNERS file for code ownership
- New test files for better coverage:
  - test_server_modules.py
  - test_infrastructure.py
  - test_core_extended.py
  - test_monitoring_extended.py

### Changed
- Split monolithic enhanced_mcp_server_v3.py into modular components:
  - config.py - ServerConfig class
  - server.py - EnhancedMCPServerV3 class
- Updated ruff from 0.8.4 to 0.15.7
- Pinned all dependencies in requirements.txt
- Fixed syntax errors in skill files:
  - technique_application.py
  - skill_drafting.py

### Fixed
- Test import paths in test_mcp_server_fix.py
- Removed --exit-zero flag from CI linting
- Added submodule handling in CI

### Security
- Updated .env.example with security warnings
- Added guidance for secrets rotation

## [0.0.1] - 2026-01-01

### Added
- Initial release
- Skill Flywheel core functionality
- 345+ specialized skills
- MCP server implementation
