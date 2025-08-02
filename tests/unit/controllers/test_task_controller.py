"""Unit tests for the TaskController class."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.controllers.task import TaskController
from app.persistence.schemas import Task as PersistenceTask
from app.schemas import CreateTaskRequest, Priority, Task


class TestTaskController:
    """Test suite for the TaskController class."""

    @pytest.fixture
    def controller(self, task_repository: MagicMock) -> TaskController:
        """Fixture to provide a TaskController instance."""
        return TaskController(task_repository)

    def test_return_on_create(
        self,
        controller: TaskController,
        create_task_request: CreateTaskRequest,
        task_repository: MagicMock,
        mock_due_date: datetime,
        mock_saved_task: PersistenceTask,
    ) -> None:
        """Test that create_task returns a Task object."""
        task_repository.add.return_value = mock_saved_task
        actual = controller.create(create_task_request)
        expected = Task(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=mock_due_date,
            description="Test description",
            completed=False,
        )
        assert expected == actual
