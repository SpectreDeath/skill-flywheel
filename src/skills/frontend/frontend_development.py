#!/usr/bin/env python3
"""
Frontend Development Skill Module
Provides comprehensive frontend development knowledge and guidance
without generating actual code. Focuses on concepts, best practices, and
architecture patterns for modern frontend development.
"""

import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FrontendDevelopmentSkill:
    """Frontend Development skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Frontend Development skill.
        
        Args:
            config: Configuration dictionary with frontend settings
        """
        self.config = config or {}
        self.frameworks = [
            'React', 'Vue.js', 'Angular', 'Svelte', 'Solid.js',
            'Preact', 'Alpine.js', 'Lit', 'Stencil'
        ]
        self.concepts = [
            'Component Architecture', 'State Management', 'Routing',
            'Performance Optimization', 'Accessibility', 'SEO',
            'Build Tools', 'Testing', 'CSS-in-JS', 'Server-Side Rendering'
        ]
        self.tools = [
            'Webpack', 'Vite', 'Rollup', 'ESBuild', 'Babel',
            'TypeScript', 'Jest', 'Cypress', 'Storybook', 'ESLint'
        ]
        
    def explain_frontend_concept(self, concept: str) -> Dict[str, Any]:
        """
        Explain a frontend development concept in detail.
        
        Args:
            concept: The frontend concept to explain
        
        Returns:
            Dictionary containing concept explanation and related information
        """
        try:
            # Get concept explanation
            explanation = self._get_concept_explanation(concept)
            
            # Get related concepts
            related_concepts = self._get_related_concepts(concept)
            
            # Get best practices
            best_practices = self._get_best_practices(concept)
            
            return {
                "status": "success",
                "concept": concept,
                "explanation": explanation,
                "related_concepts": related_concepts,
                "best_practices": best_practices,
                "framework_recommendations": self._get_framework_recommendations(concept)
            }
            
        except Exception as e:
            return {"error": f"Failed to explain concept: {str(e)}"}
    
    def analyze_frontend_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze frontend architecture requirements and provide recommendations.
        
        Args:
            requirements: Dictionary containing project requirements
        
        Returns:
            Dictionary containing architecture analysis and recommendations
        """
        try:
            # Analyze project scale
            project_scale = requirements.get("scale", "small")
            
            # Analyze performance requirements
            performance_reqs = requirements.get("performance", {})
            
            # Analyze team expertise
            team_expertise = requirements.get("team_expertise", "mixed")
            
            # Generate architecture recommendations
            architecture_recommendations = self._generate_architecture_recommendations(
                project_scale, performance_reqs, team_expertise
            )
            
            # Generate technology stack recommendations
            tech_stack = self._generate_tech_stack_recommendations(
                project_scale, performance_reqs, team_expertise
            )
            
            return {
                "status": "success",
                "requirements": requirements,
                "architecture_recommendations": architecture_recommendations,
                "technology_stack": tech_stack,
                "implementation_phases": self._get_implementation_phases(project_scale)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze architecture: {str(e)}"}
    
    def compare_frontend_frameworks(self, frameworks: List[str]) -> Dict[str, Any]:
        """
        Compare multiple frontend frameworks based on various criteria.
        
        Args:
            frameworks: List of frameworks to compare
        
        Returns:
            Dictionary containing framework comparison
        """
        try:
            comparison_results = {}
            
            for framework in frameworks:
                if framework in self.frameworks:
                    comparison_results[framework] = self._get_framework_comparison_data(framework)
                else:
                    comparison_results[framework] = {"error": f"Framework {framework} not in supported list"}
            
            # Generate comparison summary
            comparison_summary = self._generate_framework_comparison_summary(comparison_results)
            
            return {
                "status": "success",
                "frameworks": frameworks,
                "comparison_data": comparison_results,
                "comparison_summary": comparison_summary
            }
            
        except Exception as e:
            return {"error": f"Failed to compare frameworks: {str(e)}"}
    
    def provide_performance_optimization_guidance(self, project_type: str) -> Dict[str, Any]:
        """
        Provide performance optimization guidance for different project types.
        
        Args:
            project_type: Type of frontend project (SPA, SSR, static, etc.)
        
        Returns:
            Dictionary containing performance optimization guidance
        """
        try:
            # Get performance optimization strategies
            optimization_strategies = self._get_performance_optimization_strategies(project_type)
            
            # Get common performance pitfalls
            common_pitfalls = self._get_common_performance_pitfalls(project_type)
            
            # Get measurement techniques
            measurement_techniques = self._get_performance_measurement_techniques()
            
            return {
                "status": "success",
                "project_type": project_type,
                "optimization_strategies": optimization_strategies,
                "common_pitfalls": common_pitfalls,
                "measurement_techniques": measurement_techniques
            }
            
        except Exception as e:
            return {"error": f"Failed to provide performance guidance: {str(e)}"}
    
    def explain_state_management_patterns(self, pattern_type: str) -> Dict[str, Any]:
        """
        Explain different state management patterns and their use cases.
        
        Args:
            pattern_type: Type of state management pattern
        
        Returns:
            Dictionary containing pattern explanation and use cases
        """
        try:
            # Get pattern explanation
            pattern_explanation = self._get_state_management_pattern_explanation(pattern_type)
            
            # Get implementation considerations
            implementation_considerations = self._get_state_management_implementation_considerations(pattern_type)
            
            # Get framework-specific implementations
            framework_implementations = self._get_framework_specific_implementations(pattern_type)
            
            return {
                "status": "success",
                "pattern_type": pattern_type,
                "explanation": pattern_explanation,
                "implementation_considerations": implementation_considerations,
                "framework_implementations": framework_implementations
            }
            
        except Exception as e:
            return {"error": f"Failed to explain state management pattern: {str(e)}"}
    
    def _get_concept_explanation(self, concept: str) -> str:
        """Get detailed explanation for a frontend concept."""
        explanations = {
            "Component Architecture": """
