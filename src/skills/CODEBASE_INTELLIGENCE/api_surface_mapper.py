"""
API Surface Mapper Skill

This module provides skills for mapping API surfaces:
- Extract public functions, classes, and methods
- Document parameters with types and defaults
- Document return types
- Detect async APIs
- Generate API surface overview
"""

import ast
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ParameterInfo:
    """Information about a function/method parameter"""

    name: str
    type_annotation: Optional[str]
    has_default: bool
    default_value: Optional[str]
    is_var_positional: bool
    is_var_keyword: bool
    is_positional_only: bool
    is_keyword_only: bool


@dataclass
class FunctionInfo:
    """Information about a function or method"""

    name: str
    line_number: int
    is_method: bool
    is_classmethod: bool
    is_staticmethod: bool
    is_async: bool
    class_name: Optional[str]
    parameters: List[ParameterInfo]
    return_type: Optional[str]
    decorators: List[str]
    is_public: bool


@dataclass
class ClassInfo:
    """Information about a class"""

    name: str
    line_number: int
    base_classes: List[str]
    methods: List[FunctionInfo]
    is_public: bool
    is_dataclass: bool
    is_enum: bool


class APISurfaceVisitor(ast.NodeVisitor):
    """AST visitor to extract API surface information"""

    def __init__(self, source_lines: List[str], options: dict):
        self.source_lines = source_lines
        self.options = options
        self.include_private = options.get("include_private", False)
        self.include_internal = options.get("include_internal", False)

        self.functions: List[FunctionInfo] = []
        self.classes: List[ClassInfo] = []
        self.current_class: Optional[str] = None
        self.current_class_lineno: int = 0
        self.current_class_bases: List[str] = []

        self._in_dataclass = False
        self._in_enum = False
        self._in_async_function = False
        self._in_classmethod = False
        self._in_staticmethod = False
        self._in_dataclass_field = False

    def _is_public(self, name: str) -> bool:
        """Check if a name is public (not private or internal)"""
        if name.startswith("_") and not name.startswith("__"):
            return self.include_private
        if name.startswith("__") and not name.endswith("__"):
            return self.include_internal
        return True

    def _get_type_annotation(self, annotation: ast.AST) -> Optional[str]:
        """Extract type annotation as string"""
        if annotation is None:
            return None
        try:
            return ast.unparse(annotation)
        except Exception:
            return None

    def _get_default_value(self, default: ast.AST) -> Optional[str]:
        """Extract default value as string"""
        if default is None:
            return None
        try:
            return ast.unparse(default)
        except Exception:
            return None

    def _extract_parameters(self, args: ast.arguments) -> List[ParameterInfo]:
        """Extract parameter information from function arguments"""
        params = []

        pos_only_args = getattr(args, "posonlyargs", [])
        kw_only_args = getattr(args, "kwonlyargs", [])

        all_args = pos_only_args + args.args

        defaults = list(reversed(args.defaults))

        for i, arg in enumerate(all_args):
            default_idx = i - (len(all_args) - len(defaults))
            has_default = default_idx >= 0
            default_value = None
            if has_default:
                default_value = self._get_default_value(defaults[default_idx])

            param = ParameterInfo(
                name=arg.arg,
                type_annotation=self._get_type_annotation(arg.annotation),
                has_default=has_default,
                default_value=default_value,
                is_var_positional=False,
                is_var_keyword=False,
                is_positional_only=arg in pos_only_args,
                is_keyword_only=False,
            )
            params.append(param)

        if args.vararg:
            params.append(
                ParameterInfo(
                    name=args.vararg.arg,
                    type_annotation=self._get_type_annotation(args.vararg.annotation),
                    has_default=False,
                    default_value=None,
                    is_var_positional=True,
                    is_var_keyword=False,
                    is_positional_only=False,
                    is_keyword_only=False,
                )
            )

        for arg in kw_only_args:
            default_idx = 0
            if args.kw_defaults:
                for kw in args.kw_defaults:
                    if kw is not None:
                        default_idx += 1
            has_default = args.kw_defaults and any(
                k is not None for k in args.kw_defaults
            )
            default_value = None
            if has_default:
                for d in args.kw_defaults:
                    if d is not None:
                        default_value = self._get_default_value(d)
                        break

            params.append(
                ParameterInfo(
                    name=arg.arg,
                    type_annotation=self._get_type_annotation(arg.annotation),
                    has_default=has_default,
                    default_value=default_value,
                    is_var_positional=False,
                    is_var_keyword=False,
                    is_positional_only=False,
                    is_keyword_only=True,
                )
            )

        if args.kwarg:
            params.append(
                ParameterInfo(
                    name=args.kwarg.arg,
                    type_annotation=self._get_type_annotation(args.kwarg.annotation),
                    has_default=False,
                    default_value=None,
                    is_var_positional=False,
                    is_var_keyword=True,
                    is_positional_only=False,
                    is_keyword_only=False,
                )
            )

        return params

    def _extract_decorators(self, node: ast.AST) -> List[str]:
        """Extract decorator names"""
        decorators = []
        for decorator in getattr(node, "decorator_list", []):
            try:
                decorators.append(ast.unparse(decorator))
            except Exception:
                pass
        return decorators

    def _check_class_decorators(self, node: ast.ClassDef) -> tuple:
        """Check if class is dataclass or enum"""
        is_dataclass = False
        is_enum = False
        for decorator in node.decorator_list:
            try:
                dec_name = ast.unparse(decorator)
                if "dataclass" in dec_name:
                    is_dataclass = True
                if dec_name == "enum" or "Enum" in dec_name:
                    is_enum = True
            except Exception:
                pass
        return is_dataclass, is_enum

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        is_dataclass, is_enum = self._check_class_decorators(node)

        old_class = self.current_class
        old_lineno = self.current_class_lineno
        old_bases = self.current_class_bases

        self.current_class = node.name
        self.current_class_lineno = node.lineno
        self.current_class_bases = [
            self._get_type_annotation(base) for base in node.bases
        ]

        is_public = self._is_public(node.name)

        class_info = ClassInfo(
            name=node.name,
            line_number=node.lineno,
            base_classes=self.current_class_bases,
            methods=[],
            is_public=is_public,
            is_dataclass=is_dataclass,
            is_enum=is_enum,
        )

        self.generic_visit(node)

        class_info.methods = [f for f in self.functions if f.class_name == node.name]
        self.classes.append(class_info)

        self.current_class = old_class
        self.current_class_lineno = old_lineno
        self.current_class_bases = old_bases

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._process_function(node, is_async=False)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._process_function(node, is_async=True)

    def _process_function(self, node, is_async: bool) -> None:
        decorators = self._extract_decorators(node)

        is_classmethod = False
        is_staticmethod = False
        for dec in decorators:
            if "classmethod" in dec:
                is_classmethod = True
            if "staticmethod" in dec:
                is_staticmethod = True

        is_method = self.current_class is not None
        class_name = self.current_class if is_method else None

        is_public = self._is_public(node.name)

        func_info = FunctionInfo(
            name=node.name,
            line_number=node.lineno,
            is_method=is_method,
            is_classmethod=is_classmethod,
            is_staticmethod=is_staticmethod,
            is_async=is_async,
            class_name=class_name,
            parameters=self._extract_parameters(node.args),
            return_type=self._get_type_annotation(node.returns),
            decorators=decorators,
            is_public=is_public,
        )

        self.functions.append(func_info)


