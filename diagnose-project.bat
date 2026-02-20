@echo off
echo ========================================
echo Project Diagnostic Check
echo ========================================
echo.

echo [1] Checking Docker Containers...
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo [2] Checking Backend API (Docker - Port 5055)...
curl -s http://localhost:5055/api/auth/status
echo.
echo.

echo [3] Checking Database (Port 8000)...
curl -s http://localhost:8000/health
echo.
echo.

echo [4] Checking Frontend (Port 3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is RUNNING on port 3000
) else (
    echo ✗ Frontend is NOT running on port 3000
    echo   Start with: cd frontend ^&^& npm run dev
)
echo.

echo [5] Checking if local backend is running (Port 5055)...
netstat -ano | findstr :5055
echo.

echo ========================================
echo ISSUE DETECTED:
echo ========================================
echo.
echo The backend running in Docker does NOT have your auth changes!
echo.
echo SOLUTION:
echo 1. Stop Docker backend
echo 2. Run backend locally with your code
echo.
echo Commands:
echo   docker stop open-notebook-open_notebook-1
echo   .venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
echo.
echo Or use: start-backend.bat
echo.
pause
