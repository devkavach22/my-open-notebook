@echo off
cd /d "%~dp0"

echo ========================================
echo   Starting Open Notebook (Local Dev)
echo ========================================
echo.
echo This will open 3 terminal windows:
echo   1. SurrealDB (Database)
echo   2. Backend API (Python)
echo   3. Frontend (Next.js)
echo.
echo Press any key to continue...
pause >nul

echo.
echo Starting services...
echo.

REM Start Database in new window
start "Open Notebook - Database" cmd /k "start-database.bat"
timeout /t 3 /nobreak >nul

REM Start Backend in new window
start "Open Notebook - Backend API" cmd /k "start-backend.bat"
timeout /t 5 /nobreak >nul

REM Start Frontend in new window
start "Open Notebook - Frontend" cmd /k "start-frontend.bat"

echo.
echo ========================================
echo   All services are starting!
echo ========================================
echo.
echo Wait 30 seconds, then open:
echo   http://localhost:3000
echo.
echo To stop all services:
echo   Close all 3 terminal windows
echo   Or press Ctrl+C in each window
echo.
echo ========================================

timeout /t 30 /nobreak
start http://localhost:3000

echo.
echo Browser opened! Happy coding!
echo.
echo You can close this window now.
pause
