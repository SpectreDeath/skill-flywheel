"""
Test Debug Helper

Analyzes test failures to:
- Parse test output and understand failure messages
- Identify failure type (AssertionError, ImportError, Timeout, etc.)
- Analyze root cause of the failure
- Suggest specific code fixes
- Provide plain English explanation
"""

import re
import ast
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class FailureType(Enum):
    ASSERTION_ERROR = "assertion_error"
    IMPORT_ERROR = "import_error"
    SYNTAX_ERROR = "syntax_error"
    TIMEOUT_ERROR = "timeout_error"
    TYPE_ERROR = "type_error"
    ATTRIBUTE_ERROR = "attribute_error"
    VALUE_ERROR = "value_error"
    KEY_ERROR = "key_error"
    INDEX_ERROR = "index_error"
    ZERO_DIVISION_ERROR = "zero_division_error"
    RECURSION_ERROR = "recursion_error"
    MEMORY_ERROR = "memory_error"
    PERMISSION_ERROR = "permission_error"
    FILE_NOT_FOUND_ERROR = "file_not_found_error"
    CONNECTION_ERROR = "connection_error"
    RUNTIME_ERROR = "runtime_error"
    NOT_IMPLEMENTED_ERROR = "not_implemented_error"
    DEPRECATION_WARNING = "deprecation_warning"
    SKIPPED = "skipped"
    XPASS = "xpass"
    XFAIL = "xfail"
    UNKNOWN = "unknown"


@dataclass
class ParsedError:
    error_type: str
    message: str
    line_number: Optional[int]
    file_path: Optional[str]
    traceback: List[str]
    extra_info: Dict[str, Any]


def parse_error_output(error_output: str) -> ParsedError:
    """Parse error output to extract key information."""
    lines = error_output.strip().split("\n")

    error_type = "Unknown"
    message = ""
    line_number = None
    file_path = None
    traceback = []
    extra_info = {}

    for i, line in enumerate(lines):
        traceback.append(line)

        if "Error:" in line or "Exception:" in line or "FAILED" in line:
            match = re.search(
                r"(\w+(?:\.\w+)*(?:Error|Exception|Failure)):?\s*(.*)", line
            )
            if match:
                error_type = match.group(1)
                message = match.group(2).strip()

        match = re.search(r'File\s+"([^"]+)",\s+line\s+(\d+)', line)
        if match:
            file_path = match.group(1)
            line_number = int(match.group(2))

        if "assert" in line.lower():
            extra_info["assertion"] = line.strip()

        if "import" in line.lower() or "ImportError" in line:
            match = re.search(r"import\s+['\"]?(\w+)['\"]?", line)
            if match:
                extra_info["module"] = match.group(1)

        if "timeout" in line.lower():
            extra_info["timeout"] = True

        if "NoneType" in line:
            extra_info["none_type"] = True

        if "None" in line and "is not callable" in line:
            extra_info["not_callable"] = True

    if not message:
        message = lines[-1] if lines else ""

    return ParsedError(
        error_type=error_type,
        message=message,
        line_number=line_number,
        file_path=file_path,
        traceback=traceback,
        extra_info=extra_info,
    )


