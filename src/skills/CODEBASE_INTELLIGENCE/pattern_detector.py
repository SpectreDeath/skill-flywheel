"""
Pattern Detector Skill

This module provides skills for detecting design patterns in Python code:
- GoF (Gang of Four) patterns: Creational, Structural, Behavioral
- Enterprise patterns commonly used in Python applications

Supported patterns:
- Creational: Singleton, Factory, Abstract Factory, Builder, Prototype
- Structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
- Behavioral: Chain of Responsibility, Command, Iterator, Mediator, Memento,
              Observer, State, Strategy, Template Method, Visitor
"""

import ast
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class PatternMatch:
    """Represents a detected pattern match"""

    pattern_name: str
    confidence: float
    locations: List[Tuple[int, int]]
    indicators_found: List[str]
    description: str


class PatternDetector(ast.NodeVisitor):
    """AST-based pattern detector"""

    def __init__(self):
        self.classes: Dict[str, ast.ClassDef] = {}
        self.functions: Dict[str, ast.FunctionDef] = {}
        self.imports: List[str] = []
        self.class_methods: Dict[str, List[str]] = defaultdict(list)
        self.class_bases: Dict[str, List[str]] = defaultdict(list)
        self.current_class: Optional[str] = None

    def visit_ClassDef(self, node: ast.ClassDef):
        self.classes[node.name] = node
        self.class_bases[node.name] = [self._get_name(base) for base in node.bases]

        old_class = self.current_class
        self.current_class = node.name

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.class_methods[node.name].append(item.name)

        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.functions[node.name] = node
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.imports.append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self.imports.append(node.module)

    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return ""


