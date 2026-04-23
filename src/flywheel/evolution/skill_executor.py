from __future__ import annotations

import asyncio
import importlib
import importlib.util
import inspect
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Type

from .evaluator import SkillExecutor

logger = logging.getLogger(__name__)


class SkillExecutionError(Exception):
    """Raised when skill execution fails."""

    pass


class SkillNotFoundError(Exception):
    """Raised when a skill cannot be found."""

    pass


class SkillMetadata:
    """Metadata about a loaded skill."""

    def __init__(
        self,
        name: str,
        description: str,
        version: str,
        domain: str,
        file_path: Path,
    ):
        self.name = name
        self.description = description
        self.version = version
        self.domain = domain
        self.file_path = file_path

    def __repr__(self) -> str:
        return f"SkillMetadata(name={self.name!r}, version={self.version!r})"


class ExecutionResult:
    """Result of skill execution with metadata."""

    def __init__(
        self,
        success: bool,
        output: Any,
        skill_name: str,
        execution_time_ms: float,
        error: str | None = None,
        parameters_used: Dict[str, Any] | None = None,
    ):
        self.success = success
        self.output = output
        self.skill_name = skill_name
        self.execution_time_ms = execution_time_ms
        self.error = error
        self.parameters_used = parameters_used or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "output": self.output,
            "skill_name": self.skill_name,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "parameters_used": self.parameters_used,
        }


