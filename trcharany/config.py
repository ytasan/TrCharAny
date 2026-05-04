"""Application defaults."""

import logging
import os

# Global hotkey for the `keyboard` library (fixed: Ctrl+Alt+G).
# Note: on some Turkish/European layouts Left Ctrl+Left Alt is AltGr; the hook may not fire if that layout eats the chord.
DEFAULT_HOTKEY = "ctrl+alt+g"

# Delay (seconds) after simulated Ctrl+C before reading clipboard
CLIPBOARD_COPY_DELAY = float(os.environ.get("TRCHARANY_COPY_DELAY", "0.09"))

# Delay (seconds) after Ctrl+V before optional clipboard restore
CLIPBOARD_PASTE_DELAY = float(os.environ.get("TRCHARANY_PASTE_DELAY", "0.03"))

LOG_LEVEL = getattr(logging, os.environ.get("TRCHARANY_LOG_LEVEL", "INFO").upper(), logging.INFO)