PATTERN_DEFINITIONS = {
    "Singleton": {
        "category": "Creational",
        "indicators": [
            (r"_instance\s*=\s*None", 0.9, "Class-level _instance = None"),
            (r"if\s+.*instance\s+is\s+None", 0.85, "None check for instance"),
            (r"def\s+__new__", 0.95, "__new__ method override"),
            (r"def\s+get_instance", 0.8, "get_instance method"),
            (r"def\s+shared_instance", 0.8, "shared_instance method"),
            (r"@classmethod\s+def\s+instance", 0.85, "Class method for instance"),
        ],
        "class_indicators": [
            "Singleton",
            "_instance",
            "get_instance",
            "shared_instance",
        ],
        "description": "Ensures a class has only one instance and provides a global access point",
    },
    "Factory": {
        "category": "Creational",
        "indicators": [
            (r"def\s+create\w+\s*\(", 0.85, "create method"),
            (r"def\s+make\w+\s*\(", 0.8, "make method"),
            (r"def\s+build\w+\s*\(", 0.8, "build method"),
            (r"def\s+new\w+\s*\(", 0.7, "new method"),
            (r"class\s+\w*Factory\w*", 0.95, "Factory class name"),
            (r"def\s+\w*factory\w*\s*\(", 0.9, "factory method"),
        ],
        "class_indicators": ["Factory", "create_", "make_", "build_"],
        "description": "Defines an interface for creating objects, letting subclasses decide the class",
    },
    "Abstract Factory": {
        "category": "Creational",
        "indicators": [
            (r"class\s+\w*Abstract\w*Factory\w*", 0.95, "Abstract Factory class"),
            (r"class\s+\w*Factory\w*Base\w*", 0.9, "Factory base class"),
            (r"def\s+create_product", 0.85, "create_product method"),
            (r"def\s+create_\w+", 0.8, "create_ method for product"),
            (r"ABC", 0.7, "Abstract Base Class usage"),
            (r"abstractmethod", 0.85, "Abstract method decorator"),
        ],
        "class_indicators": ["AbstractFactory", "Factory", "create_"],
        "description": "Provides an interface for creating families of related objects without specifying concrete classes",
    },
    "Builder": {
        "category": "Creational",
        "indicators": [
            (r"class\s+\w*Builder\w*", 0.95, "Builder class"),
            (r"def\s+with_\w+\s*\(", 0.9, "with_ setter method"),
            (r"def\s+set_\w+\s*\(", 0.8, "set_ setter method"),
            (r"def\s+build\s*\(", 0.9, "build method"),
            (r"def\s+construct\s*\(", 0.8, "construct method"),
            (r"return\s+self", 0.7, "Fluent interface (return self)"),
        ],
        "class_indicators": ["Builder", "with_", "set_", "build"],
        "description": "Separates the construction of a complex object from its representation",
    },
    "Prototype": {
        "category": "Creational",
        "indicators": [
            (r"def\s+clone\s*\(", 0.9, "clone method"),
            (r"def\s+copy\s*\(", 0.85, "copy method"),
            (r"def\s+__copy__", 0.95, "__copy__ method"),
            (r"def\s+__deepcopy__", 0.95, "__deepcopy__ method"),
            (r"import\s+copy", 0.8, "copy module import"),
            (r"def\s+duplicate\s*\(", 0.85, "duplicate method"),
        ],
        "class_indicators": ["clone", "copy", "duplicate", "Prototype"],
        "description": "Creates new objects by copying an existing object (prototype)",
    },
    "Adapter": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Adapter\w*", 0.95, "Adapter class name"),
            (r"class\s+\w*Wrapper\w*", 0.9, "Wrapper class name"),
            (r"def\s+adapt\s*\(", 0.85, "adapt method"),
            (r"def\s+convert\s*\(", 0.8, "convert method"),
            (r"def\s+wrap\s*\(", 0.8, "wrap method"),
            (r"self\.\w+\s*=.*\(", 0.6, "Assigning wrapped object"),
        ],
        "class_indicators": ["Adapter", "Wrapper", "wrap", "adaptee"],
        "description": "Converts the interface of a class into another interface clients expect",
    },
    "Bridge": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Implementor\w*", 0.9, "Implementor class"),
            (r"class\s+\w*Abstraction\w*", 0.9, "Abstraction class"),
            (r"def\s+implement\s*\(", 0.8, "implement method"),
            (r"self\.\w+_impl", 0.85, "Implementation reference"),
            (r"self\.\w+_bridge", 0.85, "Bridge reference"),
        ],
        "class_indicators": ["Implementor", "Abstraction", "impl", "bridge"],
        "description": "Decouples an abstraction from its implementation so both can vary independently",
    },
    "Composite": {
        "category": "Structural",
        "indicators": [
            (r"def\s+add\s*\(", 0.85, "add method"),
            (r"def\s+remove\s*\(", 0.85, "remove method"),
            (r"def\s+get_children\s*\(", 0.9, "get_children method"),
            (r"def\s+children\s*\(", 0.8, "children property"),
            (r"for\s+child\s+in", 0.7, "Child iteration"),
        ],
        "class_indicators": ["Component", "Composite", "children", "add", "remove"],
        "description": "Composes objects into tree structures to represent part-whole hierarchies",
    },
    "Decorator": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Decorator\w*", 0.95, "Decorator class name"),
            (r"def\s+__init__\s*\(.*wrapper", 0.9, "Wrapper in __init__"),
            (r"def\s+__getattr__", 0.85, "__getattr__ for delegation"),
            (r"functools\.wraps", 0.9, "functools.wraps usage"),
            (r"@wraps\s*\(", 0.9, "@wraps decorator"),
        ],
        "class_indicators": ["Decorator", "wrapper", "wrapped", "component"],
        "description": "Attaches additional responsibilities to an object dynamically",
    },
    "Facade": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Facade\w*", 0.95, "Facade class name"),
            (r"def\s+__init__\s*\(.* subsystems", 0.9, "Subsystem initialization"),
            (r"self\.\w+\s*=.*\(", 0.5, "Multiple subsystem assignments"),
        ],
        "class_indicators": ["Facade", "subsystem", "_subsystem"],
        "description": "Provides a unified interface to a set of interfaces in a subsystem",
    },
    "Flyweight": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Flyweight\w*", 0.95, "Flyweight class name"),
            (r"class\s+\w*Factory\w*.*Flyweight", 0.95, "Flyweight Factory"),
            (r"_flyweights\s*=", 0.9, "Flyweight cache/storage"),
            (r"@lru_cache", 0.85, "LRU cache decorator"),
            (r"def\s+get_\w+_flyweight", 0.9, "get_flyweight method"),
        ],
        "class_indicators": ["Flyweight", "flyweight", "_pool", "_cache"],
        "description": "Uses sharing to support large numbers of fine-grained objects efficiently",
    },
    "Proxy": {
        "category": "Structural",
        "indicators": [
            (r"class\s+\w*Proxy\w*", 0.95, "Proxy class name"),
            (r"class\s+\w*Proxy\w*.*:", 0.95, "Proxy class"),
            (r"def\s+__getattr__", 0.8, "__getattr__ for delegation"),
            (r"self\._real_", 0.85, "Real subject reference"),
            (r"self\._subject", 0.85, "Subject reference"),
            (r"lazy\s+=", 0.8, "Lazy initialization"),
        ],
        "class_indicators": ["Proxy", "_real", "_subject", "_target"],
        "description": "Provides a surrogate or placeholder for another object to control access to it",
    },
    "Chain of Responsibility": {
        "category": "Behavioral",
        "indicators": [
            (r"def\s+set_next\s*\(", 0.9, "set_next method"),
            (r"def\s+set_successor\s*\(", 0.9, "set_successor method"),
            (r"def\s+handle\s*\(", 0.85, "handle method"),
            (r"def\s+next\s*\(", 0.8, "next method"),
            (r"self\.next_handler", 0.85, "Next handler reference"),
            (r"self\.successor", 0.85, "Successor reference"),
            (r"def\s+process\s*\(.*request", 0.8, "process request method"),
        ],
        "class_indicators": ["Handler", "Chain", "next", "successor", "handle"],
        "description": "Avoids coupling the sender of a request to its receiver by giving multiple objects a chance to handle the request",
    },
    "Command": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Command\w*", 0.95, "Command class name"),
            (r"def\s+execute\s*\(", 0.9, "execute method"),
            (r"def\s+undo\s*\(", 0.85, "undo method"),
            (r"def\s+redo\s*\(", 0.8, "redo method"),
            (r"def\s+run\s*\(", 0.7, "run method"),
        ],
        "class_indicators": ["Command", "execute", "undo", "redo"],
        "description": "Encapsulates a request as an object, letting you parameterize clients with different requests",
    },
    "Iterator": {
        "category": "Behavioral",
        "indicators": [
            (r"def\s+__iter__\s*\(", 0.95, "__iter__ method"),
            (r"def\s+__next__\s*\(", 0.95, "__next__ method"),
            (r"def\s+__getitem__\s*\(", 0.85, "__getitem__ method"),
            (r"def\s+next\s*\(", 0.8, "next method"),
            (r"def\s+has_next\s*\(", 0.85, "has_next method"),
            (r"yield\s+", 0.8, "Generator/yield usage"),
        ],
        "class_indicators": ["Iterator", "iter", "next", "__iter__", "__next__"],
        "description": "Provides a way to access elements of an aggregate object sequentially without exposing its representation",
    },
    "Mediator": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Mediator\w*", 0.95, "Mediator class name"),
            (r"def\s+notify\s*\(.*event", 0.85, "notify method with event"),
            (r"def\s+send\s*\(.*message", 0.85, "send method"),
            (r"self\._mediator", 0.85, "Mediator reference"),
            (r"def\s+colleague\s*\(", 0.8, "colleague method"),
        ],
        "class_indicators": ["Mediator", "_mediator", "colleague", "notify"],
        "description": "Defines an object that encapsulates how a set of objects interact",
    },
    "Memento": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Memento\w*", 0.95, "Memento class name"),
            (r"def\s+save\s*\(", 0.85, "save method"),
            (r"def\s+restore\s*\(", 0.85, "restore method"),
            (r"def\s+get_state\s*\(", 0.85, "get_state method"),
            (r"def\s+set_state\s*\(", 0.85, "set_state method"),
            (r"def\s+memento\s*\(", 0.9, "memento method"),
        ],
        "class_indicators": ["Memento", "state", "save", "restore", "history"],
        "description": "Captures and externalizes an object's internal state so the object can be restored to this state later",
    },
    "Observer": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Observer\w*", 0.95, "Observer class name"),
            (r"def\s+notify\s*\(", 0.9, "notify method"),
            (r"def\s+update\s*\(", 0.85, "update method"),
            (r"def\s+subscribe\s*\(", 0.85, "subscribe method"),
            (r"def\s+unsubscribe\s*\(", 0.85, "unsubscribe method"),
            (r"def\s+add_observer\s*\(", 0.9, "add_observer method"),
            (r"_observers\s*=", 0.9, "_observers list"),
            (r"_listeners\s*=", 0.9, "_listeners list"),
        ],
        "class_indicators": [
            "Observer",
            "_observers",
            "_listeners",
            "notify",
            "update",
        ],
        "description": "Defines a one-to-many dependency between objects so when one changes state, all dependents are notified",
    },
    "State": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*State\w*", 0.95, "State class name"),
            (r"def\s+set_state\s*\(", 0.9, "set_state method"),
            (r"def\s+change_state\s*\(", 0.9, "change_state method"),
            (r"self\._state\s*=", 0.85, "State attribute"),
            (r"class\s+\w*State\w*.*\(", 0.9, "Concrete state classes"),
        ],
        "class_indicators": ["State", "state", "set_state", "change_state"],
        "description": "Allows an object to alter its behavior when its internal state changes",
    },
    "Strategy": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Strategy\w*", 0.95, "Strategy class name"),
            (r"def\s+execute\s*\(", 0.85, "execute method"),
            (r"def\s+run\s*\(", 0.8, "run method"),
            (r"def\s+set_strategy\s*\(", 0.9, "set_strategy method"),
            (r"def\s+use_strategy\s*\(", 0.85, "use_strategy method"),
            (r"def\s+algorithm\s*\(", 0.8, "algorithm method"),
        ],
        "class_indicators": ["Strategy", "execute", "set_strategy", "algorithm"],
        "description": "Defines a family of algorithms, encapsulates each one, and makes them interchangeable",
    },
    "Template Method": {
        "category": "Behavioral",
        "indicators": [
            (r"def\s+\w+\s*\(.*\)", 0.6, "Method definition"),
            (r"def\s+step_\w+\s*\(", 0.9, "step_ method naming"),
            (r"def\s+hook\s*\(", 0.9, "hook method"),
            (r"super\(\)\.", 0.85, "super() call"),
            (r"@abstractmethod", 0.85, "Abstract method"),
        ],
        "class_indicators": ["Template", "step_", "hook", "_step"],
        "description": "Defines the skeleton of an algorithm in a method, deferring some steps to subclasses",
    },
    "Visitor": {
        "category": "Behavioral",
        "indicators": [
            (r"class\s+\w*Visitor\w*", 0.95, "Visitor class name"),
            (r"def\s+visit_\w+\s*\(", 0.95, "visit_ method"),
            (r"def\s+accept\s*\(", 0.9, "accept method"),
            (r"def\s+visit\s*\(", 0.85, "visit method"),
        ],
        "class_indicators": ["Visitor", "visit_", "accept", "Element"],
        "description": "Lets you define a new operation without changing the classes of the elements on which it operates",
    },
}


