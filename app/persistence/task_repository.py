"""Task repository for managing task data."""

from app.persistence.base_repository import BaseRepository
from app.persistence.schemas import (
    CreateTaskRequest,
    QueryParams,
    Task,
    UpdateTaskRequest,
)


class TaskRepository(BaseRepository):
    """Repository for managing task data."""

    def _create_tables(self) -> None:
        """Create the tasks table in the database."""
        with self._get_connection() as conn:
            conn.execute(
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
        with self._get_connection() as conn:
            fields = "title, priority, due_date, description, completed"
            cursor = conn.execute(
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

    def _get(self, query: dict) -> list[Task]:
        """Retrieve tasks based on the query."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            fields = [
                "id",
                "title",
                "priority",
                "due_date",
                "description",
                "completed",
            ]
            sql_query = "SELECT " + (", ".join(fields)) + " FROM tasks"  # noqa: S608
            conditions = []
            values = []

            if query:
                sql_query += " WHERE "
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

    def query(self, query_params: QueryParams) -> list[Task]:
        """Retrieve tasks by priority."""
        query = {}
        if query_params.priority is not None:
            query["priority"] = query_params.priority.value
        if query_params.completed is not None:
            query["completed"] = query_params.completed
        if query_params.id is not None:
            query["id"] = query_params.id
        return self._get(query)

    def update(self, id: int, update_task_request: UpdateTaskRequest) -> None:
        """Update an existing task."""
        update_task_request_dict = update_task_request.model_dump(
            exclude_unset=True
        )
        if not update_task_request_dict:
            return

        with self._get_connection() as conn:
            fields = []
            values = []

            for key, value in update_task_request_dict.items():
                fields.append(f"{key} = ?")
                if key == "priority":
                    values.append(value.value)
                elif key == "due_date":
                    values.append(value.isoformat())
                else:
                    values.append(value)

            sql_query = f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?"  # noqa: S608
            values.append(id)

            conn.execute(sql_query, values)

    def delete(self, id: int) -> None:
        """Delete a task by id."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
