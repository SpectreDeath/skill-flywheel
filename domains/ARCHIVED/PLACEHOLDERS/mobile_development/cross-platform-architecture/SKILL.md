---
Domain: mobile_development
Version: 1.0.0
Complexity: Medium
Type: Process
Category: Development
Estimated Execution Time: 100ms - 2 minutes
name: cross-platform-architecture
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

Automatically designs and implements optimal cross-platform mobile architecture patterns for React Native, Flutter, Swift, and Kotlin applications. This skill analyzes platform requirements, performance constraints, and development team expertise to recommend and generate architecture solutions that maximize code reuse while maintaining native performance and user experience.


## Purpose

To be provided dynamically during execution.

## Examples

To be provided dynamically during execution.

## Implementation Notes

To be provided dynamically during execution.
## Capabilities

- **Architecture Pattern Selection**: Analyze project requirements and recommend optimal cross-platform patterns (MVVM, Clean Architecture, Redux, BLoC, etc.)
- **Platform-Specific Optimization**: Generate platform-specific implementations while maintaining shared business logic
- **Code Sharing Strategy**: Design optimal code sharing strategies between React Native, Flutter, Swift, and Kotlin
- **Performance Architecture**: Implement architecture patterns optimized for mobile performance constraints
- **State Management Design**: Design scalable state management solutions across platforms
- **Dependency Injection Setup**: Configure dependency injection frameworks for cross-platform consistency
- **Navigation Architecture**: Design unified navigation patterns across platforms

## Usage Examples

### Cross-Platform Architecture Selection

```yaml
architecture_selection:
  project_requirements:
    platforms: ["iOS", "Android", "Web"]
    performance_requirements: "high"
    team_expertise: ["React Native", "Flutter"]
    code_sharing_target: "80%"
    complexity_level: "medium"
  
  recommended_architecture:
    pattern: "Clean Architecture with Platform Abstraction"
    confidence_score: 0.92
    rationale: "Balances code reuse with platform-specific optimizations"
    
    layer_structure:
      - layer: "Domain Layer"
        description: "Platform-agnostic business logic"
        technologies: ["Pure Dart", "Pure JavaScript/TypeScript"]
        code_sharing: "100%"
      
      - layer: "Platform Abstraction Layer"
        description: "Interface definitions for platform-specific features"
        technologies: ["Abstract classes", "Interfaces"]
        code_sharing: "100%"
      
      - layer: "Platform Implementation Layer"
        description: "Platform-specific implementations"
        technologies: ["Swift", "Kotlin", "Native Modules"]
        code_sharing: "0%"
      
      - layer: "Presentation Layer"
        description: "Platform-specific UI components"
        technologies: ["Flutter Widgets", "React Native Components"]
        code_sharing: "0%"
  
  implementation_strategy:
    shared_code_location: "libs/shared_domain"
    platform_specific_location: "platforms/{ios|android|web}"
    build_configuration: "monorepo with platform-specific builds"
    testing_strategy: "Shared unit tests + Platform-specific integration tests"
```

### React Native Architecture Implementation

```yaml
react_native_architecture:
  pattern: "Redux with TypeScript"
  structure:
    - directory: "src/store"
      purpose: "State management configuration"
      files: ["configureStore.ts", "rootReducer.ts", "middleware/"]
    
    - directory: "src/features"
      purpose: "Feature-based organization"
      files: ["auth/", "user/", "settings/", "common/"]
    
    - directory: "src/services"
      purpose: "API and platform abstraction"
      files: ["api/", "platform/", "storage/"]
    
    - directory: "src/components"
      purpose: "Shared UI components"
      files: ["common/", "platform-specific/"]
  
  state_management:
    store_structure:
      - slice: "auth"
        purpose: "Authentication state"
        actions: ["login", "logout", "refreshToken"]
        reducers: ["authReducer"]
      
      - slice: "user"
        purpose: "User data and preferences"
        actions: ["updateProfile", "fetchUserData"]
        reducers: ["userReducer"]
    
    middleware_configuration:
      - middleware: "thunk"
        purpose: "Async action handling"
        configuration: "Standard Redux Thunk"
      
      - middleware: "logger"
        purpose: "Development debugging"
        configuration: "Conditional based on environment"
  
  platform_integration:
    native_modules:
      - module: "PushNotifications"
        purpose: "Cross-platform push notifications"
        implementation: "React Native Push Notification"
      
      - module: "BiometricAuth"
        purpose: "Platform-specific biometric authentication"
        implementation: "react-native-biometrics"
    
    performance_optimization:
      - optimization: "Memoization"
        implementation: "React.memo, useMemo, useCallback"
      
      - optimization: "Virtualization"
        implementation: "FlatList, SectionList for long lists"
      
      - optimization: "Code splitting"
        implementation: "Dynamic imports with React.lazy"
```

