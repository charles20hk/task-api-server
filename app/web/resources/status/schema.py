"""Schema for the Status endpoint."""

from pydantic import BaseModel


class StatusResponse(BaseModel):
    """Schema for the status response."""

    status: str