def detect_singleton(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Singleton pattern"""
    matches = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if re.search(r"_instance\s*=\s*None", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__new__", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"get_instance|shared_instance", line):
            matches.append((i + 1, line.strip()))

    if len(matches) >= 2:
        confidence = min(0.6 + (len(matches) * 0.15), 0.95)
        return PatternMatch(
            pattern_name="Singleton",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Singleton"]["description"],
        )
    return None


def detect_factory(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Factory pattern"""
    matches = []
    lines = code.split("\n")

    has_factory_class = False
    for class_name in detector.classes:
        if "Factory" in class_name:
            has_factory_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+create\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+make\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+build\w+\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_factory_class or len(matches) >= 2:
        confidence = (
            min(0.5 + (len(matches) * 0.15), 0.95)
            if has_factory_class
            else min(0.4 + (len(matches) * 0.15), 0.8)
        )
        return PatternMatch(
            pattern_name="Factory",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Factory"]["description"],
        )
    return None


def detect_abstract_factory(
    code: str, detector: PatternDetector
) -> Optional[PatternMatch]:
    """Detect Abstract Factory pattern"""
    matches = []
    lines = code.split("\n")

    has_abstract = False
    for class_name in detector.classes:
        if "Abstract" in class_name and "Factory" in class_name:
            has_abstract = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"abstractmethod", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+create_product", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"ABC", line):
            matches.append((i + 1, line.strip()))

    if has_abstract and len(matches) >= 2:
        return PatternMatch(
            pattern_name="Abstract Factory",
            confidence=min(0.7 + (len(matches) * 0.1), 0.95),
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Abstract Factory"]["description"],
        )
    return None


def detect_builder(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Builder pattern"""
    matches = []
    lines = code.split("\n")

    has_builder_class = False
    for class_name in detector.classes:
        if "Builder" in class_name:
            has_builder_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+with_\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+set_\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+build\s*\(", line) and "self" not in line:
            matches.append((i + 1, line.strip()))
        if re.search(r"return\s+self", line):
            matches.append((i + 1, line.strip()))

    if has_builder_class or len(matches) >= 3:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_builder_class
            else min(0.4 + (len(matches) * 0.1), 0.75)
        )
        return PatternMatch(
            pattern_name="Builder",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Builder"]["description"],
        )
    return None


def detect_prototype(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Prototype pattern"""
    matches = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if re.search(r"def\s+clone\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__copy__\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__deepcopy__\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"import\s+copy", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+duplicate\s*\(", line):
            matches.append((i + 1, line.strip()))

    if len(matches) >= 2:
        return PatternMatch(
            pattern_name="Prototype",
            confidence=min(0.5 + (len(matches) * 0.2), 0.95),
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Prototype"]["description"],
        )
    return None


def detect_adapter(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Adapter pattern"""
    matches = []
    lines = code.split("\n")

    has_adapter_class = False
    for class_name in detector.classes:
        if "Adapter" in class_name or "Wrapper" in class_name:
            has_adapter_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+adapt\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+convert\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+wrap\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_adapter_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_adapter_class
            else min(0.4 + (len(matches) * 0.15), 0.75)
        )
        return PatternMatch(
            pattern_name="Adapter",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Adapter"]["description"],
        )
    return None


def detect_bridge(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Bridge pattern"""
    matches = []
    lines = code.split("\n")

    has_abstraction = False
    has_implementor = False
    for class_name in detector.classes:
        if "Abstraction" in class_name:
            has_abstraction = True
            matches.append((1, f"class {class_name}"))
        if "Implementor" in class_name:
            has_implementor = True
            matches.append((1, f"class {class_name}"))

    if has_abstraction and has_implementor:
        return PatternMatch(
            pattern_name="Bridge",
            confidence=0.9,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Bridge"]["description"],
        )
    return None


def detect_composite(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Composite pattern"""
    matches = []
    lines = code.split("\n")

    has_composite = False
    for class_name in detector.classes:
        if "Composite" in class_name or "Component" in class_name:
            has_composite = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+add\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+remove\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+get_children\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_composite or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_composite
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Composite",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Composite"]["description"],
        )
    return None


def detect_decorator_pattern(
    code: str, detector: PatternDetector
) -> Optional[PatternMatch]:
    """Detect Decorator pattern"""
    matches = []
    lines = code.split("\n")

    has_decorator_class = False
    for class_name in detector.classes:
        if "Decorator" in class_name:
            has_decorator_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"functools\.wraps", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"@wraps\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__getattr__", line):
            matches.append((i + 1, line.strip()))

    if has_decorator_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_decorator_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Decorator",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Decorator"]["description"],
        )
    return None


def detect_facade(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Facade pattern"""
    matches = []
    lines = code.split("\n")

    has_facade_class = False
    for class_name in detector.classes:
        if "Facade" in class_name:
            has_facade_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"self\.\w+\s*=.*\(", line) and "def" not in line:
            matches.append((i + 1, line.strip()))

    if has_facade_class:
        return PatternMatch(
            pattern_name="Facade",
            confidence=0.85,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Facade"]["description"],
        )
    return None


def detect_flyweight(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Flyweight pattern"""
    matches = []
    lines = code.split("\n")

    has_flyweight_class = False
    for class_name in detector.classes:
        if "Flyweight" in class_name:
            has_flyweight_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"@lru_cache", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"_flyweights\s*=", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"_pool\s*=", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"_cache\s*=", line):
            matches.append((i + 1, line.strip()))

    if has_flyweight_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_flyweight_class
            else min(0.4 + (len(matches) * 0.2), 0.7)
        )
        return PatternMatch(
            pattern_name="Flyweight",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Flyweight"]["description"],
        )
    return None


def detect_proxy(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Proxy pattern"""
    matches = []
    lines = code.split("\n")

    has_proxy_class = False
    for class_name in detector.classes:
        if "Proxy" in class_name:
            has_proxy_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+__getattr__", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\._real_", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\._subject", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"lazy", line):
            matches.append((i + 1, line.strip()))

    if has_proxy_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_proxy_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Proxy",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Proxy"]["description"],
        )
    return None


def detect_chain_of_responsibility(
    code: str, detector: PatternDetector
) -> Optional[PatternMatch]:
    """Detect Chain of Responsibility pattern"""
    matches = []
    lines = code.split("\n")

    has_handler = False
    for class_name in detector.classes:
        if "Handler" in class_name or "Chain" in class_name:
            has_handler = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+set_next\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+set_successor\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+handle\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\.next_handler", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\.successor", line):
            matches.append((i + 1, line.strip()))

    if has_handler or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_handler
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Chain of Responsibility",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Chain of Responsibility"]["description"],
        )
    return None


