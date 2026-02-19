@echo off
echo ========================================
echo   Stopping Open Notebook
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Stopping Docker services...
docker compose down

echo.
echo ========================================
echo   Open Notebook stopped successfully!
echo ========================================
echo.
pause
