"""Integration tests for the task update API endpoint."""

from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.dependencies import get_task_repository


class TestUpdateTaskApi:
    """Tests for the update task API endpoint."""

    @pytest.fixture(autouse=True)
    def cleanup(self) -> Generator[None, None, None]:
        """Cleanup tasks after each test."""
        yield
        task_repository = get_task_repository()
        with task_repository._get_connection() as conn:
            conn.execute("DELETE FROM tasks")
            conn.commit()

    def test_return_422_with_invalid_data(
        self,
        test_client: TestClient,
        update_task_url: str,
    ) -> None:
        """Test that a 422 error is returned with invalid data."""
        update_task_dict = {
            "title": None,
        }
        response = test_client.put(update_task_url, json=update_task_dict)
        assert response.status_code == 422

    def test_return_404_with_non_existent_task(
        self,
        test_client: TestClient,
        update_task_url: str,
    ) -> None:
        """Test that a 404 error is returned with a non-existent task."""
        response = test_client.put(
            update_task_url, json={"title": "Updated Task"}
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "Task with ID 1 not found"}

    def test_update_task(
        self,
        test_client: TestClient,
        create_task_url: str,
        update_task_url: str,
        test_app: FastAPI,
    ) -> None:
        """Test updating an existing task."""
        # First, create a task
        init_task_data_dict = {
            "title": "Test Task",
            "priority": 1,
            "due_date": "2000-02-01T15:00:00",
            "description": "Test description",
        }

        response = test_client.post(create_task_url, json=init_task_data_dict)
        task_id = response.json()["id"]
        assert task_id is not None

        # Now, update the created task
        update_task_dict = {
            "title": "Updated Task",
            "priority": 2,
            "due_date": "2001-03-01T15:00:00",
            "description": "Updated description",
            "completed": True,
        }
        update_url = test_app.url_path_for("update_task", id=task_id)
        response = test_client.put(
            update_url,
            json=update_task_dict,
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": task_id,
            **update_task_dict,
        }
