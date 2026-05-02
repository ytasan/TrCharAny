from __future__ import annotations

from trcharany.services.deasciifier_service import DeasciifierService


def test_deasciifier_empty_and_whitespace() -> None:
    s = DeasciifierService()
    assert s.deasciify("") == ""
    assert s.deasciify("   ") == "   "


def test_deasciifier_ascii_turkish() -> None:
    s = DeasciifierService()
    raw = "Opusmegi cagristiran catirtilar."
    out = s.deasciify(raw)
    assert "ç" in out or "ğ" in out or "ı" in out or "ş" in out or out != raw
