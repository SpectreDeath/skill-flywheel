import json
import os
import sqlite3
import uuid


def main():
    registry_file = r"d:\Skill Flywheel\data\skill_registry.json"
    db_file = r"d:\Skill Flywheel\data\skill_registry.db"
    sql_schema = r"d:\Skill Flywheel\data\skill_registry.sql"
    backlog_file = r"d:\Skill Flywheel\data\skills_backlog.json"
    
    # Initialize DB
    if os.path.exists(db_file):
        os.remove(db_file)
        
    conn = sqlite3.connect(db_file)
    with open(sql_schema) as f:
        conn.executescript(f.read())
        
    # Read registry
    with open(registry_file, encoding='utf-8') as f:
        skills_data = json.load(f)
        
    # Existing python modules
    existing_modules = {
        "api_integration": {
            "module_path": "src.skills.api_integration",
            "entry_function": "batch_api_calls",
            "endpoints": [
                {"route": "/skills/api_integration/batch_api_calls", "method": "POST", "desc": "Batch API calls"},
                {"route": "/skills/api_integration/transform_data", "method": "POST", "desc": "Transform data"},
                {"route": "/skills/api_integration/health_check", "method": "POST", "desc": "Health check"}
            ]
        },
        "context_hub_provider": {
            "module_path": "src.skills.context_hub_provider",
            "entry_function": "search",
            "endpoints": [
                {"route": "/skills/context_hub_provider/search", "method": "POST", "desc": "Search documentation"},
                {"route": "/skills/context_hub_provider/get_doc", "method": "POST", "desc": "Get document"},
                {"route": "/skills/context_hub_provider/annotate", "method": "POST", "desc": "Annotate document"},
                {"route": "/skills/context_hub_provider/clear_annotation", "method": "POST", "desc": "Clear annotation"}
            ]
        },
        "data_analyzer": {
            "module_path": "src.skills.data_analyzer",
            "entry_function": "analyze_dataset",
            "endpoints": [
                {"route": "/skills/data_analyzer/analyze_dataset", "method": "POST", "desc": "Analyze dataset"},
                {"route": "/skills/data_analyzer/clean_data", "method": "POST", "desc": "Clean data"},
                {"route": "/skills/data_analyzer/generate_insights", "method": "POST", "desc": "Generate insights"}
            ]
        }
    }
    
    implemented_skills = []
    backlog = []
    
    # Track which modules were explicitly found in the JSON
    found_in_json = set()
    
    for s in skills_data:
        # Convert snake_case or kebab-case
        name = s.get("name", "")
        # normalize
        normalized_name = name.replace("-", "_").lower()
        
        if normalized_name in existing_modules:
            implemented_skills.append((s, existing_modules[normalized_name], normalized_name))
            found_in_json.add(normalized_name)
        else:
            # Backlog
            backlog.append({
                "skill_id": str(uuid.uuid4()),
                "name": name,
                "domain": s.get("domain", "unknown"),
                "source_doc": s.get("path", ""),
                "status": "NOT_IMPLEMENTED"
            })
            
    # Print the missing modules in the console/log output per Phase 1 instructions
    for back_skill in backlog:
        print(f"⚠️ NO MODULE FOUND: {back_skill['name']} — needs to be written or mapped")
        
    # If the JSON didn't include some of the python files, let's add them manually
    for name, config in existing_modules.items():
        if name not in found_in_json:
            implemented_skills.append(({
                "name": name,
                "domain": "core",
                "version": "1.0.0",
                "description": f"Core skill: {name}",
                "dependencies": []
            }, config, name))
            
    # Insert implemented skills
    for s, config, name in implemented_skills:
        skill_id = str(uuid.uuid4())
        
        # INSERT into skills
        conn.execute('''
            INSERT INTO skills (skill_id, name, domain, module_path, entry_function, version, description, dependencies, health_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            skill_id,
            s.get("name", name),
            s.get("domain", "core"),
            config["module_path"],
            config["entry_function"],
            s.get("version", "1.0.0"),
            s.get("description", ""),
            json.dumps(s.get("dependencies", [])),
            "healthy"
        ))
        
        # INSERT endpoints
        for ep in config["endpoints"]:
            conn.execute('''
                INSERT INTO skill_endpoints (endpoint_id, skill_id, route, method, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                skill_id,
                ep["route"],
                ep["method"],
                ep["desc"]
            ))
            
    conn.commit()
    conn.close()
    
    # write backlog
    with open(backlog_file, 'w') as f:
        json.dump(backlog, f, indent=2)
        
    print(f"\nPopulated database with {len(implemented_skills)} implemented skills.")
    print(f"Generated backlog with {len(backlog)} missing skills.")

if __name__ == '__main__':
    main()
