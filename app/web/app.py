"""Module with functions for initialising the web application."""

from typing import TypedDict

from fastapi import FastAPI

from app.web.config import WebConfig
from app.web.urls import all_routers


def create_app(config: WebConfig) -> FastAPI:
    """Application factory.

    Creates the FastAPI application object.

    :returns: An instance of a `FastAPI
        <https://github.com/tiangolo/fastapi>`_
        :class:`FastAPI` application object.
    """

    class Arguments(TypedDict, total=False):
        title: str
        version: str
        openapi_url: str
        docs_url: str
        redoc_url: str

    app_config: Arguments = {"title": "Task API Server", "version": "0.1.0"}

    fastapp = FastAPI(**app_config)
    configure_apis(fastapp)

    return fastapp


def configure_apis(fastapp: FastAPI) -> None:
    """Configure the APIs.

    Import and register the routers.

    :param str fastapp: An instance of a `FastAPI
        <https://github.com/tiangolo/fastapi>`_
        :class:`FastAPI` application object.

    :returns: None.
    """
    for router in all_routers:
        fastapp.include_router(router, prefix="/v1")
