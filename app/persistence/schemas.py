"""Schema for persistence layer."""

from datetime import datetime

from pydantic import BaseModel

from app.schemas import Priority


class CreateTaskRequest(BaseModel):
    """Request schema for creating a task."""

    title: str
    priority: Priority
    due_date: datetime
    description: str | None
    completed: bool


class Task(BaseModel):
    """Schema for a task entity."""

    id: int
    title: str
    priority: Priority
    due_date: datetime
    description: str | None
    completed: bool


class QueryParams(BaseModel):
    """Query parameters for filtering tasks."""

    priority: Priority | None = None
    completed: bool | None = None
    id: int | None = None


class UpdateTaskRequest(BaseModel):
    """Request schema for updating a task."""

    title: str | None = None
    priority: Priority | None = None
    due_date: datetime | None = None
    description: str | None = None
    completed: bool | None = None