### Flutter Architecture Implementation

```yaml
flutter_architecture:
  pattern: "BLoC with Repository Pattern"
  structure:
    - directory: "lib/core"
      purpose: "Core architecture components"
      files: ["bloc/", "di/", "utils/", "constants/"]
    
    - directory: "lib/features"
      purpose: "Feature-based organization"
      files: ["auth/", "user/", "settings/", "common/"]
    
    - directory: "lib/domain"
      purpose: "Business logic and entities"
      files: ["entities/", "usecases/", "repositories/"]
    
    - directory: "lib/presentation"
      purpose: "UI components and screens"
      files: ["screens/", "widgets/", "themes/"]
  
  state_management:
    bloc_structure:
      - bloc: "AuthBloc"
        purpose: "Authentication state management"
        events: ["LoginEvent", "LogoutEvent", "AuthCheckEvent"]
        states: ["AuthInitial", "AuthLoading", "AuthSuccess", "AuthFailure"]
      
      - bloc: "UserBloc"
        purpose: "User data state management"
        events: ["FetchUserEvent", "UpdateUserEvent"]
        states: ["UserInitial", "UserLoading", "UserLoaded", "UserError"]
    
    repository_pattern:
      - repository: "AuthRepository"
        purpose: "Authentication data access"
        implementations: ["AuthApiRepository", "AuthLocalRepository"]
      
      - repository: "UserRepository"
        purpose: "User data access"
        implementations: ["UserApiRepository", "UserLocalRepository"]
  
  dependency_injection:
    injection_framework: "get_it with injectable"
    configuration:
      - service: "AuthService"
        lifetime: "singleton"
        implementation: "AuthApiService"
      
      - service: "UserService"
        lifetime: "singleton"
        implementation: "UserApiService"
      
      - service: "DatabaseService"
        lifetime: "singleton"
        implementation: "HiveDatabaseService"
```

## Input Format

### Architecture Design Request

```yaml
architecture_design_request:
  project_id: string              # Unique project identifier
  project_name: string            # Project name
  target_platforms: array         # Target platforms (iOS, Android, Web)
  
  technical_requirements:
    performance_requirements: "low|medium|high|critical"
    code_sharing_target: number   # Percentage of code to share
    team_expertise: array         # Team's technical expertise
    existing_codebase: boolean    # Whether existing codebase exists
    scalability_requirements: "small|medium|large|enterprise"
  
  platform_specific_requirements:
    ios_requirements: object      # iOS-specific requirements
    android_requirements: object  # Android-specific requirements
    web_requirements: object      # Web-specific requirements
  
  architecture_constraints:
    framework_constraints: array  # Required frameworks
    performance_constraints: object # Performance limitations
    compliance_requirements: array # Regulatory requirements
    deployment_constraints: object # Deployment limitations
```

### Platform Analysis Schema

