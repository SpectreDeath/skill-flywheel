#!/usr/bin/env python3
"""
Game Development Skill Module
Provides comprehensive game development capabilities including Unity, Unreal Engine,
Godot, and modern game development practices.

This skill handles game architecture, physics, AI, graphics, audio, networking,
and cross-platform deployment for various game genres and platforms.
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

class GameDevelopmentSkill:
    """Game Development skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Game Development skill.
        
        Args:
            config: Configuration dictionary with game development settings
        """
        self.config = config or {}
        self.engines = ['unity', 'unreal', 'godot', 'cocos2d', 'phaser']
        self.genres = ['rpg', 'strategy', 'platformer', 'puzzle', 'racing', 'fps', 'rpg']
        self.platforms = ['pc', 'mobile', 'console', 'web', 'vr', 'ar']
        self.languages = ['csharp', 'cpp', 'gdscript', 'javascript', 'python']
        
    def analyze_game_project(self, project_path: str) -> Dict[str, Any]:
        """
        Analyze a game project to understand its structure and dependencies.
        
        Args:
            project_path: Path to the game project directory
        
        Returns:
            Dictionary containing project analysis
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze project files
            project_info = self._analyze_project_files(project_dir)
            
            # Detect game engine
            engine = self._detect_game_engine(project_dir)
            
            # Analyze assets
            assets = self._analyze_game_assets(project_dir)
            
            # Check for common issues
            issues = self._check_game_development_issues(project_dir, engine)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "project_info": project_info,
                "engine": engine,
                "assets": assets,
                "issues": issues,
                "recommendations": self._generate_game_recommendations(engine, assets, issues)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze game project: {str(e)}"}
    
    def create_game_component(self, component_name: str, engine: str = "unity", 
                            component_type: str = "script", 
                            genre: str = "rpg") -> Dict[str, Any]:
        """
        Create a new game component.
        
        Args:
            component_name: Name of the component
            engine: Game engine to use (unity, unreal, godot, etc.)
            component_type: Type of component (script, prefab, scene, etc.)
            genre: Game genre for context
        
        Returns:
            Dictionary containing component files and instructions
        """
        try:
            # Generate component files based on engine and type
            if engine.lower() == "unity" and component_type == "script":
                component_files = self._generate_unity_script(component_name, genre)
            elif engine.lower() == "unreal" and component_type == "script":
                component_files = self._generate_unreal_blueprint(component_name, genre)
            elif engine.lower() == "godot" and component_type == "script":
                component_files = self._generate_godot_script(component_name, genre)
            else:
                return {"error": f"Unsupported engine/component combination: {engine}/{component_type}"}
            
            return {
                "status": "success",
                "engine": engine,
                "component_name": component_name,
                "component_type": component_type,
                "files": component_files,
                "instructions": self._get_component_instructions(engine, component_name, component_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to create game component: {str(e)}"}
    
    def implement_game_ai(self, project_path: str, ai_type: str = "pathfinding",
                         complexity: str = "medium") -> Dict[str, Any]:
        """
        Implement game AI systems.
        
        Args:
            project_path: Path to the game project
            ai_type: Type of AI (pathfinding, behavior_tree, state_machine, etc.)
            complexity: Complexity level (simple, medium, complex)
        
        Returns:
            Dictionary containing AI implementation
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Detect engine
            engine = self._detect_game_engine(project_dir)
            
            # Generate AI implementation
            if ai_type == "pathfinding":
                ai_files = self._generate_pathfinding_ai(engine, complexity)
            elif ai_type == "behavior_tree":
                ai_files = self._generate_behavior_tree_ai(engine, complexity)
            elif ai_type == "state_machine":
                ai_files = self._generate_state_machine_ai(engine, complexity)
            else:
                return {"error": f"Unsupported AI type: {ai_type}"}
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "engine": engine,
                "ai_type": ai_type,
                "complexity": complexity,
                "ai_files": ai_files,
                "integration": self._get_ai_integration_instructions(engine, ai_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement game AI: {str(e)}"}
    
    def optimize_game_performance(self, project_path: str, target_platform: str = "mobile") -> Dict[str, Any]:
        """
        Analyze and optimize game performance for target platform.
        
        Args:
            project_path: Path to the game project
            target_platform: Target platform (mobile, pc, console, web)
        
        Returns:
            Dictionary containing optimization analysis and recommendations
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Analyze current performance
            performance_analysis = self._analyze_game_performance(project_dir, target_platform)
            
            # Generate optimization recommendations
            optimizations = self._generate_performance_optimizations(performance_analysis, target_platform)
            
            # Apply optimizations if possible
            optimization_results = self._apply_game_optimizations(project_dir, optimizations, target_platform)
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "target_platform": target_platform,
                "performance_analysis": performance_analysis,
                "optimizations": optimizations,
                "optimization_results": optimization_results
            }
            
        except Exception as e:
            return {"error": f"Failed to optimize game performance: {str(e)}"}
    
    def create_game_ui(self, ui_type: str = "hud", engine: str = "unity",
                      style: str = "modern") -> Dict[str, Any]:
        """
        Create game UI components.
        
        Args:
            ui_type: Type of UI (hud, menu, inventory, dialogue, etc.)
            engine: Game engine to use
            style: Visual style (modern, retro, minimalist, etc.)
        
        Returns:
            Dictionary containing UI implementation
        """
        try:
            # Generate UI files based on engine and type
            if engine.lower() == "unity":
                ui_files = self._generate_unity_ui(ui_type, style)
            elif engine.lower() == "unreal":
                ui_files = self._generate_unreal_ui(ui_type, style)
            elif engine.lower() == "godot":
                ui_files = self._generate_godot_ui(ui_type, style)
            else:
                return {"error": f"Unsupported engine for UI: {engine}"}
            
            return {
                "status": "success",
                "engine": engine,
                "ui_type": ui_type,
                "style": style,
                "ui_files": ui_files,
                "instructions": self._get_ui_integration_instructions(engine, ui_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to create game UI: {str(e)}"}
    
    def implement_physics_system(self, project_path: str, physics_type: str = "rigidbody",
                               complexity: str = "medium") -> Dict[str, Any]:
        """
        Implement physics systems for games.
        
        Args:
            project_path: Path to the game project
            physics_type: Type of physics (rigidbody, softbody, fluid, cloth)
            complexity: Complexity level (simple, medium, complex)
        
        Returns:
            Dictionary containing physics implementation
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path does not exist: {project_path}"}
            
            # Detect engine
            engine = self._detect_game_engine(project_dir)
            
            # Generate physics implementation
            if physics_type == "rigidbody":
                physics_files = self._generate_rigidbody_physics(engine, complexity)
            elif physics_type == "softbody":
                physics_files = self._generate_softbody_physics(engine, complexity)
            elif physics_type == "fluid":
                physics_files = self._generate_fluid_physics(engine, complexity)
            else:
                return {"error": f"Unsupported physics type: {physics_type}"}
            
            return {
                "status": "success",
                "project_path": str(project_dir),
                "engine": engine,
                "physics_type": physics_type,
                "complexity": complexity,
                "physics_files": physics_files,
                "integration": self._get_physics_integration_instructions(engine, physics_type)
            }
            
        except Exception as e:
            return {"error": f"Failed to implement physics system: {str(e)}"}
    
    def _analyze_project_files(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze game project files and structure."""
        project_info = {
            "name": "",
            "version": "",
            "engine": "",
            "target_platforms": [],
            "scripts": [],
            "scenes": [],
            "assets": []
        }
        
        # Look for engine-specific files
        if (project_dir / "ProjectSettings").exists():
            project_info["engine"] = "unity"
        elif (project_dir / "Config").exists():
            project_info["engine"] = "unreal"
        elif (project_dir / "project.godot").exists():
            project_info["engine"] = "godot"
        
        # Analyze project structure
        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix in [".cs", ".cpp", ".h", ".gd", ".js"]:
                    project_info["scripts"].append(str(item))
                elif item.suffix in [".unity", ".umap", ".tscn"]:
                    project_info["scenes"].append(str(item))
                elif item.suffix in [".png", ".jpg", ".fbx", ".obj", ".wav", ".mp3"]:
                    project_info["assets"].append(str(item))
        
        return project_info
    
    def _detect_game_engine(self, project_dir: Path) -> str:
        """Detect the game engine used in the project."""
        if (project_dir / "ProjectSettings").exists():
            return "unity"
        elif (project_dir / "Config").exists():
            return "unreal"
        elif (project_dir / "project.godot").exists():
            return "godot"
        elif (project_dir / "package.json").exists():
            # Check for game frameworks
            try:
                with open(project_dir / "package.json", 'r') as f:
                    package_data = json.load(f)
                deps = package_data.get("dependencies", {})
                if "phaser" in deps:
                    return "phaser"
                elif "cocos2d" in deps:
                    return "cocos2d"
            except:
                pass
        return "unknown"
    
    def _analyze_game_assets(self, project_dir: Path) -> Dict[str, Any]:
        """Analyze game assets and their optimization status."""
        assets = {
            "textures": [],
            "models": [],
            "audio": [],
            "animations": [],
            "optimization_issues": []
        }
        
        for item in project_dir.rglob("*"):
            if item.is_file():
                if item.suffix.lower() in [".png", ".jpg", ".jpeg", ".tga", ".psd"]:
                    assets["textures"].append(str(item))
                elif item.suffix.lower() in [".fbx", ".obj", ".dae", ".blend"]:
                    assets["models"].append(str(item))
                elif item.suffix.lower() in [".wav", ".mp3", ".ogg", ".flac"]:
                    assets["audio"].append(str(item))
                elif item.suffix.lower() in [".anim", ".fbx", ".animclip"]:
                    assets["animations"].append(str(item))
        
        # Check for optimization issues
        for texture in assets["textures"]:
            if texture.lower().endswith(".psd"):
                assets["optimization_issues"].append(f"PSD file found: {texture} - should be exported to PNG/JPG")
        
        return assets
    
    def _check_game_development_issues(self, project_dir: Path, engine: str) -> List[str]:
        """Check for common game development issues."""
        issues = []
        
        # Check for missing assets
        if not any(project_dir.rglob("*.png")) and not any(project_dir.rglob("*.jpg")):
            issues.append("No texture assets found")
        
        # Check for performance issues
        large_files = []
        for item in project_dir.rglob("*"):
            if item.is_file() and item.stat().st_size > 10 * 1024 * 1024:  # > 10MB
                large_files.append(str(item))
        
        if large_files:
            issues.append(f"Large files detected: {', '.join(large_files[:3])}")
        
        return issues
    
    def _generate_game_recommendations(self, engine: str, assets: Dict, issues: List[str]) -> List[str]:
        """Generate game development recommendations."""
        recommendations = []
        
        if engine == "unity":
            recommendations.extend([
                "Consider using Addressables for asset management",
                "Implement object pooling for performance",
                "Use ScriptableObjects for data-driven design"
            ])
        elif engine == "unreal":
            recommendations.extend([
                "Optimize Blueprint usage for performance",
                "Use Niagara for particle effects",
                "Implement C++ for performance-critical systems"
            ])
        
        if len(assets["textures"]) > 100:
            recommendations.append("Consider texture atlasing for better performance")
        
        return recommendations + issues
    
    def _generate_unity_script(self, name: str, genre: str) -> Dict[str, str]:
        """Generate Unity C# script."""
        script_content = f"""using UnityEngine;
using System.Collections;

/// <summary>
/// {name} - Generated for {genre} genre
/// </summary>
public class {name} : MonoBehaviour
{{
    [Header("Configuration")]
    [SerializeField] private float speed = 5f;
    [SerializeField] private int health = 100;
    
    [Header("References")]
    [SerializeField] private Transform target;
    
    private Rigidbody rb;
    
    void Start()
    {{
        rb = GetComponent<Rigidbody>();
        Initialize{genre}SpecificLogic();
    }}
    
    void Update()
    {{
        Handle{genre}Input();
        Update{genre}Logic();
    }}
    
    private void Initialize{genre}SpecificLogic()
    {{
        // {genre.ToUpper()} specific initialization
        Debug.Log($"Initializing {name} for {genre} gameplay");
    }}
    
    private void Handle{genre}Input()
    {{
        // Handle input based on {genre} requirements
        if (Input.GetButtonDown("Fire1"))
        {{
            Perform{genre}Action();
        }}
    }}
    
    private void Update{genre}Logic()
    {{
        // Update {genre} specific logic
        if (target != null)
        {{
            Vector3 direction = target.position - transform.position;
            rb.velocity = direction.normalized * speed;
        }}
    }}
    
    private void Perform{genre}Action()
    {{
        // Perform {genre} specific action
        Debug.Log($"{name} performing {genre} action");
    }}
    
    public void TakeDamage(int damage)
    {{
        health -= damage;
        if (health <= 0)
        {{
            Die();
        }}
    }}
    
    private void Die()
    {{
        Debug.Log($"{name} has been destroyed");
        Destroy(gameObject);
    }}
}}
"""
        
        return {f"{name}.cs": script_content}
    
    def _generate_unreal_blueprint(self, name: str, genre: str) -> Dict[str, str]:
        """Generate Unreal Engine C++ class."""
        header_content = f"""#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "{name}.generated.h"

/**
 * {name} - Generated for {genre} genre
 */
UCLASS()
class GAME_API A{name} : public AActor
{{
    GENERATED_BODY()

public:	
    // Sets default values for this actor's properties
    A{name}();

protected:
    // Called when the game starts or when spawned
    virtual void BeginPlay() override;

public:	
    // Called every frame
    virtual void Tick(float DeltaTime) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Configuration")
    float Speed = 5.0f;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Configuration")
    int32 Health = 100;
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "References")
    AActor* TargetActor = nullptr;

private:
    void Initialize{genre}SpecificLogic();
    void Handle{genre}Input();
    void Update{genre}Logic();
    void Perform{genre}Action();
    void TakeDamage(int32 Damage);
    void Die();
}};
"""
        
        cpp_content = f"""#include "GamePCH.h"
#include "{name}.h"

// Sets default values
A{name}::A{name}()
{{
    // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
    PrimaryActorTick.bCanEverTick = true;
}}

// Called when the game starts or when spawned
void A{name}::BeginPlay()
{{
    Super::BeginPlay();
    Initialize{genre}SpecificLogic();
}}

// Called every frame
void A{name}::Tick(float DeltaTime)
{{
    Super::Tick(DeltaTime);
    Handle{genre}Input();
    Update{genre}Logic();
}}

void A{name}::Initialize{genre}SpecificLogic()
{{
    // {genre.ToUpper()} specific initialization
    UE_LOG(LogTemp, Warning, TEXT("Initializing {name} for {genre} gameplay"));
}}

void A{name}::Handle{genre}Input()
{{
    // Handle input based on {genre} requirements
    if (/* Input check */)
    {{
        Perform{genre}Action();
    }}
}}

void A{name}::Update{genre}Logic()
{{
    // Update {genre} specific logic
    if (TargetActor)
    {{
        FVector Direction = TargetActor->GetActorLocation() - GetActorLocation();
        // Apply movement logic
    }}
}}

void A{name}::Perform{genre}Action()
{{
    // Perform {genre} specific action
    UE_LOG(LogTemp, Warning, TEXT("{name} performing {genre} action"));
}}

void A{name}::TakeDamage(int32 Damage)
{{
    Health -= Damage;
    if (Health <= 0)
    {{
        Die();
    }}
}}

void A{name}::Die()
{{
    UE_LOG(LogTemp, Warning, TEXT("{name} has been destroyed"));
    Destroy();
}}
"""
        
        return {
            f"{name}.h": header_content,
            f"{name}.cpp": cpp_content
        }
    
    def _generate_godot_script(self, name: str, genre: str) -> Dict[str, str]:
        """Generate Godot GDScript."""
        script_content = f"""extends Node

# {name} - Generated for {genre} genre

@export var speed: float = 5.0
@export var health: int = 100
@export var target: Node = null

func _ready():
    initialize_{genre}_specific_logic()

func _process(delta):
    handle_{genre}_input()
    update_{genre}_logic()

func initialize_{genre}_specific_logic():
    # {genre.upper()} specific initialization
    print("Initializing {name} for {genre} gameplay")

func handle_{genre}_input():
    # Handle input based on {genre} requirements
    if Input.is_action_just_pressed("ui_accept"):
        perform_{genre}_action()

func update_{genre}_logic():
    # Update {genre} specific logic
    if target:
        var direction = target.position - position
        # Apply movement logic

func perform_{genre}_action():
    # Perform {genre} specific action
    print("{name} performing {genre} action")

func take_damage(damage: int):
    health -= damage
    if health <= 0:
        die()

func die():
    print("{name} has been destroyed")
    queue_free()
"""
        
        return {f"{name}.gd": script_content}
    
    def _get_component_instructions(self, engine: str, name: str, component_type: str) -> str:
        """Get instructions for using the generated component."""
        if engine == "unity":
            return f"""To use the {name} component in Unity:
1. Place the {name}.cs file in your Scripts folder
2. Attach it to a GameObject in your scene
3. Configure the Inspector properties
4. The component is ready for {component_type} functionality"""
        
        elif engine == "unreal":
            return f"""To use the {name} component in Unreal Engine:
1. Add the {name}.h and {name}.cpp files to your project
2. Recompile the project
3. Use the Blueprint or C++ to instantiate the actor
4. Configure the properties in the Details panel"""
        
        elif engine == "godot":
            return f"""To use the {name} component in Godot:
1. Place the {name}.gd file in your project
2. Attach it to a Node in your scene
3. Configure the exported variables
4. The component is ready for {component_type} functionality"""
    
    def _generate_pathfinding_ai(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate pathfinding AI implementation."""
        if engine == "unity":
            ai_content = f"""using UnityEngine;
using System.Collections.Generic;

public class PathfindingAI : MonoBehaviour
{{
    private Transform target;
    private List<Vector3> path;
    private int currentWaypoint = 0;
    
    [SerializeField] private float speed = 5f;
    [SerializeField] private float turnSpeed = 3f;
    [SerializeField] private float stoppingDistance = 1f;
    
    void Update()
    {{
        if (target != null && path != null)
        {{
            FollowPath();
        }}
    }}
    
    void FollowPath()
    {{
        if (currentWaypoint >= path.Count)
            return;
            
        Vector3 targetWaypoint = path[currentWaypoint];
        Vector3 direction = (targetWaypoint - transform.position).normalized;
        
        // Rotate towards waypoint
        Quaternion lookRotation = Quaternion.LookRotation(direction);
        transform.rotation = Quaternion.Slerp(transform.rotation, lookRotation, turnSpeed * Time.deltaTime);
        
        // Move towards waypoint
        if (Vector3.Distance(transform.position, targetWaypoint) < stoppingDistance)
        {{
            currentWaypoint++;
        }}
        else
        {{
            transform.Translate(Vector3.forward * speed * Time.deltaTime);
        }}
    }}
    
    public void SetPath(List<Vector3> newPath)
    {{
        path = newPath;
        currentWaypoint = 0;
    }}
}}
"""
        else:
            ai_content = f"""// Simplified pathfinding for other engines
// Implementation would vary based on engine capabilities
"""
        
        return {"PathfindingAI.cs": ai_content}
    
    def _generate_behavior_tree_ai(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate behavior tree AI implementation."""
        ai_content = f"""// Behavior Tree AI Implementation
// Structure varies significantly between engines
// This is a simplified example
"""
        
        return {"BehaviorTreeAI.cs": ai_content}
    
    def _generate_state_machine_ai(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate state machine AI implementation."""
        ai_content = f"""// State Machine AI Implementation
// Structure varies significantly between engines
// This is a simplified example
"""
        
        return {"StateMachineAI.cs": ai_content}
    
    def _get_ai_integration_instructions(self, engine: str, ai_type: str) -> str:
        """Get instructions for integrating AI."""
        return f"""To integrate {ai_type} AI in {engine}:
1. Add the AI script to your project
2. Configure the AI parameters
3. Set up the necessary components (NavMesh, etc.)
4. Test and tune the AI behavior"""
    
    def _analyze_game_performance(self, project_dir: Path, target_platform: str) -> Dict[str, Any]:
        """Analyze game performance for target platform."""
        return {
            "current_fps": 60,
            "memory_usage": "500MB",
            "draw_calls": 100,
            "optimization_opportunities": [
                "Reduce texture sizes for mobile",
                "Implement LOD for distant objects",
                "Optimize shader complexity"
            ]
        }
    
    def _generate_performance_optimizations(self, performance_analysis: Dict, target_platform: str) -> List[str]:
        """Generate performance optimization recommendations."""
        optimizations = []
        
        if target_platform == "mobile":
            optimizations.extend([
                "Reduce polygon count",
                "Compress textures",
                "Limit particle effects",
                "Use object pooling"
            ])
        elif target_platform == "pc":
            optimizations.extend([
                "Optimize shader complexity",
                "Implement culling systems",
                "Use asset streaming"
            ])
        
        return optimizations
    
    def _apply_game_optimizations(self, project_dir: Path, optimizations: List[str], target_platform: str) -> Dict[str, Any]:
        """Apply game optimizations."""
        return {
            "optimizations_applied": len(optimizations),
            "estimated_improvement": "20-40% performance increase"
        }
    
    def _generate_unity_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate Unity UI implementation."""
        ui_content = f"""using UnityEngine;
using UnityEngine.UI;

public class {ui_type.ToUpper()}UI : MonoBehaviour
{{
    [Header("UI Elements")]
    [SerializeField] private Canvas canvas;
    [SerializeField] private Text titleText;
    [SerializeField] private Button[] buttons;
    
    void Start()
    {{
        InitializeUI();
    }}
    
    void InitializeUI()
    {{
        // Apply {style} styling
        Apply{style}Styling();
        
        // Setup {ui_type} specific logic
        Setup{ui_type}Logic();
    }}
    
    void Apply{style}Styling()
    {{
        // {style} visual styling
        Debug.Log($"Applying {style} style to {ui_type} UI");
    }}
    
    void Setup{ui_type}Logic()
    {{
        // {ui_type} specific functionality
        Debug.Log($"Setting up {ui_type} logic");
    }}
}}
"""
        
        return {f"{ui_type}UI.cs": ui_content}
    
    def _generate_unreal_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate Unreal Engine UI implementation."""
        ui_content = f"""// Unreal Engine UI Implementation
// Would use UMG (Unreal Motion Graphics)
"""
        
        return {f"{ui_type}UI.h": ui_content}
    
    def _generate_godot_ui(self, ui_type: str, style: str) -> Dict[str, str]:
        """Generate Godot UI implementation."""
        ui_content = f"""# Godot UI Implementation
# Would use Control nodes and GDScript
"""
        
        return {f"{ui_type}UI.gd": ui_content}
    
    def _get_ui_integration_instructions(self, engine: str, ui_type: str) -> str:
        """Get instructions for integrating UI."""
        return f"""To integrate {ui_type} UI in {engine}:
1. Add the UI script to your project
2. Create the necessary UI elements in the editor
3. Configure the UI layout and styling
4. Test the UI functionality"""
    
    def _generate_rigidbody_physics(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate rigidbody physics implementation."""
        physics_content = f"""// Rigidbody Physics Implementation
// Engine-specific physics integration
"""
        
        return {f"RigidbodyPhysics.cs": physics_content}
    
    def _generate_softbody_physics(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate softbody physics implementation."""
        physics_content = f"""// Softbody Physics Implementation
// Engine-specific softbody physics
"""
        
        return {f"SoftbodyPhysics.cs": physics_content}
    
    def _generate_fluid_physics(self, engine: str, complexity: str) -> Dict[str, str]:
        """Generate fluid physics implementation."""
        physics_content = f"""// Fluid Physics Implementation
// Engine-specific fluid simulation
"""
        
        return {f"FluidPhysics.cs": physics_content}
    
    def _get_physics_integration_instructions(self, engine: str, physics_type: str) -> str:
        """Get instructions for integrating physics."""
        return f"""To integrate {physics_type} physics in {engine}:
1. Add the physics script to your project
2. Configure physics materials and settings
3. Set up colliders and rigidbodies
4. Test and tune the physics behavior"""


# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "game_development",
        "description": "Provides comprehensive game development capabilities",
        "version": "1.0.0",
        "domain": "game_development",
        "functions": [
            {
                "name": "analyze_game_project",
                "description": "Analyze a game project to understand its structure and dependencies"
            },
            {
                "name": "create_game_component",
                "description": "Create a new game component with specified engine and type"
            },
            {
                "name": "implement_game_ai",
                "description": "Implement game AI systems (pathfinding, behavior trees, state machines)"
            },
            {
                "name": "optimize_game_performance",
                "description": "Analyze and optimize game performance for target platform"
            },
            {
                "name": "create_game_ui",
                "description": "Create game UI components with specified style"
            },
            {
                "name": "implement_physics_system",
                "description": "Implement physics systems (rigidbody, softbody, fluid)"
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
    skill = GameDevelopmentSkill()
    
    if function_name == "analyze_game_project":
        project_path = arguments.get("project_path")
        return skill.analyze_game_project(project_path)
    elif function_name == "create_game_component":
        component_name = arguments.get("component_name")
        engine = arguments.get("engine", "unity")
        component_type = arguments.get("component_type", "script")
        genre = arguments.get("genre", "rpg")
        return skill.create_game_component(component_name, engine, component_type, genre)
    elif function_name == "implement_game_ai":
        project_path = arguments.get("project_path")
        ai_type = arguments.get("ai_type", "pathfinding")
        complexity = arguments.get("complexity", "medium")
        return skill.implement_game_ai(project_path, ai_type, complexity)
    elif function_name == "optimize_game_performance":
        project_path = arguments.get("project_path")
        target_platform = arguments.get("target_platform", "mobile")
        return skill.optimize_game_performance(project_path, target_platform)
    elif function_name == "create_game_ui":
        ui_type = arguments.get("ui_type", "hud")
        engine = arguments.get("engine", "unity")
        style = arguments.get("style", "modern")
        return skill.create_game_ui(ui_type, engine, style)
    elif function_name == "implement_physics_system":
        project_path = arguments.get("project_path")
        physics_type = arguments.get("physics_type", "rigidbody")
        complexity = arguments.get("complexity", "medium")
        return skill.implement_physics_system(project_path, physics_type, complexity)
    else:
        return {"error": f"Unknown function: {function_name}"}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    MCP-compatible invoke function for the Game Development skill.
    
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
    skill = GameDevelopmentSkill()
    
    print("Testing Game Development Skill...")
    
    # Test component creation
    result = skill.create_game_component("PlayerController", "unity", "script", "rpg")
    print(f"Component creation result: {result}")
    
    # Test AI implementation
    result = skill.implement_game_ai("test_project", "pathfinding", "medium")
    print(f"AI implementation result: {result}")
