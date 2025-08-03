"""Unit tests for the TaskRepository class."""

from datetime import datetime
from typing import Generator

import pytest

from app.persistence.schemas import (
    CreateTaskRequest,
    Priority,
    QueryParams,
    Task,
    UpdateTaskRequest,
)
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

    def test_return_tasks_on_query_with_empty_params(
        self,
        repository: TaskRepository,
        mock_due_date: datetime,
        mock_create_task_request_dict: dict,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task."""
        repository.add(mock_create_task_request)

        actual = repository.query(QueryParams())
        assert len(actual) == 1
        assert isinstance(actual[0], Task)
        assert actual[0].title == mock_create_task_request_dict["title"]
        assert actual[0].priority == Priority.MEDIUM
        assert actual[0].due_date == mock_due_date
        assert (
            actual[0].description
            == mock_create_task_request_dict["description"]
        )

    def test_returns_on_query_with_priority(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving tasks by priority."""
        repository.add(mock_create_task_request)
        repository.add(mock_create_task_request)
        tasks = repository.query(QueryParams(priority=Priority.MEDIUM))
        assert len(tasks) == 2
        task_1_data_dict = tasks[0].model_dump()
        task_2_data_dict = tasks[1].model_dump()
        del task_1_data_dict["id"]
        del task_2_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()
        assert task_2_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_query_with_status(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving tasks by completion status."""
        repository.add(mock_create_task_request)
        repository.add(mock_create_task_request)
        tasks = repository.query(QueryParams(completed=False))
        assert len(tasks) == 2
        task_1_data_dict = tasks[0].model_dump()
        task_2_data_dict = tasks[1].model_dump()
        del task_1_data_dict["id"]
        del task_2_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()
        assert task_2_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_query_with_id(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task by its id."""
        task = repository.add(mock_create_task_request)
        actual = repository.query(QueryParams(id=task.id))
        assert isinstance(actual[0], Task)
        assert actual[0].id == task.id
        task_1_data_dict = actual[0].model_dump()
        del task_1_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_query_with_title(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task by title."""
        task = repository.add(mock_create_task_request)
        actual = repository.query(QueryParams(title="Task"))
        assert isinstance(actual[0], Task)
        assert actual[0].id == task.id
        task_1_data_dict = actual[0].model_dump()
        del task_1_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()

    def test_returns_on_query_with_description(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test retrieving a task by description."""
        task = repository.add(mock_create_task_request)
        actual = repository.query(QueryParams(description="description"))
        assert isinstance(actual[0], Task)
        assert actual[0].id == task.id
        task_1_data_dict = actual[0].model_dump()
        del task_1_data_dict["id"]
        assert task_1_data_dict == mock_create_task_request.model_dump()

    def test_delete(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test deleting a task by id."""
        task = repository.add(mock_create_task_request)
        result_before = repository.query(QueryParams(id=task.id))
        assert result_before
        repository.delete(task.id)

        result_after = repository.query(QueryParams(id=task.id))
        assert not result_after

    def test_update_all_fields(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test updating a task."""
        task = repository.add(mock_create_task_request)
        update_request = UpdateTaskRequest(
            title="Updated Title",
            priority=Priority.HIGH,
            due_date=datetime(2023, 12, 31),
            description="Updated Description",
            completed=True,
        )
        repository.update(task.id, update_request)
        updated_task = repository.query(QueryParams(id=task.id))[0]

        assert updated_task.title == update_request.title
        assert updated_task.priority == update_request.priority
        assert updated_task.due_date == update_request.due_date
        assert updated_task.description == update_request.description
        assert updated_task.completed == update_request.completed

    def test_update_some_fields(
        self,
        repository: TaskRepository,
        mock_create_task_request: CreateTaskRequest,
    ) -> None:
        """Test updating a task."""
        task = repository.add(mock_create_task_request)
        update_request = UpdateTaskRequest(
            title="Updated Title",
        )
        repository.update(task.id, update_request)
        updated_task = repository.query(QueryParams(id=task.id))[0]

        assert updated_task.title == update_request.title
        assert updated_task.priority == task.priority
        assert updated_task.due_date == task.due_date
        assert updated_task.description == task.description
        assert updated_task.completed == task.completed

    def test_return_tasks_on_query_with_limit_offset(
        self,
        repository: TaskRepository,
        mock_create_task_request_dict: dict,
    ) -> None:
        """Test retrieving a task."""
        copy_1 = mock_create_task_request_dict.copy()
        copy_1["title"] = "Task 1"
        copy_2 = mock_create_task_request_dict.copy()
        copy_2["title"] = "Task 2"
        copy_3 = mock_create_task_request_dict.copy()
        copy_3["title"] = "Task 3"
        copy_4 = mock_create_task_request_dict.copy()
        copy_4["title"] = "Task 4"
        repository.add(CreateTaskRequest.model_validate(copy_1))
        repository.add(CreateTaskRequest.model_validate(copy_2))
        repository.add(CreateTaskRequest.model_validate(copy_3))
        repository.add(CreateTaskRequest.model_validate(copy_4))

        actual = repository.query(QueryParams(), limit=2, offset=1)
        assert len(actual) == 2

        assert actual[0].title == "Task 2"
        assert actual[1].title == "Task 3"
