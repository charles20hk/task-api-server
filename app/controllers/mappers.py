"""Mapper functions for task-related data."""

from app.persistence.schemas import (
    CreateTaskRequest as PersistenceCreateTaskRequest,
)
from app.persistence.schemas import Task as PersistenceTask
from app.persistence.schemas import (
    UpdateTaskRequest as PersistenceUpdateTaskRequest,
)
from app.schemas import CreateTaskRequest, Task, UpdateTaskRequest


class UpdateRequestToPersistenceMapper:
    """Mapper functions for task-related data."""

    @staticmethod
    def convert(
        update_task_request: UpdateTaskRequest,
    ) -> PersistenceUpdateTaskRequest:
        """Convert an UpdateTaskRequest to a PersistenceUpdateTaskRequest."""
        update_task_request_dict = update_task_request.model_dump(
            exclude_unset=True
        )

        data = {}
        if "title" in update_task_request_dict:
            data["title"] = update_task_request_dict["title"]
        if "priority" in update_task_request_dict:
            data["priority"] = update_task_request_dict["priority"]
        if "due_date" in update_task_request_dict:
            data["due_date"] = update_task_request_dict["due_date"]
        if "description" in update_task_request_dict:
            data["description"] = update_task_request_dict["description"]
        if "completed" in update_task_request_dict:
            data["completed"] = update_task_request_dict["completed"]

        return PersistenceUpdateTaskRequest.model_validate(data)


class PersistenceToTaskMapper:
    """Mapper functions for converting persistence models to API models."""

    @staticmethod
    def convert(persistence_task: PersistenceTask) -> Task:
        """Convert a PersistenceTask to a Task."""
        return Task(
            id=persistence_task.id,
            title=persistence_task.title,
            priority=persistence_task.priority,
            due_date=persistence_task.due_date,
            description=persistence_task.description,
            completed=persistence_task.completed,
        )


class CreateRequestToPersistenceMapper:
    """Mapper functions for converting create request to persistence model."""

    @staticmethod
    def convert(
        create_task_request: CreateTaskRequest,
    ) -> PersistenceCreateTaskRequest:
        """Convert a CreateTaskRequest to a PersistenceCreateTaskRequest."""
        return PersistenceCreateTaskRequest(
            title=create_task_request.title,
            priority=create_task_request.priority,
            due_date=create_task_request.due_date,
            description=create_task_request.description,
            completed=False,  # Default value for new tasks
        )
