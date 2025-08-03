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
    title: str | None = None
    description: str | None = None
    page_size: int = 15
    page_number: int = 1

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
