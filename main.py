from __future__ import annotations

import logging

from core.config import ensure_directories, get_settings
from core.logging_setup import setup_logging


def main() -> None:
    settings = get_settings()
    setup_logging(settings.log_level)
    ensure_directories(settings)

    logger = logging.getLogger("fruitbot")
    logger.info("Stage 1 scaffold initialized.")
    logger.info("Next: implement storage, model, web, and bot logic.")


if __name__ == "__main__":
    main()