def _filter_public(items: List, include_private: bool = False) -> List:
    """Filter to only public items"""
    if include_private:
        return items
    return [item for item in items if getattr(item, "is_public", True)]


def api_surface_mapper(code: str, options: dict = None) -> dict:
    """
    Map the API surface of Python code

    Args:
        code: Python source code to analyze
        options: Dictionary with options:
            - include_private: Include private functions (_func) (default: False)
            - include_internal: Include internal functions (__func) (default: False)
            - include_inherited: Include inherited methods (default: True)
            - max_parameters: Max parameters to include per function (default: 50)

    Returns:
        dict with:
            - status: "success" or "error"
            - public_api: List of public functions/classes
            - parameters: Parameter documentation
            - return_types: Return type documentation
            - async_apis: Async function list
            - api_summary: Overview statistics
    """
    if options is None:
        options = {}

    include_inherited = options.get("include_inherited", True)
    max_parameters = options.get("max_parameters", 50)

    try:
        tree = ast.parse(code)
        lines = code.splitlines()

        visitor = APISurfaceVisitor(lines, options)
        visitor.visit(tree)

        classes = visitor.classes
        functions = visitor.functions

        public_api = []

        public_classes = _filter_public(classes, options.get("include_private", False))
        for cls in public_classes:
            public_api.append(
                {
                    "type": "class",
                    "name": cls.name,
                    "line": cls.line_number,
                    "is_dataclass": cls.is_dataclass,
                    "is_enum": cls.is_enum,
                    "base_classes": cls.base_classes,
                    "method_count": len(cls.methods),
                }
            )

        module_functions = [f for f in functions if not f.is_method]
        public_functions = _filter_public(
            module_functions, options.get("include_private", False)
        )
        for func in public_functions:
            public_api.append(
                {
                    "type": "function",
                    "name": func.name,
                    "line": func.line_number,
                    "is_async": func.is_async,
                    "is_public": func.is_public,
                }
            )

        parameters = {}

        for func in functions:
            func_name = func.name
            if func.class_name:
                func_name = f"{func.class_name}.{func.name}"

            params_list = []
            for param in func.parameters[:max_parameters]:
                param_doc = {
                    "name": param.name,
                    "type": param.type_annotation,
                    "has_default": param.has_default,
                }
                if param.has_default and param.default_value:
                    param_doc["default"] = param.default_value
                if param.is_var_positional:
                    param_doc["is_var_positional"] = True
                if param.is_var_keyword:
                    param_doc["is_var_keyword"] = True
                if param.is_positional_only:
                    param_doc["is_positional_only"] = True
                if param.is_keyword_only:
                    param_doc["is_keyword_only"] = True

                params_list.append(param_doc)

            parameters[func_name] = {
                "parameters": params_list,
                "count": len(params_list),
                "required_count": sum(
                    1 for p in params_list if not p.get("has_default", False)
                ),
            }

        return_types = {}

        for func in functions:
            func_name = func.name
            if func.class_name:
                func_name = f"{func.class_name}.{func.name}"

            if func.return_type:
                return_types[func_name] = {
                    "return_type": func.return_type,
                    "has_return": True,
                }
            else:
                return_types[func_name] = {
                    "return_type": None,
                    "has_return": False,
                }

        async_apis = []

        for func in functions:
            if func.is_async:
                func_name = func.name
                if func.class_name:
                    func_name = f"{func.class_name}.{func.name}"

                async_apis.append(
                    {
                        "name": func_name,
                        "line": func.line_number,
                        "is_method": func.is_method,
                        "class_name": func.class_name,
                        "return_type": func.return_type,
                        "await_patterns": _detect_await_patterns(
                            code, func.line_number
                        ),
                    }
                )

        total_functions = len([f for f in functions if not f.is_method])
        total_methods = len([f for f in functions if f.is_method])
        total_classes = len(classes)
        public_functions_count = len(
            [f for f in public_functions if getattr(f, "is_public", True)]
        )
        public_classes_count = len(public_classes)

        api_summary = {
            "total_classes": total_classes,
            "total_functions": total_functions,
            "total_methods": total_methods,
            "public_classes": public_classes_count,
            "public_functions": public_functions_count,
            "async_functions": len(async_apis),
            "dataclasses": len([c for c in classes if c.is_dataclass]),
            "enums": len([c for c in classes if c.is_enum]),
            "total_api_entries": len(public_api),
        }

        return {
            "status": "success",
            "public_api": public_api,
            "parameters": parameters,
            "return_types": return_types,
            "async_apis": async_apis,
            "api_summary": api_summary,
        }

    except SyntaxError as e:
        return {
            "status": "error",
            "message": f"Syntax error in code: {str(e)}",
            "public_api": [],
            "parameters": {},
            "return_types": {},
            "async_apis": [],
            "api_summary": {},
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error mapping API surface: {str(e)}",
            "public_api": [],
            "parameters": {},
            "return_types": {},
            "async_apis": [],
            "api_summary": {},
        }


