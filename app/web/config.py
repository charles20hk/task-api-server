"""Web application configuration utilities."""

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict

from app.config import BaseConfig


class BaseWebConfig(BaseConfig):
    """Base class for WebConfig."""

    model_config = SettingsConfigDict(env_prefix="WEB__")


class ServerConfig(BaseModel):
    """Configuration for server."""

    host: str = "127.0.0.1"
    """Host to run the server on."""

    port: int = 8080
    """Port to run the server on."""


class WebConfig(BaseWebConfig):
    """Web application configuration."""

    server: ServerConfig = ServerConfig()
    """Configuration for server."""
