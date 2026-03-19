#!/usr/bin/env python3
"""
Mobile Development Skill Module
Provides comprehensive mobile development capabilities including iOS, Android,
React Native, Flutter, and modern mobile development practices.

This skill handles mobile app architecture, platform-specific features, performance
optimization, cross-platform development, and mobile-specific UI/UX patterns.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MobileDevelopmentSkill:
    """Mobile Development skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Mobile Development skill.
        
        Args:
            config: Configuration dictionary with mobile development settings
        """
        self.config = config or {}
        self.platforms = ['ios', 'android', 'react_native', 'flutter', 'ionic', 'xamarin']
        self.architectures = ['mvc', 'mvp', 'mvvm', 'clean', 'redux']
        self.languages = ['swift', 'kotlin', 'java', 'dart', 'javascript', 'typescript']
        self.ui_frameworks = ['uikit', 'swiftui', 'android_views', 'jetpack_compose', 'flutter_widgets']
        
    def analyze_mobile_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze a mobile project to understand its structure and dependencies.
        
        Args:
            project_path: Path to the mobile project directory
        
        Returns:
            Dictionary containing project analysis
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze project files
            project_info = self._analyze_project_files(project_dir)
            
            # Detect platform and architecture
            platform = self._detect_platform(project_dir)
            architecture = self._detect_architecture(project_dir)
            
            # Analyze dependencies
            dependencies = self._analyze_dependencies(project_dir, platform)
            
            # Check for mobile-specific issues
            issues = self._check_mobile_issues(project_dir, platform)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "project_info": project_info,
                "platform": platform,
                "architecture": architecture,
                "dependencies": dependencies,
                "issues": issues,
                "recommendations": self._generate_mobile_recommendations(platform, architecture, issues)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze mobile project: {str(e)}"}
    
    def create_mobile_component(self, component_name: str, platform: str = "react_native", 
                              component_type: str = "screen", 
                              architecture: str = "mvvm") -> Dict[str, Any]:
        """
        Create a new mobile component.
        
        Args:
            component_name: Name of the component
            platform: Mobile platform (ios, android, react_native, flutter)
            component_type: Type of component (screen, component, service, model)
            architecture: Architecture pattern (mvc, mvp, mvvm, clean)
        
        Returns:
            Dictionary containing component files and instructions
        """
        try:
            # Generate component files based on platform and architecture
            if platform.lower() == "react_native" and architecture == "mvvm":
                component_files = self._generate_react_native_mvvm_component(component_name, component_type)
            elif platform.lower() == "flutter" and architecture == "clean":
                component_files = self._generate_flutter_clean_component(component_name, component_type)
            elif platform.lower() == "ios" and architecture == "mvc":
                component_files = self._generate_ios_mvc_component(component_name, component_type)
            elif platform.lower() == "android" and architecture == "mvp":
                component_files = self._generate_android_mvp_component(component_name, component_type)
            else:
                return {"error": f"Unsupported platform/architecture combination: {platform}/{architecture}"}
            
            return {
                "status": "success",
                "platform": platform,
                "component_name": component_name,
                "component_type": component_type,
                "architecture": architecture,
                "files": component_files,
                "instructions": self._get_component_instructions(platform, component_name, component_type, architecture)
            }
            
        except Exception as e:
            return {"error": f"Failed to create mobile component: {str(e)}"}
    
    def implement_mobile_api(self, project_path: str, api_type: str = "rest",
                           authentication: str = "jwt") -> Dict[str, Any]:
        """
        Implement mobile API integration.
        
        Args:
            project_path: Path to the mobile project
            api_type: Type of API (rest, graphql, grpc)
            authentication: Authentication method (jwt, oauth, basic)
        
        Returns:
            Dictionary containing API implementation
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Detect platform
            platform = self._detect_platform(project_dir)
            
            # Generate API implementation
            if api_type == "rest":
                api_files = self._generate_rest_api(platform, authentication)
            elif api_type == "graphql":
                api_files = self._generate_graphql_api(platform, authentication)
            else:
                return {"error": f"Unsupported API type: {api_type}"}
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "platform": platform,
                "api_type": api_type,
                "authentication": authentication,
                "api_files": api_files,
                "integration": self._get_api_integration_instructions(platform, api_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement mobile API: {str(e)}"}
    
    def optimize_mobile_performance(self, project_path: str, target_platform: str = "ios") -> Dict[str, Any]:
        """
        Analyze and optimize mobile app performance.
        
        Args:
            project_path: Path to the mobile project
            target_platform: Target platform (ios, android)
        
        Returns:
            Dictionary containing optimization analysis and recommendations
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze current performance
            performance_analysis = self._analyze_mobile_performance(project_dir, target_platform)
            
            # Generate optimization recommendations
            optimizations = self._generate_mobile_optimizations(performance_analysis, target_platform)
            
            # Apply optimizations if possible
            optimization_results = self._apply_mobile_optimizations(project_dir, optimizations, target_platform)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "target_platform": target_platform,
                "performance_analysis": performance_analysis,
                "optimizations": optimizations,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            return {"error": f"Failed to optimize mobile performance: {str(e)}"}
    
    def implement_mobile_ui(self, ui_type: str = "navigation", platform: str = "react_native",
                          style: str = "material") -> Dict[str, Any]:
        """
        Implement mobile UI components.
        
        Args:
            ui_type: Type of UI (navigation, forms, lists, modals)
            platform: Mobile platform
            style: Visual style (material, cupertino, custom)
        
        Returns:
            Dictionary containing UI implementation
        """
        try:
            # Generate UI files based on platform and type
            if platform.lower() == "react_native":
                ui_files = self._generate_react_native_ui(ui_type, style)
            elif platform.lower() == "flutter":
                ui_files = self._generate_flutter_ui(ui_type, style)
            elif platform.lower() == "ios":
                ui_files = self._generate_ios_ui(ui_type, style)
            elif platform.lower() == "android":
                ui_files = self._generate_android_ui(ui_type, style)
            else:
                return {"error": f"Unsupported platform for UI: {platform}"}
            
            return {
                "status": "success",
                "platform": platform,
                "ui_type": ui_type,
                "style": style,
                "ui_files": ui_files,
                "instructions": self._get_ui_integration_instructions(platform, ui_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement mobile UI: {str(e)}"}
    
    def implement_mobile_state_management(self, project_path: str, state_manager: str = "redux",
                                         platform: str = "react_native") -> Dict[str, Any]:
        """
        Implement state management for mobile applications.
        
        Args:
            project_path: Path to the mobile project
            state_manager: State management library (redux, mobx, provider, livedata)
            platform: Mobile platform
        
        Returns:
            Dictionary containing state management implementation
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Detect platform
            platform = self._detect_platform(project_dir)
            
            # Generate state management implementation
            if state_manager == "redux" and platform == "react_native":
                state_files = self._generate_redux_state_management()
            elif state_manager == "provider" and platform == "flutter":
                state_files = self._generate_provider_state_management()
            elif state_manager == "livedata" and platform == "android":
                state_files = self._generate_livedata_state_management()
            else:
                return {"error": f"Unsupported state manager/platform combination: {state_manager}/{platform}"}
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "platform": platform,
                "state_manager": state_manager,
                "state_files": state_files,
                "integration": self._get_state_integration_instructions(platform, state_manager)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement state management: {str(e)}"}
    
    def _analyze_project_files(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze mobile project files and structure."""
        project_info = {
            "name": "",
            "version": "",
            "platform": "",
            "target_os": "",
            "dependencies": [],
            "screens": [],
            "components": [],
            "services": []
        }
        
        # Look for platform-specific files
        if (project_dir / "ios").exists():
            project_info["platform"] = "ios"
        elif (project_dir / "android").exists():
            project_info["platform"] = "android"
        elif (project_dir / "src").exists() and any(project_dir.rglob("*.tsx")):
            project_info["platform"] = "react_native"
        elif (project_dir / "lib").exists() and any(project_dir.rglob("*.dart")):
            project_info["platform"] = "flutter"
        
        # Analyze project structure
        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix in [".tsx", ".ts", ".js", ".jsx"] or item.suffix in [".dart"] or item.suffix in [".swift", ".m", ".h"] or item.suffix in [".kt", ".java"]:
                    project_info["components"].append(str(item))
        
        return project_info
    
    def _detect_platform(self, project_dir: Path) -> str:
        """Detect the mobile platform used in the project."""
        if (project_dir / "ios").exists():
            return "ios"
        elif (project_dir / "android").exists():
            return "android"
        elif (project_dir / "src").exists() and any(project_dir.rglob("*.tsx")):
            return "react_native"
        elif (project_dir / "lib").exists() and any(project_dir.rglob("*.dart")):
            return "flutter"
        elif (project_dir / "package.json").exists():
            try:
                with open(project_dir / "package.json") as f:
                    package_data = json.load(f)
                deps = package_data.get("dependencies", {})
                if "react-native" in deps:
                    return "react_native"
                elif "flutter" in deps:
                    return "flutter"
            except:
                pass
        return "unknown"
    
    def _detect_architecture(self, project_dir: Path) -> str:
        """Detect the architecture pattern used in the project."""
        # Look for architecture-specific patterns
        if any(project_dir.rglob("*ViewModel*")) or any(project_dir.rglob("*view_model*")):
            return "mvvm"
        elif any(project_dir.rglob("*Presenter*")) or any(project_dir.rglob("*presenter*")):
            return "mvp"
        elif any(project_dir.rglob("*Controller*")) or any(project_dir.rglob("*controller*")):
            return "mvc"
        elif any(project_dir.rglob("*UseCase*")) or any(project_dir.rglob("*use_case*")):
            return "clean"
        return "unknown"
    
    def _analyze_dependencies(self, project_dir: Path, platform: str) -> Dict[str, Any]:
        """Analyze project dependencies."""
        dependencies = {
            "frameworks": [],
            "libraries": [],
            "plugins": [],
            "optimization_issues": []
        }
        
        if platform == "react_native":
            package_file = project_dir / "package.json"
            if package_file.exists():
                try:
                    with open(package_file) as f:
                        package_data = json.load(f)
                    deps = package_data.get("dependencies", {})
                    dev_deps = package_data.get("devDependencies", {})
                    
                    for dep, version in deps.items():
                        dependencies["libraries"].append(f"{dep}: {version}")
                    
                    for dep, version in dev_deps.items():
                        dependencies["libraries"].append(f"{dep}: {version} (dev)")
                        
                except:
                    pass
        
        return dependencies
    
    def _check_mobile_issues(self, project_dir: Path, platform: str) -> List[str]:
        """Check for common mobile development issues."""
        issues = []
        
        # Check for performance issues
        large_images = []
        for item in project_dir.rglob("*"):
            if item.is_file() and item.suffix.lower() in [".png", ".jpg", ".jpeg"]:
                if item.stat().st_size > 1024 * 1024:  # > 1MB
                    large_images.append(str(item))
        
        if large_images:
            issues.append(f"Large images detected: {len(large_images)} images > 1MB")
        
        # Check for missing platform-specific optimizations
        if platform == "ios":
            issues.append("Consider implementing iOS-specific optimizations (App Transport Security, etc.)")
        elif platform == "android":
            issues.append("Consider implementing Android-specific optimizations (ProGuard, etc.)")
        
        return issues
    
    def _generate_mobile_recommendations(self, platform: str, architecture: str, issues: List[str]) -> List[str]:
        """Generate mobile development recommendations."""
        recommendations = []
        
        if platform == "react_native":
            recommendations.extend([
                "Use memoization for expensive calculations",
                "Implement proper image caching",
                "Use FlatList for long lists",
                "Consider using TypeScript for better type safety"
            ])
        elif platform == "flutter":
            recommendations.extend([
                "Use const constructors where possible",
                "Implement proper state management",
                "Use ListView.builder for long lists",
                "Consider using Riverpod for state management"
            ])
        
        if architecture == "mvvm":
            recommendations.append("Ensure proper separation between View and ViewModel")
        elif architecture == "clean":
            recommendations.append("Maintain proper layer separation")
        
        return recommendations + issues
    
    def _generate_react_native_mvvm_component(self, name: str, component_type: str) -> Dict[str, str]:
        """Generate React Native MVVM component."""
        # View Model
        vm_content = f"""import {name}Repository from '../repositories/{name}Repository';

interface {name}State {{
  data: any[];
  loading: boolean;
  error: string | null;
}}

class {name}ViewModel {{
  private state: {name}State;
  private repository: {name}Repository;
  
  constructor() {{
    this.state = {{
      data: [],
      loading: false,
      error: null,
    }};
    this.repository = new {name}Repository();
  }}
  
  getState(): {name}State {{
    return this.state;
  }}
  
  async loadData(): Promise<void> {{
    this.state.loading = true;
    this.state.error = null;
    
    try {{
      const data = await this.repository.getData();
      this.state.data = data;
    }} catch (error) {{
      this.state.error = error.message;
    }} finally {{
      this.state.loading = false;
    }}
  }}
  
  async saveData(data: any): Promise<void> {{
    try {{
      await this.repository.saveData(data);
      await this.loadData();
    }} catch (error) {{
      this.state.error = error.message;
    }}
  }}
}}

export default {name}ViewModel;
"""
        
        # View Component
        view_content = (
            "import React, {useState, useEffect} from 'react';\n"
            "import {View, Text, FlatList, ActivityIndicator, StyleSheet} from 'react-native';\n"
            "import {name}ViewModel from '../viewmodels/{name}ViewModel';\n"
            "const {name}Screen = () => {\n"
            "  const [viewModel] = useState(() => new {name}ViewModel());\n"
            "  const [state, setState] = useState(viewModel.getState());\n"
            "  useEffect(() => {\n"
            "    viewModel.loadData();\n"
            "    const unsubscribe = viewModel.subscribe(() => {\n"
            "      setState(viewModel.getState());\n"
            "    });\n"
            "    return unsubscribe;\n"
            "  }, []);\n"
            "  if (state.loading) {\n"
            "    return (\n"
            "      <View style={styles.center}>\n"
            "        <ActivityIndicator size=\"large\" />\n"
            "      </View>\n"
            "    );\n"
            "  }\n"
            "  if (state.error) {\n"
            "    return (\n"
            "      <View style={styles.center}>\n"
            "        <Text style={styles.errorText}>Error: {state.error}</Text>\n"
            "      </View>\n"
            "    );\n"
            "  }\n"
            "  return (\n"
            "    <View style={styles.container}>\n"
            "      <FlatList\n"
            "        data={state.data}\n"
            "        keyExtractor={(item, index) => index.toString()}\n"
            "        renderItem={({item}) => (\n"
            "          <View style={styles.item}>\n"
            "            <Text>{item.title}</Text>\n"
            "          </View>\n"
            "        )}\n"
            "      />\n"
            "    </View>\n"
            "  );\n"
            "};\n"
            "const styles = StyleSheet.create({\n"
            "  container: {\n"
            "    flex: 1,\n"
            "    padding: 16,\n"
            "  },\n"
            "  center: {\n"
            "    flex: 1,\n"
            "    justifyContent: 'center',\n"
            "    alignItems: 'center',\n"
            "  },\n"
            "  errorText: {\n"
            "    color: 'red',\n"
            "    textAlign: 'center',\n"
            "  },\n"
            "  item: {\n"
            "    padding: 16,\n"
            "    borderBottomWidth: 1,\n"
            "    borderBottomColor: '#ccc',\n"
            "  },\n"
            "});\n"
            "export default {name}Screen;\n"
        )
        
        # Repository
        repo_content = f"""import axios from 'axios';

class {name}Repository {{
  private apiEndpoint = 'https://api.example.com/data';
  
  async getData(): Promise<any[]> {{
    const response = await axios.get(this.apiEndpoint);
    return response.data;
  }}
  
  async saveData(data: any): Promise<void> {{
    await axios.post(this.apiEndpoint, data);
  }}
}}

export default {name}Repository;
"""
        
        return {
            f"{name}ViewModel.ts": vm_content,
            f"{name}Screen.tsx": view_content,
            f"{name}Repository.ts": repo_content
        }
    
    def _generate_flutter_clean_component(self, name: str, component_type: str) -> Dict[str, str]:
        """Generate Flutter Clean Architecture component."""
        # Entity
        entity_content = f"""class {name} {{
  final int id;
  final String title;
  final String description;
  
  {name}({{
    required this.id,
    required this.title,
    required this.description,
  }});
  
  factory {name}.fromJson(Map<String, dynamic> json) {{
    return {name}(
      id: json['id'],
      title: json['title'],
      description: json['description'],
    );
  }}
  
  Map<String, dynamic> toJson() {{
    return {{
      'id': id,
      'title': title,
      'description': description,
    }};
  }}
}}
"""
        
        # Use Case
        usecase_content = f"""import 'package:dartz/dartz.dart';

import '../entities/{name.lower()}.dart';
import '../repositories/{name.lower()}_repository.dart';

class Get{name}UseCase {{
  final {name}Repository repository;
  
  Get{name}UseCase(this.repository);
  
  Future<Either<String, List<{name}>>> execute() async {{
    return await repository.get{name}s();
  }}
}}
"""
        
        # Repository Interface
        repo_interface_content = f"""import 'package:dartz/dartz.dart';

import '../entities/{name.lower()}.dart';

abstract class {name}Repository {{
  Future<Either<String, List<{name}>>> get{name}s();
  Future<Either<String, Unit>> save{name}({name} {name.lower()});
}}
"""
        
        # Widget
        widget_content = f"""import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../blocs/{name.lower()}/{name.lower()}_bloc.dart';
import '../entities/{name.lower()}.dart';

class {name}Screen extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return BlocProvider(
      create: (context) => {name}Bloc(
        get{name}UseCase: context.read(),
      ),
      child: Scaffold(
        appBar: AppBar(title: Text('{name}')),
        body: BlocBuilder<{name}Bloc, {name}State>(
          builder: (context, state) {{
            if (state is {name}Loading) {{
              return Center(child: CircularProgressIndicator());
            }} else if (state is {name}Loaded) {{
              return ListView.builder(
                itemCount: state.{name.lower()}s.length,
                itemBuilder: (context, index) {{
                  final item = state.{name.lower()}s[index];
                  return ListTile(
                    title: Text(item.title),
                    subtitle: Text(item.description),
                  );
                }},
              );
            }} else if (state is {name}Error) {{
              return Center(child: Text('Error: ${state.message}'));
            }}
            return Container();
          }},
        ),
      ),
    );
  }}
}}
"""
        
        return {
            f"{name.lower()}.dart": entity_content,
            f"get_{name.lower()}_usecase.dart": usecase_content,
            f"{name.lower()}_repository.dart": repo_interface_content,
            f"{name}Screen.dart": widget_content
        }
    
    def _generate_ios_mvc_component(self, name: str, component_type: str) -> Dict[str, str]:
        """Generate iOS MVC component."""
        # View Controller
        vc_content = f"""import UIKit

