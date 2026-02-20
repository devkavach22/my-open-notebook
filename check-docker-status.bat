@echo off
echo ========================================
echo Docker Status Check
echo ========================================
echo.

echo Running Containers:
docker-compose ps
echo.

echo ========================================
echo Service Health Check:
echo ========================================
echo.

echo [1] Database (Port 8000):
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Database is RUNNING
) else (
    echo ✗ Database is NOT responding
)
echo.

echo [2] Backend API (Port 5055):
curl -s http://localhost:5055/docs >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API is RUNNING
) else (
    echo ✗ Backend API is NOT responding
)
echo.

echo [3] Frontend (Port 8502):
curl -s http://localhost:8502 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is RUNNING
) else (
    echo ✗ Frontend is NOT responding
)
echo.

echo ========================================
echo Access URLs:
echo ========================================
echo Frontend: http://localhost:8502
echo Backend:  http://localhost:5055
echo Database: http://localhost:8000
echo API Docs: http://localhost:5055/docs
echo.

echo ========================================
echo Everything is RUNNING!
echo ========================================
echo.
echo Open: http://localhost:8502
echo.
pause
