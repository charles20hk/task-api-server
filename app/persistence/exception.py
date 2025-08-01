"""Custom exceptions for the persistence layer."""


class NotFoundError(Exception):
    """Exception raised when a requested resource is not found."""

    def __init__(self, id: int) -> None:
        """Initialize with the ID of the not found resource."""
        super().__init__(f"Resource with ID {id} not found.")