```yaml
platform_analysis:
  react_native_analysis:
    current_usage: boolean        # Whether React Native is used
    version: string              # React Native version
    existing_architecture: string # Current architecture pattern
    performance_issues: array    # Known performance issues
    native_modules: array        # Existing native modules
  
  flutter_analysis:
    current_usage: boolean        # Whether Flutter is used
    version: string              # Flutter version
    existing_architecture: string # Current architecture pattern
    performance_issues: array    # Known performance issues
    platform_channels: array     # Existing platform channels
  
  native_analysis:
    ios_swift_analysis:
      version: string            # Swift version
      existing_patterns: array   # Existing patterns
      performance_constraints: array
      platform_features: array   # Required iOS features
    
    android_kotlin_analysis:
      version: string            # Kotlin version
      existing_patterns: array   # Existing patterns
      performance_constraints: array
      platform_features: array   # Required Android features
```

## Output Format

### Architecture Design Report

```yaml
architecture_design_report:
  project_id: string
  design_timestamp: timestamp
  selected_pattern: string
  confidence_score: number        # 0.0 to 1.0
  
  architecture_overview:
    pattern_name: string
    pattern_type: "MVVM|Clean Architecture|Redux|BLoC|VIPER|Flux"
    rationale: string             # Why this pattern was selected
    benefits: array               # Benefits of this pattern
    tradeoffs: array              # Tradeoffs and limitations
  
  layer_structure:
    - layer_name: string
      purpose: string
      technologies: array
      code_sharing_percentage: number
      dependencies: array
      responsibilities: array
  
  platform_specific_implementations:
    - platform: "iOS|Android|Web"
      implementation_details: object
      performance_optimizations: array
      platform_specific_features: array
      integration_points: array
  
  code_organization:
    directory_structure: object
    naming_conventions: object
    file_organization: object
    module_boundaries: array
  
  testing_strategy:
    unit_testing: object
    integration_testing: object
    e2e_testing: object
    platform_specific_testing: object
```

### Implementation Blueprint

```yaml
implementation_blueprint:
  pattern_name: string
  implementation_phases: array
  technology_stack: object
  code_samples: array
  
  phase_breakdown:
    - phase: "Foundation"
      duration: string
      tasks: array
      deliverables: array
      validation_criteria: array
    
    - phase: "Core Implementation"
      duration: string
      tasks: array
      deliverables: array
      validation_criteria: array
    
    - phase: "Platform Integration"
      duration: string
      tasks: array
      deliverables: array
      validation_criteria: array
  
  code_samples:
    - sample_name: string
      description: string
      code: string
      platform: string
      complexity: string
```

## Configuration Options

### Architecture Patterns

```yaml
architecture_patterns:
  mvvm:
    description: "Model-View-ViewModel pattern"
    best_for: ["data_binding", "testability", "separation_of_concerns"]
    complexity: "medium"
    platform_support: ["React Native", "Flutter", "Swift", "Kotlin"]
  
  clean_architecture:
    description: "Layered architecture with dependency inversion"
    best_for: ["large_applications", "testability", "maintainability"]
    complexity: "high"
    platform_support: ["React Native", "Flutter", "Swift", "Kotlin"]
  
  redux:
    description: "Unidirectional data flow with centralized state"
    best_for: ["complex_state_management", "predictable_state"]
    complexity: "medium"
    platform_support: ["React Native", "Flutter"]
  
  bloc:
    description: "Business Logic Component pattern"
    best_for: ["reactive_programming", "state_management"]
    complexity: "medium"
    platform_support: ["Flutter"]
  
  vipper:
    description: "View-Interactor-Presenter-Entity-Router"
    best_for: ["ios_applications", "clean_architecture"]
    complexity: "high"
    platform_support: ["Swift"]
```

### Platform Configurations

```yaml
platform_configurations:
  react_native:
    recommended_patterns: ["Redux", "Context API", "MobX"]
    performance_optimizations: ["Memoization", "Virtualization", "Code Splitting"]
    native_integration: ["Native Modules", "Bridge Components"]
  
  flutter:
    recommended_patterns: ["BLoC", "Provider", "Riverpod"]
    performance_optimizations: ["Widget Caching", "State Management", "Build Optimization"]
    platform_integration: ["Platform Channels", "Native Plugins"]
  
  swift:
    recommended_patterns: ["MVVM", "VIPER", "Clean Architecture"]
    performance_optimizations: ["Memory Management", "Concurrency", "Lazy Loading"]
    platform_integration: ["UIKit", "SwiftUI", "CocoaPods"]
  
  kotlin:
    recommended_patterns: ["MVVM", "MVP", "Clean Architecture"]
    performance_optimizations: ["Coroutines", "Memory Management", "View Binding"]
    platform_integration: ["Android Architecture Components", "Jetpack"]
```

