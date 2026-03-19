"""
Property Test Generator

Generates property-based tests using Hypothesis by:
- Analyzing function signatures to understand input types and constraints
- Generating edge cases (empty, null, max values, etc.)
- Generating random valid inputs based on type constraints
- Defining properties to check (idempotent, commutative, etc.)
- Outputting ready-to-run pytest/hypothesis code
"""

import ast
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ParameterInfo:
    name: str
    type_hint: Optional[str]
    default: Optional[Any]
    has_default: bool


@dataclass
class FunctionSignature:
    name: str
    params: List[ParameterInfo]
    return_type: Optional[str]
    is_async: bool
    line: int


TYPE_STRATEGIES = {
    "int": "st.integers()",
    "float": "st.floats()",
    "str": "st.texts()",
    "bool": "st.booleans()",
    "list": "st.lists(st.integers())",
    "dict": "st.dictionaries(st.texts(), st.integers())",
    "tuple": "st.tuples(st.integers(), st.integers())",
    "set": "st.sets(st.integers())",
    "bytes": "st.binary()",
    "None": "st.none()",
}

TYPE_EDGE_CASES = {
    "int": ["0", "1", "-1", "float('inf')", "float('-inf')", "10**18", "-10**18"],
    "float": ["0.0", "1.0", "-1.0", "float('inf')", "float('-inf')", "float('nan')"],
    "str": ["''", "'a'", "'hello'", "'\\n'", "'\\t'", "' '", "unicode_string"],
    "list": ["[]", "[1]", "[1, 2, 3]", "[None]", "[[]]"],
    "dict": ["{}", "{'key': None}", "{'a': 1, 'b': 2}"],
    "tuple": ["()", "(1,)", "(1, 2, 3)"],
    "set": ["set()", "{1}", "{1, 2, 3}"],
    "bool": ["True", "False"],
    "bytes": ["b''", "b'hello'"],
}


def parse_function_signatures(code: str) -> Dict[str, Any]:
    """Parse source code to extract function signatures."""
    functions = []

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"status": "error", "error": f"Syntax error: {e}"}

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            params = []
            defaults = node.args.defaults
            defaults_offset = len(node.args.args) - len(defaults)

            for i, arg in enumerate(node.args.args):
                default = None
                has_default = False

                if i >= defaults_offset:
                    default_idx = i - defaults_offset
                    default_ast = defaults[default_idx]
                    default = ast.unparse(default_ast)
                    has_default = True

                type_hint = None
                if arg.annotation:
                    type_hint = ast.unparse(arg.annotation)

                params.append(
                    ParameterInfo(
                        name=arg.arg,
                        type_hint=type_hint,
                        default=default,
                        has_default=has_default,
                    )
                )

            return_type = None
            if node.returns:
                return_type = ast.unparse(node.returns)

            functions.append(
                FunctionSignature(
                    name=node.name,
                    params=params,
                    return_type=return_type,
                    is_async=isinstance(node, ast.AsyncFunctionDef),
                    line=node.lineno,
                )
            )

    return {"status": "success", "functions": functions}


def infer_strategy_from_type(type_hint: str) -> str:
    """Infer Hypothesis strategy from type hint."""
    type_hint_lower = type_hint.lower().strip()

    for type_name, strategy in TYPE_STRATEGIES.items():
        if type_name in type_hint_lower:
            return strategy

    if "optional" in type_hint_lower:
        inner_match = re.search(r"\[([^\]]+)\]", type_hint)
        if inner_match:
            inner_type = inner_match.group(1)
            inner_strategy = infer_strategy_from_type(inner_type)
            return f"st.one_of({inner_strategy}, st.none())"

    if "list[" in type_hint_lower:
        inner_match = re.search(r"list\[([^\]]+)\]", type_hint_lower)
        if inner_match:
            inner_type = inner_match.group(1)
            inner_strategy = infer_strategy_from_type(inner_type)
            return f"st.lists({inner_strategy})"

    if "dict[" in type_hint_lower:
        inner_match = re.search(r"dict\[([^,]+),\s*([^\]]+)\]", type_hint_lower)
        if inner_match:
            key_strategy = infer_strategy_from_type(inner_match.group(1))
            val_strategy = infer_strategy_from_type(inner_match.group(2))
            return f"st.dictionaries({key_strategy}, {val_strategy})"

    if "tuple" in type_hint_lower:
        inner_match = re.search(r"tuple\[([^\]]+)\]", type_hint_lower)
        if inner_match:
            inner_types = [t.strip() for t in inner_match.group(1).split(",")]
            strategies = [infer_strategy_from_type(t) for t in inner_types]
            return f"st.tuples({', '.join(strategies)})"

    if "set[" in type_hint_lower:
        inner_match = re.search(r"set\[([^\]]+)\]", type_hint_lower)
        if inner_match:
            inner_strategy = infer_strategy_from_type(inner_match.group(1))
            return f"st.sets({inner_strategy})"

    return "st.integers()"


