"""Integration tests for the delete task API endpoint."""

from fastapi import FastAPI
from fastapi.testclient import TestClient


class TestDeleteTaskApi:
    """Tests for the delete task API endpoint."""

    def test_return_404_for_nonexistent_task(
        self,
        test_client: TestClient,
        delete_task_url: str,
    ) -> None:
        """Test that a 404 error is returned for a nonexistent task."""
        response = test_client.delete(delete_task_url)
        assert response.status_code == 404

    def test_return_422_for_invalid_task_id(
        self,
        test_client: TestClient,
        test_app: FastAPI,
    ) -> None:
        """Test that a 422 error is returned for an invalid task ID."""
        invalid_task_id = "invalid_id"
        response = test_client.delete(
            f"{test_app.url_path_for('delete_task', id=invalid_task_id)}"
        )
        assert response.status_code == 422

    def test_delete_task(
        self,
        test_client: TestClient,
        test_app: FastAPI,
        create_task_url: str,
    ) -> None:
        """Test deleting an existing task."""
        # First create a task to delete
        create_response = test_client.post(
            create_task_url,
            json={
                "title": "Task to Delete",
                "priority": 1,
                "due_date": "2000-02-01T15:00:00",
                "description": "Task description",
            },
        )
        assert create_response.status_code == 200
        task_id = create_response.json()["id"]

        # Now delete the created task
        delete_url = f"{test_app.url_path_for('delete_task', id=task_id)}"

        delete_response = test_client.delete(delete_url)
        assert delete_response.status_code == 200
