"""Application defaults."""

import logging
import os

# Global hotkey for the `keyboard` library (default: Ctrl+Shift+T).
# Avoid Ctrl+Alt+* on Turkish/European layouts: Left Ctrl+Left Alt is treated as AltGr,
# so Ctrl+Alt+T often never reaches a global hook reliably.
DEFAULT_HOTKEY = os.environ.get("TRCHARANY_HOTKEY", "ctrl+shift+t")

# Delay (seconds) after simulated Ctrl+C before reading clipboard
CLIPBOARD_COPY_DELAY = float(os.environ.get("TRCHARANY_COPY_DELAY", "0.09"))

# Delay (seconds) after Ctrl+V before optional clipboard restore
CLIPBOARD_PASTE_DELAY = float(os.environ.get("TRCHARANY_PASTE_DELAY", "0.03"))

LOG_LEVEL = getattr(logging, os.environ.get("TRCHARANY_LOG_LEVEL", "INFO").upper(), logging.INFO)
