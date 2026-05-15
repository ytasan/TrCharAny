from __future__ import annotations

import logging

from trcharany import config
from trcharany.app import run_app
from trcharany.win_shell import set_app_user_model_id

logger = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=config.LOG_LEVEL, format="%(levelname)s %(name)s: %(message)s")
    set_app_user_model_id()
    run_app()


if __name__ == "__main__":
    main()