Component architecture is a design pattern that breaks down user interfaces into 
reusable, self-contained components. Each component encapsulates its own logic, 
styling, and behavior, making the application more modular and maintainable.

Key principles:
- Single Responsibility: Each component should have one clear purpose
- Reusability: Components should be designed to be reused across the application
- Composability: Components should be able to be combined to create more complex UIs
- Isolation: Components should be independent and not rely on external state when possible

Benefits:
- Improved code organization and maintainability
- Easier testing and debugging
- Better developer experience and productivity
- Consistent UI/UX across the application
""",
            "State Management": """
State management refers to the practice of managing and synchronizing data across 
different parts of a frontend application. As applications grow in complexity, 
managing state becomes crucial for maintaining predictable behavior.

Types of state:
- Local State: Component-specific state that doesn't need to be shared
- Global State: Application-wide state that needs to be accessible across components
- Server State: Data fetched from external APIs
- URL State: State derived from the current URL and query parameters

State management solutions:
- Built-in solutions (React Context, Vue's reactive system)
- External libraries (Redux, Zustand, Pinia, MobX)
- Framework-specific solutions (Angular services, Svelte stores)
""",
            "Routing": """
Routing is the process of determining which content to display based on the current URL.
Modern frontend applications use client-side routing to create single-page applications
that feel like multi-page applications without full page reloads.

Key concepts:
- Route definitions and path matching
- Navigation and programmatic routing
- Route guards and authentication
- Lazy loading and code splitting
- SEO considerations for SPAs

Popular routing libraries:
- React Router (React)
- Vue Router (Vue.js)
- Angular Router (Angular)
- Svelte Router (Svelte)
""",
            "Performance Optimization": """
Frontend performance optimization involves techniques to improve the speed, 
responsiveness, and overall user experience of web applications.

Key areas to optimize:
- Bundle size reduction through tree shaking and code splitting
- Image optimization and lazy loading
- Efficient rendering patterns and virtualization
- Caching strategies and memoization
- Network optimization and resource loading

Performance metrics to monitor:
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- First Input Delay (FID)
- Time to Interactive (TTI)
""",
            "Accessibility": """
Accessibility (a11y) ensures that web applications are usable by people with 
disabilities, including visual, auditory, physical, speech, cognitive, and 
neurological disabilities.

Key principles:
- Semantic HTML structure
- Keyboard navigation support
- Screen reader compatibility
- Color contrast and visual indicators
- ARIA (Accessible Rich Internet Applications) attributes
- Focus management and skip links

Benefits:
- Legal compliance (ADA, WCAG guidelines)
- Improved SEO and search engine indexing
- Better user experience for all users
- Expanded user base and market reach
""",
            "SEO": """
Search Engine Optimization (SEO) for frontend applications involves techniques 
to make single-page applications and dynamic content discoverable by search engines.

Challenges with SPAs:
- JavaScript-dependent content rendering
- Dynamic content loading
- Client-side routing
- Meta tag management

Solutions:
- Server-Side Rendering (SSR)
- Static Site Generation (SSG)
- Pre-rendering techniques
- Proper meta tag management
- Structured data and schema.org markup
- Sitemap generation
""",
            "Build Tools": """
Build tools are essential for modern frontend development, handling tasks like 
compilation, bundling, minification, and optimization of source code.

Common build tools:
- Webpack: Module bundler with extensive plugin ecosystem
- Vite: Fast build tool with native ES modules support
- Rollup: Focused on library bundling with tree shaking
- ESBuild: Extremely fast bundler written in Go
- Parcel: Zero-configuration bundler

Build process stages:
- Development: Hot module replacement, source maps, development server
- Production: Minification, tree shaking, code splitting, asset optimization
- Testing: Test runners, coverage reporting, linting
""",
            "Testing": """
Frontend testing ensures application reliability, functionality, and user experience.
Different types of testing serve different purposes in the development process.

Testing pyramid:
- Unit Tests: Test individual components and functions
- Integration Tests: Test component interactions
- End-to-End Tests: Test complete user workflows
- Visual Regression Tests: Ensure UI consistency

Popular testing frameworks:
- Jest: JavaScript testing framework with React Testing Library
- Vitest: Vite-native testing framework
- Cypress: End-to-end testing with real browser testing
- Playwright: Modern E2E testing framework
- Storybook: Component development and testing environment
""",
            "CSS-in-JS": """
CSS-in-JS is a styling technique that involves writing CSS styles directly in 
JavaScript files, often as part of component definitions.

Benefits:
- Scoped styles prevent CSS conflicts
- Dynamic styling based on component props
- Better developer experience with IDE support
- Easier component composition and reuse

Popular CSS-in-JS libraries:
- styled-components
- Emotion
- JSS
- Styled System
- Linaria

Considerations:
- Runtime performance impact
- Bundle size increase
- Learning curve for team members
- Debugging complexity
""",
            "Server-Side Rendering": """
Server-Side Rendering (SSR) involves rendering JavaScript applications on the server
and sending fully rendered HTML to the client, improving performance and SEO.

Benefits:
- Better SEO through server-rendered HTML
- Improved perceived performance with faster initial load
- Better social media sharing with proper meta tags
- Graceful degradation for users without JavaScript

SSR frameworks:
- Next.js (React)
- Nuxt.js (Vue.js)
- Angular Universal (Angular)
- SvelteKit (Svelte)
- Astro (Multi-framework)

Challenges:
- Increased server complexity and infrastructure needs
- Hydration process complexity
- Data fetching coordination between server and client
- Caching strategies for dynamic content
"""
        }
        
        return explanations.get(concept, f"Explanation for {concept} is not available.")
    
    def _get_related_concepts(self, concept: str) -> List[str]:
        """Get related concepts for a given concept."""
        related_concepts = {
            "Component Architecture": [
                "Props and State", "Component Composition", "Higher-Order Components",
                "Render Props", "Component Lifecycle", "Reusability Patterns"
            ],
            "State Management": [
                "Global State", "Local State", "State Persistence",
                "State Synchronization", "State Immutability", "State Debugging"
            ],
            "Routing": [
                "Client-Side Routing", "Server-Side Routing", "Route Guards",
                "Lazy Loading", "Nested Routes", "Route Parameters"
            ],
            "Performance Optimization": [
                "Bundle Optimization", "Image Optimization", "Code Splitting",
                "Caching Strategies", "Virtualization", "Memoization"
            ],
            "Accessibility": [
                "Semantic HTML", "Keyboard Navigation", "Screen Reader Support",
                "ARIA Attributes", "Color Accessibility", "Focus Management"
            ],
            "SEO": [
                "Meta Tags", "Structured Data", "Sitemap Generation",
                "Server-Side Rendering", "Pre-rendering", "Social Media Optimization"
            ],
            "Build Tools": [
                "Module Bundling", "Code Transpilation", "Asset Optimization",
                "Development Server", "Hot Module Replacement", "Production Build"
            ],
            "Testing": [
                "Unit Testing", "Integration Testing", "End-to-End Testing",
                "Test-Driven Development", "Mocking", "Test Coverage"
            ],
            "CSS-in-JS": [
                "Styled Components", "Emotion", "JSS",
                "CSS Modules", "Atomic CSS", "Utility-First CSS"
            ],
            "Server-Side Rendering": [
                "Hydration", "Static Site Generation", "Incremental Static Regeneration",
                "Server Components", "Edge Rendering", "Streaming SSR"
            ]
        }
        
        return related_concepts.get(concept, [])
    
    def _get_best_practices(self, concept: str) -> List[str]:
        """Get best practices for a given concept."""
        best_practices = {
            "Component Architecture": [
                "Keep components small and focused on a single responsibility",
                "Use composition over inheritance for component relationships",
                "Implement proper prop validation and default values",
                "Avoid deep nesting by using component composition",
                "Use meaningful component names that describe their purpose",
                "Separate presentational and container components when appropriate"
            ],
            "State Management": [
                "Keep state as simple as possible",
                "Use immutable state updates to prevent side effects",
                "Centralize related state to avoid duplication",
                "Implement proper state normalization for complex data",
                "Use selectors to derive computed state",
                "Implement proper error handling and loading states"
            ],
            "Routing": [
                "Use descriptive and consistent URL patterns",
                "Implement proper error handling for 404 pages",
                "Use route guards for authentication and authorization",
                "Implement proper loading states for route transitions",
                "Optimize route-based code splitting",
                "Handle browser back/forward navigation properly"
            ],
            "Performance Optimization": [
                "Implement lazy loading for non-critical components",
                "Use memoization for expensive calculations",
                "Optimize images with proper formats and sizes",
                "Implement virtualization for long lists",
                "Minimize re-renders with proper state management",
                "Use performance monitoring and profiling tools"
            ],
            "Accessibility": [
                "Use semantic HTML elements appropriately",
                "Ensure keyboard navigation works for all interactive elements",
                "Provide alternative text for images and media",
                "Implement proper focus management and skip links",
                "Use sufficient color contrast ratios",
                "Test with screen readers and accessibility tools"
            ],
            "SEO": [
                "Use proper heading hierarchy (H1, H2, H3, etc.)",
                "Implement structured data with schema.org markup",
                "Optimize meta tags for each page",
                "Create and maintain a sitemap.xml",
                "Use canonical URLs to prevent duplicate content",
                "Implement proper robots.txt configuration"
            ],
            "Build Tools": [
                "Configure proper source maps for debugging",
                "Implement code splitting for better performance",
                "Use environment variables for configuration",
                "Set up proper linting and formatting rules",
                "Optimize build process with caching strategies",
                "Monitor bundle size and implement size budgets"
            ],
            "Testing": [
                "Write tests that focus on behavior, not implementation",
                "Use descriptive test names that explain the expected behavior",
                "Implement proper setup and teardown for tests",
                "Use mocking sparingly and only when necessary",
                "Test both happy path and edge cases",
                "Maintain good test coverage without obsessing over 100%"
            ],
            "CSS-in-JS": [
                "Avoid inline styles that could be extracted to components",
                "Use theme providers for consistent styling",
                "Implement proper style composition patterns",
                "Consider performance implications of runtime styling",
                "Use CSS-in-JS for dynamic styles, not static ones",
                "Implement proper style isolation and scoping"
            ],
            "Server-Side Rendering": [
                "Handle data fetching properly on both server and client",
                "Implement proper hydration to avoid mismatches",
                "Use proper error boundaries for SSR errors",
                "Optimize server response times",
                "Implement proper caching strategies",
                "Handle authentication and authorization on the server"
            ]
        }
        
        return best_practices.get(concept, [])
    
    def _get_framework_recommendations(self, concept: str) -> Dict[str, List[str]]:
        """Get framework recommendations for a given concept."""
        recommendations = {
            "Component Architecture": {
                "React": ["Component composition", "Hooks", "Context API"],
                "Vue.js": ["Single File Components", "Composition API", "Props"],
                "Angular": ["Component decorators", "Dependency injection", "Templates"],
                "Svelte": ["Reactive statements", "Stores", "Slots"]
            },
            "State Management": {
                "React": ["Redux", "Zustand", "React Query", "Context API"],
                "Vue.js": ["Pinia", "Vuex", "Composition API", "Provide/Inject"],
                "Angular": ["Services", "RxJS", "NgRx", "State management patterns"],
                "Svelte": ["Stores", "Reactive statements", "Context API"]
            },
            "Routing": {
                "React": ["React Router", "Next.js routing", "Reach Router"],
                "Vue.js": ["Vue Router", "Nuxt.js routing", "File-based routing"],
                "Angular": ["Angular Router", "Lazy loading", "Route guards"],
                "Svelte": ["SvelteKit routing", "Page-based routing", "Layouts"]
            },
            "Performance Optimization": {
                "React": ["Memoization", "Virtualization", "Code splitting", "Bundle optimization"],
                "Vue.js": ["Keep-alive", "Async components", "Virtualization", "Bundle optimization"],
                "Angular": ["Change detection", "Lazy loading", "Ahead-of-time compilation"],
                "Svelte": ["Compile-time optimizations", "Reactive statements", "Code splitting"]
            }
        }
        
        return recommendations.get(concept, {})
    
    def _generate_architecture_recommendations(self, project_scale: str, 
                                             performance_reqs: Dict[str, Any],
                                             team_expertise: str) -> Dict[str, Any]:
        """Generate architecture recommendations based on project requirements."""
        recommendations = {
            "project_scale": project_scale,
            "team_expertise": team_expertise,
            "architecture_patterns": [],
            "data_flow_patterns": [],
            "component_organization": "",
            "state_management_strategy": ""
        }
        
        # Architecture patterns based on scale
        if project_scale == "small":
            recommendations["architecture_patterns"] = [
                "Component-based architecture",
                "Simple state management (Context API, Pinia)",
                "File-based routing"
            ]
        elif project_scale == "medium":
            recommendations["architecture_patterns"] = [
                "Feature-based architecture",
                "State management with dedicated stores",
                "Code splitting and lazy loading"
            ]
        else:  # large
            recommendations["architecture_patterns"] = [
                "Micro-frontend architecture",
                "Domain-driven design",
                "Advanced state management (Redux, NgRx)",
                "Server-side rendering or static generation"
            ]
        
        # Data flow patterns
        if team_expertise == "beginner":
            recommendations["data_flow_patterns"] = [
                "Unidirectional data flow",
                "Simple prop drilling or context usage",
                "Synchronous data fetching"
            ]
        else:
            recommendations["data_flow_patterns"] = [
                "State management with middleware",
                "Async data fetching patterns",
                "Event-driven architecture"
            ]
        
        # Component organization
        recommendations["component_organization"] = (
            "Feature-based organization" if project_scale in ["medium", "large"] 
            else "Page-based organization"
        )
        
        # State management strategy
        if project_scale == "small":
            recommendations["state_management_strategy"] = "Local state + Context API"
        elif project_scale == "medium":
            recommendations["state_management_strategy"] = "Global state management library"
        else:
            recommendations["state_management_strategy"] = "Advanced state management with middleware"
        
        return recommendations
    
    def _generate_tech_stack_recommendations(self, project_scale: str,
                                           performance_reqs: Dict[str, Any],
                                           team_expertise: str) -> Dict[str, Any]:
        """Generate technology stack recommendations."""
        tech_stack = {
            "framework": "",
            "build_tool": "",
            "state_management": "",
            "routing": "",
            "styling": "",
            "testing": "",
            "performance_tools": []
        }
        
        # Framework selection
        if team_expertise == "beginner":
            tech_stack["framework"] = "React (most learning resources)"
        elif team_expertise == "intermediate":
            tech_stack["framework"] = "Vue.js (balanced complexity)"
        else:
            tech_stack["framework"] = "React or Angular (enterprise features)"
        
        # Build tool selection
        if project_scale == "small":
            tech_stack["build_tool"] = "Vite (fast development)"
        else:
            tech_stack["build_tool"] = "Webpack (more configuration options)"
        
        # State management
        if project_scale == "small":
            tech_stack["state_management"] = "Context API or Zustand"
        elif project_scale == "medium":
            tech_stack["state_management"] = "Redux Toolkit or Pinia"
        else:
            tech_stack["state_management"] = "Redux with middleware or NgRx"
        
        # Routing
        if project_scale == "small":
            tech_stack["routing"] = "Framework built-in routing"
        else:
            tech_stack["routing"] = "Advanced routing with lazy loading"
        
        # Styling
        tech_stack["styling"] = "CSS-in-JS or utility-first CSS"
        
        # Testing
        tech_stack["testing"] = "Jest + Testing Library or Vitest"
        
        # Performance tools
        if performance_reqs.get("high", False):
            tech_stack["performance_tools"] = [
                "Bundle analyzer",
                "Performance monitoring",
                "Image optimization tools"
            ]
        
        return tech_stack
    
    def _get_implementation_phases(self, project_scale: str) -> List[Dict[str, Any]]:
        """Get implementation phases for different project scales."""
        if project_scale == "small":
            return [
                {
                    "phase": "Phase 1: Foundation",
                    "duration": "1-2 weeks",
                    "tasks": ["Setup project structure", "Configure build tools", "Implement basic components"]
                },
                {
                    "phase": "Phase 2: Core Features",
                    "duration": "2-3 weeks",
                    "tasks": ["Implement main functionality", "Add routing", "Basic styling"]
                },
                {
                    "phase": "Phase 3: Polish",
                    "duration": "1 week",
                    "tasks": ["Testing", "Performance optimization", "Deployment"]
                }
            ]
        elif project_scale == "medium":
            return [
                {
                    "phase": "Phase 1: Architecture",
                    "duration": "2-3 weeks",
                    "tasks": ["Define architecture patterns", "Setup state management", "Configure build pipeline"]
                },
                {
                    "phase": "Phase 2: Feature Development",
                    "duration": "4-6 weeks",
                    "tasks": ["Implement core features", "Add routing and navigation", "Implement authentication"]
                },
                {
                    "phase": "Phase 3: Optimization",
                    "duration": "2-3 weeks",
                    "tasks": ["Performance optimization", "Testing and QA", "Security hardening"]
                },
                {
                    "phase": "Phase 4: Deployment",
                    "duration": "1 week",
                    "tasks": ["Production deployment", "Monitoring setup", "Documentation"]
                }
            ]
        else:
            return [
                {
                    "phase": "Phase 1: Planning",
                    "duration": "3-4 weeks",
                    "tasks": ["Architecture design", "Technology selection", "Team setup"]
                },
                {
                    "phase": "Phase 2: Foundation",
                    "duration": "4-6 weeks",
                    "tasks": ["Setup development environment", "Implement core architecture", "Create component library"]
                },
                {
                    "phase": "Phase 3: Feature Development",
                    "duration": "8-12 weeks",
                    "tasks": ["Develop core features", "Implement advanced state management", "Add comprehensive testing"]
                },
                {
                    "phase": "Phase 4: Optimization & Deployment",
                    "duration": "3-4 weeks",
                    "tasks": ["Performance optimization", "Security review", "Production deployment", "Monitoring setup"]
                }
            ]
    
    def _get_framework_comparison_data(self, framework: str) -> Dict[str, Any]:
        """Get comparison data for a specific framework."""
        comparison_data = {
            "React": {
                "learning_curve": "Moderate",
                "ecosystem": "Very Large",
                "performance": "Excellent",
                "community": "Very Active",
                "job_market": "High Demand",
                "best_for": ["Large applications", "Complex UIs", "Team development"],
                "cons": ["Frequent updates", "JSX learning curve", "Tooling complexity"]
            },
            "Vue.js": {
                "learning_curve": "Gentle",
                "ecosystem": "Large",
                "performance": "Excellent",
                "community": "Active",
                "job_market": "Growing",
                "best_for": ["Rapid prototyping", "Medium-sized applications", "Beginner to intermediate teams"],
                "cons": ["Smaller job market", "Less enterprise adoption", "Framework changes"]
            },
            "Angular": {
                "learning_curve": "Steep",
                "ecosystem": "Large",
                "performance": "Good",
                "community": "Active",
                "job_market": "Stable",
                "best_for": ["Enterprise applications", "Large teams", "TypeScript projects"],
                "cons": ["Complexity", "Verbose syntax", "Bundle size"]
            },
            "Svelte": {
                "learning_curve": "Gentle",
                "ecosystem": "Growing",
                "performance": "Excellent",
                "community": "Growing",
                "job_market": "Emerging",
                "best_for": ["Performance-critical apps", "Simple projects", "Learning modern patterns"],
                "cons": ["Smaller ecosystem", "Less mature tooling", "Smaller job market"]
            }
        }
        
        return comparison_data.get(framework, {})
    
    def _generate_framework_comparison_summary(self, comparison_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of framework comparison."""
        summary = {
            "recommended_for_beginners": "",
            "recommended_for_enterprise": "",
            "best_performance": "",
            "most_popular": "",
            "summary": ""
        }
        
        # Simple comparison logic
        if "React" in comparison_results:
            summary["most_popular"] = "React"
            summary["recommended_for_enterprise"] = "React or Angular"
        
        if "Vue.js" in comparison_results:
            summary["recommended_for_beginners"] = "Vue.js"
        
        if "Svelte" in comparison_results:
            summary["best_performance"] = "Svelte"
        
        summary["summary"] = f"Based on your selection, {', '.join(comparison_results.keys())} each have their strengths. Consider your team's experience and project requirements when making a decision."
        
        return summary
    
    def _get_performance_optimization_strategies(self, project_type: str) -> Dict[str, List[str]]:
        """Get performance optimization strategies for different project types."""
        strategies = {
            "SPA": [
                "Code splitting and lazy loading",
                "Bundle optimization and tree shaking",
                "Image optimization and lazy loading",
                "Virtualization for long lists",
                "Caching strategies",
                "Minimize re-renders with memoization"
            ],
            "SSR": [
                "Server-side caching",
                "Optimized data fetching",
                "Bundle splitting for client hydration",
                "Image optimization with proper formats",
                "CDN for static assets",
                "Database query optimization"
            ],
            "Static": [
                "Static site generation optimization",
                "Image optimization and compression",
                "Bundle size optimization",
                "Proper caching headers",
                "CDN deployment",
                "Minimize JavaScript bundle"
            ],
            "PWA": [
                "Service worker optimization",
                "App shell architecture",
                "Offline caching strategies",
                "Progressive loading",
                "Background sync optimization",
                "Resource preloading"
            ]
        }
        
        return strategies.get(project_type, [])
    
    def _get_common_performance_pitfalls(self, project_type: str) -> List[str]:
        """Get common performance pitfalls for different project types."""
        pitfalls = {
            "SPA": [
                "Large bundle sizes due to unnecessary dependencies",
                "Inefficient state management causing re-renders",
                "Poor image optimization",
                "Blocking the main thread with heavy computations",
                "Inadequate caching strategies",
                "Infinite loops in render cycles"
            ],
            "SSR": [
                "Slow server response times",
                "Inefficient data fetching on server",
                "Large HTML payloads",
                "Hydration mismatches",
                "Blocking server-side rendering",
                "Inadequate server resources"
            ],
            "Static": [
                "Large image files",
                "Unoptimized JavaScript bundles",
                "Inefficient build processes",
                "Poor caching strategies",
                "Large CSS files",
                "Inefficient asset loading"
            ],
            "PWA": [
                "Large service worker files",
                "Inefficient caching strategies",
                "Poor offline experience",
                "Slow app shell loading",
                "Background sync issues",
                "Storage quota management"
            ]
        }
        
        return pitfalls.get(project_type, [])
    
    def _get_performance_measurement_techniques(self) -> List[str]:
        """Get techniques for measuring frontend performance."""
        return [
            "Core Web Vitals monitoring",
            "Bundle size analysis with webpack-bundle-analyzer",
            "Performance profiling with browser dev tools",
            "Lighthouse audits",
            "Real User Monitoring (RUM)",
            "Synthetic monitoring",
            "Network throttling tests",
            "Memory usage analysis",
            "JavaScript execution time measurement",
            "Render performance analysis"
        ]
    
    def _get_state_management_pattern_explanation(self, pattern_type: str) -> str:
        """Get explanation for a state management pattern."""
        explanations = {
            "Redux": """
Redux is a predictable state container for JavaScript applications. It follows
the principles of unidirectional data flow and immutable state updates.

Core concepts:
- Single store containing the entire application state
- Actions that describe what happened
- Reducers that specify how the state changes in response to actions
- Pure functions for predictable state updates

Benefits:
- Predictable state changes
- Time-travel debugging capabilities
- Centralized state management
- Middleware support for side effects
- Great developer tools and ecosystem
""",
            "Context API": """
React's Context API provides a way to share values like user preferences, 
authentication status, or UI themes across the component tree without 
having to pass props down manually at every level.

Key features:
- Built into React, no additional dependencies
- Simple API with Provider and Consumer components
- Automatic re-rendering when context values change
- Can be combined with hooks for cleaner usage

Use cases:
- Theme management
- User authentication state
- Global configuration
- Shared utilities and functions
""",
            "Zustand": """
Zustand is a small, fast, and scalable state management solution using
hooks. It has a minimal API and doesn't require providers or reducers.

Key features:
- No providers needed
- Simple API with minimal boilerplate
- Built-in middleware support
- TypeScript support out of the box
- Small bundle size

Benefits:
- Easy to learn and use
- No context providers required
- Automatic subscription to state slices
- Middleware for side effects and persistence
""",
            "Pinia": """
Pinia is the official state management library for Vue.js, offering a
modern and type-safe approach to state management.

Core concepts:
- Stores as reactive objects
- Actions for state mutations
- Getters for computed state
- Modular architecture with namespacing

Benefits:
- TypeScript support by default
- No mutations, direct state modification
- Modular and scalable
- DevTools integration
- Vue 3 composition API support
"""
        }
        
        return explanations.get(pattern_type, f"Explanation for {pattern_type} is not available.")
    
    def _get_state_management_implementation_considerations(self, pattern_type: str) -> List[str]:
        """Get implementation considerations for state management patterns."""
        considerations = {
            "Redux": [
                "Boilerplate code can be verbose",
                "Learning curve for reducers and actions",
                "Need to handle immutability manually",
                "Middleware required for async operations",
                "Performance considerations with large state trees"
            ],
            "Context API": [
                "Re-renders all consumers on any context change",
                "No built-in state persistence",
                "Limited debugging capabilities",
                "Can become complex with multiple contexts",
                "No middleware support"
            ],
            "Zustand": [
                "Less mature ecosystem compared to Redux",
                "No built-in time-travel debugging",
                "State structure is less predictable",
                "Limited tooling and dev tools",
                "Smaller community and resources"
            ],
            "Pinia": [
                "Vue-specific, not framework agnostic",
                "Less mature than Vuex",
                "Limited ecosystem compared to Redux",
                "Requires Vue 3 for latest features",
                "Migration complexity from Vuex"
            ]
        }
        
        return considerations.get(pattern_type, [])
    
    def _get_framework_specific_implementations(self, pattern_type: str) -> Dict[str, str]:
        """Get framework-specific implementations of state management patterns."""
        implementations = {
            "Redux": {
                "React": "Redux Toolkit with React-Redux",
                "Vue.js": "Vuex (legacy) or Pinia",
                "Angular": "NgRx or services with RxJS",
                "Svelte": "Svelte stores or external libraries"
            },
            "Context API": {
                "React": "Built-in Context API with hooks",
                "Vue.js": "Provide/inject API",
                "Angular": "Services with dependency injection",
                "Svelte": "Context API or stores"
            },
            "Zustand": {
                "React": "Native Zustand integration",
                "Vue.js": "Not applicable (React-specific)",
                "Angular": "Not applicable (React-specific)",
                "Svelte": "Not applicable (React-specific)"
            },
            "Pinia": {
                "React": "Not applicable (Vue-specific)",
                "Vue.js": "Native Pinia integration",
                "Angular": "Not applicable (Vue-specific)",
                "Svelte": "Not applicable (Vue-specific)"
            }
        }
        
        return implementations.get(pattern_type, {})


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "frontend_development",
        "description": "Provides comprehensive frontend development knowledge and guidance",
        "version": "1.0.0",
        "domain": "frontend",
        "functions": [
            {
                "name": "explain_frontend_concept",
                "description": "Explain a frontend development concept in detail"
            },
            {
                "name": "analyze_frontend_architecture",
                "description": "Analyze frontend architecture requirements and provide recommendations"
            },
            {
                "name": "compare_frontend_frameworks",
                "description": "Compare multiple frontend frameworks based on various criteria"
            },
            {
                "name": "provide_performance_optimization_guidance",
                "description": "Provide performance optimization guidance for different project types"
            },
            {
                "name": "explain_state_management_patterns",
                "description": "Explain different state management patterns and their use cases"
            }
        ]
    }

