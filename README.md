# TrCharAny

A lightweight Windows background utility that converts ASCII-Turkish text to proper Turkish characters (`ç`, `ğ`, `ı`, `ö`, `ş`, `ü`) in any active window via a global hotkey.

## Goal

Provide seamless **copy → deasciify → paste** automation so selections in Notepad, browsers, and other apps are fixed without leaving the focused window.

## Core workflow

1. User **selects** the text in any app (required — the caret alone is not enough in classic Notepad).
2. User presses the global hotkey (default: **Ctrl+Shift+T**; avoids **Ctrl+Alt** clashing with **AltGr** on Turkish keyboards).
3. The app runs: **Ctrl+C** → process clipboard → **Ctrl+V** using a Turkish deasciifier.
4. Edge cases to handle: empty selection, non-text clipboard content, and windows that restrict automation.

## Requirements

- **Python** 3.10+
- **OS:** Windows (system tray, global hooks, clipboard)

## Project architecture (Step 1)

Modular layout so core logic, input, clipboard, and UI stay separated:

```
TrCharAny/
├── README.md
├── pyproject.toml          # or requirements.txt
├── src/
│   └── trcharany/
│       ├── __init__.py
│       ├── main.py         # entry: wire hotkey + tray + service
│       ├── deasciifier_service.py   # Step 2: wraps conversion API
│       ├── clipboard_ops.py         # copy/paste + text extraction (pyperclip / pywin32)
│       ├── hotkeys.py               # Step 3: global listener (keyboard)
│       └── tray_app.py              # Step 4: pystray icon, Exit, Status
├── assets/
│   └── icon.png            # tray icon (Pillow-compatible)
└── tests/                  # optional
```

- **deasciifier_service.py** — single place for `turkish-deasciifier` (or equivalent); testable without UI.
- **clipboard_ops.py** — robust clipboard read/write and “is this text?” checks.
- **hotkeys.py** — registers **Ctrl+Shift+T** (configurable via `TRCHARANY_HOTKEY`) and invokes the service + clipboard pipeline with minimal latency.
- **tray_app.py** — runs the tray loop, menu (**Exit**, **Status**), and hosts or signals the hotkey thread.
- **main.py** — starts tray, starts hotkey listener, clean shutdown.

## Dependencies

Install these for development (versions can be pinned in `pyproject.toml` / `requirements.txt`):

| Package | Role |
|--------|------|
| `keyboard` | Global hotkey hooks |
| `pyperclip` | Simple cross-process clipboard text (optional complement) |
| `pywin32` | Stronger Windows clipboard and focus edge cases |
| `pystray` | System tray icon and menu |
| `Pillow` | Tray icon image loading |
| `turkish-deasciifier` | Core ASCII → Turkish character restoration |

**Performance:** keep the hotkey path short (read clipboard → transform → write → simulate paste) to limit gap between copy and paste.

## Packaging (Step 5 outline)

- Prefer **PyInstaller** (`pyinstaller --onefile --windowed ...`) so users get a single `.exe`.
- Bundle `assets/icon.png` and declare hidden imports if hooks fail (`keyboard`, `pystray`).
- Test on a clean Windows VM without Python installed.

## Roadmap (Plan Mode)

1. **Architecture & dependencies** — this document.
2. **DeasciifierService** — wrap the conversion library.
3. **Hotkey + clipboard automation** — Ctrl+C / process / Ctrl+V.
4. **System tray** — Exit, Status.
5. **Single-file `.exe`** — PyInstaller (or similar).
