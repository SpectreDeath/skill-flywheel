#!/usr/bin/env python3
"""
spec-to-logic-compiler

Compiles task descriptions and specifications into executable logic programs (DML/Prolog)
for guaranteed execution semantics.
"""

import re
import logging
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def spec_to_logic_compiler(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Core implementation for spec-to-logic-compiler.

    Args:
        payload: Input parameters with source_type, spec_content, output_format, tools

    Returns:
        Result dictionary with compiled DML/Prolog code
    """
    source_type = payload.get("source_type", "markdown")
    spec_content = payload.get("spec_content", "")
    output_format = payload.get("output_format", "dml")
    tools = payload.get("tools", [])

    if not spec_content:
        return {
            "action": "spec-to-logic-compiler",
            "status": "error",
            "message": "No specification content provided",
        }

    if output_format == "dml":
        compiled_code = _compile_to_dml(spec_content, tools)
    else:
        compiled_code = _compile_to_prolog(spec_content, tools)

    execution_order = _extract_execution_order(spec_content)
    guarantees = _identify_guarantees(spec_content)

    return {
        "action": "spec-to-logic-compiler",
        "status": "success",
        "compiled_code": compiled_code,
        "execution_order": execution_order,
        "guarantees": guarantees,
    }


def _compile_to_dml(spec_content: str, tools: List[str]) -> str:
    """Compile markdown specification to DML."""

    lines = spec_content.strip().split("\n")
    title = ""
    steps = []
    arguments = {}

    # Parse markdown structure
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Extract title
        if line.startswith("# "):
            title = line[2:].strip()

        # Extract steps (numbered lists)
        if re.match(r"^\d+\.\s+", line):
            step_text = re.sub(r"^\d+\.\s+", "", line)
            steps.append(step_text)

        # Extract arguments
        if line.startswith("## Arguments") or line.startswith("## Tools"):
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("#"):
                arg_line = lines[i].strip()
                if arg_line.startswith("-"):
                    arg = re.sub(r"^-\s*", "", arg_line)
                    if ":" in arg:
                        key, val = arg.split(":", 1)
                        arguments[key.strip()] = val.strip()
                i += 1
        i += 1

    # Generate DML code
    dml = f"% Compiled from: {title}\n\n"

    # Generate tool definitions
    for tool_name in tools:
        dml += f'tool({tool_name}(Input, Output), "{tool_name} operation") :-\n'
        dml += f"    exec({tool_name}(input: Input), Output).\n\n"

    # Generate main agent predicate
    safe_name = title.replace(" ", "_").lower()
    dml += f"agent_main({_generate_params(arguments)}) :-\n"
    dml += f'    system("You are a {title} assistant."),\n'

    for idx, step in enumerate(steps):
        dml += f'    task("{step}"),\n'

    dml += '    answer("Task completed").\n'

    # Add fallback clause for backtracking
    dml += f"""
agent_main({_generate_params(arguments)}) :-
    system("Attempting with alternative approach..."),
    task("Complete {title} using fallback method"),
    answer("Completed with fallback").
"""

    return dml


def _compile_to_prolog(spec_content: str, tools: List[str]) -> str:
    """Compile specification to plain Prolog."""

    title_match = re.search(r"#\s+(.+)", spec_content)
    title = title_match.group(1) if title_match else "task"

    prolog = f"% Prolog implementation for: {title}\n\n"

    # Generate predicates for each step
    steps = re.findall(r"^\d+\.\s+(.+)$", spec_content, re.MULTILINE)

    for idx, step in enumerate(steps):
        step_name = f"step_{idx + 1}"
        prolog += f"{step_name} :-\n"
        prolog += f'    format("Executing: ~w~n", ["{step}"]),\n'
        prolog += "    true.\n\n"

    # Generate main predicate
    prolog += f"{title.replace(' ', '_').lower()}_main :-\n"
    for step in steps[:-1]:
        prolog += f'    format("~w~n", ["{step}"]),\n'
    prolog += f'    format("~w~n", ["{steps[-1]}"]).'

    return prolog


def _generate_params(arguments: Dict[str, str]) -> str:
    """Generate parameter list from arguments."""
    if not arguments:
        return "Task"
    return ", ".join([f"{k}" for k in arguments.keys()])


def _extract_execution_order(spec_content: str) -> List[str]:
    """Extract ordered steps from specification."""
    steps = re.findall(r"^\d+\.\s+(.+)$", spec_content, re.MULTILINE)
    if not steps:
        # Try bullet points
        steps = re.findall(r"^-\s+(.+)$", spec_content, re.MULTILINE)
    return steps


def _identify_guarantees(spec_content: str) -> List[str]:
    """Identify execution guarantees from spec."""
    guarantees = []

    if "fallback" in spec_content.lower() or "retry" in spec_content.lower():
        guarantees.append("automatic_retry_on_failure")

    if "validate" in spec_content.lower() or "verify" in spec_content.lower():
        guarantees.append("validation_gates")

    if "step" in spec_content.lower() or "then" in spec_content.lower():
        guarantees.append("ordered_execution")

    if "all" in spec_content.lower() or "each" in spec_content.lower():
        guarantees.append("complete_coverage")

    # Default guarantee
    guarantees.append("backtracking_fallback")

    return guarantees


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "process")
    try:
        if action == "compile":
            result = spec_to_logic_compiler(payload)
        else:
            result = {
                "action": "process",
                "status": "success",
                "message": "process completed",
            }

        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }
    except Exception as e:
        logger.error(f"Error in spec-to-logic-compiler: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }


def register_skill() -> Dict[str, str]:
    """Return skill metadata."""
    return {
        "name": "spec-to-logic-compiler",
        "description": "Compiles task descriptions and specifications into executable logic programs (DML/Prolog) for guaranteed execution semantics.",
        "version": "1.0.0",
        "domain": "logic",
    }
