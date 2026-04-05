---
Domain: APPLICATION_SECURITY
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: automated-security-testing
---
origin: manual
triggers:
  - agent
  - ai
  - development
quality:
  applied_count: 0
  success_count: 0
  completion_rate: 0.0
  token_savings_avg: 0.0
created_at: "2026-03-24T10:00:00Z"
updated_at: "2026-03-24T10:00:00Z"




## Description

Implements comprehensive automated security testing throughout the development pipeline, including static analysis, dynamic testing, interactive testing, and runtime protection, ensuring continuous security validation without slowing down development velocity.


## Purpose

To be provided dynamically during execution.

## Input Format

```yaml
request:
  action: string
  parameters: object
```

## Output Format

```yaml
response:
  status: string
  result: object
  errors: array
```

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Core Concepts

### 1. Static Application Security Testing (SAST)
- Source code analysis for security vulnerabilities
- Rule-based vulnerability detection
- Integration with development environments
- Real-time security feedback during coding

### 2. Dynamic Application Security Testing (DAST)
- Runtime application vulnerability scanning
- Black-box security testing
- Automated penetration testing
- Web application security assessment

### 3. Interactive Application Security Testing (IAST)
- Hybrid security testing approach
- Real-time vulnerability detection during testing
- Runtime application self-protection (RASP)
- Continuous security monitoring

### 4. Software Composition Analysis (SCA)
- Open source dependency vulnerability scanning
- License compliance checking
- Supply chain security assessment
- Automated dependency updates

## Implementation Framework

### Phase 1: Tool Selection and Integration
1. **Security Testing Tool Assessment**
   - Evaluate SAST, DAST, IAST, and SCA tools
   - Assess tool accuracy and false positive rates
   - Consider integration capabilities with existing tools
   - Evaluate scalability and performance requirements

2. **Development Environment Integration**
   - IDE plugins for real-time security feedback
   - Pre-commit hooks for security checks
   - Local security testing capabilities
   - Developer-friendly security tooling

### Phase 2: CI/CD Pipeline Integration
1. **Build-Time Security Testing**
   - SAST integration in build processes
   - Automated code quality and security gates
   - Security test result reporting and tracking
   - Vulnerability prioritization and triage

2. **Deployment-Time Security Testing**
   - DAST scanning in staging environments
   - Automated security regression testing
   - Infrastructure security validation
   - Container and cloud security scanning

### Phase 3: Runtime Security
1. **Runtime Application Protection**
   - RASP implementation for real-time protection
   - Web application firewall (WAF) configuration
   - Runtime vulnerability detection
   - Automated incident response

2. **Continuous Security Monitoring**
   - Real-time security metrics collection
   - Automated security alerting
   - Security dashboard and reporting
   - Compliance monitoring and reporting

### Phase 4: Advanced Testing Capabilities
1. **API Security Testing**
   - Automated API security scanning
   - GraphQL security testing
   - REST API vulnerability assessment
   - API authentication and authorization testing

2. **Mobile Application Security Testing**
   - Mobile app static and dynamic analysis
   - Mobile-specific vulnerability detection
   - Mobile app runtime protection
   - Mobile app compliance checking

## Best Practices

### 1. Comprehensive Coverage
- Test all application components and dependencies
- Include both custom code and third-party components
- Cover all attack vectors and security controls
- Test across different environments and configurations

### 2. Accuracy and Reliability
- Minimize false positives through proper configuration
- Regularly update security rules and signatures
- Validate security test results manually when needed
- Maintain high confidence in automated security testing

### 3. Developer Experience
- Provide clear, actionable security feedback
- Integrate security testing seamlessly into development workflow
- Offer security guidance and remediation advice
- Minimize security testing friction

### 4. Continuous Improvement
- Regularly review and update security testing processes
- Analyze security test results for trends and patterns
- Update security testing tools and configurations
- Learn from security incidents and near-misses

## Dependencies

### SAST Tools
- SonarQube, SonarCloud for code quality and security
- Checkmarx, Veracode for enterprise SAST
- CodeQL, Semgrep for open source SAST
- ESLint, Pylint with security plugins

### DAST Tools
- OWASP ZAP, Burp Suite for web application testing
- Acunetix, Netsparker for automated scanning
- Tenable.io, Qualys for comprehensive vulnerability scanning
- Custom DAST solutions for specific requirements

### IAST and RASP
- Contrast Security, Hdiv for IAST solutions
- Signal Sciences, Imperva for RASP
- Custom runtime security monitoring
- Container security runtime protection

### SCA Tools
- Snyk, WhiteSource for dependency scanning
- OWASP Dependency-Check for open source scanning
- Black Duck, Nexus IQ for enterprise solutions
- GitHub Dependabot for automated updates

