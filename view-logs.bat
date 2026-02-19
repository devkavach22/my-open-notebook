@echo off
echo ========================================
echo   Viewing API Logs
echo ========================================
echo.
echo Press Ctrl+C to stop viewing logs
echo.

REM Navigate to project directory
cd /d "%~dp0"

docker compose logs -f open_notebook
