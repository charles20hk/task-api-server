"""Fixtures for unit tests."""

from datetime import datetime

import pytest

from app.persistence.schemas import Task as PersistenceTask
from app.schemas import CreateTaskRequest, Priority, Task


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
    }


@pytest.fixture
def create_task_request(
    mock_create_task_request_dict: dict,
) -> CreateTaskRequest:
    """Fixture to provide a mock task creation request."""
    return CreateTaskRequest.model_validate(mock_create_task_request_dict)


@pytest.fixture
def mock_saved_task(mock_create_task_request_dict: dict) -> PersistenceTask:
    """Fixture to provide a mock saved task."""
    return PersistenceTask(
        id=1,
        title=mock_create_task_request_dict["title"],
        priority=Priority(mock_create_task_request_dict["priority"]),
        due_date=datetime.fromisoformat(
            mock_create_task_request_dict["due_date"]
        ),
        description=mock_create_task_request_dict["description"],
        completed=False,
    )


@pytest.fixture
def mock_task_response(mock_create_task_request_dict: dict) -> Task:
    """Fixture to provide a mock task."""
    return Task(
        id=1,
        title=mock_create_task_request_dict["title"],
        priority=Priority(mock_create_task_request_dict["priority"]),
        due_date=datetime.fromisoformat(
            mock_create_task_request_dict["due_date"]
        ),
        description=mock_create_task_request_dict["description"],
        completed=False,
    )
