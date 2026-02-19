@echo off
echo ========================================
echo   Exporting API Logs
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Exporting logs to api_logs.txt...
docker compose logs open_notebook > api_logs.txt

echo.
echo ========================================
echo   Logs exported successfully!
echo ========================================
echo.
echo File: api_logs.txt
echo Location: %cd%
echo.
echo Opening file...
start notepad api_logs.txt

pause