def detect_command(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Command pattern"""
    matches = []
    lines = code.split("\n")

    has_command_class = False
    for class_name in detector.classes:
        if "Command" in class_name:
            has_command_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+execute\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+undo\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+redo\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_command_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_command_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Command",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Command"]["description"],
        )
    return None


def detect_iterator(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Iterator pattern"""
    matches = []
    lines = code.split("\n")

    for i, line in enumerate(lines):
        if re.search(r"def\s+__iter__\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__next__\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+__getitem__\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+has_next\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"yield\s+", line):
            matches.append((i + 1, line.strip()))

    if len(matches) >= 2:
        return PatternMatch(
            pattern_name="Iterator",
            confidence=min(0.5 + (len(matches) * 0.2), 0.95),
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Iterator"]["description"],
        )
    return None


def detect_mediator(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Mediator pattern"""
    matches = []
    lines = code.split("\n")

    has_mediator_class = False
    for class_name in detector.classes:
        if "Mediator" in class_name:
            has_mediator_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+notify\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+send\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\._mediator", line):
            matches.append((i + 1, line.strip()))

    if has_mediator_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_mediator_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Mediator",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Mediator"]["description"],
        )
    return None


def detect_memento(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Memento pattern"""
    matches = []
    lines = code.split("\n")

    has_memento_class = False
    for class_name in detector.classes:
        if "Memento" in class_name:
            has_memento_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+save\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+restore\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+get_state\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+set_state\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_memento_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_memento_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Memento",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Memento"]["description"],
        )
    return None


def detect_observer(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Observer pattern"""
    matches = []
    lines = code.split("\n")

    has_observer_class = False
    for class_name in detector.classes:
        if "Observer" in class_name:
            has_observer_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+notify\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+update\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+subscribe\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+add_observer\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"_observers\s*=", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"_listeners\s*=", line):
            matches.append((i + 1, line.strip()))

    if has_observer_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_observer_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Observer",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Observer"]["description"],
        )
    return None


def detect_state(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect State pattern"""
    matches = []
    lines = code.split("\n")

    has_state_class = False
    for class_name in detector.classes:
        if "State" in class_name:
            has_state_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+set_state\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+change_state\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"self\._state\s*=", line):
            matches.append((i + 1, line.strip()))

    if has_state_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_state_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="State",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["State"]["description"],
        )
    return None


