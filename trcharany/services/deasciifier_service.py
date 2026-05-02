from __future__ import annotations

import logging

from turkish import Deasciifier

logger = logging.getLogger(__name__)


class DeasciifierService:
    """Wraps Turkish deasciification (ASCII → proper diacritics)."""

    def deasciify(self, text: str) -> str:
        if not text or not text.strip():
            return text
        try:
            d = Deasciifier(text)
            return d.convert_to_turkish()
        except Exception:
            logger.exception("Deasciifier failed; returning original text")
            return text