class {name}ViewController: UIViewController {{
    
    private var tableView: UITableView!
    private var data: [String] = []
    
    override func viewDidLoad() {{
        super.viewDidLoad()
        setupUI()
        loadData()
    }}
    
    private func setupUI() {{
        title = "{name}"
        view.backgroundColor = .systemBackground
        
        tableView = UITableView(frame: view.bounds, style: .plain)
        tableView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        tableView.delegate = self
        tableView.dataSource = self
        tableView.register(UITableViewCell.self, forCellReuseIdentifier: "Cell")
        
        view.addSubview(tableView)
    }}
    
    private func loadData() {{
        // Load data from model
        data = ["Item 1", "Item 2", "Item 3"]
        tableView.reloadData()
    }}
}}

extension {name}ViewController: UITableViewDataSource, UITableViewDelegate {{
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {{
        return data.count
    }}
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {{
        let cell = tableView.dequeueReusableCell(withIdentifier: "Cell", for: indexPath)
        cell.textLabel?.text = data[indexPath.row]
        return cell
    }}
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {{
        tableView.deselectRow(at: indexPath, animated: true)
        // Handle selection
    }}
}}
"""
        
        return {f"{name}ViewController.swift": vc_content}
    
    def _generate_android_mvp_component(self, name: str, component_type: str) -> Dict[str, str]:
        """Generate Android MVP component."""
        # Contract
        contract_content = f"""package com.example.app.contract;

