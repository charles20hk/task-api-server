"""Run the web application, this is the entry script."""

import uvicorn

from app.web.app import create_app
from app.web.config import WebConfig


def main() -> None:
    """Run the application with uvicorn."""
    config = WebConfig.load()

    uvicorn.run(
        create_app(config),
        host=config.server.host,
        port=config.server.port,
    )


if __name__ == "__main__":
    main()