def identify_failure_type(parsed: ParsedError, test_code: str) -> FailureType:
    """Identify the type of failure from parsed error."""
    error_type_lower = parsed.error_type.lower()
    message_lower = parsed.message.lower()

    if "assert" in error_type_lower or "assert" in message_lower:
        return FailureType.ASSERTION_ERROR

    if "import" in error_type_lower or "importerror" in error_type_lower:
        return FailureType.IMPORT_ERROR

    if "syntax" in error_type_lower:
        return FailureType.SYNTAX_ERROR

    if "timeout" in error_type_lower or "timeout" in message_lower:
        return FailureType.TIMEOUT_ERROR

    if "type" in error_type_lower:
        return FailureType.TYPE_ERROR

    if "attribute" in error_type_lower:
        return FailureType.ATTRIBUTE_ERROR

    if "value" in error_type_lower:
        return FailureType.VALUE_ERROR

    if "key" in error_type_lower:
        return FailureType.KEY_ERROR

    if "index" in error_type_lower:
        return FailureType.INDEX_ERROR

    if "zero" in error_type_lower or "division" in error_type_lower:
        return FailureType.ZERO_DIVISION_ERROR

    if "recursion" in error_type_lower:
        return FailureType.RECURSION_ERROR

    if "memory" in error_type_lower:
        return FailureType.MEMORY_ERROR

    if "permission" in error_type_lower:
        return FailureType.PERMISSION_ERROR

    if "file" in error_type_lower and "not found" in message_lower:
        return FailureType.FILE_NOT_FOUND_ERROR

    if "connection" in error_type_lower or "connectionrefused" in error_type_lower:
        return FailureType.CONNECTION_ERROR

    if "not implemented" in error_type_lower:
        return FailureType.NOT_IMPLEMENTED_ERROR

    if "deprecation" in error_type_lower:
        return FailureType.DEPRECATION_WARNING

    if "skipped" in message_lower:
        return FailureType.SKIPPED

    if "xfail" in message_lower or "xpass" in message_lower:
        return FailureType.XFAIL if "xfail" in message_lower else FailureType.XPASS

    if "runtime" in error_type_lower:
        return FailureType.RUNTIME_ERROR

    return FailureType.UNKNOWN


def analyze_assertion_error(
    parsed: ParsedError, test_code: str
) -> Tuple[str, str, str]:
    """Analyze assertion errors and return root cause, explanation, and fix."""
    message = parsed.message.lower()
    assertion_line = parsed.extra_info.get("assertion", "")

    if "assertEqual" in assertion_line or "assert_equal" in assertion_line:
        return (
            "Values are not equal",
            f"The test expected one value but got another. Expected: 'expected_value', Got: 'actual_value'",
            "Check the expected vs actual values. Verify the function returns the correct value or fix the test expectation.",
        )

    if "assertTrue" in assertion_line or "assert_true" in assertion_line:
        return (
            "Condition evaluated to False",
            "The test expected the condition to be True but it was False",
            "Verify the condition logic in your code returns True when expected.",
        )

    if "assertFalse" in assertion_line or "assert_false" in assertion_line:
        return (
            "Condition evaluated to True",
            "The test expected the condition to be False but it was True",
            "Verify the condition logic in your code returns False when expected.",
        )

    if "assertIsNone" in assertion_line or "assert_none" in assertion_line:
        return (
            "Expected None but got a value",
            "The test expected None but the code returned a non-None value",
            "Ensure the function returns None or fix the test expectation.",
        )

    if "assertIsNotNone" in assertion_line or "assert_is_not_none" in assertion_line:
        return (
            "Expected a value but got None",
            "The test expected a non-None value but got None",
            "Ensure the function returns a valid value instead of None.",
        )

    if "assertIn" in assertion_line or "assert_in" in assertion_line:
        return (
            "Item not found in collection",
            "The test expected an item to be in a collection but it wasn't found",
            "Check if the item exists in the collection or if the collection is populated correctly.",
        )

    if "assertRaises" in assertion_line or "assert_raises" in assertion_line:
        return (
            "Expected exception not raised",
            "The test expected an exception to be raised but it wasn't",
            "Ensure the code raises the expected exception or the test needs adjustment.",
        )

    if "== " in assertion_line:
        match = re.search(r"assert\s+\[?(.+?)\]?\s*==\s*\[?(.+?)\]?", assertion_line)
        if match:
            left = match.group(1).strip()
            right = match.group(2).strip()
            return (
                f"Comparison failed: {left} != {right}",
                f"The values '{left}' and '{right}' are not equal",
                f"Investigate why {left} differs from {right}. Check data types and values.",
            )

    return (
        "Assertion failed",
        parsed.message,
        "Review the assertion and fix either the test expectation or the code being tested.",
    )


