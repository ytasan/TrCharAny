from __future__ import annotations

import logging
import threading
import time

import keyboard

import win32clipboard
import win32con

from trcharany import config
from trcharany.services.deasciifier_service import DeasciifierService

logger = logging.getLogger(__name__)

_pipeline_lock = threading.Lock()


def _read_clipboard_unicode() -> str | None:
    try:
        win32clipboard.OpenClipboard()
        try:
            if not win32clipboard.IsClipboardFormatAvailable(win32con.CF_UNICODETEXT):
                return None
            data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            if data is None:
                return None
            return str(data)
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        logger.exception("Failed to read clipboard")
        return None


def _write_clipboard_unicode(text: str) -> bool:
    try:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32con.CF_UNICODETEXT)
            return True
        finally:
            win32clipboard.CloseClipboard()
    except Exception:
        logger.exception("Failed to write clipboard")
        return False


class ClipboardPipeline:
    """Copy selection → deasciify → paste, with best-effort clipboard restore."""

    def __init__(self, service: DeasciifierService | None = None) -> None:
        self._service = service or DeasciifierService()

    def run(self) -> str:
        """Run the pipeline; returns a short status message for UI."""
        if not _pipeline_lock.acquire(blocking=False):
            return "Busy"
        try:
            return self._run_locked()
        finally:
            _pipeline_lock.release()

    def _run_locked(self) -> str:
        backup = _read_clipboard_unicode()

        try:
            keyboard.send("ctrl+c")
        except Exception:
            logger.exception("Ctrl+C failed")
            return "Copy failed"

        time.sleep(config.CLIPBOARD_COPY_DELAY)

        selected = _read_clipboard_unicode()
        if selected is None:
            logger.info("No Unicode text on clipboard after copy")
            if backup is not None:
                _write_clipboard_unicode(backup)
            return "No text"

        if not selected.strip():
            if backup is not None:
                _write_clipboard_unicode(backup)
            return "Empty"

        converted = self._service.deasciify(selected)
        if converted == selected:
            if backup is not None:
                _write_clipboard_unicode(backup)
            return "Unchanged"

        if not _write_clipboard_unicode(converted):
            if backup is not None:
                _write_clipboard_unicode(backup)
            return "Clipboard error"

        try:
            keyboard.send("ctrl+v")
        except Exception:
            logger.exception("Ctrl+V failed")
            if backup is not None:
                _write_clipboard_unicode(backup)
            return "Paste failed"

        time.sleep(config.CLIPBOARD_PASTE_DELAY)

        if backup is not None:
            _write_clipboard_unicode(backup)

        return "OK"
