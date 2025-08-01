"""Task repository for managing task data."""

import sqlite3

from app.persistence.base_repository import BaseRepository
from app.persistence.exception import NotFoundError
from app.persistence.schema import CreateTaskRequest, Priority, Task


class TaskRepository(BaseRepository):
    """Repository for managing task data."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        """Initialize the task repository with a database connection."""
        super().__init__(conn)

    def _create_tables(self) -> None:
        """Create the tasks table in the database."""
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    due_date TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN NOT NULL DEFAULT 0
                )
                """
            )

    def add(self, data_model: CreateTaskRequest) -> Task:
        """Add a new task to the database."""
        with self._conn:
            fields = "title, priority, due_date, description, completed"
            cursor = self._conn.execute(
                f"INSERT INTO tasks ({fields}) VALUES (?, ?, ?, ?, ?)",  # noqa: S608
                (
                    data_model.title,
                    data_model.priority.value,
                    data_model.due_date.isoformat(),
                    data_model.description,
                    data_model.completed,
                ),
            )
            return Task(
                id=cursor.lastrowid,
                title=data_model.title,
                priority=data_model.priority,
                due_date=data_model.due_date,
                description=data_model.description,
                completed=data_model.completed,
            )

    def get(self, query: dict) -> list[Task]:
        """Retrieve tasks based on the query."""
        cursor = self._conn.cursor()
        fields = [
            "id",
            "title",
            "priority",
            "due_date",
            "description",
            "completed",
        ]
        sql_query = "SELECT " + (", ".join(fields)) + " FROM tasks WHERE "  # noqa: S608
        conditions = []
        values = []

        for key, value in query.items():
            conditions.append(f"{key} = ?")
            values.append(value)

        sql_query += " AND ".join(conditions)
        cursor.execute(sql_query, values)
        rows = cursor.fetchall()

        return [
            Task.model_validate(
                {
                    fields[0]: row[0],
                    fields[1]: row[1],
                    fields[2]: row[2],
                    fields[3]: row[3],
                    fields[4]: row[4],
                    fields[5]: bool(row[5]),
                }
            )
            for row in rows
        ]

    def get_by_priority(self, priority: Priority) -> list[Task]:
        """Retrieve tasks by priority."""
        return self.get({"priority": priority.value})

    def get_by_status(self, completed: bool) -> list[Task]:
        """Retrieve tasks by completion status."""
        return self.get({"completed": completed})

    def get_by_id(self, id: int) -> Task:
        """Retrieve a task by its id."""
        tasks = self.get({"id": id})
        if not tasks:
            raise NotFoundError(id)
        return tasks[0]

    def delete(self, id: int) -> None:
        """Delete a task by id."""
        with self._conn:
            self._conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
