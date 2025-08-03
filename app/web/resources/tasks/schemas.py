"""Schemas for the tasks API."""

from pydantic import BaseModel

from app.schemas import Task


class DeleteTaskResponse(BaseModel):
    """Response schema for deleting a task."""

    message: str


class Pagination(BaseModel):
    """Pagination schema for metadata in response."""

    count: int
    total_pages: int
    next_page_url: str | None = None
    previous_page_url: str | None = None


class GetTasksResponse(BaseModel):
    """Response schema for a list of tasks."""

    tasks: list[Task]
    pagination: Pagination
