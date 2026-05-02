from __future__ import annotations

import logging
import signal
import threading

import pystray

from trcharany import config
from trcharany.automation.clipboard_pipeline import ClipboardPipeline
from trcharany.input.hotkey_listener import HotkeyListener
from trcharany.services.deasciifier_service import DeasciifierService
from trcharany.ui.tray import build_tray_icon
from trcharany.win_console import install_console_ctrl_handler

logger = logging.getLogger(__name__)


class Application:
    """System tray app + global hotkey → clipboard deasciify pipeline."""

    def __init__(self) -> None:
        self._service = DeasciifierService()
        self._pipeline = ClipboardPipeline(self._service)
        self._listener = HotkeyListener(self._pipeline, on_result=self._on_hotkey_result)
        self._icon: pystray.Icon | None = None
        self._shutdown_lock = threading.Lock()
        self._shutdown_started = False

    def _on_hotkey_result(self, status: str) -> None:
        icon = self._icon
        if icon is not None:
            setter = getattr(icon, "_trcharany_set_status", None)
            if callable(setter):
                setter(status)

    def _quit(self) -> None:
        with self._shutdown_lock:
            if self._shutdown_started:
                return
            self._shutdown_started = True
        logger.info("Exiting")
        try:
            self._listener.stop()
        except Exception:
            logger.exception("Error stopping hotkey listener")
        try:
            if self._icon is not None:
                self._icon.stop()
        except Exception:
            logger.exception("Error stopping tray icon")

    def _on_sigint(self, _signum: int, _frame: object | None) -> None:
        """Run shutdown off the signal stack so pystray Win32 callbacks stay clean."""
        logger.info("Ctrl+C (SIGINT); stopping...")
        threading.Thread(target=self._quit, name="trcharany-sigint-shutdown", daemon=True).start()

    def run(self) -> None:
        self._icon = build_tray_icon(on_exit=self._quit)
        self._listener.start()
        logger.info("TrCharAny started; hotkey %s", config.DEFAULT_HOTKEY)
        if not install_console_ctrl_handler(self):
            signal.signal(signal.SIGINT, self._on_sigint)
        self._icon.run()


def run_app() -> None:
    Application().run()
