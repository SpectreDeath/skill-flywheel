"""
Library Skill Generator

Generates skill modules that wrap Python library public APIs.
This enables dynamic skill creation based on any Python library.
"""

import datetime as dt
import importlib
import inspect
import json
import logging
import os
import sqlite3
import sys
import time
import uuid
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(CURRENT_DIR, "..", "..", "..", ".."))
SKILLS_ROOT = os.path.join(PROJECT_ROOT, "src", "flywheel", "skills")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

REGISTRY_DB_PATH = os.path.join(DATA_DIR, "skill_registry.db")
BACKLOG_PATH = os.path.join(DATA_DIR, "skills_backlog.json")


def get_library_version(library_module: Any) -> str | None:
    """Get library version if available"""
    version = None
    if hasattr(library_module, "__version__"):
        version = library_module.__version__
    elif hasattr(library_module, "version"):
        version = library_module.version
    return version


RESERVED_NAMES = {"invoke", "register_skill"}


def get_public_api(library_module: Any) -> List[tuple]:
    """
    Get public API members from a library module.

    Returns list of (name, member) tuples for public functions and classes.
    Excludes:
        - Names starting with underscore
        - Names containing "wrapper" (to avoid recursive wrapping)
        - Reserved names like invoke, register_skill
        - Names that don't actually exist as module attributes
    """
    public_members = []
    module_name = library_module.__name__

    for name, member in inspect.getmembers(library_module):
        if name.startswith("_"):
            continue
        if "wrapper" in name.lower():
            continue
        if name in RESERVED_NAMES:
            continue

        if not hasattr(library_module, name):
            continue

        if not callable(member):
            continue
        if inspect.isfunction(member) or inspect.isclass(member):
            public_members.append((name, member))
    return public_members


def generate_skill_code(
    library_name: str,
    public_names: List[str],
    domain: str,
    library_version: str | None = None,
) -> str:
    """
    Generate skill module code using .format() (not f-strings).

    Args:
        library_name: Name of the Python library
        public_names: List of public function/class names to wrap
        domain: Target skill domain
        library_version: Optional library version

    Returns:
        Generated skill module code as string
    """
    wrapped_names_json = json.dumps(public_names)

    wrapper_functions = []
    for name in public_names:
        wrapper_code = '''async def {name}_wrapper(args: list, kwargs: dict):
    """
    Wrapper for {library_name}.{name}
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import {library_name}
        member = getattr({library_name}, "{name}")
        if inspect.isclass(member):
            return member(*args, **kwargs)
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {{"error": str(e)}}
'''.format(library_name=library_name, name=name)
        wrapper_functions.append(wrapper_code)

    wrapper_dispatch = []
    for name in public_names:
        wrapper_dispatch.append('        "{}": {}_wrapper,'.format(name, name))
    wrapper_dispatch_str = "\n".join(wrapper_dispatch)

    skill_code = '''"""
Auto-generated skill for {library_name}

This skill wraps the public API of the {library_name} library.
Generated on: {timestamp}
Library version: {library_version}

Wrapped components: {wrapped_count}
"""
import inspect
import logging
from typing import Any, Dict, List

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WRAPPED_NAMES = {wrapped_names_json}

{wrapper_functions}
async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for skill invocation.
    
    Expected payload:
        - action: str (optional): Name of wrapper to call. If omitted, returns list of available wrappers
        - args: list (optional): Positional arguments for the wrapper
        - kwargs: dict (optional): Keyword arguments for the wrapper
    
    Returns:
        dict with 'result' and 'metadata' keys
    """
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action")
    args = payload.get("args", [])
    kwargs = payload.get("kwargs", {{}})
    
    if action is None:
        return {{
            "result": {{
                "available_wrappers": list(WRAPPED_NAMES),
                "message": "Available wrappers. Use action parameter to call a specific wrapper."
            }},
            "metadata": {{
                "timestamp": timestamp,
                "library": "{library_name}",
                "function_count": len(WRAPPED_NAMES)
            }}
        }}
    
    if action not in WRAPPED_NAMES:
        return {{
            "result": {{"error": "Unknown action: " + action}},
            "metadata": {{
                "timestamp": timestamp,
                "error": "Action not found in wrapped names"
            }}
        }}
    
    wrappers = {{
{wrapper_dispatch_str}
    }}
    
    try:
        result = await wrappers[action](args, kwargs)
        elapsed = time.time() - start_time
        
        return {{
            "result": result,
            "metadata": {{
                "timestamp": timestamp,
                "library": "{library_name}",
                "library_version": "{library_version}" if "{library_version}" != "None" else None,
                "action": action,
                "elapsed_seconds": elapsed
            }}
        }}
    except Exception as e:
        logger.error("Error invoking {{}}: {{}}".format(action, str(e)))
        return {{
            "result": {{"error": str(e)}},
            "metadata": {{
                "timestamp": timestamp,
                "library": "{library_name}",
                "error": str(e)
            }}
        }}


def register_skill():
    """Return skill metadata for registration"""
    return {{
        "name": "{library_name}-wrapper",
        "description": "Auto-generated skill wrapping {library_name} public API",
        "domain": "{domain}",
        "version": "1.0.0",
    }}
'''.format(
        library_name=library_name,
        timestamp=dt.datetime.now().isoformat(),
        library_version=library_version if library_version else "unknown",
        wrapped_count=len(public_names),
        wrapped_names_json=wrapped_names_json,
        wrapper_functions="\n".join(wrapper_functions),
        wrapper_dispatch_str=wrapper_dispatch_str,
        domain=domain,
    )

    return skill_code


