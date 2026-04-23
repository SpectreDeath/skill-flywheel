"""
Mock Generator

Creates mock objects for testing by:
- Analyzing class/function interfaces
- Generating MagicMock-based mock classes
- Handling recursive dependency mocking
- Configuring return values for common patterns
- Outputting ready-to-use test code
"""

import ast
from dataclasses import dataclass
from typing import Any, Dict, List, Set
from datetime import datetime


@dataclass
class MethodSignature:
    name: str
    args: List[str]
    kwargs: List[str]
    return_annotation: str | None
    is_async: bool = False


@dataclass
class ClassInfo:
    name: str
    bases: List[str]
    methods: List[MethodSignature]
    attributes: List[str]
    decorators: List[str]


def parse_class(code: str, target: str) -> ClassInfo | None:
    """Parse Python code to extract class information."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == target:
            methods = []
            attributes = []
            decorators = [
                d.id if isinstance(d, ast.Name) else ast.unparse(d)
                for d in node.decorator_list
            ]

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    args = [arg.arg for arg in item.args.args if arg.arg != "self"]
                    kwargs = [arg.arg for arg in item.args.kwonlyargs]
                    return_annotation = (
                        ast.unparse(item.returns) if item.returns else None
                    )

                    methods.append(
                        MethodSignature(
                            name=item.name,
                            args=args,
                            kwargs=kwargs,
                            return_annotation=return_annotation,
                            is_async=isinstance(item, ast.AsyncFunctionDef),
                        )
                    )
                elif isinstance(item, ast.AnnAssign):
                    if isinstance(item.target, ast.Name):
                        attributes.append(item.target.id)

            return ClassInfo(
                name=node.name,
                bases=[ast.unparse(base) for base in node.bases],
                methods=methods,
                attributes=attributes,
                decorators=decorators,
            )

    return None


def parse_function(code: str, target: str) -> MethodSignature | None:
    """Parse Python code to extract function signature."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == target
        ):
            args = [arg.arg for arg in node.args.args if arg.arg != "self"]
            kwargs = [arg.arg for arg in node.args.kwonlyargs]
            return_annotation = ast.unparse(node.returns) if node.returns else None

            return MethodSignature(
                name=node.name,
                args=args,
                kwargs=kwargs,
                return_annotation=return_annotation,
                is_async=isinstance(node, ast.AsyncFunctionDef),
            )

    return None


def extract_dependencies(code: str, target: str) -> Set[str]:
    """Extract dependencies (imports and types) used by the target class/function."""
    dependencies = set()

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return dependencies

    target_node = None

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == target or (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == target
        ):
            target_node = node
            break

    if not target_node:
        return dependencies

    for node in ast.walk(target_node):
        if isinstance(node, ast.Name):
            if node.id[0].isupper():
                dependencies.add(node.id)
        elif isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id[0].isupper():
                dependencies.add(node.value.id)

    return dependencies


def generate_mock_class(class_info: ClassInfo, framework: str = "unittest.mock") -> str:
    """Generate a MagicMock-based mock class."""
    mock_type = "MagicMock" if framework == "unittest.mock" else "Mock"

    lines = [f"class {class_info.name}Mock({mock_type}):"]
    lines.append(f'    """Auto-generated mock for {class_info.name}"""')
    lines.append("")
    lines.append("    def __init__(self, *args, **kwargs):")
    lines.append("        super().__init__(*args, **kwargs)")
    lines.append("        self._mock_configs = {}")
    lines.append("")

    for method in class_info.methods:
        if method.name == "__init__":
            continue
        if method.is_async:
            lines.append(
                f"    async def {method.name}(self, {', '.join(method.args)}, {', '.join(f'{k}=None' for k in method.kwargs)}):"
            )
        else:
            lines.append(
                f"    def {method.name}(self, {', '.join(method.args)}, {', '.join(f'{k}=None' for k in method.kwargs)}):"
            )

        lines.append(f"        mock_method = getattr(self, '{method.name}', None)")
        lines.append(
            """        if mock_method and hasattr(mock_method, 'return_value'):"""
        )
        lines.append("            return mock_method.return_value")
        lines.append("        return None")
        lines.append("")

    for attr in class_info.attributes:
        lines.append("    @property")
        lines.append(f"    def {attr}(self):")
        lines.append(f"        return getattr(self, '_{attr}', None)")
        lines.append("")

    return "\n".join(lines)


def generate_mock_function(
    func_sig: MethodSignature, framework: str = "unittest.mock"
) -> str:
    """Generate a mock function."""
    mock_type = "MagicMock" if framework == "unittest.mock" else "Mock"
    async_prefix = "async " if func_sig.is_async else ""

    params = ", ".join(func_sig.args + [f"{k}=None" for k in func_sig.kwargs])

    lines = [
        f"{async_prefix}def {func_sig.name}_mock({params}):",
        f'    """Auto-generated mock for {func_sig.name}"""',
        f"    mock = {mock_type}()",
    ]

    if func_sig.return_annotation:
        lines.append(f"    # Return type: {func_sig.return_annotation}")

    lines.append("    return mock")

    return "\n".join(lines)


