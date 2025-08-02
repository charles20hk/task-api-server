"""Base repository class for data access."""

import sqlite3
from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Base repository class that provides a common interface...

    for all repositories.
    """

    def __init__(self, db_name: str | None = None) -> None:
        """Initialize the repository with a database connection."""
        self._conn = self._get_connection(db_name)
        self._create_tables()

    def _get_connection(
        self, db_name: str | None = None
    ) -> sqlite3.Connection:
        """Get the database connection."""
        return sqlite3.connect(db_name or "tasks_db")

    @abstractmethod
    def _create_tables(self) -> None:
        """Create necessary tables in the database."""

    @abstractmethod
    def add(self, data_model: T) -> T:
        """Add a new entity to the database."""

    @abstractmethod
    def get(self, query: dict) -> list[T]:
        """Retrieve entities from the database based on the query."""

    @abstractmethod
    def delete(self, id: int) -> None:
        """Delete an entity by id from the database."""
