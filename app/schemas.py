"""Schema for persistence layer."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel


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
