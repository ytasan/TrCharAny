"""Windows shell integration (taskbar / Start identity for script runs)."""

from __future__ import annotations

import ctypes
import logging
import sys

logger = logging.getLogger(__name__)

# Unique id so Windows can group and label the app (not the generic "pythonw" bucket).
_APP_USER_MODEL_ID = "TrCharAny.TrCharAny.Application.1"


def set_app_user_model_id() -> None:
    """Call before creating UI so the taskbar / notification area can use our identity."""
    if sys.platform != "win32":
        return
    try:
        shell32 = ctypes.windll.shell32
        shell32.SetCurrentProcessExplicitAppUserModelID.argtypes = [ctypes.c_wchar_p]
        shell32.SetCurrentProcessExplicitAppUserModelID.restype = ctypes.c_long
        shell32.SetCurrentProcessExplicitAppUserModelID(_APP_USER_MODEL_ID)
    except Exception:
        logger.debug("SetCurrentProcessExplicitAppUserModelID failed", exc_info=True)
