"""Task controller module."""

from app.controllers.exception import NotFoundError
from app.persistence.schemas import (
    CreateTaskRequest as PersistenceCreateTaskRequest,
)
from app.persistence.schemas import (
    QueryParams,
)
from app.persistence.schemas import Task as PersistenceTask
from app.persistence.task_repository import TaskRepository
from app.schemas import CreateTaskRequest, Task, TaskQueryParams


class TaskController:
    """Controller for managing tasks."""

    def __init__(self, task_repository: TaskRepository) -> None:
        """Initialize the TaskController with a task repository."""
        self.task_repository = task_repository

    def _convert_persistence_to_task(
        self, saved_task: PersistenceTask
    ) -> Task:
        """Convert a PersistenceTask to a Task."""
        return Task(
            id=saved_task.id,
            title=saved_task.title,
            priority=saved_task.priority,
            due_date=saved_task.due_date,
            description=saved_task.description,
            completed=saved_task.completed,
        )

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
        return self._convert_persistence_to_task(saved_task)

    def get(self, task_query_params: TaskQueryParams) -> list[Task]:
        """Retrieve tasks based on query parameters."""
        saved_tasks = self.task_repository.query(
            QueryParams(
                priority=task_query_params.priority,
                completed=task_query_params.completed,
            )
        )
        return [
            self._convert_persistence_to_task(task) for task in saved_tasks
        ]

    def get_by_id(self, id: int) -> Task:
        """Retrieve a task by its ID."""
        saved_task = self.task_repository.query(QueryParams(id=id))
        if not saved_task:
            raise NotFoundError(id)
        return self._convert_persistence_to_task(saved_task[0])
