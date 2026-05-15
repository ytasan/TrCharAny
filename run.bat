@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%~dp0"
set "PYW=%ROOT%.venv\Scripts\pythonw.exe"

if exist "%PYW%" goto :launch

if exist "%ROOT%.venv\Scripts\python.exe" (
    echo TrCharAny: .venv is broken or incomplete - pythonw.exe is missing.
    echo Remove the .venv folder, then from this folder run:
    echo   python -m venv .venv
    echo   .\.venv\Scripts\pip install -e .
    pause
    exit /b 1
)

echo TrCharAny: No virtual environment yet.
echo.
echo Open PowerShell or CMD here and run once:
echo   python -m venv .venv
echo   .\.venv\Scripts\pip install -e .
echo.
echo Then double-click this file again.
pause
exit /b 1

:launch
rem No console window: look for the tray icon near the clock - expand hidden icons if needed.
start "" "%PYW%" -m trcharany %*
endlocal
