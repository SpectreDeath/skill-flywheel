import functools
import logging
from collections.abc import Callable
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, TypeVar, Union

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ErrorCode(str, Enum):
    """Standard error codes for Skill Flywheel."""

    SKILL_NOT_FOUND = "SKILL_NOT_FOUND"
    SKILL_LOAD_ERROR = "SKILL_LOAD_ERROR"
    SKILL_EXECUTION_ERROR = "SKILL_EXECUTION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    REGISTRY_ERROR = "REGISTRY_ERROR"
    ORCHESTRATION_ERROR = "ORCHESTRATION_ERROR"
    EVOLUTION_ERROR = "EVOLUTION_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class SkillFlywheelError(Exception):
    """Base exception for all Skill Flywheel errors."""

    def __init__(
        self,
        message: str,
        error_code: Union[ErrorCode, str] = ErrorCode.UNKNOWN_ERROR,
        details: Dict[str, Any] | None = None,
    ):
        self.message = message
        self.error_code = (
            error_code if isinstance(error_code, str) else error_code.value
        )
        self.details = details or {}
        self.timestamp = datetime.now(timezone.utc).isoformat()
        super().__init__(self.message)

    def __str__(self) -> str:
        base_msg = f"[{self.error_code}] {self.message}"
        if self.details:
            base_msg += f" | Details: {self.details}"
        return base_msg

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for serialization."""
        return {
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp,
            "exception_type": self.__class__.__name__,
        }


class SkillNotFoundError(SkillFlywheelError):
    """Raised when a requested skill does not exist."""

    def __init__(
        self,
        message: str = "Skill not found",
        skill_name: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        if skill_name:
            message = f"Skill '{skill_name}' not found"
        error_details = details or {}
        if skill_name:
            error_details["skill_name"] = skill_name
        super().__init__(
            message=message,
            error_code=ErrorCode.SKILL_NOT_FOUND,
            details=error_details,
        )


class SkillLoadError(SkillFlywheelError):
    """Raised when a skill fails to load."""

    def __init__(
        self,
        message: str = "Failed to load skill",
        skill_name: str | None = None,
        reason: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if skill_name:
            error_details["skill_name"] = skill_name
        if reason:
            error_details["reason"] = reason
        if skill_name:
            message = f"Failed to load skill '{skill_name}'"
            if reason:
                message += f": {reason}"
        super().__init__(
            message=message,
            error_code=ErrorCode.SKILL_LOAD_ERROR,
            details=error_details,
        )


class SkillExecutionError(SkillFlywheelError):
    """Raised when skill execution fails."""

    def __init__(
        self,
        message: str = "Skill execution failed",
        skill_name: str | None = None,
        execution_context: Dict[str, Any] | None = None,
        cause: Exception | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if skill_name:
            error_details["skill_name"] = skill_name
        if execution_context:
            error_details["execution_context"] = execution_context
        if cause:
            error_details["cause"] = str(cause)
            error_details["cause_type"] = type(cause).__name__
        if skill_name:
            message = f"Skill '{skill_name}' execution failed"
            if cause:
                message += f": {cause}"
        super().__init__(
            message=message,
            error_code=ErrorCode.SKILL_EXECUTION_ERROR,
            details=error_details,
        )


class ValidationError(SkillFlywheelError):
    """Raised when validation fails."""

    def __init__(
        self,
        message: str = "Validation failed",
        field: str | None = None,
        value: Any | None = None,
        constraint: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if field:
            error_details["field"] = field
        if value is not None:
            error_details["value"] = str(value)
        if constraint:
            error_details["constraint"] = constraint
        if field:
            message = f"Validation failed for field '{field}'"
            if constraint:
                message += f": {constraint}"
        super().__init__(
            message=message,
            error_code=ErrorCode.VALIDATION_ERROR,
            details=error_details,
        )


class ConfigurationError(SkillFlywheelError):
    """Raised when a configuration error occurs."""

    def __init__(
        self,
        message: str = "Configuration error",
        config_key: str | None = None,
        config_path: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if config_key:
            error_details["config_key"] = config_key
        if config_path:
            error_details["config_path"] = config_path
        if config_key:
            message = f"Configuration error for key '{config_key}'"
        super().__init__(
            message=message,
            error_code=ErrorCode.CONFIGURATION_ERROR,
            details=error_details,
        )


class RegistryError(SkillFlywheelError):
    """Raised when a registry operation fails."""

    def __init__(
        self,
        message: str = "Registry operation failed",
        operation: str | None = None,
        registry_path: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if operation:
            error_details["operation"] = operation
        if registry_path:
            error_details["registry_path"] = registry_path
        if operation:
            message = f"Registry operation '{operation}' failed"
        super().__init__(
            message=message,
            error_code=ErrorCode.REGISTRY_ERROR,
            details=error_details,
        )


class OrchestrationError(SkillFlywheelError):
    """Raised when agent orchestration fails."""

    def __init__(
        self,
        message: str = "Agent orchestration failed",
        agent_id: str | None = None,
        workflow_id: str | None = None,
        step: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if agent_id:
            error_details["agent_id"] = agent_id
        if workflow_id:
            error_details["workflow_id"] = workflow_id
        if step:
            error_details["failed_step"] = step
        if agent_id or workflow_id:
            message = "Agent orchestration failed"
            if agent_id:
                message += f" for agent '{agent_id}'"
            if workflow_id:
                message += f" in workflow '{workflow_id}'"
        super().__init__(
            message=message,
            error_code=ErrorCode.ORCHESTRATION_ERROR,
            details=error_details,
        )


class EvolutionError(SkillFlywheelError):
    """Raised when skill evolution fails."""

    def __init__(
        self,
        message: str = "Skill evolution failed",
        skill_name: str | None = None,
        evolution_stage: str | None = None,
        details: Dict[str, Any] | None = None,
    ):
        error_details = details or {}
        if skill_name:
            error_details["skill_name"] = skill_name
        if evolution_stage:
            error_details["evolution_stage"] = evolution_stage
        if skill_name:
            message = f"Evolution failed for skill '{skill_name}'"
            if evolution_stage:
                message += f" at stage '{evolution_stage}'"
        super().__init__(
            message=message,
            error_code=ErrorCode.EVOLUTION_ERROR,
            details=error_details,
        )


T = TypeVar("T")


def error_handler(
    default_message: str = "An error occurred",
    error_code: Union[ErrorCode, str] = ErrorCode.UNKNOWN_ERROR,
    reraise: bool = True,
    log_level: str = "error",
) -> Callable[[Callable[..., T]], Callable[..., T | None]]:
    """
    Decorator for standardized error handling.

    Args:
        default_message: Default error message if none provided
        error_code: Error code to use for the exception
        reraise: Whether to re-raise the exception after logging
        log_level: Logging level for the error ('debug', 'info', 'warning', 'error', 'critical')

    Returns:
        Decorated function with standardized error handling

    Example:
        @error_handler(default_message="Failed to process skill", error_code=ErrorCode.SKILL_EXECUTION_ERROR)
        def process_skill(skill_name: str):
            ...
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T | None]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T | None:
            log_func = getattr(logger, log_level.lower(), logger.error)
            try:
                return func(*args, **kwargs)
            except SkillFlywheelError:
                raise
            except ValidationError:
                raise
            except Exception as e:
                error_msg = str(e) if str(e) else default_message
                error_details = {"function": func.__name__}
                if args:
                    error_details["args"] = str(args)[:200]
                if kwargs:
                    error_details["kwargs"] = str(kwargs)[:200]

                log_func(f"{error_msg}: {e}", exc_info=True)

                if reraise:
                    raise SkillFlywheelError(
                        message=error_msg,
                        error_code=error_code,
                        details=error_details,
                    ) from e
                return None

        return wrapper

    return decorator


class ErrorResponse(BaseModel):
    """Pydantic model for API error responses."""

    error_code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: Dict[str, Any] = Field(
        default_factory=dict, description="Additional error details"
    )
    timestamp: str = Field(..., description="ISO timestamp of when the error occurred")
    exception_type: str | None = Field(
        None, description="Type of exception that was raised"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "error_code": "SKILL_NOT_FOUND",
                "message": "Skill 'unknown_skill' not found",
                "details": {"skill_name": "unknown_skill"},
                "timestamp": "2024-01-15T10:30:00Z",
                "exception_type": "SkillNotFoundError",
            }
        }
    }

    @classmethod
    def from_exception(cls, exc: SkillFlywheelError) -> "ErrorResponse":
        """Create ErrorResponse from a SkillFlywheelError exception."""

if __name__ == "__main__":
    return cls(
                error_code=exc.error_code,
                message=exc.message,
                details=exc.details,
                timestamp=exc.timestamp,
                exception_type=exc.__class__.__name__,
            )