def analyze_import_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze import errors and return root cause, explanation, and fix."""
    module = parsed.extra_info.get("module", "unknown module")

    if "No module named" in parsed.message:
        return (
            f"Module '{module}' not installed",
            f"The required module '{module}' is not installed in the environment",
            f"Install the module with: pip install {module}",
        )

    if "cannot import" in parsed.message:
        return (
            f"Cannot import from '{module}'",
            f"The import statement failed - possibly the module or name doesn't exist",
            f"Check if the module exists and exports the correct names. Verify imports are correct.",
        )

    return (
        f"Import error for '{module}'",
        parsed.message,
        "Verify the module is installed and the import path is correct.",
    )


def analyze_type_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze type errors and return root cause, explanation, and fix."""
    message = parsed.message

    if "NoneType" in message:
        if "is not callable" in message:
            return (
                "None is not callable",
                "Attempted to call None as a function. Usually means a variable that should be a function is None.",
                "Ensure the variable is assigned a valid function before calling it. Check for typos in function names.",
            )
        if "'NoneType' object" in message and "subscriptable" in message:
            return (
                "Cannot index None",
                "Attempted to access an index on None (e.g., None[key])",
                "Ensure the variable is initialized with a valid value before indexing.",
            )
        return (
            "NoneType operation error",
            "Operation performed on None which is not valid",
            "Ensure the variable is properly initialized before the operation.",
        )

    if "not support" in message and "operand" in message:
        return (
            "Unsupported operand type",
            "The operation between different types is not supported",
            "Convert types appropriately or use a different operation.",
        )

    if "missing" in message and "argument" in message:
        match = re.search(
            r"missing\s+(\d+)\s+required\s+argument[s]?:\s+['\"](\w+)['\"]", message
        )
        if match:
            return (
                f"Missing {match.group(1)} required argument(s)",
                f"The function call is missing required argument(s)",
                f"Add the required argument(s) to the function call.",
            )

    if "too many" in message and "argument" in message:
        return (
            "Too many arguments",
            "More arguments provided than the function accepts",
            "Remove extra arguments or check if you're calling the wrong function.",
        )

    return (
        "Type error",
        message,
        "Check the types of variables and ensure operations are compatible.",
    )


def analyze_attribute_error(
    parsed: ParsedError, test_code: str
) -> Tuple[str, str, str]:
    """Analyze attribute errors and return root cause, explanation, and fix."""
    message = parsed.message

    match = re.search(r"'(\w+)' object has no attribute '(\w+)'", message)
    if match:
        obj_type = match.group(1)
        attr_name = match.group(2)
        return (
            f"'{obj_type}' has no attribute '{attr_name}'",
            f"The object of type '{obj_type}' doesn't have the attribute '{attr_name}'",
            f"Check if the attribute name is correct or if the object type is what you expect. Verify the attribute exists on the class.",
        )

    if "has no attribute" in message:
        parts = message.split("'")
        if len(parts) >= 4:
            return (
                "Missing attribute",
                message,
                "Verify the attribute name and object type are correct.",
            )

    return ("Attribute error", message, "Check if the attribute exists on the object.")


def analyze_value_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze value errors and return root cause, explanation, and fix."""
    message = parsed.message

    if "empty" in message.lower() and "sequence" in message.lower():
        return (
            "Empty sequence",
            "Attempted to pop from an empty sequence",
            "Add a check for empty sequence before popping, or ensure the sequence has elements.",
        )

    if "too many values to unpack" in message:
        return (
            "Too many values to unpack",
            "More values than variables in unpacking assignment",
            "Ensure the number of variables matches the number of values in the iterable.",
        )

    if "not enough values to unpack" in message:
        return (
            "Not enough values to unpack",
            "Fewer values than variables in unpacking assignment",
            "Ensure the iterable has enough values for all variables.",
        )

    return ("Value error", message, "Check that the value is valid for the operation.")


def analyze_key_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze key errors and return root cause, explanation, and fix."""
    message = parsed.message

    match = re.search(r"KeyError: ['\"](\w+)['\"]", message)
    if match:
        key = match.group(1)
        return (
            f"Key '{key}' not found",
            f"The dictionary does not contain the key '{key}'",
            f"Add the key to the dictionary, use dict.get() with a default, or check if the key exists first.",
        )

    return (
        "Key error",
        message,
        "Check if the key exists in the dictionary before accessing.",
    )


