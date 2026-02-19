@echo off
cd /d "%~dp0"

echo ========================================
echo Restarting Backend Server
echo ========================================
echo.

echo Stopping any existing backend processes on port 5055...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5055 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak >nul

echo.
echo Starting backend server...
echo.
start "Open Notebook Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload"

echo.
echo Backend server started in new window!
echo Watch that window for logs.
echo.
pause
