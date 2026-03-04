import os
import json
import datetime
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
server_name = os.environ.get("MCP_SERVER_NAME", "SkillFlywheel")
mcp = FastMCP(server_name)

# Configuration from environment or defaults
# Path relative to container /app mounting point
REGISTRY_FILE = Path(os.environ.get("REGISTRY_FILE", "/app/skill_registry.json"))
SKILLS_DIR = Path(os.environ.get("SKILLS_DIR", "/app/domains"))
TELEMETRY_LOG = Path(os.environ.get("TELEMETRY_LOG", "/app/telemetry/usage_log.jsonl"))
MCP_DOMAINS = os.environ.get("MCP_DOMAINS", "").split(",") if os.environ.get("MCP_DOMAINS") else []

def log_telemetry(skill_id, request, duration=0, status="success"):
    """Log skill usage to a JSONL file."""
    try:
        TELEMETRY_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "skill": skill_id,
            "request_preview": request[:100] if request else "",
            "duration": duration,
            "status": status,
            "server": server_name
        }
        with open(TELEMETRY_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        print(f"Telemetry logging error: {e}")

def register_skills():
    """Dynamically register tools for each skill using the registry index."""
    if not REGISTRY_FILE.exists():
        print(f"Registry file not found at {REGISTRY_FILE}. Run reindex_skills.py first.")
        return

    try:
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)
            
        registered_count = 0
        for skill in registry:
            domain = skill.get('domain', 'General')
            
            # Filter by domain if MCP_DOMAINS is set
            if MCP_DOMAINS and domain not in MCP_DOMAINS:
                continue
                
            skill_id = skill['name'].lower().replace('-', '_')
            description = skill['description'] or skill['purpose'] or f"Execute the {skill_id} skill."
            
            # Use path from registry, resolve against workspace root
            # Registry paths seem to be relative to workspace root (parent of skills dir)
            root_dir = REGISTRY_FILE.parent
            skill_file = root_dir / skill['path']
            
            # Create a closure for the tool function
            def create_tool_func(path, sid):
                async def skill_tool(ctx, request: str = ""):
                    """
                    Execute this skill.
                    Instruction: Following the workflow and constraints in this skill, process the request.
                    """
                    import time
                    start_time = time.time()
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        result = f"SYSTEM INSTRUCTIONS FOR SKILL:\n\n{content}\n\nUSER REQUEST: {request}\n\nGUIDANCE: Follow the Workflow and Constraints sections strictly."
                        log_telemetry(sid, request, duration=time.time() - start_time, status="success")
                        return result
                    except Exception as e:
                        log_telemetry(sid, request, status=f"error: {str(e)}")
                        return f"Error loading skill content: {str(e)}"
                return skill_tool

            # Register the tool with a unique name
            tool_func = create_tool_func(skill_file, skill_id)
            tool_func.__name__ = f"skill_{skill_id}"
            mcp.tool(name=f"skill_{skill_id}", description=description)(tool_func)
            registered_count += 1
            
        print(f"Registered {registered_count} skills from domains: {', '.join(MCP_DOMAINS) if MCP_DOMAINS else 'All'}")
    except Exception as e:
        print(f"Error registering skills: {e}")

@mcp.tool()
async def find_skill(ctx, query: str, category: str = None):
    """
    Search the AgentSkills library for relevant skills based on a query.
    Useful when you aren't sure which specialized skill to use.
    """
    import subprocess
    import json
    
    script_path = Path(__file__).parent / "registry_search.py"
    cmd = ["python", str(script_path), query]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"SEARCH RESULTS for '{query}':\n\n{result.stdout}"
    except Exception as e:
        return f"Error searching registry: {str(e)}"

if __name__ == "__main__":
    register_skills()
    port = int(os.environ.get("PORT", 8000))
    # Standard MCP transport is stdio, but for multi-container we might want HTTP
    # Keeping default stdio but allowing HTTP if specified for container networking
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "http":
        mcp.run(transport="http", port=port)
    else:
        mcp.run()
