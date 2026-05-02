# TrCharAny — documentation / cleanup todos

## README alignment

- [x] **Python version:** README says Python **3.10+**; the real requirement in [`pyproject.toml`](pyproject.toml) is **`requires-python = ">=3.11"`** (because `turkish-deasciifier` from Git targets 3.11+). Update README to **3.11+** and match wording with install/run instructions.
- [ ] **Project layout diagram:** README still shows **`src/trcharany/`** and files like `main.py`, `clipboard_ops.py`, `hotkey_listener.py` under `src/`. The actual layout is **`trcharany/`** at repo root (see [`trcharany/`](trcharany/) — e.g. `__main__.py`, `app.py`, `automation/clipboard_pipeline.py`, `input/hotkey_listener.py`, `ui/tray.py`). Replace the architecture tree in README with the current structure.
- [ ] **Run instructions:** Optionally add a short “How to run” section (`pip install -e .`, `python -m trcharany`, optional `dist\TrCharAny.exe`) so it stays in sync with reality.
