@echo off
cd /d "%~dp0"

echo ========================================
echo   Switching to Local Development
echo ========================================
echo.
echo This will:
echo   1. Stop Docker containers
echo   2. Start local backend with your changes
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo Stopping Docker containers...
docker compose down

echo.
echo ========================================
echo   Docker stopped!
echo ========================================
echo.
echo Now you need to start 3 services manually:
echo.
echo Terminal 1: start-database.bat
echo Terminal 2: start-backend.bat
echo Terminal 3: start-frontend.bat
echo.
echo Or simply run: start-all-local.bat
echo.
echo ========================================

pause
