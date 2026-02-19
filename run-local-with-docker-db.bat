@echo off
cd /d "%~dp0"

echo ========================================
echo   Running Backend Locally with Docker DB
echo ========================================
echo.
echo This will:
echo   1. Keep Docker database running
echo   2. Stop Docker backend
echo   3. Start local backend with your changes
echo.

echo Stopping Docker backend only...
docker compose stop open_notebook

echo.
echo Starting local backend...
echo Backend will run on: http://localhost:5055
echo.

.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
