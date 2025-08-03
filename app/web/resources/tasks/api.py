"""The tasks API."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.params import Query

from app.controllers.exception import NotFoundError
from app.controllers.task import TaskController
from app.dependencies import get_task_controller
from app.schemas import (
    CreateTaskRequest,
    Task,
    TaskQueryParams,
    UpdateTaskRequest,
)
from app.web.resources.pagination import PaginationBuilder
from app.web.resources.tasks.schemas import (
    DeleteTaskResponse,
    GetTasksResponse,
)


async def create_task(
    create_task_request: CreateTaskRequest,
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
) -> Task:
    """Create a new task."""
    return task_controller.create(create_task_request)


async def query(
    query: Annotated[TaskQueryParams, Query()],
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
    request: Request,
) -> GetTasksResponse:
    """Query tasks with query parameters.

    It returns a list of tasks and pagination metadata.
    """
    tasks, total = task_controller.get(query)

    pagination = PaginationBuilder.create(
        page_size=query.page_size,
        count=total,
        page_number=query.page_number,
        url=str(request.url),
    )
    return GetTasksResponse(tasks=tasks, pagination=pagination)


async def get_task_by_id(
    id: int,
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
) -> Task:
    """Get a task by its ID."""
    try:
        return task_controller.get_by_id(id)
    except NotFoundError as exc:
        raise HTTPException(
            status_code=404, detail=f"Task with ID {exc.id} not found"
        )


async def update_task(
    id: int,
    update_task_request: UpdateTaskRequest,
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
) -> Task:
    """Update a task."""
    try:
        return task_controller.update(
            id=id, update_task_request=update_task_request
        )
    except NotFoundError as exc:
        raise HTTPException(
            status_code=404, detail=f"Task with ID {exc.id} not found"
        )


async def delete_task(
    id: int,
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
) -> DeleteTaskResponse:
    """Delete a task."""
    try:
        task_controller.delete(id)
        return DeleteTaskResponse(message="Task deleted successfully")
    except NotFoundError as exc:
        raise HTTPException(
            status_code=404, detail=f"Task with ID {exc.id} not found"
        )