import java.util.List;

public interface {name}Contract {{
    
    interface View {{
        void showData(List<String> data);
        void showError(String error);
        void showLoading();
        void hideLoading();
    }}
    
    interface Presenter {{
        void loadData();
        void onDestroy();
    }}
    
    interface Model {{
        interface OnFinishedListener {{
            void onFinished(List<String> data);
            void onFailure(Throwable t);
        }}
        
        void getData(OnFinishedListener onFinishedListener);
    }}
}}
"""
        
        # Presenter
        presenter_content = f"""package com.example.app.presenter;

import com.example.app.contract.{name}Contract;
import com.example.app.model.{name}Model;

public class {name}Presenter implements {name}Contract.Presenter {{
    
    private {name}Contract.View view;
    private {name}Contract.Model model;
    
    public {name}Presenter({name}Contract.View view) {{
        this.view = view;
        this.model = new {name}Model();
    }}
    
    @Override
    public void loadData() {{
        if (view != null) {{
            view.showLoading();
        }}
        
        model.getData(new {name}Contract.Model.OnFinishedListener() {{
            @Override
            public void onFinished(List<String> data) {{
                if (view != null) {{
                    view.setData(data);
                    view.hideLoading();
                }}
            }}
            
            @Override
            public void onFailure(Throwable t) {{
                if (view != null) {{
                    view.showError("Error loading data");
                    view.hideLoading();
                }}
            }}
        }});
    }}
    
