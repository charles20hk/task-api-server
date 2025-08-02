"""Dependency injection for urls."""

from app.controllers.task import TaskController
from app.persistence.task_repository import TaskRepository
from app.web.config import WebConfig


def get_web_config() -> WebConfig:
    """Dependency to get the web configuration."""
    return WebConfig.load()


def get_task_repository() -> TaskRepository:
    """Dependency to get the task repository."""
    web_config = get_web_config()
    return TaskRepository(db_name=web_config.database.db_name)


def get_task_controller() -> TaskController:
    """Dependency to get the task controller."""
    return TaskController(get_task_repository())