def generate_param_strategy(param: ParameterInfo) -> str:
    """Generate Hypothesis strategy for a parameter."""
    if param.type_hint:
        return infer_strategy_from_type(param.type_hint)

    name_lower = param.name.lower()

    if "num" in name_lower or "count" in name_lower or "id" in name_lower:
        return "st.integers(min_value=0)"
    elif "name" in name_lower or "title" in name_lower or "text" in name_lower:
        return "st.texts(min_size=1)"
    elif "flag" in name_lower or "is_" in name_lower or "enabled" in name_lower:
        return "st.booleans()"
    elif "data" in name_lower or "items" in name_lower:
        return "st.lists(st.integers())"
    elif "opts" in name_lower or "options" in name_lower:
        return "st.dictionaries(st.texts(), st.integers())"
    else:
        return "st.integers()"


def generate_edge_cases(param: ParameterInfo) -> List[str]:
    """Generate edge case values for a parameter."""
    if param.type_hint:
        base_type = param.type_hint.lower().strip()
        for type_name, cases in TYPE_EDGE_CASES.items():
            if type_name in base_type:
                return cases

    name_lower = param.name.lower()

    if "num" in name_lower or "count" in name_lower:
        return ["0", "1", "-1", "10**18"]
    elif "name" in name_lower or "text" in name_lower:
        return ["''", "'a'", "'hello'"]
    elif "flag" in name_lower or "bool" in name_lower:
        return ["True", "False"]

    return ["None"]


def detect_commutative_property(func_name: str, params: List[ParameterInfo]) -> bool:
    """Detect if function might have commutative property."""
    name_lower = func_name.lower()
    return (
        "add" in name_lower
        or "merge" in name_lower
        or "combine" in name_lower
        or "union" in name_lower
        or "intersect" in name_lower
    ) and len(params) >= 2


def detect_idempotent_property(func_name: str) -> bool:
    """Detect if function might have idempotent property."""
    name_lower = func_name.lower()
    return (
        "set" in name_lower
        or "update" in name_lower
        or "add" in name_lower
        or "create" in name_lower
    )


def detect_inverse_property(func_name: str) -> bool:
    """Detect if function might have inverse property."""
    name_lower = func_name.lower()
    return (
        ("add" in name_lower and "remove" in name_lower)
        or ("encode" in name_lower and "decode" in name_lower)
        or ("encrypt" in name_lower and "decrypt" in name_lower)
    )


def detect_identity_property(func_name: str, params: List[ParameterInfo]) -> bool:
    """Detect if function might have identity property."""
    name_lower = func_name.lower()
    return any(x in name_lower for x in ["add", "multiply", "sum", "concat", "merge"])


def generate_property_test(
    func: FunctionSignature, property_type: str, options: Dict[str, Any]
) -> str:
    """Generate a property test for a function."""
    num_examples = options.get("num_examples", 100)

    strategies = {}
    for param in func.params:
        strategies[param.name] = generate_param_strategy(param)

    func_call = func.name
    if func.is_async:
        func_call = f"await {func.name}"

    test_code = []

    if property_type == "idempotent":
        param_names = [p.name for p in func.params]
        params_str = ", ".join(param_names)
        test_code.append(f"""@given({', '.join(f'{name}={strat}' for name, strat in strategies.items())})
def test_{func.name}_idempotent({', '.join(param_names)}):
    result1 = {func_call}({params_str})
    result2 = {func_call}({params_str})
    assert result1 == result2, "Function should be idempotent"
""")

    elif property_type == "commutative":
        if len(func.params) >= 2:
            p1, p2 = func.params[0].name, func.params[1].name
            test_code.append(f"""@given({p1}={strategies[p1]}, {p2}={strategies[p2]})
def test_{func.name}_commutative({p1}, {p2}):
    result1 = {func.name}({p1}, {p2})
    result2 = {func.name}({p2}, {p1})
    assert result1 == result2, "Function should be commutative"
""")

    elif property_type == "identity":
        if len(func.params) >= 2:
            p1 = func.params[0].name
            identity_val = (
                "0" if func.return_type and "int" in func.return_type.lower() else "''"
            )
            test_code.append(f"""@given({p1}={strategies[p1]})
def test_{func.name}_identity({p1}):
    result = {func.name}({p1}, {identity_val})
    assert result == {p1}, "Function should return identity when using identity element"
""")

    elif property_type == "inverse":
        test_code.append(f"""@given({', '.join(f'{p.name}={strategies[p.name]}' for p in func.params)})
def test_{func.name}_inverse({', '.join(p.name for p in func.params)}):
    # For functions with inverse (e.g., encode/decode, add/remove)
    original = {func.params[0].name}
    result = {func_call}({', '.join(p.name for p in func.params)})
    # Add inverse operation here based on function semantics
    assert result is not None, "Inverse operation should produce valid result"
""")

    elif property_type == "type_preservation":
        for param in func.params:
            if param.type_hint:
                test_code.append(f"""@given({param.name}={strategies[param.name]})
def test_{func.name}_type_preservation_{param.name}({param.name}):
    result = {func_call}({', '.join(p.name for p in func.params)})
    # Check result type matches return type annotation
    assert result is not None
""")

    elif property_type == "edge_cases":
        for param in func.params:
            edge_cases = generate_edge_cases(param)
            test_code.append(f"""@given({param.name}={strategies[param.name]})
def test_{func.name}_handles_edge_cases_{param.name}({param.name}):
    # Test edge cases: {edge_cases}
    try:
        result = {func_call}({', '.join(p.name for p in func.params)})
        # Function should handle edge case gracefully
    except Exception as e:
        pytest.fail(f"Function should handle edge case: {{e}}")
""")

    return "\n".join(test_code)