## Error Handling

### Architecture Design Failures

```yaml
architecture_design_failures:
  conflicting_requirements:
    retry_strategy: "requirement_prioritization"
    max_retries: 2
    fallback_action: "simplified_architecture"
  
  performance_constraints_violation:
    retry_strategy: "performance_optimization"
    max_retries: 3
    fallback_action: "platform_specific_optimization"
  
  team_expertise_mismatch:
    retry_strategy: "training_recommendation"
    max_retries: 1
    fallback_action: "gradual_migration"
  
  technology_stack_conflicts:
    retry_strategy: "alternative_technologies"
    max_retries: 2
    fallback_action: "hybrid_approach"
```

### Implementation Errors

```yaml
implementation_errors:
  pattern_violation:
    detection_strategy: "static_analysis"
    recovery_strategy: "refactoring_guidance"
    escalation: "architecture_review"
  
  performance_degradation:
    detection_strategy: "profiling"
    recovery_strategy: "optimization_recommendations"
    escalation: "performance_audit"
  
  platform_integration_failure:
    detection_strategy: "integration_testing"
    recovery_strategy: "alternative_integration"
    escalation: "native_development"
```

## Performance Optimization

### Architecture-Level Optimization

```yaml
architecture_optimization:
  code_sharing_optimization: true
  platform_specific_optimization: true
  performance_monitoring: true
  scalability_optimization: true
  
  optimization_techniques:
    - technique: "Shared Business Logic"
      applicable_platforms: ["React Native", "Flutter", "Swift", "Kotlin"]
      performance_gain: "significant"
      complexity_overhead: "low"
    
    - technique: "Platform-Specific Rendering"
      applicable_platforms: ["React Native", "Flutter"]
      performance_gain: "high"
      complexity_overhead: "medium"
    
    - technique: "Lazy Loading Architecture"
      applicable_platforms: ["All platforms"]
      performance_gain: "moderate"
      complexity_overhead: "low"
```

### Platform-Specific Optimization

```yaml
platform_specific_optimization:
  react_native_optimization:
    - optimization: "Bridge Minimization"
      technique: "Reduce native bridge calls"
      impact: "Reduced JavaScript thread blocking"
    
    - optimization: "Image Optimization"
      technique: "Use native image loading"
      impact: "Reduced memory usage and faster rendering"
    
    - optimization: "List Virtualization"
      technique: "Implement FlatList/SectionList"
      impact: "Improved scroll performance"
  
  flutter_optimization:
    - optimization: "Widget Caching"
      technique: "Use const widgets and memoization"
      impact: "Reduced rebuild cycles"
    
    - optimization: "State Management Optimization"
      technique: "Efficient state updates"
      impact: "Reduced widget tree rebuilds"
    
    - optimization: "Build Optimization"
      technique: "Optimize build methods"
      impact: "Faster UI rendering"
```

## Integration Examples

### With Development Frameworks

```yaml
framework_integration:
  react_native_frameworks:
    navigation: "React Navigation"
    state_management: ["Redux", "MobX", "Context API"]
    testing: ["Jest", "Detox", "React Native Testing Library"]
    build_tools: ["Metro", "Expo", "Fastlane"]
  
  flutter_frameworks:
    navigation: "Flutter Navigator"
    state_management: ["BLoC", "Provider", "Riverpod"]
    testing: ["Flutter Test", "Integration Test"]
    build_tools: ["Flutter Build", "Fastlane"]
  
  native_frameworks:
    ios_frameworks: ["UIKit", "SwiftUI", "Combine"]
    android_frameworks: ["Android Architecture Components", "Jetpack Compose"]
    testing_frameworks: ["XCTest", "Espresso", "JUnit"]
```

