@echo off
cd /d "%~dp0\frontend"

echo ========================================
echo   Starting Open Notebook Frontend
echo ========================================
echo.
echo Frontend will run on: http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

npm run dev
