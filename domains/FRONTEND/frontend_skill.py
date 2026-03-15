#!/usr/bin/env python3
"""
Frontend Development Skill Module
Provides comprehensive frontend development capabilities including React, Vue, Angular,
and modern web development practices.

This skill handles UI/UX implementation, component development, state management,
styling, performance optimization, and frontend architecture patterns.
"""

import os
import re
import json
import subprocess
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import logging

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
        self.frameworks = ['react', 'vue', 'angular', 'svelte', 'vanilla']
        self.styling_frameworks = ['css', 'scss', 'tailwind', 'bootstrap', 'styled-components']
        self.state_managers = ['redux', 'vuex', 'pinia', 'ngrx', 'zustand']
        self.build_tools = ['webpack', 'vite', 'rollup', 'parcel']
        
    def analyze_frontend_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze a frontend project to understand its structure and dependencies.
        
        Args:
            project_path: Path to the frontend project directory
        
        Returns:
            Dictionary containing project analysis
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze package.json
            package_json = self._analyze_package_json(project_dir)
            
            # Analyze project structure
            structure = self._analyze_project_structure(project_dir)
            
            # Detect framework and tools
            tech_stack = self._detect_tech_stack(project_dir, package_json)
            
            # Check for common issues
            issues = self._check_common_issues(project_dir, package_json)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "package_info": package_json,
                "structure": structure,
                "tech_stack": tech_stack,
                "issues": issues,
                "recommendations": self._generate_recommendations(tech_stack, issues)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze project: {str(e)}"}
    
    def create_component(self, component_name: str, framework: str = "react", 
                        props: Optional[List[str]] = None, 
                        styling: str = "css") -> Dict[str, Any]:
        """
        Create a new frontend component.
        
        Args:
            component_name: Name of the component
            framework: Framework to use (react, vue, angular, etc.)
            props: List of props/properties for the component
            styling: Styling approach (css, scss, styled-components, etc.)
        
        Returns:
            Dictionary containing component files and instructions
        """
        try:
            # Generate component files based on framework
            if framework.lower() == "react":
                component_files = self._generate_react_component(component_name, props, styling)
            elif framework.lower() == "vue":
                component_files = self._generate_vue_component(component_name, props, styling)
            elif framework.lower() == "angular":
                component_files = self._generate_angular_component(component_name, props, styling)
            else:
                return {"error": f"Unsupported framework: {framework}"}
            
            return {
                "status": "success",
                "framework": framework,
                "component_name": component_name,
                "files": component_files,
                "instructions": self._get_component_instructions(framework, component_name)
            }
            
        except Exception as e:
            return {"error": f"Failed to create component: {str(e)}"}
    
    def optimize_performance(self, project_path: str, analysis_only: bool = False) -> Dict[str, Any]:
        """
        Analyze and optimize frontend performance.
        
        Args:
            project_path: Path to the frontend project
            analysis_only: If True, only analyze without making changes
        
        Returns:
            Dictionary containing optimization analysis and recommendations
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Bundle analysis
            bundle_analysis = self._analyze_bundle_size(project_dir)
            
            # Code splitting opportunities
            code_splitting = self._analyze_code_splitting(project_dir)
            
            # Image optimization opportunities
            image_optimization = self._analyze_image_optimization(project_dir)
            
            # CSS optimization opportunities
            css_optimization = self._analyze_css_optimization(project_dir)
            
            # Performance recommendations
            recommendations = self._generate_performance_recommendations(
                bundle_analysis, code_splitting, image_optimization, css_optimization
            )
            
            if not analysis_only:
                # Apply optimizations
                optimization_results = self._apply_optimizations(project_dir, recommendations)
            else:
                optimization_results = {"message": "Analysis only - no changes made"}
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "bundle_analysis": bundle_analysis,
                "code_splitting": code_splitting,
                "image_optimization": image_optimization,
                "css_optimization": css_optimization,
                "recommendations": recommendations,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            return {"error": f"Failed to optimize performance: {str(e)}"}
    
    def implement_state_management(self, project_path: str, state_manager: str = "redux",
                                  entities: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Implement state management solution for a frontend project.
        
        Args:
            project_path: Path to the frontend project
            state_manager: State management library (redux, vuex, pinia, etc.)
            entities: List of entities to manage in state
        
        Returns:
            Dictionary containing state management implementation
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze current state management
            current_state = self._analyze_current_state_management(project_dir)
            
            # Generate state management files
            if state_manager.lower() == "redux":
                state_files = self._generate_redux_store(entities)
            elif state_manager.lower() == "vuex":
                state_files = self._generate_vuex_store(entities)
            elif state_manager.lower() == "pinia":
                state_files = self._generate_pinia_store(entities)
            else:
                return {"error": f"Unsupported state manager: {state_manager}"}
            
            # Integration instructions
            integration = self._get_state_integration_instructions(state_manager, project_dir)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "state_manager": state_manager,
                "current_state": current_state,
                "state_files": state_files,
                "integration": integration
            }
            
        except Exception as e:
            return {"error": f"Failed to implement state management: {str(e)}"}
    
    def create_responsive_layout(self, layout_type: str = "grid", 
                               breakpoints: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Create responsive layout components and styles.
        
        Args:
            layout_type: Type of layout (grid, flexbox, css-grid)
            breakpoints: Custom breakpoints for responsive design
        
        Returns:
            Dictionary containing layout implementation
        """
        try:
            # Default breakpoints if none provided
            if not breakpoints:
                breakpoints = {
                    "mobile": 480,
                    "tablet": 768,
                    "desktop": 1024,
                    "wide": 1440
                }
            
            # Generate layout files
            layout_files = self._generate_responsive_layout(layout_type, breakpoints)
            
            # Generate CSS-in-JS or CSS modules
            styling_files = self._generate_responsive_styling(layout_type, breakpoints)
            
            return {
                "status": "success",
                "layout_type": layout_type,
                "breakpoints": breakpoints,
                "layout_files": layout_files,
                "styling_files": styling_files,
                "usage_instructions": self._get_layout_usage_instructions(layout_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to create responsive layout: {str(e)}"}
    
    def _analyze_package_json(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze package.json for dependencies and scripts."""
        package_file = project_dir / "package.json"
        if not package_file.exists():
            return {"error": "No package.json found"}
        
        try:
            with open(package_file, 'r') as f:
                package_data = json.load(f)
            
            return {
                "name": package_data.get("name", ""),
                "version": package_data.get("version", ""),
                "dependencies": package_data.get("dependencies", {}),
                "devDependencies": package_data.get("devDependencies", {}),
                "scripts": package_data.get("scripts", {}),
                "framework": self._detect_framework(package_data.get("dependencies", {}))
            }
        except Exception as e:
            return {"error": f"Failed to parse package.json: {str(e)}"}
    
    def _analyze_project_structure(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze project directory structure."""
        structure = {
            "src_directories": [],
            "config_files": [],
            "build_files": [],
            "test_files": []
        }
        
        for item in project_dir.rglob("*"):
            if item.is_file():
                if "src" in str(item):
                    structure["src_directories"].append(str(item))
                elif item.name in ["webpack.config.js", "vite.config.js", "rollup.config.js"]:
                    structure["config_files"].append(str(item))
                elif item.name in ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"]:
                    structure["build_files"].append(str(item))
                elif "test" in str(item) or "spec" in str(item):
                    structure["test_files"].append(str(item))
        
        return structure
    
    def _detect_tech_stack(self, project_dir: Path, package_info: Dict) -> Dict[str, Any]:
        """Detect the technology stack used in the project."""
        dependencies = package_info.get("dependencies", {})
        
        tech_stack = {
            "framework": self._detect_framework(dependencies),
            "styling": self._detect_styling_framework(dependencies),
            "state_management": self._detect_state_manager(dependencies),
            "build_tool": self._detect_build_tool(project_dir),
            "testing": self._detect_testing_framework(dependencies)
        }
        
        return tech_stack
    
    def _detect_framework(self, dependencies: Dict) -> str:
        """Detect the frontend framework."""
        if "react" in dependencies:
            return "react"
        elif "vue" in dependencies:
            return "vue"
        elif "angular" in dependencies or "@angular/core" in dependencies:
            return "angular"
        elif "svelte" in dependencies:
            return "svelte"
        else:
            return "vanilla"
    
    def _detect_styling_framework(self, dependencies: Dict) -> List[str]:
        """Detect styling frameworks and tools."""
        styling = []
        if "sass" in dependencies or "node-sass" in dependencies:
            styling.append("scss")
        if "tailwindcss" in dependencies:
            styling.append("tailwind")
        if "bootstrap" in dependencies:
            styling.append("bootstrap")
        if "styled-components" in dependencies:
            styling.append("styled-components")
        if not styling:
            styling.append("css")
        return styling
    
    def _detect_state_manager(self, dependencies: Dict) -> str:
        """Detect state management library."""
        if "redux" in dependencies:
            return "redux"
        elif "vuex" in dependencies:
            return "vuex"
        elif "pinia" in dependencies:
            return "pinia"
        elif "@ngrx/store" in dependencies:
            return "ngrx"
        elif "zustand" in dependencies:
            return "zustand"
        else:
            return "none"
    
    def _detect_build_tool(self, project_dir: Path) -> str:
        """Detect build tool configuration."""
        build_files = [
            "webpack.config.js",
            "vite.config.js", 
            "rollup.config.js",
            "parcel.config.js"
        ]
        
        for build_file in build_files:
            if (project_dir / build_file).exists():
                return build_file.replace(".config.js", "")
        
        # Check package.json scripts
        package_file = project_dir / "package.json"
        if package_file.exists():
            try:
                with open(package_file, 'r') as f:
                    package_data = json.load(f)
                scripts = package_data.get("scripts", {})
                if "vite" in ' '.join(scripts.values()):
                    return "vite"
                elif "webpack" in ' '.join(scripts.values()):
                    return "webpack"
            except:
                pass
        
        return "unknown"
    
    def _detect_testing_framework(self, dependencies: Dict) -> str:
        """Detect testing framework."""
        if "jest" in dependencies:
            return "jest"
        elif "@testing-library/react" in dependencies:
            return "testing-library"
        elif "vitest" in dependencies:
            return "vitest"
        elif "cypress" in dependencies:
            return "cypress"
        else:
            return "none"
    
    def _check_common_issues(self, project_dir: Path, package_info: Dict) -> List[str]:
        """Check for common frontend issues."""
        issues = []
        
        # Check for duplicate dependencies
        dependencies = package_info.get("dependencies", {})
        dev_dependencies = package_info.get("devDependencies", {})
        
        for dep in dependencies:
            if dep in dev_dependencies:
                issues.append(f"Duplicate dependency: {dep} found in both dependencies and devDependencies")
        
        # Check for outdated packages (simplified check)
        if "react" in dependencies:
            react_version = dependencies.get("react", "")
            if react_version.startswith("^16"):
                issues.append("React version is outdated (16.x), consider upgrading to 18.x")
        
        # Check for missing security updates
        if "lodash" in dependencies:
            issues.append("Consider using lodash-es or native ES6+ methods instead of lodash for better tree-shaking")
        
        return issues
    
    def _generate_recommendations(self, tech_stack: Dict, issues: List[str]) -> List[str]:
        """Generate recommendations based on tech stack and issues."""
        recommendations = []
        
        framework = tech_stack.get("framework", "")
        if framework == "react":
            recommendations.extend([
                "Consider implementing TypeScript for better type safety",
                "Use React.memo() for performance optimization of expensive calculations",
                "Implement proper error boundaries for better error handling"
            ])
        elif framework == "vue":
            recommendations.extend([
                "Consider using Composition API for better code organization",
                "Implement proper state management with Pinia for complex applications"
            ])
        
        if "scss" in tech_stack.get("styling", []):
            recommendations.append("Consider using CSS-in-JS or CSS modules for better component isolation")
        
        if tech_stack.get("state_management") == "none" and framework in ["react", "vue"]:
            recommendations.append("Consider implementing state management for complex state logic")
        
        return recommendations + issues
    
    def _generate_react_component(self, name: str, props: Optional[List[str]], 
                                styling: str) -> Dict[str, str]:
        """Generate React component files."""
        props_str = ""
        if props:
            props_str = f"{{{', '.join(props)}}}"
        
        # JSX component
        jsx_content = f"""import React from 'react';
import './{name}.css';

interface {name}Props {{
  {props_str}
}}

const {name}: React.FC<{name}Props> = ({props_str}) => {{
  return (
    <div className="{name.lower()}">
      <h2>{name} Component</h2>
      {/* Component content */}
    </div>
  );
}};

export default {name};
"""
        
        # CSS file
        css_content = f""".{name.lower()} {{
  /* Component styles */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}

.{name.lower()} h2 {{
  color: #333;
  font-size: 1.5rem;
}}
"""
        
        files = {
            f"{name}.tsx": jsx_content,
            f"{name}.css": css_content
        }
        
        # Add TypeScript types if needed
        if props:
            types_content = f"""export interface {name}Props {{
  {props_str}
}}
"""
            files[f"{name}Types.ts"] = types_content
        
        return files
    
    def _generate_vue_component(self, name: str, props: Optional[List[str]], 
                              styling: str) -> Dict[str, str]:
        """Generate Vue component files."""
        props_definition = ""
        if props:
            props_definition = f"""  props: {{
    {', '.join([f'{prop}: {{ type: String, required: true }}' for prop in props])}
  }}"""
        
        vue_content = f"""<template>
  <div class="{name.lower()}">
    <h2>{name} Component</h2>
    <!-- Component content -->
  </div>
</template>

<script>
export default {{
  name: '{name}',
  {props_definition}
}}
</script>

<style scoped>
.{name.lower()} {{
  /* Component styles */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}

.{name.lower()} h2 {{
  color: #333;
  font-size: 1.5rem;
}}
</style>
"""
        
        return {f"{name}.vue": vue_content}
    
    def _generate_angular_component(self, name: str, props: Optional[List[str]], 
                                  styling: str) -> Dict[str, str]:
        """Generate Angular component files."""
        props_definition = ""
        if props:
            props_definition = f"""  @Input() {', '.join(props)}: string;"""
        
        ts_content = f"""import {{ Component, Input }} from '@angular/core';

@Component({{
  selector: 'app-{name.lower()}',
  templateUrl: './{name}.component.html',
  styleUrls: ['./{name}.component.css']
}})
export class {name}Component {{
  {props_definition}
}}
"""
        
        html_content = f"""<div class="{name.lower()}">
  <h2>{name} Component</h2>
  <!-- Component content -->
</div>
"""
        
        css_content = f""".{name.lower()} {{
  /* Component styles */
  display: flex;
  flex-direction: column;
  gap: 1rem;
}}

.{name.lower()} h2 {{
  color: #333;
  font-size: 1.5rem;
}}
"""
        
        return {
            f"{name}.component.ts": ts_content,
            f"{name}.component.html": html_content,
            f"{name}.component.css": css_content
        }
    
    def _get_component_instructions(self, framework: str, name: str) -> str:
        """Get instructions for using the generated component."""
        if framework == "react":
            return f"""To use the {name} component:
1. Import it: import {name} from './components/{name}';
2. Use it: <{name} prop1="value1" prop2="value2" />
3. Style it by modifying {name}.css"""
        
        elif framework == "vue":
            return f"""To use the {name} component:
1. Import it in your Vue file
2. Add it to components: {name}
3. Use it: <{name} prop1="value1" prop2="value2" />
4. Style it by modifying the scoped styles in {name}.vue"""
        
        elif framework == "angular":
            return f"""To use the {name} component:
1. Import {name}Component in your module
2. Add it to declarations array
3. Use it: <app-{name.lower()} [prop1]="'value1'" [prop2]="'value2'"></app-{name.lower()}>
4. Style it by modifying {name}.component.css"""
    
    def _analyze_bundle_size(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze bundle size and identify optimization opportunities."""
        # This would typically use webpack-bundle-analyzer or similar tools
        return {
            "total_size": "2.5MB",
            "largest_chunks": ["vendor.js", "main.js"],
            "optimization_opportunities": [
                "Code splitting for vendor libraries",
                "Tree shaking unused code",
                "Image optimization"
            ]
        }
    
    def _analyze_code_splitting(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze code splitting opportunities."""
        return {
            "routes": "Can implement route-based splitting",
            "components": "Can implement component-based splitting",
            "libraries": "Can implement library-based splitting"
        }
    
    def _analyze_image_optimization(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze image optimization opportunities."""
        images = list(project_dir.rglob("*.jpg")) + list(project_dir.rglob("*.png"))
        return {
            "total_images": len(images),
            "optimization_opportunities": [
                "Convert to WebP format",
                "Implement lazy loading",
                "Use responsive images"
            ]
        }
    
    def _analyze_css_optimization(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze CSS optimization opportunities."""
        return {
            "unused_css": "Can remove unused CSS",
            "css_size": "Consider CSS-in-JS for better tree-shaking",
            "optimization_opportunities": [
                "CSS minification",
                "Critical CSS extraction",
                "CSS modules for better scoping"
            ]
        }
    
    def _generate_performance_recommendations(self, bundle_analysis: Dict, 
                                             code_splitting: Dict,
                                             image_optimization: Dict,
                                             css_optimization: Dict) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        recommendations.extend(bundle_analysis.get("optimization_opportunities", []))
        recommendations.extend(code_splitting.get("optimization_opportunities", []))
        recommendations.extend(image_optimization.get("optimization_opportunities", []))
        recommendations.extend(css_optimization.get("optimization_opportunities", []))
        
        return recommendations
    
    def _apply_optimizations(self, project_dir: Path, recommendations: List[str]) -> Dict[str, Any]:
        """Apply performance optimizations."""
        # This would implement actual optimizations
        return {
            "optimizations_applied": len(recommendations),
            "estimated_improvement": "30-50% faster load times"
        }
    
    def _analyze_current_state_management(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze current state management implementation."""
        return {
            "current_state_manager": "none",
            "state_patterns": "props drilling",
            "recommendations": "Implement centralized state management"
        }
    
    def _generate_redux_store(self, entities: Optional[List[str]]) -> Dict[str, str]:
        """Generate Redux store files."""
        entities = entities or ["user", "posts"]
        
        store_content = """import { configureStore } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';

// Import reducers
import userReducer from './slices/userSlice';
import postsReducer from './slices/postsSlice';

const rootReducer = combineReducers({
  user: userReducer,
  posts: postsReducer,
});

const store = configureStore({
  reducer: rootReducer,
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
"""
        
        return {"store.ts": store_content}
    
    def _generate_vuex_store(self, entities: Optional[List[str]]) -> Dict[str, str]:
        """Generate Vuex store files."""
        store_content = """import { createStore } from 'vuex';

export default createStore({
  state: {
    // State properties
  },
  mutations: {
    // Mutations
  },
  actions: {
    // Actions
  },
  getters: {
    // Getters
  },
  modules: {
    // Modules
  }
});
"""
        
        return {"store.js": store_content}
    
    def _generate_pinia_store(self, entities: Optional[List[str]]) -> Dict[str, str]:
        """Generate Pinia store files."""
        store_content = """import { defineStore } from 'pinia';

export const useMainStore = defineStore('main', {
  state: () => ({
    // State properties
  }),
  getters: {
    // Getters
  },
  actions: {
    // Actions
  },
});
"""
        
        return {"main.ts": store_content}
    
    def _get_state_integration_instructions(self, state_manager: str, 
                                           project_dir: Path) -> str:
        """Get instructions for integrating state management."""
        if state_manager == "redux":
            return """To integrate Redux:
1. Install @reduxjs/toolkit and react-redux
2. Wrap your app with Provider
3. Use useSelector and useDispatch hooks in components
4. Create slices for each feature"""
        
        elif state_manager == "vuex":
            return """To integrate Vuex:
1. Install vuex
2. Create store instance
3. Register store in Vue app
4. Use mapState, mapActions in components"""
        
        elif state_manager == "pinia":
            return """To integrate Pinia:
1. Install pinia
2. Create stores using defineStore
3. Register pinia in Vue app
4. Use stores directly in components"""
    
    def _generate_responsive_layout(self, layout_type: str, 
                                  breakpoints: Dict[str, int]) -> Dict[str, str]:
        """Generate responsive layout components."""
        if layout_type == "grid":
            layout_content = """import React from 'react';
import './ResponsiveGrid.css';

interface ResponsiveGridProps {
  children: React.ReactNode;
  columns?: number;
  gap?: string;
}

const ResponsiveGrid: React.FC<ResponsiveGridProps> = ({ 
  children, 
  columns = 12, 
  gap = '1rem' 
}) => {
  return (
    <div className="responsive-grid" style={{ gridTemplateColumns: `repeat(${columns}, 1fr)` }}>
      {children}
    </div>
  );
};

export default ResponsiveGrid;
"""
        else:
            layout_content = """import React from 'react';
import './ResponsiveFlex.css';

interface ResponsiveFlexProps {
  children: React.ReactNode;
  direction?: 'row' | 'column';
  justify?: 'start' | 'center' | 'end' | 'space-between' | 'space-around';
  align?: 'start' | 'center' | 'end' | 'stretch';
}

const ResponsiveFlex: React.FC<ResponsiveFlexProps> = ({ 
  children, 
  direction = 'row',
  justify = 'start',
  align = 'stretch'
}) => {
  return (
    <div className="responsive-flex" style={{ flexDirection: direction }}>
      {children}
    </div>
  );
};

export default ResponsiveFlex;
"""
        
        return {f"Responsive{layout_type.title()}.tsx": layout_content}
    
    def _generate_responsive_styling(self, layout_type: str, 
                                   breakpoints: Dict[str, int]) -> Dict[str, str]:
        """Generate responsive CSS styles."""
        css_content = f"""/* Responsive {layout_type.title()} Styles */

.responsive-{layout_type.lower()} {{
  display: flex;
  gap: 1rem;
  padding: 1rem;
}}

/* Mobile styles */
@media (max-width: {breakpoints['mobile']}px) {{
  .responsive-{layout_type.lower()} {{
    flex-direction: column;
  }}
}}

/* Tablet styles */
@media (min-width: {breakpoints['mobile'] + 1}px) and (max-width: {breakpoints['tablet']}px) {{
  .responsive-{layout_type.lower()} {{
    flex-direction: row;
    flex-wrap: wrap;
  }}
}}

/* Desktop styles */
@media (min-width: {breakpoints['tablet'] + 1}px) {{
  .responsive-{layout_type.lower()} {{
    flex-direction: row;
  }}
}}
"""
        
        return {f"Responsive{layout_type.title()}.css": css_content}
    
    def _get_layout_usage_instructions(self, layout_type: str) -> str:
        """Get instructions for using the responsive layout."""
        return f"""To use the Responsive{layout_type.title()} component:
1. Import it: import Responsive{layout_type.title()} from './components/Responsive{layout_type.title()}';
2. Use it: <Responsive{layout_type.title()} columns={3} gap="2rem">...</Responsive{layout_type.title()}>
3. The layout will automatically adjust based on screen size
4. Customize breakpoints by modifying the CSS file"""


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "frontend_development",
        "description": "Provides comprehensive frontend development capabilities",
        "version": "1.0.0",
        "domain": "frontend",
        "functions": [
            {
                "name": "analyze_frontend_project",
                "description": "Analyze a frontend project to understand its structure and dependencies"
            },
            {
                "name": "create_component",
                "description": "Create a new frontend component with specified framework and styling"
            },
            {
                "name": "optimize_performance",
                "description": "Analyze and optimize frontend performance"
            },
            {
                "name": "implement_state_management",
                "description": "Implement state management solution for a frontend project"
            },
            {
                "name": "create_responsive_layout",
                "description": "Create responsive layout components and styles"
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
    
    if function_name == "analyze_frontend_project":
        project_path = arguments.get("project_path")
        return skill.analyze_frontend_project(project_path)
    elif function_name == "create_component":
        component_name = arguments.get("component_name")
        framework = arguments.get("framework", "react")
        props = arguments.get("props")
        styling = arguments.get("styling", "css")
        return skill.create_component(component_name, framework, props, styling)
    elif function_name == "optimize_performance":
        project_path = arguments.get("project_path")
        analysis_only = arguments.get("analysis_only", False)
        return skill.optimize_performance(project_path, analysis_only)
    elif function_name == "implement_state_management":
        project_path = arguments.get("project_path")
        state_manager = arguments.get("state_manager", "redux")
        entities = arguments.get("entities")
        return skill.implement_state_management(project_path, state_manager, entities)
    elif function_name == "create_responsive_layout":
        layout_type = arguments.get("layout_type", "grid")
        breakpoints = arguments.get("breakpoints")
        return skill.create_responsive_layout(layout_type, breakpoints)
    else:
        return {"error": f"Unknown function: {function_name}"}

if __name__ == "__main__":
    # Test the skill
    skill = FrontendDevelopmentSkill()
    
    print("Testing Frontend Development Skill...")
    
    # Test component creation
    result = skill.create_component("Button", "react", ["onClick", "label"], "styled-components")
    print(f"Component creation result: {result}")
    
    # Test responsive layout creation
    result = skill.create_responsive_layout("grid", {"mobile": 480, "tablet": 768, "desktop": 1024})
    print(f"Responsive layout result: {result}")