### With CI/CD Pipelines

```yaml
cicd_integration:
  build_pipelines:
    react_native:
      build_command: "npm run build"
      test_command: "npm test"
      deploy_command: "fastlane deploy"
    
    flutter:
      build_command: "flutter build"
      test_command: "flutter test"
      deploy_command: "fastlane deploy"
    
    native:
      ios:
        build_command: "xcodebuild"
        test_command: "xcodebuild test"
        deploy_command: "fastlane ios deploy"
      
      android:
        build_command: "./gradlew build"
        test_command: "./gradlew test"
        deploy_command: "fastlane android deploy"
  
  quality_gates:
    code_coverage: "minimum 80%"
    performance_metrics: "defined thresholds"
    security_scanning: "enabled"
    architecture_compliance: "validated"
```

## Best Practices

1. **Architecture Selection**:
   - Analyze project requirements thoroughly before selecting architecture patterns
   - Consider team expertise and learning curve
   - Plan for scalability and maintainability
   - Choose patterns that align with platform capabilities

2. **Code Sharing Strategy**:
   - Share business logic and domain models
   - Keep platform-specific code separate
   - Use abstraction layers for platform differences
   - Maintain consistent APIs across platforms

3. **Performance Optimization**:
   - Profile applications regularly
   - Optimize critical paths and bottlenecks
   - Use platform-specific optimizations
   - Monitor memory usage and battery impact

4. **Testing Strategy**:
   - Implement comprehensive unit tests
   - Use integration tests for platform-specific features
   - Include performance and security testing
   - Automate testing in CI/CD pipelines

## Troubleshooting

### Common Issues

1. **Performance Problems**: Review architecture decisions, optimize rendering, reduce bridge calls, implement caching strategies
2. **Code Sharing Issues**: Check abstraction layers, review platform differences, validate API consistency
3. **Platform Integration Problems**: Verify native module implementations, check platform channel configurations, validate dependency management
4. **State Management Complexity**: Simplify state structure, review data flow, consider alternative patterns
5. **Build and Deployment Issues**: Check build configurations, validate platform-specific settings, review CI/CD pipeline

### Debug Mode

```yaml
debug_config:
  enabled: true
  log_level: "debug"
  architecture_debugging: true
  performance_debugging: true
  platform_integration_debugging: true
  state_management_debugging: true
```

## Monitoring and Metrics

### Key Performance Indicators

```yaml
kpi_metrics:
  architecture_quality:
    code_sharing_percentage: number
    maintainability_index: number
    test_coverage: number
    architecture_compliance: number
  
  performance_metrics:
    app_startup_time: number
    memory_usage: number
    battery_impact: number
    user_experience_score: number
  
  development_metrics:
    development_velocity: number
    bug_resolution_time: number
    feature_delivery_time: number
    team_satisfaction: number
```

## Dependencies

- **Architecture Analysis Tools**: Tools for analyzing existing codebases and architecture patterns
- **Performance Profiling Tools**: Tools for measuring and optimizing application performance
- **Code Quality Tools**: Static analysis and code quality measurement tools
- **Testing Frameworks**: Comprehensive testing frameworks for all platforms
- **CI/CD Tools**: Continuous integration and deployment tools for mobile applications

## Version History

- **1.0.0**: Initial release with basic cross-platform architecture patterns and implementation guidance
- **1.1.0**: Added advanced performance optimization techniques and platform-specific optimizations
- **1.2.0**: Enhanced integration with development frameworks and CI/CD pipelines
- **1.3.0**: Improved code sharing strategies and dependency injection patterns
- **1.4.0**: Advanced machine learning-based architecture recommendations and automated optimization

## License

This skill is part of the Agent Skills Library and follows the project's licensing terms.


## Constraints

To be provided dynamically during execution.