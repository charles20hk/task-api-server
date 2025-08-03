"""Unit tests for the TaskController class."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from app.controllers.exception import NotFoundError
from app.controllers.task import TaskController
from app.persistence.schemas import QueryParams
from app.persistence.schemas import Task as PersistenceTask
from app.schemas import (
    CreateTaskRequest,
    Priority,
    Task,
    TaskQueryParams,
    UpdateTaskRequest,
)


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

    def test_return_on_get_without_params(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        mock_due_date: datetime,
        mock_saved_task: PersistenceTask,
        mock_task_response: Task,
    ) -> None:
        """Test that get returns a list of Task objects."""
        task_repository.query.return_value = [mock_saved_task]
        actual = controller.get(TaskQueryParams())
        task = Task(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=mock_due_date,
            description="Test description",
            completed=False,
        )
        expected = [task]
        task_repository.query.assert_called_once_with(QueryParams())
        assert expected == actual

    def test_return_on_get_with_params(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        mock_due_date: datetime,
        mock_saved_task: PersistenceTask,
    ) -> None:
        """Test that get returns a list of Task objects."""
        task_repository.query.return_value = [mock_saved_task]
        actual = controller.get(
            TaskQueryParams(
                priority=Priority.MEDIUM.value,
                completed=False,
            )
        )
        task = Task(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=mock_due_date,
            description="Test description",
            completed=False,
        )
        expected = [task]
        task_repository.query.assert_called_once_with(
            QueryParams(priority=Priority.MEDIUM, completed=False)
        )
        assert expected == actual

    def test_return_on_get_by_id(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        mock_due_date: datetime,
        mock_saved_task: PersistenceTask,
    ) -> None:
        """Test that get_by_id returns a Task object."""
        task_repository.query.return_value = [mock_saved_task]
        actual = controller.get_by_id(1)
        expected = Task(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=mock_due_date,
            description="Test description",
            completed=False,
        )
        task_repository.query.assert_called_once_with(QueryParams(id=1))
        assert expected == actual

    def test_raise_not_found_error_on_get_by_id(
        self,
        controller: TaskController,
        task_repository: MagicMock,
    ) -> None:
        """Test that get_by_id raises Not Found Error when no task is found."""
        task_repository.query.return_value = []
        with pytest.raises(NotFoundError):
            controller.get_by_id(1)

    def test_raise_not_found_error_on_update(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        update_task_request: UpdateTaskRequest,
    ) -> None:
        """Test that update raises Not Found Error when no task is found."""
        task_repository.query.return_value = []
        with pytest.raises(NotFoundError):
            controller.update(1, update_task_request)

    def test_return_on_update(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        update_task_request: UpdateTaskRequest,
        mock_saved_task: PersistenceTask,
        updated_task: Task,
    ) -> None:
        """Test that update returns an updated Task object."""
        task_repository.query.side_effect = [[mock_saved_task], [updated_task]]
        task_repository.update.return_value = None

        actual = controller.update(1, update_task_request)

        assert actual == updated_task
        task_repository.update.assert_called_once()

    def test_raise_not_found_error_on_delete(
        self,
        controller: TaskController,
        task_repository: MagicMock,
    ) -> None:
        """Test that delete raises Not Found Error when no task is found."""
        task_repository.query.return_value = []
        with pytest.raises(NotFoundError):
            controller.delete(1)

    def test_repo_delete_called_on_delete(
        self,
        controller: TaskController,
        task_repository: MagicMock,
        mock_saved_task: PersistenceTask,
    ) -> None:
        """Test that delete calls the repository's delete method."""
        task_repository.query.return_value = [mock_saved_task]
        task_repository.delete.return_value = None
        controller.delete(1)
        task_repository.delete.assert_called_once_with(id=1)
