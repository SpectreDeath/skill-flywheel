import os
import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DiscoveryService")

# Registry path relative to container
REGISTRY_FILE = Path(os.environ.get("REGISTRY_FILE", "/app/skill_registry.json"))

# Defined port mapping for specialized domain services
DOMAIN_PORT_MAP = {
    "orchestration": 8001,
    "security": 8002,
    "data-ai": 8003,
    "devops": 8004,
    "engineering": 8005,
    "ux-mobile": 8006,
    "advanced": 8007,
    "strategy": 8008,
    "agent-rd": 8009
}

# Service grouping strategy
SERVICE_GROUPS = {
    "orchestration": ["orchestration", "skill_registry", "SKILL", "META_SKILL_DISCOVERY", "meta_agent_enhancement", "FLOW", "TEMPLATES", "agent_evolution"],
    "security": ["APPLICATION_SECURITY", "security_engineering", "skill_validation", "DEVSECOPS", "forensics", "osint_collector"],
    "data-ai": ["ML_AI", "DATA_ENGINEERING", "probabilistic_models", "epistemology", "AI_ETHICS"],
    "devops": ["DEVOPS", "CLOUD_ENGINEERING", "DATABASE_ENGINEERING", "MODERN_BACKEND_DEVELOPMENT", "mcp_tools", "EDGE_COMPUTING"],
    "engineering": ["SPECIFICATION_ENGINEERING", "formal_methods"],
    "ux-mobile": ["FRONTEND", "mobile_development"],
    "advanced": ["QUANTUM_COMPUTING", "WEB3", "ALGO_PATTERNS", "search_algorithms", "logic", "logic_programming"],
    "strategy": ["strategy_analysis", "epidemiology", "game_theory", "GAME_DEV"],
    "agent-rd": ["AI_AGENT_DEVELOPMENT", "generated_skills"]
}

def get_domain_service_map():
    """Dynamically generate the domain to service mapping."""
    mapping = {}
    for service, domains in SERVICE_GROUPS.items():
        port = DOMAIN_PORT_MAP.get(service, 8000)
        endpoint = f"mcp-{service}:{port}"
        for domain in domains:
            mapping[domain] = endpoint
            # Add common variations
            mapping[domain.lower()] = endpoint
            mapping[domain.capitalize()] = endpoint
            mapping[domain.replace('_', '-')] = endpoint
    return mapping

DOMAIN_SERVICE_MAP = get_domain_service_map()

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
