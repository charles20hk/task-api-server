"""Integration tests for the create task API endpoint."""

from fastapi.testclient import TestClient


class TestCreateTaskApi:
    """Tests for the create task API endpoint."""

    def test_return_422_with_invalid_data(
        self, test_client: TestClient, create_task_url: str
    ) -> None:
        """Test that a 422 error is returned with invalid data."""
        response = test_client.post(
            create_task_url,
            json={
                "title": "Test Task",
                "priority": "invalid_priority",
                "due_date": "invalid_due_date",
                "description": "Test description",
            },
        )
        assert response.status_code == 422

    def test_return_422_without_data(
        self, test_client: TestClient, create_task_url: str
    ) -> None:
        """Test that a 422 error is returned without data."""
        response = test_client.post(create_task_url)
        assert response.status_code == 422

    def test_return_task(
        self, test_client: TestClient, create_task_url: str
    ) -> None:
        """Test creating a task."""
        response = test_client.post(
            create_task_url,
            json={
                "title": "Test Task",
                "priority": 1,
                "due_date": "2000-02-01T15:00:00",
                "description": "Test description",
            },
        )
        assert response.status_code == 200
        assert response.json() is not None
        response_dict = response.json()
        assert response_dict["title"] == "Test Task"
        assert response_dict["priority"] == 1
        assert response_dict["due_date"] == "2000-02-01T15:00:00"
        assert response_dict["description"] == "Test description"
        assert response_dict["completed"] is False
        assert "id" in response_dict
