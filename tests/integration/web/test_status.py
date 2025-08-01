"""Integration tests for the status API endpoint."""

from fastapi.testclient import TestClient


class TestStatusApi:
    """Integration tests for status API endpoint."""

    def test_get_status(
        self, test_client: TestClient, status_url: str
    ) -> None:
        """Test that the status endpoint returns correct status."""
        response = test_client.get(status_url)

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
