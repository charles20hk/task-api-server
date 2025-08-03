"""Integration tests for the get task by id API endpoint."""

from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_task_repository


class TestGetTaskByIDApi:
    """Tests for the get task by id API endpoint."""

    @pytest.fixture(autouse=True)
    def cleanup(self) -> Generator[None, None, None]:
        """Cleanup tasks after each test."""
        yield
        task_repository = get_task_repository()
        with task_repository._get_connection() as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()

    def test_return_404_with_invalid_id(
        self, test_client: TestClient, test_app: FastAPI
    ) -> None:
        """Test that a 404 error is returned with an invalid task ID."""
        url = test_app.url_path_for("get_task_by_id", id=999999)
        response = test_client.get(url)
        assert response.status_code == 404

    def test_return_422_with_non_numeric_id(
        self, test_client: TestClient, test_app: FastAPI
    ) -> None:
        """Test that a 422 error is returned with a non-numeric task ID."""
        url = test_app.url_path_for("get_task_by_id", id="non-numeric")
        response = test_client.get(url)
        assert response.status_code == 422

    def test_return_task_by_id(
        self, test_client: TestClient, create_task_url: str, test_app: FastAPI
    ) -> None:
        """Test return task by ID."""
        create_task_dict = {
            "title": "Test Task",
            "priority": 3,
            "due_date": "2000-02-01T15:00:00",
            "description": "Test description",
        }
        response = test_client.post(create_task_url, json=create_task_dict)
        task_id = response.json()["id"]

        url = test_app.url_path_for("get_task_by_id", id=task_id)
        response = test_client.get(url)
        expected = {
            "id": task_id,
            "title": create_task_dict["title"],
            "priority": create_task_dict["priority"],
            "due_date": create_task_dict["due_date"],
            "description": create_task_dict["description"],
            "completed": False,
        }
        assert response.status_code == 200
        assert response.json() == expected
