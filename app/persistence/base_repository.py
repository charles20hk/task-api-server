"""Base repository class for data access."""

import sqlite3
from abc import ABC, abstractmethod
from typing import Generic, TypeVar


T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Base repository class that provides a common interface...

    for all repositories.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Initialize the repository with a database connection."""
        self._conn = conn
        self._create_tables()

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
