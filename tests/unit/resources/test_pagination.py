"""Test cases for pagination builder."""

from app.web.resources.pagination import PaginationBuilder


class TestPaginationBuilder:
    """Test cases for PaginationBuilder class."""

    def test_update_url_param(self) -> None:
        """Test updating a URL parameter."""
        url = "http://example.com/tasks?page=1"
        updated_url = PaginationBuilder.update_url_param(url, "page", 2)
        assert updated_url == "http://example.com/tasks?page=2"

    def test_generate_page_url(self) -> None:
        """Test generating a pagination URL."""
        page_number = 2
        page_size = 10
        get_tasks_url = "http://example.com/tasks"
        page_url = PaginationBuilder.generate_page_url(
            page_number, page_size, get_tasks_url
        )
        assert (
            page_url == "http://example.com/tasks?page_number=2&page_size=10"
        )

    def test_create_pagination(self) -> None:
        """Test creating pagination metadata."""
        pagination = PaginationBuilder.create(
            10, 100, 1, "http://example.com/tasks/?page_size=1&page_number=1"
        )
        assert pagination.count == 100
        assert pagination.total_pages == 10
        assert (
            pagination.next_page_url
            == "http://example.com/tasks/?page_size=10&page_number=2"
        )
        assert pagination.previous_page_url is None
