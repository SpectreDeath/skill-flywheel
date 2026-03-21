"""
Unit tests for exceptions module (error classes, handlers)
"""

import logging
import os
import sys
from unittest.mock import MagicMock, Mock, patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flywheel.core.exceptions import (
    ConfigurationError,
    ErrorCode,
    ErrorResponse,
    EvolutionError,
    OrchestrationError,
    RegistryError,
    SkillExecutionError,
    SkillFlywheelError,
    SkillLoadError,
    SkillNotFoundError,
    ValidationError,
    error_handler,
)


class TestErrorCode:
    """Tests for ErrorCode enum."""

    def test_error_code_values(self):
        """Test ErrorCode enum values."""
        assert ErrorCode.SKILL_NOT_FOUND.value == "SKILL_NOT_FOUND"
        assert ErrorCode.SKILL_LOAD_ERROR.value == "SKILL_LOAD_ERROR"
        assert ErrorCode.SKILL_EXECUTION_ERROR.value == "SKILL_EXECUTION_ERROR"
        assert ErrorCode.VALIDATION_ERROR.value == "VALIDATION_ERROR"
        assert ErrorCode.CONFIGURATION_ERROR.value == "CONFIGURATION_ERROR"
        assert ErrorCode.REGISTRY_ERROR.value == "REGISTRY_ERROR"
        assert ErrorCode.ORCHESTRATION_ERROR.value == "ORCHESTRATION_ERROR"
        assert ErrorCode.EVOLUTION_ERROR.value == "EVOLUTION_ERROR"
        assert ErrorCode.UNKNOWN_ERROR.value == "UNKNOWN_ERROR"

    def test_error_code_is_string(self):
        """Test ErrorCode can be used as string."""
        code = ErrorCode.SKILL_NOT_FOUND
        assert isinstance(code, str)
        assert code == "SKILL_NOT_FOUND"


class TestSkillFlywheelError:
    """Tests for SkillFlywheelError base class."""

    def test_basic_error(self):
        """Test basic error creation."""
        error = SkillFlywheelError("Test error")
        assert error.message == "Test error"
        assert error.error_code == "UNKNOWN_ERROR"
        assert error.details == {}

    def test_error_with_code(self):
        """Test error with custom error code."""
        error = SkillFlywheelError("Test error", error_code=ErrorCode.SKILL_NOT_FOUND)
        assert error.error_code == "SKILL_NOT_FOUND"

    def test_error_with_string_code(self):
        """Test error with string error code."""
        error = SkillFlywheelError("Test error", error_code="CUSTOM_CODE")
        assert error.error_code == "CUSTOM_CODE"

    def test_error_with_details(self):
        """Test error with details dict."""
        details = {"key": "value", "count": 5}
        error = SkillFlywheelError("Test error", details=details)
        assert error.details == details

    def test_error_str_representation(self):
        """Test error string representation."""
        error = SkillFlywheelError(
            "Test error", error_code="TEST_CODE", details={"key": "value"}
        )
        error_str = str(error)
        assert "[TEST_CODE] Test error" in error_str
        assert "key" in error_str

    def test_error_to_dict(self):
        """Test error to_dict method."""
        error = SkillFlywheelError(
            "Test error", error_code="TEST_CODE", details={"key": "value"}
        )
        error_dict = error.to_dict()

        assert error_dict["error_code"] == "TEST_CODE"
        assert error_dict["message"] == "Test error"
        assert error_dict["details"] == {"key": "value"}
        assert "timestamp" in error_dict
        assert error_dict["exception_type"] == "SkillFlywheelError"

    def test_error_timestamp_is_isoformat(self):
        """Test that timestamp is in ISO format."""
        error = SkillFlywheelError("Test error")
        assert "T" in error.timestamp
        assert (
            "Z" in error.timestamp
            or "+" in error.timestamp
            or error.timestamp.endswith(":")
        )


class TestSkillNotFoundError:
    """Tests for SkillNotFoundError."""

    def test_default_message(self):
        """Test default error message."""
        error = SkillNotFoundError()
        assert error.message == "Skill not found"
        assert error.error_code == "SKILL_NOT_FOUND"

    def test_with_skill_name(self):
        """Test error with skill name."""
        error = SkillNotFoundError(skill_name="my_skill")
        assert "my_skill" in error.message
        assert error.details["skill_name"] == "my_skill"

    def test_with_custom_message(self):
        """Test error with custom message (without skill_name)."""
        error = SkillNotFoundError(message="Custom not found")
        assert error.message == "Custom not found"


