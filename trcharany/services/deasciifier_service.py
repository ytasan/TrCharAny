from __future__ import annotations

import logging
import re

from turkish import Deasciifier

from trcharany.config import deascii_exception_words

logger = logging.getLogger(__name__)


class DeasciifierService:
    """Wraps Turkish deasciification (ASCII → proper diacritics)."""

    def __init__(
        self,
        *,
        exception_words: frozenset[str] | None = None,
    ) -> None:
        self._exception_words = exception_words if exception_words is not None else deascii_exception_words()

    def deasciify(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            masked, originals = self._mask_exceptions(text)
            d = Deasciifier(masked)
            out = d.convert_to_turkish()
            return self._unmask_exceptions(out, originals)
        except Exception:
            logger.exception("Deasciifier failed; returning original text")
            return text

    def _mask_exceptions(self, text: str) -> tuple[str, list[str]]:
        """Replace whole-word exceptions with placeholders; preserve original spans."""
        if not self._exception_words:
            return text, []

        parts: list[str] = sorted(self._exception_words, key=len, reverse=True)
        pattern = re.compile(
            r"\b(" + "|".join(re.escape(p) for p in parts) + r")\b",
            re.IGNORECASE,
        )
        originals: list[str] = []

        def repl(match: re.Match[str]) -> str:
            originals.append(match.group(0))
            return f"__TRCHARANY_EXC_{len(originals) - 1}__"

        return pattern.sub(repl, text), originals

    @staticmethod
    def _unmask_exceptions(text: str, originals: list[str]) -> str:
        for i, orig in enumerate(originals):
            text = text.replace(f"__TRCHARANY_EXC_{i}__", orig)
        return text