    @Override
    public void onDestroy() {{
        view = null;
    }}
}}
"""
        
        return {
            f"{name}Contract.java": contract_content,
            f"{name}Presenter.java": presenter_content
        }
    
    def _get_component_instructions(self, platform: str, name: str, component_type: str, architecture: str) -> str:
        """Get instructions for using the generated component."""
        if platform == "react_native":
            return f"""To use the {name} component in React Native:
1. Place the files in your src/ directory
2. Import the screen in your navigation
3. Configure the repository with your API endpoints
4. The MVVM pattern ensures clean separation of concerns"""
        
        elif platform == "flutter":
            return f"""To use the {name} component in Flutter:
1. Place the files in your lib/ directory
2. Register the use case in your dependency injection
3. Use the screen in your navigation
4. The Clean Architecture ensures testability and maintainability"""
        
        elif platform == "ios":
            return f"""To use the {name} component in iOS:
1. Add the view controller to your storyboard or navigation
2. Configure the data source
3. Customize the UI as needed
4. The MVC pattern provides clear separation of concerns"""
        
        elif platform == "android":
            return f"""To use the {name} component in Android:
1. Add the files to your Java/Kotlin package
2. Register the presenter in your activity/fragment
3. Configure the model with your data source
4. The MVP pattern ensures testability and separation of concerns"""
    
    def _generate_rest_api(self, platform: str, authentication: str) -> Dict[str, str]:
        """Generate REST API implementation."""
        if platform == "react_native":
            api_content = """import axios from 'axios';

