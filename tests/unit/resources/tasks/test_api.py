"""Unit tests for the tasks API endpoint."""

from unittest.mock import MagicMock, create_autospec, patch

import pytest
from fastapi import HTTPException

from app.controllers.exception import NotFoundError
from app.controllers.task import TaskController
from app.schemas import (
    CreateTaskRequest,
    Priority,
    Task,
    TaskQueryParams,
    UpdateTaskRequest,
)
from app.web.resources.tasks.api import (
    create_task,
    delete_task,
    get_task_by_id,
    query,
    update_task,
)
from app.web.resources.tasks.schemas import GetTasksResponse, Pagination


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
    async def test_controller_get_called_on_query(
        self,
        mock_task_controller: MagicMock,
        query_params: TaskQueryParams,
        mock_task_response: Task,
    ) -> None:
        """Test that get is called on the task controller...

        when retrieving a task.
        """
        mock_task_controller.get.return_value = ([mock_task_response], 1)
        mock_request = MagicMock(url="http://testserver/tasks")
        with patch(
            "app.web.resources.tasks.api.PaginationBuilder.create"
        ) as mock_pagination_builder_create:
            mock_pagination = Pagination(
                count=1,
                total_pages=1,
                previous_page_url=None,
                next_page_url=None,
            )
            mock_pagination_builder_create.return_value = mock_pagination

            actual = await query(
                query=query_params,
                task_controller=mock_task_controller,
                request=mock_request,
            )
            mock_task_controller.get.assert_called_once_with(query_params)
            expected = GetTasksResponse(
                tasks=[mock_task_response],
                pagination=mock_pagination,
            )
            assert actual == expected

    @pytest.mark.anyio
    async def test_controller_get_by_id_called_on_get_task_by_id(
        self,
        mock_task_controller: MagicMock,
        mock_task_response: Task,
    ) -> None:
        """Test that get is called on the task controller...

        when retrieving a task.
        """
        mock_task_controller.get_by_id.return_value = mock_task_response
        result = await get_task_by_id(1, mock_task_controller)
        mock_task_controller.get_by_id.assert_called_once_with(1)
        assert result == mock_task_response

    @pytest.mark.anyio
    async def test_raise_404_on_get_task_by_id_when_not_found(
        self,
        mock_task_controller: MagicMock,
        mock_task_response: Task,
    ) -> None:
        """Test that HTTPException is raised with 404 status code...

        when task is not found.
        """
        mock_task_controller.get_by_id.side_effect = NotFoundError(1)
        with pytest.raises(HTTPException) as exc_info:
            await get_task_by_id(1, mock_task_controller)
        assert exc_info.value.status_code == 404

    @pytest.mark.anyio
    async def test_raise_404_on_update_task_when_not_found(
        self,
        mock_task_controller: MagicMock,
        update_task_request: UpdateTaskRequest,
    ) -> None:
        """Test that HTTPException is raised with 404 status code...

        when task is not found.
        """
        mock_task_controller.update.side_effect = NotFoundError(1)
        with pytest.raises(HTTPException) as exc_info:
            await update_task(1, update_task_request, mock_task_controller)
        assert exc_info.value.status_code == 404

    @pytest.mark.anyio
    async def test_returns_on_update_task(
        self,
        mock_task_controller: MagicMock,
        update_task_request: UpdateTaskRequest,
        updated_task: Task,
    ) -> None:
        """Test that update is called on the task controller...

        when updating a task.
        """
        mock_task_controller.update.return_value = updated_task
        result = await update_task(
            1, update_task_request, mock_task_controller
        )
        mock_task_controller.update.assert_called_once_with(
            id=1, update_task_request=update_task_request
        )
        assert result == updated_task

    @pytest.mark.anyio
    async def test_raise_404_on_delete_task_when_not_found(
        self,
        mock_task_controller: MagicMock,
    ) -> None:
        """Test that HTTPException is raised with 404 status code...

        when task is not found.
        """
        mock_task_controller.delete.side_effect = NotFoundError(1)
        with pytest.raises(HTTPException) as exc_info:
            await delete_task(1, mock_task_controller)
        assert exc_info.value.status_code == 404

    @pytest.mark.anyio
    async def test_returns_on_delete_task(
        self,
        mock_task_controller: MagicMock,
    ) -> None:
        """Test that delete is called on the task controller...

        when deleting a task.
        """
        mock_task_controller.delete.return_value = None
        result = await delete_task(1, mock_task_controller)
        mock_task_controller.delete.assert_called_once_with(1)
        assert result.message == "Task deleted successfully"
