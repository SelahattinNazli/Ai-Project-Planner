"""
Basic tests for AI Project Planner
"""

import pytest
from pathlib import Path


def test_project_structure():
    """Test if essential project files exist"""
    assert Path("app.py").exists()
    assert Path("main.py").exists()
    assert Path("Dockerfile").exists()
    assert Path("docker-compose.yml").exists()
    assert Path("pyproject.toml").exists()


def test_config_files():
    """Test if config files exist"""
    assert Path("config/agents.yaml").exists()
    assert Path("config/tasks.yaml").exists()


def test_src_modules():
    """Test if source modules exist"""
    assert Path("src/__init__.py").exists()
    assert Path("src/agents.py").exists()
    assert Path("src/tasks.py").exists()
    assert Path("src/crew.py").exists()
    assert Path("src/models.py").exists()


def test_imports():
    """Test if main modules can be imported"""
    try:
        from src import ProjectPlannerCrew, ProjectPlan
        from src.agents import ProjectAgents
        from src.tasks import ProjectTasks
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_helper_module():
    """Test helper module"""
    from helper import load_env
    # Should not raise error
    load_env()