"""Schema for persistence layer."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_validator

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

    @classmethod
    def _check_field_is_set_to_none(cls, field_name: str, v: Any) -> Any:  # noqa: ANN401
        """Check if a field is set to None."""
        if v is None:
            raise ValueError(f"{field_name} must not be None.")
        return v

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, v: Any) -> Any:  # noqa: ANN401
        """Raise ValueError if title is None."""
        return cls._check_field_is_set_to_none("Title", v)

    @field_validator("priority", mode="before")
    @classmethod
    def validate_priority(cls, v: Any) -> Any:  # noqa: ANN401
        """Raise ValueError if priority is None."""
        return cls._check_field_is_set_to_none("Priority", v)

    @field_validator("completed", mode="before")
    @classmethod
    def validate_completed(cls, v: Any) -> Any:  # noqa: ANN401
        """Raise ValueError if completed is None."""
        return cls._check_field_is_set_to_none("Completed", v)

    @field_validator("due_date", mode="before")
    @classmethod
    def validate_due_date(cls, v: Any) -> Any:  # noqa: ANN401
        """Raise ValueError if due_date is None."""
        return cls._check_field_is_set_to_none("Due Date", v)