class SkillLoader:
    """Loads skills from the skills directory with caching."""

    def __init__(self, skills_dir: Path | None = None):
        if skills_dir is None:
            skills_dir = Path(__file__).parent.parent.parent / "skills"
        self.skills_dir = Path(skills_dir)
        self._cache: Dict[str, Type] = {}
        self._metadata_cache: Dict[str, SkillMetadata] = {}

    def discover_skills(self) -> List[str]:
        """Discover all available skill names."""
        skill_names = []
        if not self.skills_dir.exists():
            logger.warning(f"Skills directory does not exist: {self.skills_dir}")
            return skill_names

        for file_path in self.skills_dir.rglob("*.py"):
            if (
                file_path.name.startswith("_")
                or file_path.name == "test_integration.py"
            ):
                continue

            module_name = self._get_module_name_from_path(file_path)
            if module_name:
                skill_names.append(module_name)

        return skill_names

    def _get_module_name_from_path(self, file_path: Path) -> str | None:
        """Convert file path to skill module name."""
        try:
            rel_path = file_path.relative_to(self.skills_dir)
            parts = list(rel_path.parts)
            if parts[-1] == "__init__.py":
                return None
            if parts[-1] != "__init__.py":
                parts[-1] = parts[-1][:-3]
            return ".".join(parts)
        except ValueError:
            return None

    def load_skill(self, skill_name: str) -> Type:
        """Load a skill module by name with caching."""
        if skill_name in self._cache:
            return self._cache[skill_name]

        try:
            module = self._import_skill_module(skill_name)
            self._cache[skill_name] = module
            return module
        except Exception as e:
            raise SkillNotFoundError(f"Could not load skill '{skill_name}': {e}")

    def _import_skill_module(self, skill_name: str) -> Type:
        """Import a skill module from the skills directory."""
        if "." in skill_name:
            parts = skill_name.split(".")
            file_path = self.skills_dir / Path(*parts).with_suffix(".py")
        else:
            file_path = self.skills_dir / f"{skill_name}.py"

        if not file_path.exists():
            file_path = self.skills_dir / skill_name / "__init__.py"

        if not file_path.exists():
            raise SkillNotFoundError(f"Skill file not found: {skill_name}")

        spec = importlib.util.spec_from_file_location(skill_name, file_path)
        if spec is None or spec.loader is None:
            raise SkillNotFoundError(f"Could not load spec for skill: {skill_name}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def get_skill_metadata(self, skill_name: str) -> SkillMetadata:
        """Get metadata for a skill."""
        if skill_name in self._metadata_cache:
            return self._metadata_cache[skill_name]

        module = self.load_skill(skill_name)

        if hasattr(module, "register_skill"):
            metadata = module.register_skill()
        else:
            metadata = {
                "name": skill_name,
                "description": "Unknown skill",
                "version": "0.0.0",
                "domain": "UNKNOWN",
            }

        if "." in skill_name:
            parts = skill_name.split(".")
            file_path = self.skills_dir / Path(*parts).with_suffix(".py")
        else:
            file_path = self.skills_dir / f"{skill_name}.py"

        if not file_path.exists():
            file_path = self.skills_dir / skill_name / "__init__.py"

        skill_metadata = SkillMetadata(
            name=metadata.get("name", skill_name),
            description=metadata.get("description", ""),
            version=metadata.get("version", "0.0.0"),
            domain=metadata.get("domain", "UNKNOWN"),
            file_path=file_path,
        )

        self._metadata_cache[skill_name] = skill_metadata
        return skill_metadata

    def list_skills_metadata(self) -> List[SkillMetadata]:
        """List metadata for all discoverable skills."""
        skill_names = self.discover_skills()
        metadata_list = []
        for name in skill_names:
            try:
                metadata_list.append(self.get_skill_metadata(name))
            except SkillNotFoundError:
                continue
        return metadata_list

    def is_skill_available(self, skill_name: str) -> bool:
        """Check if a skill is available."""
        try:
            self.load_skill(skill_name)
            return True
        except SkillNotFoundError:
            return False

    def clear_cache(self) -> None:
        """Clear the skill cache."""
        self._cache.clear()
        self._metadata_cache.clear()


class RealSkillExecutor(SkillExecutor):
    """Real implementation of SkillExecutor that executes actual skills."""

    def __init__(
        self,
        skill_loader: SkillLoader | None = None,
        skills_dir: Path | None = None,
        default_timeout_ms: float = 30000,
    ):
        self.skill_loader = skill_loader or SkillLoader(skills_dir)
        self.default_timeout_ms = default_timeout_ms
        self._execution_history: List[ExecutionResult] = []

    async def execute(
        self, skill_name: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a skill with given input and parameters."""
        start_time = time.time()

        try:
            module = self.skill_loader.load_skill(skill_name)

            if not hasattr(module, "invoke"):
                raise SkillExecutionError(
                    f"Skill '{skill_name}' does not have an 'invoke' function"
                )

            invoke_func = module.invoke

            payload = {
                **input_data,
                **parameters,
            }

            if inspect.iscoroutinefunction(invoke_func):
                result = await invoke_func(payload)
            else:
                result = invoke_func(payload)

            execution_time_ms = (time.time() - start_time) * 1000

            success = result.get("status") != "error"

            execution_result = ExecutionResult(
                success=success,
                output=result,
                skill_name=skill_name,
                execution_time_ms=execution_time_ms,
                parameters_used=parameters,
                error=result.get("error") if not success else None,
            )

            self._execution_history.append(execution_result)

            return {
                "success": success,
                "output": result,
                "skill_name": skill_name,
                "execution_time_ms": execution_time_ms,
                "parameters": parameters,
            }

        except SkillNotFoundError as e:
            execution_time_ms = (time.time() - start_time) * 1000
            error_result = ExecutionResult(
                success=False,
                output=None,
                skill_name=skill_name,
                execution_time_ms=execution_time_ms,
                error=str(e),
                parameters_used=parameters,
            )
            self._execution_history.append(error_result)
            return {
                "success": False,
                "error": str(e),
                "skill_name": skill_name,
                "failure_category": "not_found",
                "execution_time_ms": execution_time_ms,
            }

        except Exception as e:
            execution_time_ms = (time.time() - start_time) * 1000
            logger.exception(f"Error executing skill '{skill_name}'")
            error_result = ExecutionResult(
                success=False,
                output=None,
                skill_name=skill_name,
                execution_time_ms=execution_time_ms,
                error=str(e),
                parameters_used=parameters,
            )
            self._execution_history.append(error_result)
            return {
                "success": False,
                "error": str(e),
                "skill_name": skill_name,
                "failure_category": "execution_error",
                "execution_time_ms": execution_time_ms,
            }

    def execute_sync(
        self, skill_name: str, input_data: Dict[str, Any], parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Synchronous version of execute."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(
                    loop.run_until_complete,
                    self.execute(skill_name, input_data, parameters),
                )
                return future.result()
        else:
            return loop.run_until_complete(
                self.execute(skill_name, input_data, parameters)
            )

    def get_execution_history(self) -> List[ExecutionResult]:
        """Get the execution history."""
        return self._execution_history.copy()

    def clear_history(self) -> None:
        """Clear execution history."""
        self._execution_history.clear()

    def list_available_skills(self) -> List[str]:
        """List all available skill names."""
        return self.skill_loader.discover_skills()

    def get_skill_info(self, skill_name: str) -> SkillMetadata | None:
        """Get metadata for a skill."""
        try:
            return self.skill_loader.get_skill_metadata(skill_name)
        except SkillNotFoundError:
            return None


def create_real_executor(
    skills_dir: Path | None = None, default_timeout_ms: float = 30000
) -> RealSkillExecutor:
    """Factory function to create a RealSkillExecutor with default settings."""
    return RealSkillExecutor(
        skill_loader=SkillLoader(skills_dir),
        default_timeout_ms=default_timeout_ms,
    )


def get_skill_from_registry(skill_name: str) -> Any:
    """Import and return a skill module from the skills package."""

if __name__ == "__main__":
    try:
            import src.skills

            skills_path = Path(src.skills.__file__).parent

            loader = SkillLoader(skills_path)
            return loader.load_skill(skill_name)
        except Exception as e:
            raise SkillNotFoundError(
                f"Could not load skill '{skill_name}' from registry: {e}"
            )