"""Unit tests for the tasks API endpoint."""

from unittest.mock import MagicMock, create_autospec

import pytest

from app.controllers.task import TaskController
from app.schemas import CreateTaskRequest, Task
from app.web.resources.tasks.api import create_task


class TestCreateTaskAPI:
    """Tests for the create_task API endpoint."""

    @pytest.fixture
    def mock_task_controller(self) -> MagicMock:
        """Fixture to provide a mock task controller."""
        return create_autospec(TaskController)

    @pytest.mark.anyio
    async def test_create_called_on_create_task(
        self,
        mock_task_controller: MagicMock,
        create_task_request: CreateTaskRequest,
        mock_task_response: Task,
    ) -> None:
        """Test that create is called on the task controller...

        when creating a task.
        """
        mock_task_controller.create.return_value = mock_task_response
        result = await create_task(create_task_request, mock_task_controller)
        mock_task_controller.create.assert_called_once()
        assert result == mock_task_response
