@echo off
echo ========================================
echo Rebuilding Docker with Auth Code
echo ========================================
echo.

echo Stopping existing containers...
docker-compose down

echo.
echo Building new Docker image with your local code...
echo This may take 5-10 minutes...
docker-compose build --no-cache

echo.
echo Starting containers...
docker-compose up -d

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo Docker Rebuild Complete!
echo ========================================
echo.
echo Frontend: http://localhost:8502
echo Backend API: http://localhost:5055
echo Database: http://localhost:8000
echo.
echo Testing auth endpoint...
curl http://localhost:5055/api/auth/status

echo.
echo.
echo Press any key to exit...
pause > nul
