"""
PyTest configuration and shared fixtures for teamresumes tests.

This module provides common fixtures and configuration used across
all test modules in the teamresumes test suite.
"""

import os
import tempfile
import pytest
from pathlib import Path
from typing import Generator, Dict, Any


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """Provide path to test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_resume_data() -> Dict[str, Any]:
    """Provide sample resume data for testing."""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-123-4567",
        "address": {
            "street": "123 Main St",
            "city": "Anytown",
            "state": "CA",
            "zip": "12345"
        },
        "experience": [
            {
                "title": "Senior Developer",
                "company": "Tech Corp",
                "start_date": "2020-01-01",
                "end_date": "2023-12-31",
                "description": "Developed software solutions"
            }
        ],
        "education": [
            {
                "degree": "Bachelor of Science",
                "field": "Computer Science",
                "school": "University of Technology",
                "graduation_year": 2019
            }
        ],
        "skills": ["Python", "JavaScript", "SQL", "Git"]
    }


@pytest.fixture
def mock_file_system(temp_dir: Path) -> Dict[str, Path]:
    """Set up a mock file system structure for testing."""
    structure = {
        "input": temp_dir / "input",
        "output": temp_dir / "output",
        "templates": temp_dir / "templates",
        "cache": temp_dir / "cache"
    }

    for path in structure.values():
        path.mkdir(parents=True, exist_ok=True)

    return structure


@pytest.fixture
def env_vars() -> Generator[None, None, None]:
    """Set up test environment variables."""
    original_env = os.environ.copy()

    # Set test environment variables
    test_env = {
        "TESTING": "true",
        "LOG_LEVEL": "DEBUG",
        "CACHE_ENABLED": "false"
    }

    os.environ.update(test_env)

    try:
        yield
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)


@pytest.fixture(autouse=True)
def isolate_tests():
    """Automatically isolate each test to prevent side effects."""
    # This fixture runs automatically for every test
    # Add any cleanup or isolation logic here
    yield
    # Cleanup after test
    pass


# Performance testing helpers
@pytest.fixture
def performance_threshold():
    """Define performance thresholds for tests."""
    return {
        "max_execution_time": 5.0,  # seconds
        "max_memory_usage": 100,    # MB
        "max_file_operations": 1000
    }


# Mock external dependencies
@pytest.fixture
def mock_external_apis():
    """Mock external API calls for testing."""
    # Add mock setup for external APIs when needed
    return {}