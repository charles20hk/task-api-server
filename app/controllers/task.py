"""Task controller module."""

from app.persistence.schemas import (
    CreateTaskRequest as PersistenceCreateTaskRequest,
)
from app.persistence.task_repository import TaskRepository
from app.schemas import CreateTaskRequest, Task


class TaskController:
    """Controller for managing tasks."""

    def __init__(self, task_repository: TaskRepository) -> None:
        """Initialize the TaskController with a task repository."""
        self.task_repository = task_repository

    def create(self, create_task_request: CreateTaskRequest) -> Task:
        """Create a new task."""
        persistence_request = PersistenceCreateTaskRequest(
            title=create_task_request.title,
            priority=create_task_request.priority,
            due_date=create_task_request.due_date,
            description=create_task_request.description,
            completed=False,
        )

        saved_task = self.task_repository.add(persistence_request)
        return Task(
            id=saved_task.id,
            title=saved_task.title,
            priority=saved_task.priority,
            due_date=saved_task.due_date,
            description=saved_task.description,
            completed=saved_task.completed,
        )
