from __future__ import annotations

import logging
from pathlib import Path

from collections.abc import Callable

import pystray
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

_ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"
_DEFAULT_ICON_PATH = _ASSETS_DIR / "icon.png"


def _make_default_icon(size: int = 64) -> Image.Image:
    img = Image.new("RGBA", (size, size), (30, 144, 255, 255))
    draw = ImageDraw.Draw(img)
    margin = size // 8
    draw.rounded_rectangle(
        (margin, margin, size - margin, size - margin),
        radius=size // 10,
        fill=(255, 255, 255, 255),
    )
    try:
        font = ImageFont.truetype("segoeui.ttf", size=int(size * 0.45))
    except OSError:
        font = ImageFont.load_default()
    text = "T"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(
        ((size - tw) // 2, (size - th) // 2 - bbox[1]),
        text,
        fill=(30, 144, 255, 255),
        font=font,
    )
    return img


def load_tray_image() -> Image.Image:
    path = _DEFAULT_ICON_PATH
    if path.is_file():
        try:
            return Image.open(path).convert("RGBA")
        except OSError:
            logger.warning("Could not load %s, using generated icon", path)
    _ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    img = _make_default_icon()
    try:
        img.save(_DEFAULT_ICON_PATH, format="PNG")
    except OSError:
        logger.debug("Could not write default icon to %s", _DEFAULT_ICON_PATH)
    return img


def build_tray_icon(
    on_exit: Callable[[], None],
) -> pystray.Icon:
    state: dict[str, str] = {"status": "Idle — select text, press hotkey"}

    def status_text(_: object) -> str:
        return f"Status: {state['status']}"

    def noop(_: object) -> None:
        return None

    def exit_app(_: object) -> None:
        on_exit()

    menu = pystray.Menu(
        pystray.MenuItem(status_text, noop, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", exit_app),
    )

    icon = pystray.Icon("trcharany", load_tray_image(), "TrCharAny — Turkish deasciifier", menu)

    def set_status(msg: str) -> None:
        state["status"] = msg
        try:
            icon.update_menu()
        except Exception:
            logger.debug("update_menu not available or failed")

    icon._trcharany_set_status = set_status  # type: ignore[attr-defined]
    icon._trcharany_state = state  # type: ignore[attr-defined]

    return icon
