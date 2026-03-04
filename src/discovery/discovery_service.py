import os
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DiscoveryService")

# Registry path relative to container
REGISTRY_FILE = Path(os.environ.get("REGISTRY_FILE", "/app/skill_registry.json"))

# Defined domain to service mapping (from docker-compose names)
# Note: These names must match the service names in docker-compose.yml
DOMAIN_SERVICE_MAP = {
    # Orchestration & Meta
    "orchestration": "mcp-orchestration:8001",
    "Orchestration": "mcp-orchestration:8001",
    "skill_registry": "mcp-orchestration:8001",
    "Skill_Registry": "mcp-orchestration:8001",
    "SKILL": "mcp-orchestration:8001",
    "META_SKILL_DISCOVERY": "mcp-orchestration:8001",
    "Meta_Skill_Discovery": "mcp-orchestration:8001",
    "meta_agent_enhancement": "mcp-orchestration:8001",
    "FLOW": "mcp-orchestration:8001",
    "TEMPLATES": "mcp-orchestration:8001",
    "agent_evolution": "mcp-orchestration:8001",
    "Agent_Evolution": "mcp-orchestration:8001",
    
    # Security
    "APPLICATION_SECURITY": "mcp-security:8002",
    "Application_Security": "mcp-security:8002",
    "security_engineering": "mcp-security:8002",
    "Security_Engineering": "mcp-security:8002",
    "skill_validation": "mcp-security:8002",
    "Skill_Validation": "mcp-security:8002",
    "DEVSECOPS": "mcp-security:8002",
    "forensics": "mcp-security:8002",
    "Forensics": "mcp-security:8002",
    "osint_collector": "mcp-security:8002",
    "Osint_Collector": "mcp-security:8002",
    
    # Data & AI
    "ML_AI": "mcp-data-ai:8003",
    "DATA_ENGINEERING": "mcp-data-ai:8003",
    "Data_Engineering": "mcp-data-ai:8003",
    "probabilistic_models": "mcp-data-ai:8003",
    "Probabilistic_Models": "mcp-data-ai:8003",
    "epistemology": "mcp-data-ai:8003",
    "AI_ETHICS": "mcp-data-ai:8003",
    "Ai_Ethics": "mcp-data-ai:8003",
    
    # DevOps & Infrastructure
    "DEVOPS": "mcp-devops:8004",
    "Devops": "mcp-devops:8004",
    "CLOUD_ENGINEERING": "mcp-devops:8004",
    "Cloud_Engineering": "mcp-devops:8004",
    "DATABASE_ENGINEERING": "mcp-devops:8004",
    "Database_Engineering": "mcp-devops:8004",
    "MODERN_BACKEND_DEVELOPMENT": "mcp-devops:8004",
    "Modern_Backend_Development": "mcp-devops:8004",
    "mcp_tools": "mcp-devops:8004",
    "EDGE_COMPUTING": "mcp-devops:8004",
    "Edge_Computing": "mcp-devops:8004",
    
    # Engineering
    "SPECIFICATION_ENGINEERING": "mcp-engineering:8005",
    "Specification_Engineering": "mcp-engineering:8005",
    "formal_methods": "mcp-engineering:8005",
    
    # UI/Mobile
    "FRONTEND": "mcp-ux-mobile:8006",
    "Frontend": "mcp-ux-mobile:8006",
    "mobile_development": "mcp-ux-mobile:8006",
    "Mobile_Development": "mcp-ux-mobile:8006",
    
    # Advanced
    "QUANTUM_COMPUTING": "mcp-advanced:8007",
    "WEB3": "mcp-advanced:8007",
    "Web3": "mcp-advanced:8007",
    "ALGO_PATTERNS": "mcp-advanced:8007",
    "search_algorithms": "mcp-advanced:8007",
    "Search_Algorithms": "mcp-advanced:8007",
    "logic": "mcp-advanced:8007",
    "Logic": "mcp-advanced:8007",
    "logic_programming": "mcp-advanced:8007",
    
    # Strategy
    "strategy_analysis": "mcp-strategy:8008",
    "Strategy_Analysis": "mcp-strategy:8008",
    "epidemiology": "mcp-strategy:8008",
    "Epidemiology": "mcp-strategy:8008",
    "game_theory": "mcp-strategy:8008",
    "Game_Theory": "mcp-strategy:8008",
    "GAME_DEV": "mcp-strategy:8008",
    
    # Agent R&D
    "AI_AGENT_DEVELOPMENT": "mcp-agent-rd:8009",
    "Ai_Agent_Development": "mcp-agent-rd:8009",
    "generated_skills": "mcp-agent-rd:8009"
}

@mcp.tool()
async def list_available_services():
    """Returns a list of all domain MCP endpoints and their internal network addresses."""
    # Group by service for a cleaner view
    services = {}
    for domain, endpoint in DOMAIN_SERVICE_MAP.items():
        service_name = endpoint.split(':')[0]
        if service_name not in services:
            services[service_name] = {"endpoint": endpoint, "domains": []}
        services[service_name]["domains"].append(domain)
    
    return [
        {
            "service": name,
            "internal_endpoint": data["endpoint"],
            "external_endpoint": f"http://localhost:{data['endpoint'].split(':')[1]}",
            "domains": data["domains"]
        } for name, data in services.items()
    ]

@mcp.tool()
async def find_domain_for_skill(skill_name: str):
    """Identifies which domain server hosts a specific skill by querying the registry."""
    if not REGISTRY_FILE.exists():
        return f"Error: Registry file not found at {REGISTRY_FILE}"
    
    try:
        # Standardize query format (lowercase, hyphens)
        query = skill_name.lower().replace('_', '-')
        with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
            registry = json.load(f)
            
        for skill in registry:
            if skill['name'].lower() == query or skill['name'].lower().replace('_', '-') == query:
                domain = skill.get('domain')
                endpoint = DOMAIN_SERVICE_MAP.get(domain)
                
                # Fallback for sub-domains or inconsistent casing in registry
                if not endpoint:
                    # Check if the domain is a sub-key (e.g., 'skill_validation' mapping to 'security')
                    endpoint = DOMAIN_SERVICE_MAP.get(domain.upper())
                
                if endpoint:
                    return {
                        "skill": skill['name'],
                        "domain": domain,
                        "service": endpoint.split(':')[0],
                        "internal_endpoint": f"http://{endpoint}",
                        "external_endpoint": f"http://localhost:{endpoint.split(':')[1]}"
                    }
                return f"Skill '{skill_name}' found in domain '{domain}', but no service is mapped for this domain."
                
        return f"Skill '{skill_name}' not found in the registry."
    except Exception as e:
        return f"Error querying registry: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # Discovery service always runs in HTTP mode for container internal access
    mcp.run(transport="http", port=port)