### CI/CD Integration
- Jenkins, GitLab CI, GitHub Actions for pipeline integration
- Docker, Kubernetes for container security testing
- Terraform, CloudFormation for infrastructure security
- Slack, Teams for security alerting and notifications

## Success Metrics

### Testing Coverage Metrics
- Percentage of code covered by security testing
- Number of vulnerabilities detected and fixed
- Time from vulnerability detection to remediation
- Security test execution frequency and reliability

### Development Efficiency Metrics
- Time added to development cycle by security testing
- Developer satisfaction with security testing tools
- Reduction in manual security testing effort
- Security testing automation percentage

### Security Quality Metrics
- Number and severity of vulnerabilities in production
- False positive rates in automated security testing
- Security test accuracy and reliability
- Security debt reduction over time

### Business Impact Metrics
- Cost savings from early vulnerability detection
- Reduction in security incidents and breaches
- Improved compliance audit results
- Enhanced customer trust and satisfaction

## Troubleshooting

### 1. Tool Overload
- Don't implement too many security testing tools
- Avoid redundant security testing capabilities
- Don't ignore tool integration and compatibility
- Focus on quality over quantity of security tools

### 2. Poor Configuration
- Don't use default security testing configurations
- Avoid ignoring false positive management
- Don't neglect regular tool updates and maintenance
- Ensure proper tuning for your specific environment

### 3. Lack of Integration
- Don't treat security testing as separate from development
- Avoid manual security testing processes
- Don't ignore the need for automated workflows
- Ensure security testing integrates with existing tools

### 4. Insufficient Training
- Don't assume developers understand security testing results
- Avoid ignoring the need for security testing training
- Don't neglect security testing best practices education
- Provide ongoing support for security testing adoption

## Implementation Checklist

- [ ] Assess current security testing maturity
- [ ] Select appropriate security testing tools
- [ ] Integrate security testing into development environment
- [ ] Implement CI/CD pipeline security testing
- [ ] Configure runtime security monitoring
- [ ] Establish security testing policies and procedures
- [ ] Train development teams on security testing
- [ ] Monitor and optimize security testing effectiveness
- [ ] Regularly review and update security testing approach
- [ ] Measure and report on security testing outcomes

## Advanced Features

### AI-Powered Security Testing
- Machine learning for vulnerability detection
- Intelligent false positive reduction
- Automated security test optimization
- Predictive security risk assessment

### Cloud-Native Security Testing
- Kubernetes security testing automation
- Serverless application security testing
- Cloud infrastructure security validation
- Multi-cloud security testing strategies

### DevSecOps Integration
- Security testing as code
- Infrastructure security testing automation
- Container security testing pipelines
- GitOps security testing workflows

## Future Enhancements

### Quantum-Resistant Security Testing
- Post-quantum cryptography testing
- Quantum computing security implications
- Future-proof security testing approaches
- Quantum-safe algorithm validation

### AI/ML Security Testing
- Adversarial machine learning testing
- AI model security validation
- Machine learning security automation
- Intelligent security testing orchestration

This skill provides a comprehensive framework for implementing automated security testing that ensures continuous security validation while maintaining development velocity and quality.


## Capabilities

To be provided dynamically during execution.

## Usage Examples

### Basic Usage
'Use automated-security-testing to analyze my current project context.'

### Advanced Usage
'Run automated-security-testing with focus on high-priority optimization targets.'

## Configuration Options

- `execution_depth`: Control the thoroughness of the analysis (default: standard).
- `report_format`: Choose between markdown, json, or console output.
- `verbose`: Enable detailed logging for debugging purposes.

## Error Handling

- **Invalid Input**: The skill will report specific missing parameters and request clarification.
- **Timeout**: Large-scale operations will be chunked to avoid process hangs.
- **Tool Failure**: Fallback mechanisms will attempt alternative logic paths.

## Performance Optimization

- **Caching**: Results are cached when applicable to reduce redundant computations.
- **Lazy Loading**: Supporting assets are only loaded when strictly necessary.
- **Parallelization**: Multi-target scans are executed in parallel where supported.

## Integration Examples

### Pipeline Integration
This skill is a core component of `FLOW.full_cycle.yaml` and works well with `skill-drafting` for automated refinement.

## Monitoring and Metrics

- **Execution Time**: Tracked per run to identify bottlenecks.
- **Success Rate**: Monitored across automated cycles to ensure reliability.
- **Token Usage**: Optimized to minimize context window consumption.

## Version History

- **1.0.0**: Initial automated generation via Skill Flywheel Phase 7.

## License

MIT License - Part of the Open AgentSkills Library.

## Constraints

To be provided dynamically during execution.