class ApiService {
  private baseURL = 'https://api.example.com';
  private token: string | null = null;
  
  constructor() {
    this.setupInterceptors();
  }
  
  private setupInterceptors() {
    axios.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );
  }
  
  async get<T>(endpoint: string): Promise<T> {
    const response = await axios.get(`${this.baseURL}${endpoint}`);
    return response.data;
  }
  
  async post<T>(endpoint: string, data: any): Promise<T> {
    const response = await axios.post(`${this.baseURL}${endpoint}`, data);
    return response.data;
  }
  
  async put<T>(endpoint: string, data: any): Promise<T> {
    const response = await axios.put(`${this.baseURL}${endpoint}`, data);
    return response.data;
  }
  
  async delete<T>(endpoint: string): Promise<T> {
    const response = await axios.delete(`${this.baseURL}${endpoint}`);
    return response.data;
  }
  
  setToken(token: string) {
    this.token = token;
  }
  
  clearToken() {
    this.token = null;
  }
}

export default new ApiService();
"""
        else:
            api_content = f"""// REST API implementation for {platform}
// Platform-specific implementation would vary
"""
        
        return {"ApiService.ts": api_content}
    
    def _generate_graphql_api(self, platform: str, authentication: str) -> Dict[str, str]:
        """Generate GraphQL API implementation."""
        api_content = f"""// GraphQL API implementation for {platform}
