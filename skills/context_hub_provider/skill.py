#!/usr/bin/env python3
"""
Context Hub Provider Skill
Wraps the chub CLI tool for Strategy & Analysis domain operations.

This skill provides autonomous skill synthesis capabilities through
the context-hub CLI tool, focusing on strategy and analysis workflows.
"""

import os
import subprocess
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContextHubProvider:
    """Context Hub Provider skill implementation."""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the Context Hub Provider.
        
        Args:
            config: Configuration dictionary with chub CLI settings
        """
        self.config = config or {}
        self.chub_path = self._find_chub_cli()
        self.domain = "strategy_analysis"
        
    def _find_chub_cli(self) -> Optional[str]:
        """Find the chub CLI executable in the system."""
        # Get the root directory (two levels up from skills directory)
        current_dir = os.getcwd()
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        
        # Check common locations for chub CLI
        possible_paths = [
            "chub",
            "/usr/local/bin/chub",
            "/usr/bin/chub",
            "context-hub/cli/bin/chub",
            os.path.join(root_dir, "context-hub", "cli", "bin", "chub"),
            os.path.join(root_dir, "context-hub", "cli", "bin", "chub.cmd")
        ]
        
        # Try with node first for Node.js scripts
        for path in possible_paths:
            try:
                result = subprocess.run(
                    ["node", path, "--cli-version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    logger.info(f"Found chub CLI at: node {path}")
                    return path  # Return just the path, we'll prepend "node" when executing
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        # Try without node for direct execution
        for path in possible_paths:
            try:
                result = subprocess.run(
                    [path, "--cli-version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    logger.info(f"Found chub CLI at: {path}")
                    return path
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        
        logger.warning("chub CLI not found in standard locations")
        return None
    
    def is_available(self) -> bool:
        """Check if the chub CLI is available."""
        return self.chub_path is not None
    
    def _get_chub_command(self) -> List[str]:
        """Get the command to run chub CLI (with node if needed)."""
        if self.chub_path and self.chub_path.endswith('.js'):
            return ["node", self.chub_path]
        elif self.chub_path and self.chub_path.endswith('chub'):
            # Check if it's a Node.js script by looking for shebang
            try:
                with open(self.chub_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#!') and 'node' in first_line:
                        return ["node", self.chub_path]
            except:
                pass
        return [self.chub_path] if self.chub_path else []
    
    def get_context_hub_info(self) -> Dict[str, Any]:
        """
        Get information about the context hub system.
        
        Returns:
            Dictionary containing context hub information
        """
        if not self.is_available():
            return {"error": "chub CLI not available"}
        
        try:
            chub_cmd = self._get_chub_command()
            result = subprocess.run(
                chub_cmd + ["--cli-version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Parse the output to extract relevant information
                info_lines = result.stdout.strip().split('\n')
                info_dict = {}
                
                for line in info_lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        info_dict[key.strip()] = value.strip()
                    elif line.strip():
                        info_dict["version"] = line.strip()
                
                return {
                    "status": "success",
                    "info": info_dict,
                    "domain": self.domain
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to get context hub info: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout while getting context hub info"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def list_skills(self, domain: Optional[str] = None) -> Dict[str, Any]:
        """
        List available skills in the context hub.
        
        Args:
            domain: Optional domain filter (defaults to strategy_analysis)
        
        Returns:
            Dictionary containing skill information
        """
        if not self.is_available():
            return {"error": "chub CLI not available"}
        
        target_domain = domain or self.domain
        try:
            chub_cmd = self._get_chub_command()
            result = subprocess.run(
                chub_cmd + ["skills", "list", "--domain", target_domain],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                # Parse skills output
                skills_data = self._parse_skills_output(result.stdout)
                return {
                    "status": "success",
                    "domain": target_domain,
                    "skills": skills_data,
                    "count": len(skills_data)
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to list skills: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout while listing skills"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def create_skill(self, skill_name: str, skill_description: str, 
                    skill_type: str = "analysis") -> Dict[str, Any]:
        """
        Create a new skill in the context hub.
        
        Args:
            skill_name: Name of the skill
            skill_description: Description of the skill
            skill_type: Type of skill (analysis, strategy, etc.)
        
        Returns:
            Dictionary containing creation result
        """
        if not self.is_available():
            return {"error": "chub CLI not available"}
        
        try:
            # Create skill command
            chub_cmd = self._get_chub_command()
            cmd = chub_cmd + [
                "skills", "create",
                "--name", skill_name,
                "--description", skill_description,
                "--type", skill_type,
                "--domain", self.domain
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                return {
                    "status": "success",
                    "message": f"Skill '{skill_name}' created successfully",
                    "skill_name": skill_name,
                    "domain": self.domain
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to create skill: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout while creating skill"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def analyze_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze context data using the context hub.
        
        Args:
            context_data: Dictionary containing context to analyze
        
        Returns:
            Dictionary containing analysis results
        """
        if not self.is_available():
            return {"error": "chub CLI not available"}
        
        try:
            # Convert context data to JSON string for CLI input
            context_json = json.dumps(context_data)
            
            chub_cmd = self._get_chub_command()
            result = subprocess.run(
                chub_cmd + ["analyze", "--input", "-"],
                input=context_json,
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if result.returncode == 0:
                # Parse analysis output
                analysis_result = self._parse_analysis_output(result.stdout)
                return {
                    "status": "success",
                    "analysis": analysis_result,
                    "domain": self.domain
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to analyze context: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout while analyzing context"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def synthesize_skills(self, requirements: List[str]) -> Dict[str, Any]:
        """
        Synthesize new skills based on requirements.
        
        Args:
            requirements: List of skill requirements
        
        Returns:
            Dictionary containing synthesis results
        """
        if not self.is_available():
            return {"error": "chub CLI not available"}
        
        try:
            # Convert requirements to JSON
            requirements_json = json.dumps({"requirements": requirements})
            
            chub_cmd = self._get_chub_command()
            result = subprocess.run(
                chub_cmd + ["synthesize", "--requirements", "-"],
                input=requirements_json,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes for synthesis
            )
            
            if result.returncode == 0:
                synthesis_result = self._parse_synthesis_output(result.stdout)
                return {
                    "status": "success",
                    "synthesis": synthesis_result,
                    "domain": self.domain
                }
            else:
                return {
                    "status": "error",
                    "message": f"Failed to synthesize skills: {result.stderr}"
                }
                
        except subprocess.TimeoutExpired:
            return {"error": "Timeout while synthesizing skills"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
    
    def _parse_skills_output(self, output: str) -> List[Dict[str, Any]]:
        """Parse skills list output from chub CLI."""
        skills = []
        lines = output.strip().split('\n')
        
        for line in lines:
            if line.strip() and not line.startswith('#'):
                # Simple parsing - in a real implementation, this would
                # depend on the actual chub CLI output format
                parts = line.split('\t')
                if len(parts) >= 2:
                    skills.append({
                        "name": parts[0],
                        "description": parts[1],
                        "type": parts[2] if len(parts) > 2 else "unknown"
                    })
        
        return skills
    
    def _parse_analysis_output(self, output: str) -> Dict[str, Any]:
        """Parse analysis output from chub CLI."""
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            # Fallback parsing for non-JSON output
            return {"raw_output": output}
    
    def _parse_synthesis_output(self, output: str) -> Dict[str, Any]:
        """Parse synthesis output from chub CLI."""
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            return {"raw_output": output}

# MCP Integration Functions
def register_skill() -> Dict[str, Any]:
    """Register this skill with the MCP server."""
    return {
        "name": "context_hub_provider",
        "description": "Provides context hub functionality for strategy and analysis domain",
        "version": "1.0.0",
        "domain": "strategy_analysis",
        "functions": [
            {
                "name": "get_context_hub_info",
                "description": "Get information about the context hub system"
            },
            {
                "name": "list_skills",
                "description": "List available skills in the context hub"
            },
            {
                "name": "create_skill",
                "description": "Create a new skill in the context hub"
            },
            {
                "name": "analyze_context",
                "description": "Analyze context data using the context hub"
            },
            {
                "name": "synthesize_skills",
                "description": "Synthesize new skills based on requirements"
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
    provider = ContextHubProvider()
    
    if function_name == "get_context_hub_info":
        return provider.get_context_hub_info()
    elif function_name == "list_skills":
        domain = arguments.get("domain")
        return provider.list_skills(domain)
    elif function_name == "create_skill":
        skill_name = arguments.get("skill_name")
        skill_description = arguments.get("skill_description")
        skill_type = arguments.get("skill_type", "analysis")
        return provider.create_skill(skill_name, skill_description, skill_type)
    elif function_name == "analyze_context":
        context_data = arguments.get("context_data", {})
        return provider.analyze_context(context_data)
    elif function_name == "synthesize_skills":
        requirements = arguments.get("requirements", [])
        return provider.synthesize_skills(requirements)
    else:
        return {"error": f"Unknown function: {function_name}"}

if __name__ == "__main__":
    # Test the skill
    provider = ContextHubProvider()
    
    print("Testing Context Hub Provider Skill...")
    print(f"chub CLI available: {provider.is_available()}")
    
    if provider.is_available():
        info = provider.get_context_hub_info()
        print(f"Context Hub Info: {info}")
    else:
        print("chub CLI not found - skill will not be functional")