"""Schema for persistence layer."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, field_validator


class Priority(Enum):
    """Enum for task priority levels."""

    HIGH = 1
    MEDIUM = 2
    LOW = 3


class CreateTaskRequest(BaseModel):
    """Request schema for creating a task."""

    title: str
    priority: Priority
    due_date: datetime
    description: str | None = None


class Task(BaseModel):
    """Schema for a task entity."""

    id: int
    title: str
    priority: Priority
    due_date: datetime
    description: str | None = None
    completed: bool


class TaskQueryParams(BaseModel):
    """Query parameters for retrieving tasks."""

    priority: Priority | None = None
    completed: bool | None = None

    @field_validator("priority", mode="before")
    @classmethod
    def validate_int(cls, v: Any) -> int | None:  # noqa: ANN401
        """Convert priority to int."""
        try:
            if v is not None:
                return int(v)
            return None
        except ValueError:
            raise ValueError("Priority must be an integer.")
