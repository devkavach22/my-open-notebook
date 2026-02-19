@echo off
echo ========================================
echo   Restarting Open Notebook
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo [1/3] Stopping services...
docker compose down

echo.
echo [2/3] Starting services...
docker compose up -d

echo.
echo [3/3] Waiting for startup (30 seconds)...
timeout /t 30 /nobreak > nul

echo.
echo Opening browser...
start http://localhost:8502

echo.
echo ========================================
echo   Open Notebook restarted!
echo ========================================
echo.
pause
