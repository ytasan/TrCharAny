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


def test_deasciifier_yasin_exception_preserves_spelling() -> None:
    s = DeasciifierService()
    assert s.deasciify("yasin") == "yasin"
    assert s.deasciify("Yasin") == "Yasin"
    assert "yasin" in s.deasciify("Merhaba yasin nasilsin")