def save_skill_module(
    domain: str, library_name: str, code: str, overwrite: bool = False
) -> str:
    """
    Save the generated skill module to disk.

    Args:
        domain: Target domain (e.g., 'skill_management')
        library_name: Name of the library
        code: Generated Python code
        overwrite: Whether to overwrite existing file

    Returns:
        Path to saved file

    Raises:
        FileExistsError: If file exists and overwrite is False
    """
    domain_path = os.path.join(SKILLS_ROOT, domain)
    os.makedirs(domain_path, exist_ok=True)

    file_path = os.path.join(domain_path, "{}.py".format(library_name))

    if os.path.exists(file_path) and not overwrite:
        raise FileExistsError("Skill file already exists: {}".format(file_path))

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    logger.info("Saved skill module to: {}".format(file_path))
    return file_path


def verify_module_import(file_path: str) -> bool:
    """
    Verify that the generated module can be imported cleanly.

    Args:
        file_path: Path to the generated module

    Returns:
        True if import succeeds

    Raises:
        Exception: If import fails
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location("generated_skill", file_path)
    if spec is None or spec.loader is None:
        raise Exception("Failed to create module spec")

    module = importlib.util.module_from_spec(spec)

    sys_modules_backup = sys.modules.copy()
    try:
        spec.loader.exec_module(module)

        if not hasattr(module, "invoke"):
            raise Exception("Module missing invoke function")

        if not callable(module.invoke):
            raise Exception("invoke is not callable")

        logger.info("Module imported successfully")
        return True
    finally:
        sys.modules.clear()
        sys.modules.update(sys_modules_backup)


def register_skill_in_db(
    domain: str,
    library_name: str,
    module_path: str,
    skill_id: str | None = None,
    version: str | None = None,
    description: str | None = None,
) -> str:
    """
    Register the skill in the skill registry database.

    Args:
        domain: Target domain
        library_name: Library name
        module_path: Path to the generated module
        skill_id: Optional skill ID override
        version: Optional version string
        description: Optional description

    Returns:
        The skill_id used for registration
    """
    if skill_id is None:
        skill_id = str(uuid.uuid4())

    if version is None:
        version = "1.0.0"

    if description is None:
        description = "Auto-generated skill wrapping {} public API".format(library_name)

    conn = sqlite3.connect(REGISTRY_DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO skills (skill_id, name, domain, module_path, entry_function, version, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                skill_id,
                "{}-wrapper".format(library_name),
                domain,
                module_path,
                "invoke",
                version,
                description,
            ),
        )
        conn.commit()
        logger.info("Registered skill with ID: {}".format(skill_id))
    except sqlite3.IntegrityError:
        logger.warning("Skill already exists, updating...")
        cursor.execute(
            """
            UPDATE skills 
            SET name = ?, domain = ?, module_path = ?, entry_function = ?, version = ?, description = ?
            WHERE skill_id = ?
        """,
            (
                "{}-wrapper".format(library_name),
                domain,
                module_path,
                "invoke",
                version,
                description,
                skill_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()

    return skill_id


def find_related_skills_in_backlog(library_name: str, domain: str) -> List[Dict]:
    """
    Find related skills in the backlog that should be marked as IMPLEMENTED.

    Related skills are determined by:
    1. Skills in the same domain with names containing the library name
    2. Skills that reference the library name in their name

    Args:
        library_name: The library name
        domain: The target domain

    Returns:
        List of related backlog entries
    """
    if not os.path.exists(BACKLOG_PATH):
        return []

    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)

    library_lower = library_name.lower()
    related = []

    for entry in backlog:
        name = entry.get("name", "").lower()
        entry_domain = entry.get("domain", "").lower()

        is_related = (entry_domain == domain.lower() and library_lower in name) or (
            library_lower in name
        )

        if is_related and entry.get("status") != "IMPLEMENTED":
            related.append(entry)

    return related


def update_backlog_status(skill_entries: List[Dict]) -> bool:
    """
    Update the backlog to mark related skills as IMPLEMENTED.

    Args:
        skill_entries: List of backlog entries to update

    Returns:
        True if update was successful
    """
    if not skill_entries:
        logger.info("No related skills found in backlog")
        return True

    if not os.path.exists(BACKLOG_PATH):
        logger.warning("Backlog file not found: {}".format(BACKLOG_PATH))
        return False

    with open(BACKLOG_PATH, "r", encoding="utf-8") as f:
        backlog = json.load(f)

    today = dt.datetime.now().strftime("%Y-%m-%d")
    updated_count = 0

    for entry in backlog:
        for skill_entry in skill_entries:
            if entry.get("skill_id") == skill_entry.get("skill_id"):
                entry["status"] = "IMPLEMENTED"
                entry["implemented_at"] = today
                updated_count += 1

    if updated_count > 0:
        with open(BACKLOG_PATH, "w", encoding="utf-8") as f:
            json.dump(backlog, f, indent=2)
        logger.info("Updated {} skills in backlog".format(updated_count))

    return True


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a new skill module by wrapping a Python library's public API.

    Expected payload keys:
        - library: str — Python library to generate a skill for (e.g., "polars", "sklearn")
        - domain: str — target skill domain (e.g., "skill_management")
        - skill_id: str (optional) — override generated skill_id
        - focus: list (optional) — explicit list of public components to include
        - overwrite: bool (optional) — whether to overwrite existing file (default: False)

    Returns:
        dict with:
        - result: dict containing generated_path, registered_id, functions_wrapped
        - metadata: dict containing timestamp, library_version, function_count
    """
    timestamp = dt.datetime.now().isoformat()

    library = payload.get("library")
    domain = payload.get("domain")
    skill_id_override = payload.get("skill_id")
    focus = payload.get("focus")
    overwrite = payload.get("overwrite", False)

    if not library:
        return {
            "result": {"error": "Missing required parameter: library"},
            "metadata": {
                "timestamp": timestamp,
                "error": "library parameter is required",
            },
        }

    if not domain:
        return {
            "result": {"error": "Missing required parameter: domain"},
            "metadata": {
                "timestamp": timestamp,
                "error": "domain parameter is required",
            },
        }

    logger.info("Generating skill for library: {}, domain: {}".format(library, domain))

    library_module = None
    try:
        skill_path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)))

        if library in sys.modules:
            del sys.modules[library]

        path_backup = sys.path.copy()

        def is_skill_path(p):
            p_norm = os.path.normpath(p)
            return (
                p_norm == skill_path
                or p_norm.startswith(skill_path + os.sep)
                or p_norm.startswith(skill_path + "/")
            )

        filtered = [p for p in sys.path if is_skill_path(p)]
        logger.info("Paths to filter: {}".format(filtered))

        sys.path[:] = [p for p in sys.path if not is_skill_path(p)]

        logger.info(
            "Filtered sys.path. Original: {}, New: {}".format(
                len(path_backup), len(sys.path)
            )
        )

        try:
            library_module = importlib.import_module(library)
        finally:
            sys.path[:] = path_backup
    except ImportError as e:
        return {
            "result": {"error": "Library not installed: {}".format(library)},
            "metadata": {
                "timestamp": timestamp,
                "error": "ImportError: {}".format(str(e)),
            },
        }

    library_version = get_library_version(library_module)
    logger.info("Library version: {}".format(library_version))

    logger.info("Library module file: {}".format(library_module.__file__))

    public_members = get_public_api(library_module)
    public_names = [name for name, _ in public_members]

    logger.info("Found {} public API members".format(len(public_names)))

    if focus:
        missing = [name for name in focus if name not in public_names]
        if missing:
            return {
                "result": {"error": "Focus contains invalid names: {}".format(missing)},
                "metadata": {
                    "timestamp": timestamp,
                    "error": "Invalid names in focus",
                    "valid_names": public_names,
                },
            }
        public_names = focus
        logger.info("Restricted to focus items: {}".format(public_names))

    if not public_names:
        return {
            "result": {"error": "Library has no public API after filtering"},
            "metadata": {
                "timestamp": timestamp,
                "library_version": library_version,
                "function_count": 0,
            },
        }

    generated_path = None
    try:
        code = generate_skill_code(library, public_names, domain, library_version)
        generated_path = save_skill_module(domain, library, code, overwrite)
        logger.info("Saved to: {}".format(generated_path))
    except FileExistsError:
        return {
            "result": {
                "message": "Skill file already exists, skipping generation",
                "generated_path": os.path.join(
                    SKILLS_ROOT,
                    domain,
                    "{}.py".format(library),
                ),
                "functions_wrapped": public_names,
            },
            "metadata": {
                "timestamp": timestamp,
                "library_version": library_version,
                "function_count": len(public_names),
                "skipped": True,
            },
        }

    try:
        verify_module_import(generated_path)
    except Exception as e:
        if generated_path and os.path.exists(generated_path):
            os.remove(generated_path)
        return {
            "result": {"error": "Generated module failed to import: {}".format(str(e))},
            "metadata": {"timestamp": timestamp, "error": "Import verification failed"},
        }

    registered_id = register_skill_in_db(
        domain=domain,
        library_name=library,
        module_path=generated_path,
        skill_id=skill_id_override,
        version=library_version,
    )

    related_skills = find_related_skills_in_backlog(library, domain)
    if related_skills:
        update_backlog_status(related_skills)

    return {
        "result": {
            "generated_path": generated_path,
            "registered_id": registered_id,
            "functions_wrapped": public_names,
        },
        "metadata": {
            "timestamp": timestamp,
            "library_version": library_version,
            "function_count": len(public_names),
        },
    }


def register_skill():
    """Return skill metadata for registration"""

if __name__ == "__main__":
    return {
            "name": "library-skill-generator",
            "description": "Generate skill modules by wrapping Python library public APIs",
            "version": "1.0.0",
            "domain": "skill_management",
        }