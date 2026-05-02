from __future__ import annotations

import logging
import threading
from collections.abc import Callable

import keyboard

from trcharany import config
from trcharany.automation.clipboard_pipeline import ClipboardPipeline

logger = logging.getLogger(__name__)


class HotkeyListener:
    """Registers a global hotkey and runs the clipboard pipeline on a worker thread."""

    def __init__(
        self,
        pipeline: ClipboardPipeline,
        hotkey: str | None = None,
        on_result: Callable[[str], None] | None = None,
    ) -> None:
        self._pipeline = pipeline
        self._hotkey = hotkey or config.DEFAULT_HOTKEY
        self._on_result = on_result
        self._remove_hotkey: Callable[[], None] | None = None

    def _callback(self) -> None:
        def worker() -> None:
            status = self._pipeline.run()
            if self._on_result:
                self._on_result(status)

        threading.Thread(target=worker, daemon=True).start()

    def start(self) -> None:
        if self._remove_hotkey is not None:
            return
        try:
            self._remove_hotkey = keyboard.add_hotkey(self._hotkey, self._callback)
            logger.info("Hotkey registered: %s", self._hotkey)
        except Exception:
            logger.exception("Failed to register hotkey")
            self._remove_hotkey = None

    def stop(self) -> None:
        if self._remove_hotkey is None:
            return
        remover = self._remove_hotkey
        self._remove_hotkey = None
        try:
            remover()
        except TypeError:
            try:
                keyboard.remove_hotkey(remover)
            except Exception:
                logger.exception("remove_hotkey failed")
        except Exception:
            logger.exception("Hotkey remover failed")
