"""Fixtures for controller unit tests."""

from unittest.mock import MagicMock, create_autospec

import pytest

from app.persistence.task_repository import TaskRepository


@pytest.fixture
def task_repository() -> MagicMock:
    """Fixture to provide a mock TaskRepository."""
    return create_autospec(TaskRepository)
