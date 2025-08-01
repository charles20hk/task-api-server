"""Configuration utilities."""

from typing import Self

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """Base class for configs."""

    model_config = SettingsConfigDict(
        env_file=(".env"),
        env_nested_delimiter="__",
        extra="ignore",
        frozen=True,
        nested_model_default_partial_update=True,
        use_attribute_docstrings=True,
    )

    @classmethod
    def load(cls) -> Self:  # pragma: no cover
        """Load the config."""
        return cls()
