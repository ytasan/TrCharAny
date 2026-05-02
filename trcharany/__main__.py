from __future__ import annotations

import logging

from trcharany import config
from trcharany.app import run_app

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=config.LOG_LEVEL, format="%(levelname)s %(name)s: %(message)s")
    run_app()


if __name__ == "__main__":
    main()