def execute_function(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a function from this skill.
    
    Args:
        function_name: Name of the function to execute
        arguments: Arguments for the function
    
    Returns:
        Function execution result
    """
    skill = FrontendDevelopmentSkill()
    
    if function_name == "explain_frontend_concept":
        concept = arguments.get("concept")
        return skill.explain_frontend_concept(concept)
    elif function_name == "analyze_frontend_architecture":
        requirements = arguments.get("requirements", {})
        return skill.analyze_frontend_architecture(requirements)
    elif function_name == "compare_frontend_frameworks":
        frameworks = arguments.get("frameworks", [])
        return skill.compare_frontend_frameworks(frameworks)
    elif function_name == "provide_performance_optimization_guidance":
        project_type = arguments.get("project_type", "SPA")
        return skill.provide_performance_optimization_guidance(project_type)
    elif function_name == "explain_state_management_patterns":
        pattern_type = arguments.get("pattern_type")
        return skill.explain_state_management_patterns(pattern_type)
    else:
        return {"error": f"Unknown function: {function_name}"}

def invoke(function_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Invoke a function from this skill.
    
    Args:
        function_name: Name of the function to execute
        arguments: Arguments for the function
    
    Returns:
        Function execution result
    """
    return execute_function(function_name, arguments)

if __name__ == "__main__":
    # Test the skill
    skill = FrontendDevelopmentSkill()
    
    print("Testing Frontend Development Skill...")
    
    # Test concept explanation
    result = skill.explain_frontend_concept("Component Architecture")
    print(f"Concept explanation result: {result}")
    
    # Test architecture analysis
    requirements = {
        "scale": "medium",
        "performance": {"high": True},
        "team_expertise": "intermediate"
    }
    result = skill.analyze_frontend_architecture(requirements)
    print(f"Architecture analysis result: {result}")
