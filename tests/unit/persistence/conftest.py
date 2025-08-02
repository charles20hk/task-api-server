"""Fixtures for persistent unit tests."""

from datetime import datetime

import pytest

from app.persistence.schemas import CreateTaskRequest
from app.persistence.task_repository import TaskRepository
from app.schemas import Priority


@pytest.fixture
def repository() -> TaskRepository:
    """Fixture to create a TaskRepository instance."""
    return TaskRepository("tasks.db")


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