def detect_strategy(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Strategy pattern"""
    matches = []
    lines = code.split("\n")

    has_strategy_class = False
    for class_name in detector.classes:
        if "Strategy" in class_name:
            has_strategy_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+execute\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+run\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+set_strategy\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+use_strategy\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_strategy_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_strategy_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Strategy",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Strategy"]["description"],
        )
    return None


def detect_template_method(
    code: str, detector: PatternDetector
) -> Optional[PatternMatch]:
    """Detect Template Method pattern"""
    matches = []
    lines = code.split("\n")

    has_template = False
    for class_name in detector.classes:
        if "Template" in class_name:
            has_template = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+step_\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+hook\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"super\(\)\.", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"@abstractmethod", line):
            matches.append((i + 1, line.strip()))

    if has_template or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_template
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Template Method",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Template Method"]["description"],
        )
    return None


def detect_visitor(code: str, detector: PatternDetector) -> Optional[PatternMatch]:
    """Detect Visitor pattern"""
    matches = []
    lines = code.split("\n")

    has_visitor_class = False
    for class_name in detector.classes:
        if "Visitor" in class_name:
            has_visitor_class = True
            matches.append((1, f"class {class_name}"))

    for i, line in enumerate(lines):
        if re.search(r"def\s+visit_\w+\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+accept\s*\(", line):
            matches.append((i + 1, line.strip()))
        if re.search(r"def\s+visit\s*\(", line):
            matches.append((i + 1, line.strip()))

    if has_visitor_class or len(matches) >= 2:
        confidence = (
            min(0.7 + (len(matches) * 0.1), 0.95)
            if has_visitor_class
            else min(0.4 + (len(matches) * 0.15), 0.7)
        )
        return PatternMatch(
            pattern_name="Visitor",
            confidence=confidence,
            locations=[(m[0], m[0]) for m in matches],
            indicators_found=[m[1] for m in matches],
            description=PATTERN_DEFINITIONS["Visitor"]["description"],
        )
    return None


PATTERN_DETECTORS = {
    "Singleton": detect_singleton,
    "Factory": detect_factory,
    "Abstract Factory": detect_abstract_factory,
    "Builder": detect_builder,
    "Prototype": detect_prototype,
    "Adapter": detect_adapter,
    "Bridge": detect_bridge,
    "Composite": detect_composite,
    "Decorator": detect_decorator_pattern,
    "Facade": detect_facade,
    "Flyweight": detect_flyweight,
    "Proxy": detect_proxy,
    "Chain of Responsibility": detect_chain_of_responsibility,
    "Command": detect_command,
    "Iterator": detect_iterator,
    "Mediator": detect_mediator,
    "Memento": detect_memento,
    "Observer": detect_observer,
    "State": detect_state,
    "Strategy": detect_strategy,
    "Template Method": detect_template_method,
    "Visitor": detect_visitor,
}


def pattern_detector(code: str, options: dict) -> dict:
    """
    Detect design patterns in Python code.

    Args:
        code: Python source code to analyze
        options: Dictionary specifying which patterns to detect
                 {
                     "patterns": ["Singleton", "Factory", ...],  # List of patterns to check
                     "min_confidence": 0.5,  # Minimum confidence threshold
                     "include_opportunities": True  # Include missing opportunities
                 }

    Returns:
        dict: {
            "status": "success" or "error",
            "patterns": {...},
            "pattern_count": {...},
            "missing_opportunities": [...]
        }
    """
    try:
        tree = ast.parse(code)
        detector = PatternDetector()
        detector.visit(tree)

        patterns_to_detect = options.get("patterns", list(PATTERN_DEFINITIONS.keys()))
        min_confidence = options.get("min_confidence", 0.5)
        include_opportunities = options.get("include_opportunities", True)

        detected_patterns = {}
        pattern_count = {}

        for pattern_name in patterns_to_detect:
            if pattern_name in PATTERN_DETECTORS:
                detector_func = PATTERN_DETECTORS[pattern_name]
                result = detector_func(code, detector)

                if result and result.confidence >= min_confidence:
                    detected_patterns[pattern_name] = {
                        "confidence": round(result.confidence, 2),
                        "locations": result.locations,
                        "indicators_found": result.indicators_found[:5],
                        "description": result.description,
                        "category": PATTERN_DEFINITIONS[pattern_name]["category"],
                    }
                    pattern_count[pattern_name] = pattern_count.get(pattern_name, 0) + 1

        missing_opportunities = []
        if include_opportunities:
            for pattern_name, definition in PATTERN_DEFINITIONS.items():
                if pattern_name not in detected_patterns:
                    missing_opportunities.append(
                        {
                            "pattern": pattern_name,
                            "category": definition["category"],
                            "description": definition["description"],
                            "suggestion": f"Consider using {pattern_name} pattern if you need: {definition['description']}",
                        }
                    )

        return {
            "status": "success",
            "patterns": detected_patterns,
            "pattern_count": pattern_count,
            "missing_opportunities": missing_opportunities[:10],
            "summary": {
                "total_patterns_found": len(detected_patterns),
                "categories": {
                    "Creational": sum(
                        1
                        for p in detected_patterns.values()
                        if p["category"] == "Creational"
                    ),
                    "Structural": sum(
                        1
                        for p in detected_patterns.values()
                        if p["category"] == "Structural"
                    ),
                    "Behavioral": sum(
                        1
                        for p in detected_patterns.values()
                        if p["category"] == "Behavioral"
                    ),
                },
            },
        }

    except SyntaxError as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to parse Python code",
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Pattern detection failed",
        }


def invoke(payload: dict) -> dict:
    """Main entry point for MCP skill invocation"""
    code = payload.get("code", "")
    options = payload.get("options", {})

    if not code:
        return {"result": {"status": "error", "message": "No code provided"}}

    result = pattern_detector(code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration"""
    return {
        "name": "pattern-detector",
        "description": "Detect GoF and enterprise design patterns in Python code - identifies Creational (Singleton, Factory, Abstract Factory, Builder, Prototype), Structural (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy), and Behavioral (Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor) patterns with confidence scores",
        "version": "1.0.0",
        "domain": "CODEBASE_INTELLIGENCE",
    }
