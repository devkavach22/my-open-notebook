@echo off
echo ========================================
echo   Starting Open Notebook
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo [1/4] Starting Docker services...
docker compose up -d

echo.
echo [2/4] Waiting for services to start (30 seconds)...
timeout /t 30 /nobreak > nul

echo.
echo [3/4] Checking status...
docker compose ps

echo.
echo [4/4] Opening browser...
start http://localhost:8502

echo.
echo ========================================
echo   Open Notebook is running!
echo ========================================
echo.
echo   Frontend: http://localhost:8502
echo   API:      http://localhost:5055
echo   API Docs: http://localhost:5055/docs
echo.
echo   To stop: Run stop.bat or press Ctrl+C
echo ========================================
echo.
pause
