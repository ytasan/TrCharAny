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

- **Python** 3.11+ (matches [`requires-python`](pyproject.toml); `turkish-deasciifier` from Git targets 3.11+)
- **OS:** Windows (system tray, global hooks, clipboard)

## How to run

### Development (recommended: virtual environment)

Use a **venv** in the repo root so dependencies install under your user folder and `python -m trcharany` uses the same interpreter that has `pystray`, `keyboard`, etc. (A global `pip install -e .` on Windows can fail with **permission denied** on `pywin32`, or you may run `python` from a different install and get **ModuleNotFoundError**.)

1. Open a terminal at the **repository root** (the folder that contains `pyproject.toml`).

2. Create and use a venv (Python 3.11+):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks the activation script, run once (current user only):  
   `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

   **Without** activating the venv, you can still run the app with the venv’s interpreter explicitly:

   ```powershell
   .\.venv\Scripts\python.exe -m trcharany
   ```

3. Install the project in editable mode:

   ```powershell
   pip install -e .
   ```

   Optional (tests, tooling): `pip install -e ".[dev]"`

4. Start the app (tray icon + global hotkey). With the venv **activated**:

   ```powershell
   python -m trcharany
   ```

   Or use the installed console script: `trcharany`

5. In **VS Code / Cursor**, choose **Python: Select Interpreter** and pick `.venv\Scripts\python.exe` so integrated terminals use the venv by default.

### Built executable

From the repo root (with build deps installed, e.g. dev extras), `pyinstaller trcharany.spec` produces `dist\TrCharAny.exe` (no Python needed on the target machine).

## Project layout

Modular layout so services, input, automation, and UI stay separated:

```
TrCharAny/
├── README.md
├── pyproject.toml
├── trcharany.spec           # PyInstaller one-file build
├── trcharany/
│   ├── __init__.py
│   ├── __main__.py          # entry: python -m trcharany
│   ├── app.py               # wires tray, hotkey, and shutdown
│   ├── config.py            # defaults; hotkey via TRCHARANY_HOTKEY env
│   ├── win_console.py
│   ├── automation/
│   │   ├── __init__.py
│   │   └── clipboard_pipeline.py
│   ├── input/
│   │   ├── __init__.py
│   │   └── hotkey_listener.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── deasciifier_service.py
│   └── ui/
│       ├── __init__.py
│       └── tray.py
├── assets/
│   └── icon.png
└── tests/
    ├── __init__.py
    └── test_deasciifier_service.py
```

- **services/deasciifier_service.py** — wraps `turkish-deasciifier`; testable without UI.
- **automation/clipboard_pipeline.py** — clipboard read/write and the copy → deasciify → paste path (pywin32).
- **input/hotkey_listener.py** — global listener (**Ctrl+Shift+T** by default, override with `TRCHARANY_HOTKEY`).
- **ui/tray.py** — system tray icon and menu.
- **app.py** / **__main__.py** — application entry and lifecycle.

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
