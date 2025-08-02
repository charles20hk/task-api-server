"""Dependency injection for urls."""

from app.controllers.task import TaskController
from app.persistence.task_repository import TaskRepository


def get_task_repository() -> TaskRepository:
    """Dependency to get the task repository."""
    return TaskRepository()


def get_task_controller() -> TaskController:
    """Dependency to get the task controller."""
    return TaskController(get_task_repository())
