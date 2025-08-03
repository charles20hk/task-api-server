"""Schemas for the tasks API."""

from pydantic import BaseModel


class DeleteTaskResponse(BaseModel):
    """Response schema for deleting a task."""

    message: str
