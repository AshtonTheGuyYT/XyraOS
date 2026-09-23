@echo off
title Windows 10 - Xyra Edition
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
    echo Python not found. Install from https://python.org and retry.
    pause
    exit /b 1
)

echo Installing dependencies...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check

echo.
echo Starting Xyra Edition...
echo.
python app.py

pause