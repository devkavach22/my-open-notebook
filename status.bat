@echo off
echo ========================================
echo   Open Notebook Status
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Checking Docker services...
echo.
docker compose ps

echo.
echo ========================================
echo   Access URLs:
echo ========================================
echo   Frontend: http://localhost:8502
echo   API:      http://localhost:5055
echo   API Docs: http://localhost:5055/docs
echo ========================================
echo.
pause
