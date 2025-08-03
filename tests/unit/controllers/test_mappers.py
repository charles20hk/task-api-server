"""Unit tests for UpdateRequestToPersistenceMapper."""

from datetime import date

from app.controllers.mappers import (
    CreateRequestToPersistenceMapper,
    PersistenceToTaskMapper,
    UpdateRequestToPersistenceMapper,
)
from app.persistence.schemas import (
    CreateTaskRequest as PersistenceCreateTaskRequest,
)
from app.persistence.schemas import Task as PersistenceTask
from app.persistence.schemas import (
    UpdateTaskRequest as PersistenceUpdateTaskRequest,
)
from app.schemas import CreateTaskRequest, Priority, Task, UpdateTaskRequest


class TestUpdateRequestToPersistenceMapper:
    """Tests for UpdateRequestToPersistenceMapper."""

    def test_convert_with_all_fields(self) -> None:
        """Test convert method with all fields."""
        update_request = UpdateTaskRequest(
            title="New Title",
            priority=Priority.MEDIUM,
            due_date=date(2023, 12, 31),
            description="Updated description",
            completed=True,
        )
        actual = UpdateRequestToPersistenceMapper.convert(update_request)
        expected = PersistenceUpdateTaskRequest(
            title="New Title",
            priority=Priority.MEDIUM,
            due_date=date(2023, 12, 31),
            description="Updated description",
            completed=True,
        )
        assert actual == expected

    def test_convert_with_partial_fields(self) -> None:
        """Test convert method with partial fields."""
        update_request = UpdateTaskRequest(
            title="New Title", priority=Priority.MEDIUM
        )
        actual = UpdateRequestToPersistenceMapper.convert(update_request)
        expected = PersistenceUpdateTaskRequest(
            title="New Title",
            priority=Priority.MEDIUM,
        )
        assert actual == expected


class TestPersistenceToTaskMapper:
    """Tests for PersistenceToTaskMapper."""

    def test_convert(self) -> None:
        """Test convert method."""
        persistence_task = PersistenceTask(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=date(2023, 12, 31),
            description="Test description",
            completed=False,
        )
        actual = PersistenceToTaskMapper.convert(persistence_task)
        expected = Task(
            id=1,
            title="Test Task",
            priority=Priority.MEDIUM,
            due_date=date(2023, 12, 31),
            description="Test description",
            completed=False,
        )
        assert actual == expected


class TestCreateRequestToPersistenceMapper:
    """Tests for CreateRequestToPersistenceMapper."""

    def test_convert(self) -> None:
        """Test convert method."""
        create_request = CreateTaskRequest(
            title="New Task",
            priority=Priority.HIGH,
            due_date=date(2023, 12, 31),
            description="Task description",
        )
        actual = CreateRequestToPersistenceMapper.convert(create_request)
        expected = PersistenceCreateTaskRequest(
            title="New Task",
            priority=Priority.HIGH,
            due_date=date(2023, 12, 31),
            description="Task description",
            completed=False,  # Default value for new tasks
        )
        assert actual == expected
