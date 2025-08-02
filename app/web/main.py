"""Run the web application, this is the entry script."""

import uvicorn

from app.dependencies import get_web_config
from app.web.app import create_app


def main() -> None:
    """Run the application with uvicorn."""
    config = get_web_config()

    uvicorn.run(
        create_app(config),
        host=config.server.host,
        port=config.server.port,
    )


if __name__ == "__main__":
    main()