def analyze_index_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze index errors and return root cause, explanation, and fix."""
    message = parsed.message

    if "list index out of range" in message:
        return (
            "List index out of range",
            "Attempted to access an index that doesn't exist in the list",
            "Ensure the index is within bounds (0 to len(list)-1). Add bounds checking.",
        )

    return ("Index error", message, "Check that the index is valid for the sequence.")


def analyze_timeout_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze timeout errors and return root cause, explanation, and fix."""
    return (
        "Test timeout",
        "The test took too long to complete and was terminated",
        "Optimize the code being tested, increase the timeout setting, or check for infinite loops.",
    )


def analyze_syntax_error(parsed: ParsedError, test_code: str) -> Tuple[str, str, str]:
    """Analyze syntax errors and return root cause, explanation, and fix."""
    message = parsed.message

    if "invalid syntax" in message:
        return (
            "Invalid syntax",
            "The code has a syntax error that prevents it from being parsed",
            "Check for missing brackets, quotes, colons, or other syntax issues.",
        )

    return ("Syntax error", message, "Fix the syntax error in the code.")


def analyze_root_cause(
    parsed: ParsedError, failure_type: FailureType, test_code: str
) -> Tuple[str, str, str]:
    """Analyze the root cause based on failure type."""

    if failure_type == FailureType.ASSERTION_ERROR:
        return analyze_assertion_error(parsed, test_code)

    if failure_type == FailureType.IMPORT_ERROR:
        return analyze_import_error(parsed, test_code)

    if failure_type == FailureType.TYPE_ERROR:
        return analyze_type_error(parsed, test_code)

    if failure_type == FailureType.ATTRIBUTE_ERROR:
        return analyze_attribute_error(parsed, test_code)

    if failure_type == FailureType.VALUE_ERROR:
        return analyze_value_error(parsed, test_code)

    if failure_type == FailureType.KEY_ERROR:
        return analyze_key_error(parsed, test_code)

    if failure_type == FailureType.INDEX_ERROR:
        return analyze_index_error(parsed, test_code)

    if failure_type == FailureType.TIMEOUT_ERROR:
        return analyze_timeout_error(parsed, test_code)

    if failure_type == FailureType.SYNTAX_ERROR:
        return analyze_syntax_error(parsed, test_code)

    if failure_type == FailureType.SKIPPED:
        return (
            "Test skipped",
            "The test was skipped (possibly due to @skip decorator or condition)",
            "Remove the skip decorator or fix the skip condition.",
        )

    if failure_type == FailureType.XFAIL:
        return (
            "Expected failure",
            "The test was expected to fail and did fail",
            "This is expected behavior. Remove @xfail if the issue is fixed.",
        )

    if failure_type == FailureType.XPASS:
        return (
            "Unexpected pass",
            "The test was expected to fail but passed",
            "The issue may be fixed. Consider removing @xfail decorator.",
        )

    return (
        "Unknown error",
        parsed.message,
        "Review the error message and traceback to identify the issue.",
    )


