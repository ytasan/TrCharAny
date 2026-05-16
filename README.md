# TrCharAny

A lightweight Windows background utility that converts ASCII-Turkish text to proper Turkish characters (`ç`, `ğ`, `ı`, `ö`, `ş`, `ü`) in any active window via a global hotkey.

## Goal

Provide seamless **copy → deasciify → paste** automation so selections in Notepad, browsers, and other apps are fixed without leaving the focused window.

## Inspiration

The behavior and purpose mirror **[deasciifier.com](https://deasciifier.com/)** (Turkish ASCII → proper Turkish characters). This work was shaped using that site as the reference example; here the same idea runs locally via a global hotkey instead of a browser workflow.

## Core workflow

1. User **selects** the text in any app (required — the caret alone is not enough in classic Notepad).
2. User presses the global hotkey (**Ctrl+Alt+G**).
3. The app runs: **Ctrl+C** → process clipboard → **Ctrl+V** using a Turkish deasciifier.
4. Edge cases to handle: empty selection, non-text clipboard content, and windows that restrict automation.

## Requirements

- **Python** 3.11+ (matches [`requires-python`](pyproject.toml); `turkish-deasciifier` from Git targets 3.11+)
- **OS:** Windows (system tray, global hooks, clipboard)

## How to run

### Development (recommended: virtual environment)

Use a **venv** in the repo root so dependencies install under your user folder and `python -m trcharany` uses the same interpreter that has `pystray`, `keyboard`, etc. (A global `pip install -e .` on Windows can fail with **permission denied** on `pywin32`, or you may run `python` from a different install and get **ModuleNotFoundError**.)

1. Open a terminal at the **repository root** (the folder that contains `pyproject.toml`).

2. Create a venv (Python 3.11+). You only need this **once** unless you delete `.venv`:

   ```powershell
   python -m venv .venv
   ```

   You do **not** have to run `Activate.ps1` if you start the app via the venv’s `python.exe` (below), [`run.bat`](run.bat), or the IDE interpreter — that avoids both **execution policy** issues and some **antivirus** false positives on `Activate.ps1`.

   Optional — activate the venv in the current shell (then `python` points at `.venv`):

   - PowerShell: `.\.venv\Scripts\Activate.ps1`  
     If scripts are blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (current user only).
   - Command Prompt: `.\.venv\Scripts\activate.bat` (often not flagged like `Activate.ps1`.)

   **Antivirus** may report `ScriptContainedMaliciousContent` or similar for `Activate.ps1`. Prefer: `.\.venv\Scripts\python.exe -m trcharany`, or from repo root run **`run.bat`** (double-click or `.\run.bat` in PowerShell).

3. Install the project in editable mode (use venv’s **pip** if you did not activate the shell):

   ```powershell
   .\.venv\Scripts\pip.exe install -e .
   ```

   If the venv is already activated: `pip install -e .`

   Optional (tests, tooling): `pip install -e ".[dev]"` (same `pip` / `.\.venv\Scripts\pip.exe` rule).

4. Start the app (tray icon + global hotkey):

   ```powershell
   .\.venv\Scripts\python.exe -m trcharany
   ```

   Or run [`run.bat`](run.bat) from the repo root. If the venv shell is **activated**, `python -m trcharany` or the `trcharany` console script also works.

5. In **VS Code / Cursor**, choose **Python: Select Interpreter** and pick `.venv\Scripts\python.exe` so integrated terminals use the venv by default.

### Background launch (`run.bat`) and Windows startup

- **[`run.bat`](run.bat)** starts TrCharAny with **`.venv\Scripts\pythonw.exe`** (GUI interpreter, **no console window**). It uses `start` so the batch exits immediately.
- **First-time setup:** `run.bat` requires a working `.venv` with `pythonw.exe` and an editable install (`pip install -e .`). If the venv is missing, the batch prints steps and pauses.
- **Run at sign-in:** Running `run.bat` once does **not** enable auto-start. Create a shortcut: **Win+R** → `shell:startup` → **New → Shortcut** → target the full path to `run.bat` (e.g. `C:\Users\…\TrCharAny\run.bat`).
- **Tray icon:** Look next to the clock. On **Windows 11**, new icons may sit under **^** (hidden icons); open that area or drag the icon to the visible tray. **Exit:** right-click the tray icon → **Exit**.
- **Task Manager:** The process often appears as **Python** / **`pythonw.exe`** with a command line containing `-m trcharany`. The packaged **`TrCharAny.exe`** shows that name in the **Name** column instead.
- **Windows identity:** At startup the app sets an explicit **App User Model ID** (`trcharany/win_shell.py`) so the shell can group and label TrCharAny more consistently than a generic Python run.

### Troubleshooting

- **`Permission denied` when running `python -m venv .venv`:** Usually the old `.venv` is in use (TrCharAny, another terminal, or the IDE). Quit the app, close terminals using that venv, then either run **`.\.venv\Scripts\pip install -e .`** if the venv is already fine, or remove and recreate:
  ```powershell
  Remove-Item -Recurse -Force .venv
  python -m venv .venv
  .\.venv\Scripts\pip install -e .
  ```
- **`pythonw.exe` missing but `python.exe` exists in `.venv\Scripts`:** Remove `.venv` and recreate as above.

### Built executable

From the repo root (with build deps installed, e.g. dev extras), `pyinstaller trcharany.spec` produces `dist\TrCharAny.exe` (no Python needed on the target machine).

## Project layout

Modular layout so services, input, automation, and UI stay separated:

```
TrCharAny/
├── README.md
├── run.bat                  # starts via pythonw: no console; needs .venv + pip install -e .
├── pyproject.toml
├── trcharany.spec           # PyInstaller one-file build
├── trcharany/
│   ├── __init__.py
│   ├── __main__.py          # entry: python -m trcharany
│   ├── app.py               # wires tray, hotkey, and shutdown
│   ├── config.py            # defaults (global hotkey Ctrl+Alt+G)
│   ├── win_console.py       # Ctrl+C / console-close on console runs (Windows)
│   ├── win_shell.py         # App User Model ID for taskbar/shell (Windows)
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
│   ├── trcharany-logo-concept.png  # tray icon (primary)
│   └── icon.png                     # generated fallback if the concept asset is missing
└── tests/
    ├── __init__.py
    └── test_deasciifier_service.py
```

- **services/deasciifier_service.py** — wraps `turkish-deasciifier`; testable without UI.
- **automation/clipboard_pipeline.py** — clipboard read/write and the copy → deasciify → paste path (pywin32).
- **input/hotkey_listener.py** — global listener (**Ctrl+Alt+G**).
- **ui/tray.py** — system tray icon and menu.
- **app.py** / **__main__.py** — application entry and lifecycle.
- **win_shell.py** — Windows **App User Model ID** registration at launch.

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
- Bundle `assets/` (includes the tray PNG) and declare hidden imports if hooks fail (`keyboard`, `pystray`).
- Test on a clean Windows VM without Python installed.

## Roadmap (Plan Mode)

1. **Architecture & dependencies** — this document.
2. **DeasciifierService** — wrap the conversion library.
3. **Hotkey + clipboard automation** — Ctrl+C / process / Ctrl+V.
4. **System tray** — Exit, Status.
5. **Single-file `.exe`** — PyInstaller (or similar).
