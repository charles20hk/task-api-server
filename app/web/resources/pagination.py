"""Pagination Builder."""

from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from app.web.resources.tasks.schemas import Pagination


class PaginationBuilder:
    """A class to build pagination metadata."""

    @staticmethod
    def update_url_param(url: str, key: str, value: Any) -> str:  # noqa: ANN401
        """Update a URL parameter."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        query_params[key] = [value]

        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query))
        return new_url

    @staticmethod
    def generate_page_url(
        page_number: int,
        page_size: int,
        url: str,
    ) -> str:
        """Generate a pagination URL."""
        url = PaginationBuilder.update_url_param(
            url, "page_number", page_number
        )
        url = PaginationBuilder.update_url_param(url, "page_size", page_size)

        return url

    @staticmethod
    def create(
        page_size: int,
        count: int,
        page_number: int,
        url: str,
    ) -> Pagination:
        """Build pagination metadata."""
        total_pages = (count // page_size) + (
            1 if count % page_size > 0 else 0
        )

        previous_page = (
            (page_number - 1) if page_number > 1 and total_pages > 1 else None
        )
        previous_page_url = (
            PaginationBuilder.generate_page_url(previous_page, page_size, url)
            if previous_page
            else None
        )

        next_page = (page_number + 1) if page_number < total_pages else None
        next_page_url = (
            PaginationBuilder.generate_page_url(next_page, page_size, url)
            if next_page
            else None
        )

        return Pagination(
            count=count,
            total_pages=total_pages,
            next_page_url=next_page_url,
            previous_page_url=previous_page_url,
        )
