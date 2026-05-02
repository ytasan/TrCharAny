"""Windows-only: Ctrl+C / console close via SetConsoleCtrlHandler.

signal.SIGINT is unreliable while the main thread blocks inside pystray's message loop.
"""

from __future__ import annotations

import ctypes
import logging
import sys
import threading
from ctypes import wintypes
from typing import Any

logger = logging.getLogger(__name__)

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
CTRL_CLOSE_EVENT = 2

_HandlerRoutine = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_SetConsoleCtrlHandler = _kernel32.SetConsoleCtrlHandler
_SetConsoleCtrlHandler.argtypes = [_HandlerRoutine, wintypes.BOOL]
_SetConsoleCtrlHandler.restype = wintypes.BOOL


def install_console_ctrl_handler(app: Any) -> bool:
    """Register handler so Ctrl+C reaches us even when the main thread is in icon.run()."""
    if sys.platform != "win32":
        return False

    @_HandlerRoutine
    def _handler(ctrl_type: int) -> bool:
        if ctrl_type not in (CTRL_C_EVENT, CTRL_BREAK_EVENT, CTRL_CLOSE_EVENT):
            return False
        logger.info("Console shutdown event (%s); stopping...", ctrl_type)
        threading.Thread(
            target=app._quit,
            name="trcharany-console-ctrl",
            daemon=True,
        ).start()
        return True

    setattr(app, "_win32_console_handler", _handler)

    if not _SetConsoleCtrlHandler(_handler, True):
        logger.warning(
            "SetConsoleCtrlHandler failed (%s); use tray Exit or task manager",
            ctypes.get_last_error(),
        )
        return False
    return True
