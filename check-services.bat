@echo off
echo ========================================
echo Checking All Services Status
echo ========================================
echo.

echo [1/4] Checking SurrealDB (Port 8000)...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ SurrealDB is RUNNING
) else (
    echo ✗ SurrealDB is NOT running
)
echo.

echo [2/4] Checking Backend API (Port 5055)...
curl -s http://localhost:5055/api/auth/status >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API is RUNNING
) else (
    echo ✗ Backend API is NOT running
    echo   Start with: .venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
)
echo.

echo [3/4] Checking Frontend (Port 3000)...
curl -s http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is RUNNING
) else (
    echo ✗ Frontend is NOT running
    echo   Start with: cd frontend ^&^& npm run dev
)
echo.

echo [4/4] Testing Database Connection...
.venv\Scripts\python.exe -c "import asyncio; from surrealdb import AsyncSurreal; asyncio.run((lambda: AsyncSurreal('ws://localhost:8000/rpc').connect())())" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Database connection OK
) else (
    echo ✗ Database connection FAILED
)
echo.

echo ========================================
echo Summary
echo ========================================
echo If all services are running, try:
echo 1. Clear browser cache (Ctrl+Shift+Delete)
echo 2. Restart frontend: cd frontend ^&^& npm run dev
echo 3. Open: http://localhost:3000/login
echo.
pause