def generate_debug_steps(
    failure_type: FailureType, parsed: ParsedError, test_code: str
) -> List[str]:
    """Generate debug steps based on failure type."""
    steps = [
        "1. Review the error message and traceback",
        "2. Identify the failing line in the code",
        "3. Check the types of all variables involved",
    ]

    if failure_type == FailureType.ASSERTION_ERROR:
        steps.extend(
            [
                "4. Print the actual vs expected values",
                "5. Verify the function logic produces correct output",
                "6. Check test expectations are correct",
            ]
        )

    elif failure_type == FailureType.IMPORT_ERROR:
        steps.extend(
            [
                "4. Verify the module is installed: pip list | grep <module>",
                "5. Check the Python path: import sys; print(sys.path)",
                "6. Try importing the module directly in Python shell",
            ]
        )

    elif failure_type in [
        FailureType.TYPE_ERROR,
        FailureType.ATTRIBUTE_ERROR,
        FailureType.VALUE_ERROR,
    ]:
        steps.extend(
            [
                "4. Add print statements to check variable types",
                "5. Use type hints to verify expected types",
                "6. Add debugging output before the error line",
            ]
        )

    elif failure_type == FailureType.TIMEOUT_ERROR:
        steps.extend(
            [
                "4. Add timing to identify slow operations",
                "5. Check for infinite loops",
                "6. Consider using pytest-timeout plugin",
            ]
        )

    elif failure_type == FailureType.KEY_ERROR:
        steps.extend(
            [
                "4. Print the dictionary keys to verify key exists",
                "5. Use dict.get() with default instead of []",
                "6. Add check: if key in dict: ...",
            ]
        )

    elif failure_type == FailureType.INDEX_ERROR:
        steps.extend(
            [
                "4. Print the list length and index",
                "5. Add bounds check: if index < len(list): ...",
                "6. Consider using enumerate() or for-in loop",
            ]
        )

    steps.append("7. Run the test in isolation to confirm the issue")

    return steps


def test_debug_helper(error_output: str, test_code: str, options: dict) -> dict:
    """
    Main function to analyze test failures.

    Args:
        error_output: The test failure output
        test_code: The test code that failed
        options: Language, framework (e.g., {"language": "python", "framework": "pytest"})

    Returns:
        dict with:
        - status: "success" or "error"
        - failure_type: Type of failure
        - root_cause: Identified root cause
        - explanation: Plain English explanation
        - suggested_fix: Code change suggestion
        - debug_steps: Steps to debug further
    """
    if not error_output:
        return {"status": "error", "message": "No error output provided"}

    try:
        parsed = parse_error_output(error_output)
        failure_type = identify_failure_type(parsed, test_code)
        root_cause, explanation, suggested_fix = analyze_root_cause(
            parsed, failure_type, test_code
        )
        debug_steps = generate_debug_steps(failure_type, parsed, test_code)

        return {
            "status": "success",
            "failure_type": failure_type.value,
            "root_cause": root_cause,
            "explanation": explanation,
            "suggested_fix": suggested_fix,
            "debug_steps": debug_steps,
            "parsed_details": {
                "error_type": parsed.error_type,
                "message": parsed.message,
                "line_number": parsed.line_number,
                "file_path": parsed.file_path,
                "extra_info": parsed.extra_info,
            },
        }

    except Exception as e:
        return {"status": "error", "message": f"Failed to analyze error: {str(e)}"}


def invoke(payload: dict) -> dict:
    """
    Main entry point for the skill.

    Args:
        payload: dict with error_output, test_code, options

    Returns:
        dict with analysis result
    """
    error_output = payload.get("error_output", "")
    test_code = payload.get("test_code", "")
    options = payload.get("options", {})

    if not error_output:
        return {"status": "error", "message": "No error_output provided"}

    result = test_debug_helper(error_output, test_code, options)
    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "test-debug-helper",
        "description": "Analyzes test failures to identify root cause, explain errors, and suggest fixes",
        "version": "1.0.0",
        "domain": "TESTING_QUALITY",
        "capabilities": [
            "test_output_parsing",
            "failure_type_identification",
            "root_cause_analysis",
            "error_explanation",
            "fix_suggestion",
            "debug_steps_generation",
        ],
    }
