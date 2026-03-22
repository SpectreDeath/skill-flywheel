"""Pytest fixtures for Skill Flywheel tests."""

import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_db(temp_dir):
    """Provide a temporary database file path."""
    db_path = temp_dir / "test.db"
    yield str(db_path)
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def mock_env(temp_dir):
    """Provide mock environment variables."""
    env = {
        "DB_PATH": str(temp_dir / "test.db"),
        "SKILLS_DIR": str(temp_dir / "skills"),
        "CACHE_DIR": str(temp_dir / "cache"),
    }
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ.update(env)
        yield env
        for key in env:
            if key in os.environ:
                del os.environ[key]


@pytest.fixture
def sample_skills_dir(temp_dir):
    """Create a directory with sample skill files."""
    skills_dir = temp_dir / "skills"
    skills_dir.mkdir()

    # Create test skills
    for i in range(3):
        skill_file = skills_dir / f"test_skill_{i}.py"
        skill_file.write_text(f"""
def invoke(payload):
    return {{"result": "Result from skill {i}"}}
""")

    yield skills_dir


@pytest.fixture
def test_registry_data():
    """Provide sample registry data."""
    return {
        "skills": [
            {
                "name": f"test-skill-{i}",
                "domain": "Testing",
                "description": f"Test skill {i}",
                "path": f"skills/test_skill_{i}.py",
            }
            for i in range(3)
        ]
    }


@pytest.fixture
def mock_unified_server(temp_db, sample_skills_dir, monkeypatch):
    """Provide a mocked unified server for testing."""
    from flywheel.server.unified_server import UnifiedMCPServer

    # Mock the DB_PATH in the module
    monkeypatch.setattr("flywheel.server.unified_server.DB_PATH", temp_db)

    return UnifiedMCPServer()


@pytest.fixture
def client(mock_unified_server):
    """Provide a test client for the FastAPI app."""
    from fastapi.testclient import TestClient

    return TestClient(mock_unified_server.app)