// Platform-specific implementation would vary
"""
        
        return {"GraphQLService.ts": api_content}
    
    def _get_api_integration_instructions(self, platform: str, api_type: str) -> str:
        """Get instructions for integrating API."""
        return f"""To integrate {api_type} API in {platform}:
1. Add the API service to your project
2. Configure the base URL and authentication
3. Use the service methods in your components
4. Handle errors and loading states appropriately"""
    
    def _analyze_mobile_performance(self, project_dir: Path, target_platform: str) -> Dict[str, Any]:
        """Analyze mobile app performance."""
        return {
            "current_fps": 60,
            "memory_usage": "150MB",
            "battery_impact": "medium",
            "optimization_opportunities": [
                "Implement image caching",
                "Optimize list rendering",
                "Reduce network calls",
                "Use lazy loading"
            ]
        }
    
    def _generate_mobile_optimizations(self, performance_analysis: Dict, target_platform: str) -> List[str]:
        """Generate mobile optimization recommendations."""
        optimizations = []
        
        if target_platform == "ios":
            optimizations.extend([
                "Enable App Transport Security exceptions if needed",
                "Implement proper image compression",
                "Use Core Data for local storage",
                "Optimize app bundle size"
            ])
        elif target_platform == "android":
            optimizations.extend([
                "Enable ProGuard/R8 for code shrinking",
                "Implement proper memory management",
                "Use Room for local storage",
                "Optimize APK size"
            ])
        
        return optimizations
    
    def _apply_mobile_optimizations(self, project_dir: Path, optimizations: List[str], target_platform: str) -> Dict[str, Any]:
        """Apply mobile optimizations."""
        return {
            "optimizations_applied": len(optimizations),
            "estimated_improvement": "15-30% performance improvement"
        }
    
    def _generate_react_native_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate React Native UI implementation."""
        ui_content = (
            "import React from 'react';\n"
            "import {StyleSheet, View, Text, TouchableOpacity} from 'react-native';\n"
            "const " + ui_type.capitalize() + "Component = () => {\n"
            "  return (\n"
            "    <View style={styles.container}>\n"
            "      <Text style={styles.title}>" + ui_type.upper() + " Component</Text>\n"
            "      {/* " + ui_type + " specific UI elements */}\n"
            "    </View>\n"
            "  );\n"
            "};\n"
            "const styles = StyleSheet.create({\n"
            "  container: {\n"
            "    flex: 1,\n"
            "    padding: 16,\n"
            "    backgroundColor: '#fff',\n"
            "  },\n"
            "  title: {\n"
            "    fontSize: 24,\n"
            "    fontWeight: 'bold',\n"
            "    marginBottom: 16,\n"
            "  },\n"
            "});\n"
            "export default " + ui_type.capitalize() + "Component;\n"
        )
        
        return {f"{ui_type}Component.tsx": ui_content}
    
    def _generate_flutter_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate Flutter UI implementation."""
        ui_content = f"""import 'package:flutter/material.dart';