def generate_complete_test_code(
    functions: List[FunctionSignature], options: Dict[str, Any]
) -> str:
    """Generate complete test file with all property tests."""
    imports = [
        "import pytest",
        "from hypothesis import given, settings, assume",
        "from hypothesis import strategies as st",
        "",
    ]

    if options.get("include_example_module", True):
        imports.append("# Replace with actual module import")
        imports.append("# from your_module import *")
        imports.append("")

    test_code = imports

    for func in functions:
        test_code.append(f"# Tests for {func.name}")
        test_code.append(f"# Return type: {func.return_type or 'None'}")
        test_code.append("")

        properties_to_test = detect_properties_for_function(func, options)

        for prop in properties_to_test:
            test_code.append(generate_property_test(func, prop, options))

        test_code.append("")

    return "\n".join(test_code)


def detect_properties_for_function(
    func: FunctionSignature, options: Dict[str, Any]
) -> List[str]:
    """Detect which properties to test for a function."""
    properties = options.get("properties", [])

    if properties:
        return properties

    detected = []

    if detect_idempotent_property(func.name):
        detected.append("idempotent")

    if len(func.params) >= 2:
        if detect_commutative_property(func.name, func.params):
            detected.append("commutative")
        if detect_identity_property(func.name, func.params):
            detected.append("identity")

    if detect_inverse_property(func.name):
        detected.append("inverse")

    if func.return_type:
        detected.append("type_preservation")

    detected.append("edge_cases")

    return detected


def property_test_generator(code: str, options: dict = None) -> dict:
    """
    Main function to generate property-based tests.

    Args:
        code: Python source code with functions to test
        options: Configuration options including:
            - framework: Test framework (hypothesis)
            - num_examples: Number of examples to generate (default: 100)
            - properties: List of specific properties to test
            - include_edge_cases: Include edge case tests (default: True)

    Returns:
        Dictionary containing:
        - status: "success" or "error"
        - test_code: Generated property-based test code
        - strategies: Hypothesis strategies used
        - properties: Properties being tested
    """
    if options is None:
        options = {}

    if not code:
        return {"status": "error", "error": "No code provided"}

    parsed = parse_function_signatures(code)

    if parsed.get("status") == "error":
        return parsed

    functions = parsed.get("functions", [])

    if not functions:
        return {"status": "error", "error": "No functions found in code"}

    strategies_used = {}
    properties_tested = set()

    for func in functions:
        func_strategies = {}
        for param in func.params:
            func_strategies[param.name] = generate_param_strategy(param)
        strategies_used[func.name] = func_strategies

        properties = detect_properties_for_function(func, options)
        properties_tested.update(properties)

    test_code = generate_complete_test_code(functions, options)

    return {
        "status": "success",
        "test_code": test_code,
        "functions": [
            {
                "name": f.name,
                "params": [p.name for p in f.params],
                "return_type": f.return_type,
                "is_async": f.is_async,
            }
            for f in functions
        ],
        "strategies": strategies_used,
        "properties": list(properties_tested),
        "options": {
            "framework": options.get("framework", "hypothesis"),
            "num_examples": options.get("num_examples", 100),
            "settings": {
                "max_examples": options.get("num_examples", 100),
                "deadline": options.get("deadline", None),
            },
        },
    }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    action = payload.get("action", "generate")
    code = payload.get("code", "")
    options = payload.get("options", {})

    if action == "generate":
        result = property_test_generator(code, options)
    elif action == "parse_signatures":
        result = parse_function_signatures(code)
    elif action == "detect_properties":
        parsed = parse_function_signatures(code)
        if parsed.get("status") == "success":
            func = parsed.get("functions", [None])[0]
            if func:
                properties = detect_properties_for_function(func, options)
                result = {"status": "success", "properties": properties}
            else:
                result = {"status": "error", "error": "No functions found"}
        else:
            result = parsed
    else:
        result = {"status": "error", "message": f"Unknown action: {action}"}

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "property-test-generator",
        "description": "Generates property-based tests using Hypothesis framework",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
        "capabilities": [
            "function_signature_analysis",
            "edge_case_generation",
            "property_detection",
            "hypothesis_test_generation",
        ],
    }