class TestSkillLoadError:
    """Tests for SkillLoadError."""

    def test_default_message(self):
        """Test default error message."""
        error = SkillLoadError()
        assert "Failed to load skill" in error.message
        assert error.error_code == "SKILL_LOAD_ERROR"

    def test_with_skill_name(self):
        """Test error with skill name."""
        error = SkillLoadError(skill_name="bad_skill", reason="Import error")
        assert "bad_skill" in error.message
        assert error.details["skill_name"] == "bad_skill"
        assert error.details["reason"] == "Import error"

    def test_with_reason(self):
        """Test error with reason."""
        error = SkillLoadError(skill_name="test", reason="Syntax error")
        assert error.details["reason"] == "Syntax error"


class TestSkillExecutionError:
    """Tests for SkillExecutionError."""

    def test_default_message(self):
        """Test default error message."""
        error = SkillExecutionError()
        assert "execution failed" in error.message.lower()
        assert error.error_code == "SKILL_EXECUTION_ERROR"

    def test_with_skill_name_and_cause(self):
        """Test error with skill name and cause."""
        cause = ValueError("Invalid input")
        error = SkillExecutionError(skill_name="test_skill", cause=cause)

        assert "test_skill" in error.message
        assert error.details["skill_name"] == "test_skill"
        assert error.details["cause"] == "Invalid input"
        assert error.details["cause_type"] == "ValueError"

    def test_with_execution_context(self):
        """Test error with execution context."""
        context = {"step": 2, "total_steps": 5}
        error = SkillExecutionError(execution_context=context)
        assert error.details["execution_context"] == context


class TestValidationError:
    """Tests for ValidationError."""

    def test_default_message(self):
        """Test default error message."""
        error = ValidationError()
        assert "Validation failed" in error.message
        assert error.error_code == "VALIDATION_ERROR"

    def test_with_field(self):
        """Test error with field name."""
        error = ValidationError(field="username", constraint="must be alphanumeric")
        assert "username" in error.message
        assert error.details["field"] == "username"
        assert error.details["constraint"] == "must be alphanumeric"

    def test_with_value(self):
        """Test error with value."""
        error = ValidationError(field="age", value=-5, constraint="must be positive")
        assert error.details["value"] == "-5"


class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_default_message(self):
        """Test default error message."""
        error = ConfigurationError()
        assert error.error_code == "CONFIGURATION_ERROR"

    def test_with_config_key(self):
        """Test error with config key."""
        error = ConfigurationError(config_key="database_url")
        assert "database_url" in error.message
        assert error.details["config_key"] == "database_url"

    def test_with_config_path(self):
        """Test error with config path."""
        error = ConfigurationError(config_path="/config/database.json")
        assert error.details["config_path"] == "/config/database.json"


class TestRegistryError:
    """Tests for RegistryError."""

    def test_default_message(self):
        """Test default error message."""
        error = RegistryError()
        assert error.error_code == "REGISTRY_ERROR"

    def test_with_operation(self):
        """Test error with operation."""
        error = RegistryError(operation="register", registry_path="/skills")
        assert "register" in error.message
        assert error.details["operation"] == "register"


class TestOrchestrationError:
    """Tests for OrchestrationError."""

    def test_default_message(self):
        """Test default error message."""
        error = OrchestrationError()
        assert error.error_code == "ORCHESTRATION_ERROR"

    def test_with_agent_and_workflow(self):
        """Test error with agent and workflow."""
        error = OrchestrationError(
            agent_id="agent_1", workflow_id="workflow_1", step="execute"
        )
        assert "agent_1" in error.message
        assert "workflow_1" in error.message
        assert error.details["agent_id"] == "agent_1"
        assert error.details["workflow_id"] == "workflow_1"
        assert error.details["failed_step"] == "execute"


class TestEvolutionError:
    """Tests for EvolutionError."""

    def test_default_message(self):
        """Test default error message."""
        error = EvolutionError()
        assert error.error_code == "EVOLUTION_ERROR"

    def test_with_skill_and_stage(self):
        """Test error with skill name and stage."""
        error = EvolutionError(skill_name="my_skill", evolution_stage="mutation")
        assert "my_skill" in error.message
        assert "mutation" in error.message
        assert error.details["skill_name"] == "my_skill"
        assert error.details["evolution_stage"] == "mutation"


