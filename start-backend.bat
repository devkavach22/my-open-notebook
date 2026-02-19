@echo off
cd /d "%~dp0"

echo ========================================
echo   Starting Open Notebook Backend API
echo ========================================
echo.
echo Backend will run on: http://localhost:5055
echo API Docs available at: http://localhost:5055/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start backend using virtual environment Python
.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
