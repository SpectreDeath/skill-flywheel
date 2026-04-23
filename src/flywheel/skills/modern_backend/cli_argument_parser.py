#!/usr/bin/env python3
"""
CLI Argument Parser Builder

Creates structured CLI argument parsers with subcommands,
argument validation, and grouped help output.

Pattern extracted from Claw Code's build_parser() function.
"""

import argparse
import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def build_subcommand(
    parent: argparse.ArgumentParser,
    name: str,
    help_text: str,
    arguments: Optional[List[Dict[str, Any]]] = None,
) -> argparse.ArgumentParser:
    """Add a subcommand with optional arguments to a parser."""
    subparsers_action = None
    for action in parent._subparsers._actions:
        if isinstance(action, argparse._SubParsersAction):
            subparsers_action = action
            break

    if subparsers_action is None:
        subparsers_action = parent.add_subparsers(dest='command', required=True)

    subparser = subparsers_action.add_parser(name, help=help_text)

    if arguments:
        for arg in arguments:
            arg_name = arg.pop('name')
            subparser.add_argument(arg_name, **arg)

    return subparser


def create_cli_parser(
    title: str = "CLI Parser",
    description: str = "",
    subcommands: Optional[List[Dict[str, Any]]] = None
) -> argparse.ArgumentParser:
    """
    Create a CLI argument parser with subcommands.

    Args:
        title: Parser title
        description: Parser description
        subcommands: List of subcommand definitions

    Returns:
        Configured ArgumentParser
    """
    parser = argparse.ArgumentParser(
        prog=title.lower().replace(' ', '-'),
        description=description or title
    )

    if subcommands:
        subparsers = parser.add_subparsers(dest='command')

        for cmd in subcommands:
            subparser = subparsers.add_parser(
                cmd['name'],
                help=cmd.get('help', '')
            )

            for arg in cmd.get('arguments', []):
                arg_copy = dict(arg)
                arg_name = arg_copy.pop('name')
                subparser.add_argument(arg_name, **arg_copy)

    return parser


def parse_arguments(parser: argparse.ArgumentParser, args: Optional[List[str]] = None) -> Dict[str, Any]:
    """Parse arguments and return as dictionary."""
    try:
        namespace = parser.parse_args(args)
        return vars(namespace)
    except SystemExit:
        return {"error": "Invalid arguments"}


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """MCP skill invocation."""
    action = payload.get("action", "build_parser")

    if action == "build_parser":
        title = payload.get("title", "CLI Tool")
        description = payload.get("description", "")
        subcommands = payload.get("subcommands", [])

        parser = create_cli_parser(title, description, subcommands)

        return {
            "result": {
                "title": title,
                "description": description,
                "subcommand_count": len(subcommands),
                "subcommands": [cmd.get('name', '') for cmd in subcommands]
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "parse":
        args_str = payload.get("args", [])
        subcommands = payload.get("subcommands", [])
        title = payload.get("title", "CLI Tool")

        parser = create_cli_parser(title, "", subcommands)
        result = parse_arguments(parser, args_str)

        return {
            "result": result,
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    elif action == "validate_args":
        required = payload.get("required", [])
        provided = payload.get("provided", {})

        missing = [r for r in required if r not in provided]

        return {
            "result": {
                "valid": len(missing) == 0,
                "missing_args": missing,
                "provided_count": len(provided),
                "required_count": len(required)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }

    else:
        return {
            "result": {"error": f"Unknown action: {action}"},
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat(),
            },
        }


def register_skill():
    """Return skill metadata."""

if __name__ == "__main__":
    return {
            "name": "cli-argument-parser",
            "description": "Build structured CLI argument parsers with subcommands, validation, and grouped help output",
            "version": "1.0.0",
            "domain": "MODERN_BACKEND",
        }