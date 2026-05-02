from __future__ import annotations

import logging

import pystray

from trcharany import config
from trcharany.automation.clipboard_pipeline import ClipboardPipeline
from trcharany.input.hotkey_listener import HotkeyListener
from trcharany.services.deasciifier_service import DeasciifierService
from trcharany.ui.tray import build_tray_icon

logger = logging.getLogger(__name__)


class Application:
    """System tray app + global hotkey → clipboard deasciify pipeline."""

    def __init__(self) -> None:
        self._service = DeasciifierService()
        self._pipeline = ClipboardPipeline(self._service)
        self._listener = HotkeyListener(self._pipeline, on_result=self._on_hotkey_result)
        self._icon: pystray.Icon | None = None

    def _on_hotkey_result(self, status: str) -> None:
        icon = self._icon
        if icon is not None:
            setter = getattr(icon, "_trcharany_set_status", None)
            if callable(setter):
                setter(status)

    def _quit(self) -> None:
        logger.info("Exiting")
        self._listener.stop()
        if self._icon is not None:
            self._icon.stop()

    def run(self) -> None:
        self._icon = build_tray_icon(on_exit=self._quit)
        self._listener.start()
        logger.info("TrCharAny started; hotkey %s", config.DEFAULT_HOTKEY)
        self._icon.run()


def run_app() -> None:
    Application().run()