def _detect_await_patterns(code: str, line_number: int) -> List[str]:
    """Detect await patterns in a function"""
    patterns = []
    lines = code.splitlines()

    func_start = line_number - 1
    func_end = func_start
    indent_level = 0

    if func_start < len(lines):
        first_line = lines[func_start]
        if "def " in first_line or "async def " in first_line:
            indent_level = len(first_line) - len(first_line.lstrip())

            for i in range(func_start + 1, len(lines)):
                line = lines[i]
                if line.strip() and not line.startswith(" " * (indent_level + 1)):
                    func_end = i
                    break
                func_end = i

    func_code = "\n".join(lines[func_start:func_end])

    if "await " in func_code:
        patterns.append("await_expression")
    if "asyncio" in func_code:
        patterns.append("asyncio")
    if "gather" in func_code:
        patterns.append("gather")
    if "create_task" in func_code:
        patterns.append("create_task")
    if "wait_for" in func_code:
        patterns.append("wait_for")
    if "sleep" in func_code:
        patterns.append("sleep")

    return patterns


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation

    Args:
        payload: Dictionary with:
            - code: Python source code (required)
            - options: Analysis options (optional)

    Returns:
        dict with analysis result
    """
    code = payload.get("code")
    options = payload.get("options", {})

    if not code:
        return {"result": {"status": "error", "message": "No code provided"}}

    result = api_surface_mapper(code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "api-surface-mapper",
        "description": "Map Python API surfaces - extracts public functions, classes, methods, documents parameters with types and defaults, documents return types, detects async APIs, and generates API surface overview statistics",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }


if __name__ == "__main__":
    test_code = """
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class User:
    name: str
    email: str
    age: Optional[int] = None
    status: Status = Status.ACTIVE


def public_function(x: int, y: int = 10) -> int:
    return x + y


def _private_helper(data: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in data}


async def fetch_data(url: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    import asyncio
    await asyncio.sleep(0.1)
    return {"url": url, "status": "ok"}


async def process_items(items: List[int]) -> List[int]:
    import asyncio
    results = await asyncio.gather(*[fetch_item(i) for i in items])
    return results


async def fetch_item(item: int) -> int:
    await asyncio.sleep(0.01)
    return item * 2


class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b
    
    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b
    
    @classmethod
    def create(cls, value: int) -> "Calculator":
        return cls()
    
    def _internal_method(self, data: str) -> None:
        pass


class Service:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def process(self, data: List[str]) -> Dict[str, int]:
        results = {}
        for item in data:
            results[item] = len(item)
        return results
    
    def __private__(self) -> None:
        pass
"""

    options = {
        "include_private": False,
        "include_internal": False,
        "include_inherited": True,
    }

    result = api_surface_mapper(test_code, options)
    import json

    print(json.dumps(result, indent=2))
