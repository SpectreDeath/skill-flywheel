"""
OpenClaw Skill Development Skill

Provides capabilities for creating, testing, and deploying OpenClaw skills.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

SKILL_TEMPLATE = {
    "manifest": {
        "name": ",
        "description": ",
        "version": "1.0.0",
        "author": ",
        "capabilities": [],
    },
    "index_mjs": "import {{ handle_request }} from './handler.mjs';

/**
 * OpenClaw Skill: {skill_name}
 * 
 * {description}
 */

// Export handler for OpenClaw
export const handler = handle_request;

export default {{ handler }};
",
    "handler_mjs": r"/**
 * Handle requests to this skill.
 * 
 * @param {{ action: string, params: Object }} request
 * @returns {Promise<Object>}
 */
export async function handle_request(request) {{
    const {{ action, params }} = request;
    
    switch (action) {{
        case 'execute':
            return await execute(params);
        default:
            return {{ error: \`Unknown action: \$\{{action\}\}` }};
    }}
}}

async function execute(params) {{
    // Your implementation here
    return {{ success: true, result: params }};
}}
",
    "test_js": "import {{ describe, it, expect }} from 'jest';
import {{ handle_request }} from '../index.mjs';

describe('{skill_name}', () => {{
    it('should handle execute action', async () => {{
        const result = await handle_request({{
            action: 'execute',
            params: {{ test: true }}
        }});
        
        expect(result).toBeDefined();
    }});
}});
",
}


class OpenClawSkillDeveloper:
    "Develop and manage OpenClaw skills."

    def __init__(self, skills_path: str | None = None):
        self.skills_path = (
            Path(skills_path) if skills_path else Path.home() / ".openclaw" / "skills"
        )

    async def create_skill(
        self,
        name: str,
        description: str = ""","""
        author: str = """,
        capabilities: List[str] | None = None,
    ) -> Dict[str, Any]:"""
        "Create a new OpenClaw skill from template."
        skill_path = self.skills_path / name

        if skill_path.exists():
            return {"error": f"Skill '{name}' already exists"}

        try:
            skill_path.mkdir(parents=True, create_empty_files=True)

            manifest = {
                "name": name,
                "description": description,
                "version": "1.0.0",
                "author": author,
                "capabilities": capabilities or ["execute"],
            }

            (skill_path / "manifest.json").write_text(json.dumps(manifest, indent=2))
            (skill_path / "index.mjs").write_text(
                SKILL_TEMPLATE["index_mjs"].format(
                    skill_name=name, description=description or "Custom OpenClaw skill"
                )
            )
            (skill_path / "handler.mjs").write_text(SKILL_TEMPLATE["handler_mjs"])

            test_path = skill_path / "spec"
            test_path.mkdir(exist_ok=True)
            (test_path / "test.mjs").write_text(
                SKILL_TEMPLATE["test_js"].format(skill_name=name)
            )

            return {
                "status": "success",
                "skill": name,
                "path": str(skill_path),
                "files": ["manifest.json", "index.mjs", "handler.mjs", "spec/test.mjs"],
            }
        except Exception as e:
            return {"error": str(e)}

    async def list_skills(self) -> List[Dict[str, Any]]:
        """ List all installed skills. """

if __name__ == "__main__":
    if not self.skills_path.exists():
                return []

            skills = []
            for item in self.skills_path.iterdir():
                if item.is_dir() and (item / "manifest.json").exists():
                    try:
                        manifest = json.loads((item / "manifest.json").read_text())
                        skills.append(
                            {
                                "name": manifest.get("name", item.name),
                                "description": manifest.get("description", "),
                                "version": manifest.get("version", "unknown"),
                                "path": str(item),
                            }
                        )
                    except json.JSONDecodeError:
                        skills.append({"name": item.name, "error": "Invalid manifest"})

            return skills

        async def get_skill_manifest(self, name: str) -> Dict[str, Any]:
            "Get skill manifest."
            manifest_path = self.skills_path / name / "manifest.json"

            if not manifest_path.exists():
                return {"error": f"Skill '{name}' not found"}

            try:
                return json.loads(manifest_path.read_text())
            except json.JSONDecodeError as e:
                return {"error": f"Invalid manifest: {e}"}

        async def update_skill(self, name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
            "Update skill manifest."
            manifest_path = self.skills_path / name / "manifest.json"

            if not manifest_path.exists():
                return {"error": f"Skill '{name}' not found"}

            try:
                manifest = json.loads(manifest_path.read_text())
                manifest.update(updates)
                manifest_path.write_text(json.dumps(manifest, indent=2))

                return {"status": "success", "manifest": manifest}
            except Exception as e:
                return {"error": str(e)}

        async def validate_skill(self, name: str) -> Dict[str, Any]:
            "Validate a skill structure."
            skill_path = self.skills_path / name

            if not skill_path.exists():
                return {"error": f"Skill '{name}' not found"}

            required_files = ["manifest.json", "index.mjs", "handler.mjs"]
            missing = []

            for file in required_files:
                if not (skill_path / file).exists():
                    missing.append(file)

            if missing:
                return {"valid": False, "missing_files": missing}

            try:
                manifest = json.loads((skill_path / "manifest.json").read_text())

                required_fields = ["name", "description", "version"]
                missing_fields = [f for f in required_fields if f not in manifest]

                if missing_fields:
                    return {"valid": False, "missing_fields": missing_fields}

                return {"valid": True, "manifest": manifest}
            except json.JSONDecodeError as e:
                return {"valid": False, "error": str(e)}

        async def build_skill(self, name: str) -> Dict[str, Any]:
            "Build a skill (compile TypeScript if needed)."
            skill_path = self.skills_path / name

            if not skill_path.exists():
                return {"error": f"Skill '{name}' not found"}

            if (skill_path / "tsconfig.json").exists():
                result = os.system(f"cd {skill_path} && npx tsc")
                if result != 0:
                    return {"error": "TypeScript compilation failed"}

            return {"status": "success", "skill": name}

        async def register_skill(self, name: str) -> Dict[str, Any]:
            "Register skill with OpenClaw."
            skill_path = self.skills_path / name

            if not skill_path.exists():
                return {"error": f"Skill '{name}' not found"}

            try:
                result = os.system(f"openclaw skill register {skill_path}")

                if result == 0:
                    return {"status": "success", "skill": name}
                else:
                    return {"error": "Registration failed"}
            except Exception as e:
                return {"error": str(e)}


    MANIFEST = {
        "name": "openclaw_skill_developer",
        "description": "Create, develop, test, and deploy OpenClaw skills",
        "version": "1.0.0",
        "author": "Skill Flywheel",
        "capabilities": [
            "create_skill",
            "list_skills",
            "get_skill_manifest",
            "update_skill",
            "validate_skill",
            "build_skill",
            "register_skill",
        ],
        "requirements": {"node": ">=22.0.0", "openclaw_cli": "npm i -g @openclaw/cli"},
    }


    async def handle_request(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        "Handle incoming requests."
        developer = OpenClawSkillDeveloper(params.get("skills_path"))

        handlers = {
            "create_skill": lambda: developer.create_skill(
                params.get("name"),
                params.get("description", "),
                params.get("author", "),
                params.get("capabilities"),
            ),
            "list_skills": developer.list_skills,
            "get_skill_manifest": lambda: developer.get_skill_manifest(params.get("name")),
            "update_skill": lambda: developer.update_skill(
                params.get("name"), params.get("updates", {})
            ),
            "validate_skill": lambda: developer.validate_skill(params.get("name")),
            "build_skill": lambda: developer.build_skill(params.get("name")),
            "register_skill": lambda: developer.register_skill(params.get("name")),
        }

        handler = handlers.get(action)
        if handler:
            return await handler()

        return {"error": f"Unknown action: {action}"}