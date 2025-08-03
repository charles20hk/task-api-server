"""Task controller module."""

from app.controllers.exception import NotFoundError
from app.controllers.mappers import (
    CreateRequestToPersistenceMapper,
    PersistenceToTaskMapper,
    UpdateRequestToPersistenceMapper,
)
from app.persistence.schemas import (
    QueryParams,
)
from app.persistence.task_repository import TaskRepository
from app.schemas import (
    CreateTaskRequest,
    Task,
    TaskQueryParams,
    UpdateTaskRequest,
)


class TaskController:
    """Controller for managing tasks."""

    def __init__(self, task_repository: TaskRepository) -> None:
        """Initialize the TaskController with a task repository."""
        self.task_repository = task_repository

    def create(self, create_task_request: CreateTaskRequest) -> Task:
        """Create a new task."""
        saved_task = self.task_repository.add(
            CreateRequestToPersistenceMapper.convert(create_task_request)
        )
        return PersistenceToTaskMapper.convert(saved_task)

    def get(
        self, task_query_params: TaskQueryParams
    ) -> tuple[list[Task], int]:
        """Retrieve tasks based on query parameters."""
        saved_tasks = self.task_repository.query(
            query_params=QueryParams(
                priority=task_query_params.priority,
                completed=task_query_params.completed,
                title=task_query_params.title,
                description=task_query_params.description,
            ),
            limit=task_query_params.page_size,
            offset=task_query_params.page_size
            * (task_query_params.page_number - 1),
        )
        total_tasks = len(
            self.task_repository.query(
                query_params=QueryParams(
                    priority=task_query_params.priority,
                    completed=task_query_params.completed,
                    title=task_query_params.title,
                    description=task_query_params.description,
                )
            )
        )
        return [
            PersistenceToTaskMapper.convert(task) for task in saved_tasks
        ], total_tasks

    def get_by_id(self, id: int) -> Task:
        """Retrieve a task by its ID."""
        saved_task = self.task_repository.query(QueryParams(id=id))
        if not saved_task:
            raise NotFoundError(id)
        return PersistenceToTaskMapper.convert(saved_task[0])

    def update(self, id: int, update_task_request: UpdateTaskRequest) -> Task:
        """Update an existing task."""
        saved_task = self.task_repository.query(QueryParams(id=id))
        if not saved_task:
            raise NotFoundError(id)

        persistence_request = UpdateRequestToPersistenceMapper.convert(
            update_task_request
        )
        self.task_repository.update(
            id=id, update_task_request=persistence_request
        )
        updated_task = self.task_repository.query(QueryParams(id=id))[0]
        return PersistenceToTaskMapper.convert(updated_task)

    def delete(self, id: int) -> None:
        """Delete a task by its ID."""
        saved_task = self.task_repository.query(QueryParams(id=id))
        if not saved_task:
            raise NotFoundError(id)
        self.task_repository.delete(id=id)