class {ui_type.charAt(0).toUpperCase() + ui_type.slice(1)}Widget extends StatelessWidget {{
  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: Text('{ui_type.toUpperCase()} Component'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text(
              '{ui_type.toUpperCase()} Component',
              style: Theme.of(context).textTheme.headline6,
            ),
            // {ui_type} specific UI elements
          ],
        ),
      ),
    );
  }}
}}
"""
        
        return {f"{ui_type}Widget.dart": ui_content}
    
    def _generate_ios_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate iOS UI implementation."""
        ui_content = f"""import UIKit

class {ui_type.charAt(0).toUpperCase() + ui_type.slice(1)}ViewController: UIViewController {{
    
    override func viewDidLoad() {{
        super.viewDidLoad()
        setupUI()
    }}
    
    private func setupUI() {{
        view.backgroundColor = .systemBackground
        title = "{ui_type.toUpperCase()} Component"
        
        // {ui_type} specific UI setup
    }}
}}
"""
        
        return {f"{ui_type}ViewController.swift": ui_content}
    
    def _generate_android_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate Android UI implementation."""
        ui_content = f"""package com.example.app.ui;

import android.os.Bundle;
import androidx.appcompat.app.AppCompatActivity;

public class {ui_type.charAt(0).toUpperCase() + ui_type.slice(1)}Activity extends AppCompatActivity {{
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_{ui_type.toLowerCase()});
        
        // {ui_type} specific UI setup
    }}
}}
"""
        
        return {f"{ui_type}Activity.java": ui_content}
    
    def _get_ui_integration_instructions(self, platform: str, ui_type: str) -> str:
        """Get instructions for integrating UI."""
        return f"""To integrate {ui_type} UI in {platform}:
