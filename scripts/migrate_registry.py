import json
import os
import sqlite3
import uuid
from pathlib import Path


def discover_python_modules(skills_root: Path) -> dict:
    """
    Scans the skills directory recursively for Python modules.
    Returns a dict mapping normalized name to module configuration.
    """
    modules = {}
    if not skills_root.exists():
        print(f"⚠️ Skills directory not found: {skills_root}")
        return modules

    for path in skills_root.rglob("*.py"):
        if path.name == "__init__.py" or "__pycache__" in str(path):
            continue

        # Normalized name (lowercase,_ instead of -)
        skill_name = path.stem.lower().replace("-", "_")
        
        # Calculate module path (relative to src/)
        # Example: D:\Skill Flywheel\src\flywheel\skills\web3\smart_contract_audit.py
        # relative to D:\Skill Flywheel\src -> flywheel.skills.web3.smart_contract_audit
        try:
            rel_path = path.relative_to(skills_root.parent.parent) # src level
            module_parts = rel_path.with_suffix("").parts
            module_path = ".".join(module_parts)
            
            modules[skill_name] = {
                "module_path": module_path,
                "entry_function": path.stem, # default to file stem
                "endpoints": [
                    {"route": f"/skills/{skill_name}/{path.stem}", "method": "POST", "desc": f"Execute {path.stem}"}
                ]
            }
        except Exception as e:
            print(f"⚠️ Error mapping module for {path}: {e}")

    return modules


def main():
    root_dir = Path(__file__).parent.parent
    registry_file = root_dir / "data" / "skill_registry.json"
    db_file = root_dir / "data" / "skill_registry.db"
    sql_schema = root_dir / "data" / "skill_registry.sql"
    backlog_file = root_dir / "data" / "skills_backlog.json"
    skills_root = root_dir / "src" / "flywheel" / "skills"
    
    print(f"🚀 Starting registry migration from {root_dir}")
    
    # Discovery
    existing_modules = discover_python_modules(skills_root)
    print(f"🔍 Discovered {len(existing_modules)} Python skill modules.")
    
    # Initialize DB
    if db_file.exists():
        os.remove(db_file)
        
    conn = sqlite3.connect(str(db_file))
    with open(sql_schema) as f:
        conn.executescript(f.read())
        
    # Read registry
    if not registry_file.exists():
        print(f"❌ Registry file not found: {registry_file}")
        return
        
    with open(registry_file, encoding='utf-8') as f:
        skills_data = json.load(f)
        
    implemented_skills = []
    backlog = []
    
    # Track which modules were explicitly found in the JSON
    found_in_json = set()
    
    for s in skills_data:
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
            
    # Add mapped modules that might not be in the JSON
    for name, config in existing_modules.items():
        if name not in found_in_json:
            implemented_skills.append(({
                "name": name,
                "domain": "discovered",
                "version": "1.0.0",
                "description": f"Auto-discovered skill: {name}",
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
            s.get("domain", "core") if name in found_in_json else "discovered",
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
            
        # Add to backlog as IMPLEMENTED
        backlog.append({
            "skill_id": skill_id,
            "name": s.get("name", name),
            "domain": s.get("domain", "core"),
            "source_doc": s.get("path", ""),
            "status": "IMPLEMENTED"
        })
            
    conn.commit()
    conn.close()
    
    # write backlog
    with open(backlog_file, 'w') as f:
        json.dump(backlog, f, indent=2)
        
    print(f"\n✅ Migration Complete:")
    print(f"   - Implemented skills: {len(implemented_skills)}")
    print(f"   - Backlog skills (NOT_IMPLEMENTED): {len([b for b in backlog if b['status'] == 'NOT_IMPLEMENTED'])}")
    print(f"   - Backlog skills (IMPLEMENTED): {len([b for b in backlog if b['status'] == 'IMPLEMENTED'])}")
    print(f"   - Total registry entries: {len(backlog)}")


if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
