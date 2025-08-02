"""Integration tests for the query tasks API endpoint."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_task_repository


class TestQueryTasksApi:
    """Tests for the query tasks API endpoint."""

    @pytest.fixture(autouse=True)
    def cleanup(self) -> Generator[None, None, None]:
        """Cleanup tasks after each test."""
        yield
        task_repository = get_task_repository()
        with task_repository._get_connection() as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()

    @pytest.mark.parametrize(
        ("priority", "completed"),
        [
            ("high", "true"),
            ("1", "unknown"),
        ],
    )
    def test_return_422_with_invalid_data(
        self,
        test_client: TestClient,
        query_tasks_url: str,
        priority: str,
        completed: str,
    ) -> None:
        """Test that a 422 error is returned with invalid data."""
        url = f"{query_tasks_url}?priority={priority}&completed={completed}"
        response = test_client.get(url)
        assert response.status_code == 422

    def test_return_tasks(
        self,
        test_client: TestClient,
        create_task_url: str,
        query_tasks_url: str,
    ) -> None:
        """Test return tasks."""
        create_task_dict = {
            "title": "Test Task",
            "priority": 3,
            "due_date": "2000-02-01T15:00:00",
            "description": "Test description",
        }
        response = test_client.post(
            create_task_url,
            json=create_task_dict,
        )
        response = test_client.post(
            create_task_url,
            json=create_task_dict,
        )

        url = f"{query_tasks_url}?priority=3&completed=false"
        response = test_client.get(url)
        assert response.status_code == 200
        assert response.json() is not None
        response_dict = response.json()
        assert isinstance(response_dict, list)
        assert len(response_dict) == 2
        for task_dict in response_dict:
            assert task_dict["title"] == "Test Task"
            assert task_dict["priority"] == 3
            assert task_dict["due_date"] == "2000-02-01T15:00:00"
            assert task_dict["description"] == "Test description"
            assert task_dict["completed"] is False
            assert "id" in task_dict
