"""Unit tests for the TaskRepository class."""

from datetime import datetime
from typing import Generator

import pytest

from app.persistence.exception import NotFoundError
from app.persistence.schemas import CreateTaskRequest, Priority, Task
from app.persistence.task_repository import TaskRepository


class TestTaskRepository:
    """Tests for the TaskRepository class."""

    @pytest.fixture(autouse=True)
    def cleanup(
        self, repository: TaskRepository
    ) -> Generator[None, None, None]:
        """Cleanup the database before each test."""
        yield
        with repository._get_connection() as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()

    def test_task_added(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test adding a task to the repository."""
        actual = repository.add(mock_create_task_request)
        assert isinstance(actual, Task)
        assert actual.title == mock_create_task_request.title
        assert actual.priority == mock_create_task_request.priority
        assert actual.due_date == mock_create_task_request.due_date
        assert actual.description == mock_create_task_request.description
        assert actual.completed == mock_create_task_request.completed
        assert actual.id

    def test_return_task_on_get(
        self,
        repository: TaskRepository,
        mock_due_date: datetime,
        mock_create_task_request_dict: dict,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task."""
        repository.add(mock_create_task_request)

        actual = repository.get({"title": "Test Task"})
        assert len(actual) == 1
        assert isinstance(actual[0], Task)
        assert actual[0].title == mock_create_task_request_dict["title"]
        assert actual[0].priority == Priority.MEDIUM
        assert actual[0].due_date == mock_due_date
        assert (
            actual[0].description
            == mock_create_task_request_dict["description"]
        )

    def test_returns_on_get_by_priority(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving tasks by priority."""
        repository.add(mock_create_task_request)
        repository.add(mock_create_task_request)
        tasks = repository.get_by_priority(Priority.MEDIUM)
        assert len(tasks) == 2
        task_1_data_dict = tasks[0].model_dump()
        task_2_data_dict = tasks[1].model_dump()
        del task_1_data_dict["id"]
        del task_2_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()
        assert task_2_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_get_by_status(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving tasks by completion status."""
        repository.add(mock_create_task_request)
        repository.add(mock_create_task_request)
        tasks = repository.get_by_status(False)
        assert len(tasks) == 2
        task_1_data_dict = tasks[0].model_dump()
        task_2_data_dict = tasks[1].model_dump()
        del task_1_data_dict["id"]
        del task_2_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()
        assert task_2_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_get_by_id(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task by its id."""
        task = repository.add(mock_create_task_request)
        actual = repository.get_by_id(task.id)
        assert isinstance(actual, Task)
        assert actual.id == task.id
        task_1_data_dict = actual.model_dump()
        del task_1_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()

    def test_raise_not_found_on_get_by_id(
        self, repository: TaskRepository
    ) -> None:
        """Test raising NotFoundError when task is not found by id."""
        with pytest.raises(NotFoundError):
            repository.get_by_id(999)

    def test_delete(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test deleting a task by id."""
        task = repository.add(mock_create_task_request)
        result = repository.get_by_id(task.id)
        assert result
        repository.delete(task.id)
        with pytest.raises(NotFoundError):
            repository.get_by_id(task.id)
