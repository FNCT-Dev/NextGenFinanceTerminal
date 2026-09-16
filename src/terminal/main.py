"""Application entry point for the core command-line check."""

import logging

from terminal.core.config import Settings
from terminal.core.logging import configure_logging


def main() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    logging.getLogger(__name__).info("%s: core architecture is ready", settings.app_name)


if __name__ == "__main__":
    main()
