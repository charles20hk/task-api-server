"""Unit tests for schemas."""

import pytest

from app.schemas import Priority, TaskQueryParams


class TestTaskQueryParams:
    """Test suite for TaskQueryParams schema."""

    def test_priority_validation(self) -> None:
        """Test that priority can be set as an int."""
        params = TaskQueryParams(priority=1)
        assert params.priority == Priority.HIGH

    def test_priority_validation_invalid(self) -> None:
        """Test that setting priority to a non-int raises ValueError."""
        with pytest.raises(ValueError, match="Priority must be an integer."):
            TaskQueryParams(priority="high")
