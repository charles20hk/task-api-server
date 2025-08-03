"""Unit tests for the schemas."""

import pytest

from app.persistence.schemas import UpdateTaskRequest


class TestUpdateTaskRequest:
    """Tests for the UpdateTaskRequest schema."""

    def test_raise_value_error_if_completed_is_none(self) -> None:
        """Test that ValueError is raised if completed is None."""
        with pytest.raises(ValueError):  # noqa: PT011
            UpdateTaskRequest(completed=None)

    def test_raise_value_error_if_priority_is_none(self) -> None:
        """Test that ValueError is raised if priority is None."""
        with pytest.raises(ValueError):  # noqa: PT011
            UpdateTaskRequest(priority=None)

    def test_raise_value_error_if_due_date_is_none(self) -> None:
        """Test that ValueError is raised if due_date is None."""
        with pytest.raises(ValueError):  # noqa: PT011
            UpdateTaskRequest(due_date=None)

    def test_raise_value_error_if_title_is_none(self) -> None:
        """Test that ValueError is raised if title is None."""
        with pytest.raises(ValueError):  # noqa: PT011
            UpdateTaskRequest(title=None)
