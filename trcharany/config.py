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

# ASCII whole words passed through deasciification unchanged (lowercased for matching).
_DEFAULT_DEASCII_EXCEPTION_WORDS: tuple[str, ...] = ("yasin",)


def deascii_exception_words() -> frozenset[str]:
    """Built-in exceptions plus optional TRCHARANY_DEASCII_EXCEPTIONS (comma-separated)."""
    words = {w.lower() for w in _DEFAULT_DEASCII_EXCEPTION_WORDS}
    extra = os.environ.get("TRCHARANY_DEASCII_EXCEPTIONS", "")
    for part in extra.split(","):
        p = part.strip()
        if p:
            words.add(p.lower())
    return frozenset(words)

