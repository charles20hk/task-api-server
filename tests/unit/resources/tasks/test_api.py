"""Unit tests for the tasks API endpoint."""

from unittest.mock import MagicMock, create_autospec

import pytest

from app.controllers.task import TaskController
from app.schemas import CreateTaskRequest, Priority, Task, TaskQueryParams
from app.web.resources.tasks.api import create_task, query


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

    @pytest.fixture
    def query_params(self) -> TaskQueryParams:
        """Fixture to provide a mock task query parameters."""
        return TaskQueryParams(completed=True, priority=Priority.HIGH.value)

    @pytest.mark.anyio
    async def test_controller_get_called_on_get_task(
        self,
        mock_task_controller: MagicMock,
        query_params: TaskQueryParams,
        mock_task_response: Task,
    ) -> None:
        """Test that get is called on the task controller...

        when retrieving a task.
        """
        mock_task_controller.get.return_value = mock_task_response
        result = await query(query_params, mock_task_controller)
        mock_task_controller.get.assert_called_once_with(query_params)
        assert result == mock_task_response