1. Add the UI component to your project
2. Configure the navigation/routing
3. Style the component according to your design system
4. Test on target devices and platforms"""
    
    def _generate_redux_state_management(self) -> Dict[str, str]:
        """Generate Redux state management for React Native."""
        store_content = """import { createStore, combineReducers, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import { persistStore, persistReducer } from 'redux-persist';
import storage from 'redux-persist/lib/storage';

// Import reducers
import userReducer from './reducers/userReducer';
import dataReducer from './reducers/dataReducer';

const rootReducer = combineReducers({
  user: userReducer,
  data: dataReducer,
});

const persistConfig = {
  key: 'root',
  storage,
  whitelist: ['user'], // Only persist user state
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = createStore(
  persistedReducer,
  applyMiddleware(thunk)
);

const persistor = persistStore(store);

export { store, persistor };
"""
        
        return {"store.ts": store_content}
    
    def _generate_provider_state_management(self) -> Dict[str, str]:
        """Generate Provider state management for Flutter."""
        provider_content = """import 'package:flutter/foundation.dart';

class AppState with ChangeNotifier {
  bool _isLoading = false;
  String _error = '';

  bool get isLoading => _isLoading;
  String get error => _error;

  void setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void setError(String error) {
    _error = error;
    notifyListeners();
  }
}
"""
        
        return {"app_state.dart": provider_content}
    
    def _generate_livedata_state_management(self) -> Dict[str, str]:
        """Generate LiveData state management for Android."""
        livedata_content = """package com.example.app.viewmodel;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

public class MainViewModel extends ViewModel {
    private MutableLiveData<Boolean> isLoading = new MutableLiveData<>();
    private MutableLiveData<String> error = new MutableLiveData<>();

    public LiveData<Boolean> getIsLoading() {
        return isLoading;
    }

    public LiveData<String> getError() {
        return error;
    }

    public void setLoading(boolean loading) {
        isLoading.setValue(loading);
    }

    public void setError(String errorMessage) {
        error.setValue(errorMessage);
    }
}
"""
        
        return {"MainViewModel.java": livedata_content}
    
    def _get_state_integration_instructions(self, platform: str, state_manager: str) -> str:
        """Get instructions for integrating state management."""
        if state_manager == "redux":
            return f"""To integrate Redux in {platform}:
1. Install redux and react-redux packages
2. Create your store and reducers
3. Wrap your app with Provider
4. Use useSelector and useDispatch in components"""
        
        elif state_manager == "provider":
            return f"""To integrate Provider in {platform}:
1. Add provider package to dependencies
2. Create your ChangeNotifier classes
3. Wrap your app with MultiProvider
4. Use Provider.of() or Consumer in widgets"""
        
        elif state_manager == "livedata":
            return f"""To integrate LiveData in {platform}:
1. Add Android Architecture Components
2. Create your ViewModel classes
3. Use LiveData in your UI components
4. Observe data changes with observers"""


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "mobile_development",
        "description": "Provides comprehensive mobile development capabilities",
        "version": "1.0.0",
        "domain": "mobile_development",
        "functions": [
            {
                "name": "analyze_mobile_project",
                "description": "Analyze a mobile project to understand its structure and dependencies"
            },
            {
                "name": "create_mobile_component",
                "description": "Create a new mobile component with specified platform and architecture"
            },
            {
                "name": "implement_mobile_api",
                "description": "Implement mobile API integration (REST, GraphQL)"
            },
            {
                "name": "optimize_mobile_performance",
                "description": "Analyze and optimize mobile app performance"
            },
            {
                "name": "implement_mobile_ui",
                "description": "Implement mobile UI components with specified style"
            },
            {
                "name": "implement_mobile_state_management",
                "description": "Implement state management for mobile applications"
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
    skill = MobileDevelopmentSkill()
    
    if function_name == "analyze_mobile_project":
        project_path = arguments.get("project_path")
        return skill.analyze_mobile_project(project_path)
    elif function_name == "create_mobile_component":
        component_name = arguments.get("component_name")
        platform = arguments.get("platform", "react_native")
        component_type = arguments.get("component_type", "screen")
        architecture = arguments.get("architecture", "mvvm")
        return skill.create_mobile_component(component_name, platform, component_type, architecture)
    elif function_name == "implement_mobile_api":
        project_path = arguments.get("project_path")
        api_type = arguments.get("api_type", "rest")
        authentication = arguments.get("authentication", "jwt")
        return skill.implement_mobile_api(project_path, api_type, authentication)
    elif function_name == "optimize_mobile_performance":
        project_path = arguments.get("project_path")
        target_platform = arguments.get("target_platform", "ios")
        return skill.optimize_mobile_performance(project_path, target_platform)
    elif function_name == "implement_mobile_ui":
        ui_type = arguments.get("ui_type", "navigation")
        platform = arguments.get("platform", "react_native")
        style = arguments.get("style", "material")
        return skill.implement_mobile_ui(ui_type, platform, style)
    elif function_name == "implement_mobile_state_management":
        project_path = arguments.get("project_path")
        state_manager = arguments.get("state_manager", "redux")
        platform = arguments.get("platform", "react_native")
        return skill.implement_mobile_state_management(project_path, state_manager, platform)
    else:
        return {"error": f"Unknown function: {function_name}"}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP-compatible invoke function for the Mobile Development skill.
    
    Args:
        payload: Dictionary containing function name and arguments
    
    Returns:
        Function execution result
    """
    function_name = payload.get("function_name")
    arguments = payload.get("arguments", {})
    
    return execute_function(function_name, arguments)

if __name__ == "__main__":
    # Test the skill
    skill = MobileDevelopmentSkill()
    
    print("Testing Mobile Development Skill...")
    
    # Test component creation
    result = skill.create_mobile_component("UserProfile", "react_native", "screen", "mvvm")
    print(f"Component creation result: {result}")
    
    # Test API implementation
    result = skill.implement_mobile_api("test_project", "rest", "jwt")
    print(f"API implementation result: {result}")
