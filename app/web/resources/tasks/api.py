"""The status API."""

from typing import Annotated

from fastapi import Depends

from app.controllers.task import TaskController
from app.dependencies import get_task_controller
from app.schemas import CreateTaskRequest, Task


async def create_task(
    create_task_request: CreateTaskRequest,
    task_controller: Annotated[TaskController, Depends(get_task_controller)],
) -> Task:
    """Create a new task."""
    return task_controller.create(create_task_request)
