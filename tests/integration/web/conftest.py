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