class TestErrorResponse:
    """Tests for ErrorResponse Pydantic model."""

    def test_create_error_response(self):
        """Test creating ErrorResponse."""
        response = ErrorResponse(
            error_code="SKILL_NOT_FOUND",
            message="Skill not found",
            details={"skill_name": "test"},
            timestamp="2024-01-15T10:30:00Z",
            exception_type="SkillNotFoundError",
        )

        assert response.error_code == "SKILL_NOT_FOUND"
        assert response.message == "Skill not found"
        assert response.details == {"skill_name": "test"}

    def test_error_response_from_exception(self):
        """Test creating ErrorResponse from exception."""
        exc = SkillNotFoundError(skill_name="test_skill")
        response = ErrorResponse.from_exception(exc)

        assert response.error_code == "SKILL_NOT_FOUND"
        assert response.message == "Skill 'test_skill' not found"
        assert response.details["skill_name"] == "test_skill"
        assert response.exception_type == "SkillNotFoundError"

    def test_error_response_json_schema(self):
        """Test ErrorResponse JSON schema."""
        response = ErrorResponse(
            error_code="TEST", message="Test message", timestamp="2024-01-15T10:30:00Z"
        )

        json_data = response.model_dump()
        assert "error_code" in json_data
        assert "message" in json_data
        assert "timestamp" in json_data

    def test_error_response_default_details(self):
        """Test ErrorResponse default details."""
        response = ErrorResponse(
            error_code="TEST", message="Test message", timestamp="2024-01-15T10:30:00Z"
        )

        assert response.details == {}


class TestErrorHandlerDecorator:
    """Tests for error_handler decorator."""

    def test_error_handler_reraises_skillflywheel_errors(self):
        """Test that SkillFlywheelError is re-raised."""

        @error_handler()
        def raises_skill_error():
            raise SkillFlywheelError("Custom error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            raises_skill_error()
        assert "Custom error" in str(exc_info.value)

    def test_error_handler_reraises_validation_errors(self):
        """Test that ValidationError is re-raised."""

        @error_handler()
        def raises_validation_error():
            raise ValidationError(field="test")

        with pytest.raises(ValidationError):
            raises_validation_error()

    def test_error_handler_wraps_generic_exception(self):
        """Test that generic exceptions are wrapped."""

        @error_handler(
            default_message="Wrapped error", error_code=ErrorCode.SKILL_EXECUTION_ERROR
        )
        def raises_generic():
            raise ValueError("Original error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            raises_generic()

        assert "Original error" in str(exc_info.value)
        assert exc_info.value.error_code == "SKILL_EXECUTION_ERROR"

    def test_error_handler_includes_function_name(self):
        """Test that function name is included in details."""

        @error_handler(default_message="Error", error_code=ErrorCode.UNKNOWN_ERROR)
        def my_function():
            raise RuntimeError("Error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            my_function()

        assert "my_function" in exc_info.value.details["function"]

    def test_error_handler_with_custom_code_string(self):
        """Test error_handler with string error code."""

        @error_handler(error_code="CUSTOM_ERROR")
        def raises_error():
            raise Exception("Error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            raises_error()

        assert exc_info.value.error_code == "CUSTOM_ERROR"

    def test_error_handler_reraise_false(self):
        """Test error_handler with reraise=False returns None."""

        @error_handler(default_message="Error", reraise=False)
        def raises_error():
            raise ValueError("Original")

        result = raises_error()
        assert result is None

    def test_error_handler_logs_error(self, caplog):
        """Test that error_handler logs the error."""

        @error_handler(default_message="Error", log_level="error")
        def raises_error():
            raise ValueError("Original error")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(SkillFlywheelError):
                raises_error()

        assert any("Original error" in record.message for record in caplog.records)

    def test_error_handler_preserves_exception_chain(self):
        """Test that exception chain is preserved."""
        original = ValueError("Original cause")

        @error_handler(default_message="Error")
        def raises_error():
            raise original

        with pytest.raises(SkillFlywheelError) as exc_info:
            raises_error()

        assert exc_info.value.__cause__ is original

    def test_error_handler_with_args_in_details(self):
        """Test that args are included in error details."""

        @error_handler(default_message="Error")
        def func_with_args(a, b):
            raise RuntimeError("Error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            func_with_args(1, 2)

        assert "args" in exc_info.value.details

    def test_error_handler_with_kwargs_in_details(self):
        """Test that kwargs are included in error details."""

        @error_handler(default_message="Error")
        def func_with_kwargs(x=1, y=2):
            raise RuntimeError("Error")

        with pytest.raises(SkillFlywheelError) as exc_info:
            func_with_kwargs(x=10)

        assert "kwargs" in exc_info.value.details

    def test_error_handler_successful_execution(self):
        """Test error_handler with successful execution."""

        @error_handler(default_message="Error")
        def successful_func():
            return "success"

        result = successful_func()
        assert result == "success"
