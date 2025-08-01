"""The status API."""

from fastapi import Request, Response

from app.web.resources.status.schema import StatusResponse


async def get_status(request: Request, response: Response) -> StatusResponse:
    """Get the status of the API."""
    return StatusResponse(status="ok")
