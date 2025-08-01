"""Fixtures for persistent unit tests."""

import sqlite3
from datetime import datetime

import pytest

from app.persistence.schema import CreateTaskRequest, Priority
from app.persistence.task_repository import TaskRepository


@pytest.fixture
def conn() -> sqlite3.Connection:
    """Fixture to create an in-memory SQLite connection."""
    return sqlite3.connect(":memory:")


@pytest.fixture
def repository(conn: sqlite3.Connection) -> TaskRepository:
    """Fixture to create a TaskRepository instance."""
    repo = TaskRepository(conn)
    return repo


@pytest.fixture
def mock_due_date() -> datetime:
    """Fixture to provide a mock due date."""
    return datetime(2023, 12, 31, 12, 0, 0)


@pytest.fixture
def mock_create_task_request_dict(mock_due_date: datetime) -> dict:
    """Fixture to provide a mock task creation request dictionary."""
    return {
        "title": "Test Task",
        "priority": Priority.MEDIUM.value,
        "due_date": mock_due_date.isoformat(),
        "description": "Test description",
        "completed": False,
    }


@pytest.fixture
def mock_create_task_request(
    mock_create_task_request_dict: dict,
) -> CreateTaskRequest:
    """Fixture to provide a mock task creation request."""
    return CreateTaskRequest.model_validate(mock_create_task_request_dict)