def generate_config_code(
    class_info: ClassInfo, config: Dict[str, Any], framework: str
) -> str:
    """Generate configuration code for setting return values."""
    lines = []

    lines.append(f"def configure_{class_info.name.lower()}_mock(mock_obj, config):")
    lines.append('    """Configure mock with return values."""')
    lines.append(f"    configs = config.get('{class_info.name}', {{}})")
    lines.append("")
    lines.append("    for method_name, return_value in configs.items():")
    lines.append("        if hasattr(mock_obj, method_name):")
    lines.append(
        """            getattr(mock_obj, method_name).return_value = return_value"""
    )
    lines.append("        elif hasattr(mock_obj, '_' + method_name):")
    lines.append("            setattr(mock_obj, '_' + method_name, return_value)")
    lines.append("")
    lines.append("    return mock_obj")
    lines.append("")

    lines.append("# Usage example:")
    lines.append(f"# mock = {class_info.name}Mock()")
    lines.append(f"# mock = configure_{class_info.name.lower()}_mock(mock, {{")
    lines.append(f"#     '{class_info.name}': {{")

    for method in class_info.methods[:3]:
        lines.append(f"#         '{method.name}': <return_value>,")

    lines.append("#     })")

    return "\n".join(lines)


def generate_test_code(
    target: str,
    class_info: ClassInfo | None,
    func_sig: MethodSignature | None,
    config: Dict[str, Any],
    framework: str,
) -> str:
    """Generate complete test code with mocks."""
    lines = []

    framework_imports = {
        "unittest.mock": "from unittest.mock import MagicMock, patch",
        "pytest-mock": "import pytest",
    }

    lines.append(
        framework_imports.get(framework, "from unittest.mock import MagicMock")
    )
    lines.append("")
    lines.append(f"class Test{target}:")
    lines.append(f'    """Tests for {target}"""')
    lines.append("")

    if class_info:
        lines.append("    def setup_method(self):")
        lines.append(
            f"        self.mock_{class_info.name.lower()} = {class_info.name}Mock()"
        )
        lines.append(
            f"        self.mock_{class_info.name.lower()} = configure_{class_info.name.lower()}_mock("
        )
        lines.append(f"            self.mock_{class_info.name.lower()}, {{")
        lines.append(f"                '{class_info.name}': {{")

        for method in class_info.methods[:3]:
            default_value = _get_default_return_value(method.return_annotation)
            lines.append(f"                    '{method.name}': {default_value},")

        lines.append("                })")
        lines.append("        )")
        lines.append("")

        lines.append(f"    def test_{class_info.name.lower()}_creation(self):")
        lines.append(f"        assert self.mock_{class_info.name.lower()} is not None")
        lines.append("")

        for method in class_info.methods[:2]:
            lines.append(f"    def test_{method.name}(self):")
            lines.append(
                f"        result = self.mock_{class_info.name.lower()}.{method.name}()"
            )
            lines.append(
                """        assert result is not None  # Configure expected return value"""
            )
            lines.append("")

    return "\n".join(lines)


def _get_default_return_value(return_annotation: str | None) -> str:
    """Get a sensible default return value based on type annotation."""
    if not return_annotation:
        return "None"

    annotation = return_annotation.lower()

    if "list" in annotation:
        return "[]"
    elif "dict" in annotation:
        return "{}"
    elif "set" in annotation:
        return "set()"
    elif "int" in annotation:
        return "0"
    elif "float" in annotation:
        return "0.0"
    elif "bool" in annotation:
        return "True"
    elif "str" in annotation:
        return "''"
    elif "optional" in annotation or "none" in annotation:
        return "None"
    else:
        return "None"


def mock_generator(code: str, target: str, options: dict) -> dict:
    """
    Generate mock objects for testing.

    Args:
        code: Python code with classes to mock
        target: Class/function name to mock
        options: Mock framework (unittest.mock, pytest-mock)

    Returns:
        dict with status, mock_code, mock_class, and config
    """
    framework = options.get("framework", "unittest.mock")
    return_configs = options.get("return_configs", {})

    class_info = parse_class(code, target)
    func_sig = parse_function(code, target)
    dependencies = extract_dependencies(code, target)

    if class_info is None and func_sig is None:
        return {
            "status": "error",
            "message": f"Could not find class or function '{target}' in the provided code",
            "mock_code": "",
            "mock_class": "",
            "config": {},
        }

    mock_class = ""
    config_code = ""
    if class_info:
        mock_class = generate_mock_class(class_info, framework)
        config_code = generate_config_code(class_info, return_configs, framework)
    elif func_sig:
        mock_class = generate_mock_function(func_sig, framework)
        config_code = ""

    test_code = generate_test_code(
        target, class_info, func_sig, return_configs, framework
    )

    full_mock_code = f"""
# Generated Mock for {target}
# Framework: {framework}

{mock_class}

{config_code}

{test_code}
"""

    return {
        "status": "success",
        "mock_code": full_mock_code.strip(),
        "mock_class": mock_class,
        "config": {
            "framework": framework,
            "dependencies": list(dependencies),
            "methods": [m.name for m in class_info.methods]
            if class_info
            else [func_sig.name]
            if func_sig
            else [],
            "return_values": return_configs,
        },
    }


async def invoke(payload: dict) -> dict:
    """
    Main entry point for the skill.

    Args:
        payload: dict with code, target, options

    Returns:
        dict with result
    """
    code = payload.get("code", "")
    target = payload.get("target", "")
    options = payload.get("options", {})

    if not code:
        return {"status": "error", "message": "No code provided"}

    if not target:
        return {"status": "error", "message": "No target class/function specified"}

    result = mock_generator(code, target, options)
    return{
        "result": result,
        "metadata": {
            "action": action,
            "timestamp": datetime.now().isoformat(),
        },
    }
def register_skill():
    """Return skill metadata."""
    return {
        "name": "mock-generator",
        "description": "Creates mock objects for testing by analyzing class/function interfaces and generating MagicMock-based mock code",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
        "capabilities": [
            "class_interface_analysis",
            "function_signature_parsing",
            "magicmock_generation",
            "recursive_dependency_mocking",
            "return_value_configuration",
            "test_code_generation",
        ],
    }
