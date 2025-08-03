"""Fixtures for integration tests in the web module."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.web.app import create_app
from app.web.config import WebConfig


@pytest.fixture(scope="session")
def config() -> WebConfig:
    """Fixture for web application config."""
    return WebConfig()


@pytest.fixture(scope="session")
def test_app(config: WebConfig) -> FastAPI:
    """Fixture for the application created for tests."""
    return create_app(config)


@pytest.fixture
def test_client(test_app: FastAPI) -> TestClient:
    """Fixture for the application client."""
    return TestClient(test_app)


@pytest.fixture(scope="session")
def status_url(test_app: FastAPI) -> str:
    """Fixture for the status url."""
    return test_app.url_path_for("get_status")


@pytest.fixture(scope="session")
def create_task_url(test_app: FastAPI) -> str:
    """Fixture for the create task url."""
    return test_app.url_path_for("create_task")


@pytest.fixture(scope="session")
def query_tasks_url(test_app: FastAPI) -> str:
    """Fixture for the query tasks url."""
    return test_app.url_path_for("query")


@pytest.fixture(scope="session")
def update_task_url(test_app: FastAPI) -> str:
    """Fixture for the update task url."""
    return test_app.url_path_for("update_task", id=1)


@pytest.fixture(scope="session")
def delete_task_url(test_app: FastAPI) -> str:
    """Fixture for the delete task url."""
    return test_app.url_path_for("delete_task", id=1)
