@echo off
echo ========================================
echo Starting SurrealDB Database
echo ========================================
echo.

echo Starting database container...
docker-compose up -d surrealdb

echo.
echo Waiting for database to be ready...
timeout /t 5 /nobreak > nul

echo.
echo ========================================
echo Database Status
echo ========================================
docker ps | findstr surrealdb

echo.
echo Database is running on port 8000
echo.
echo Press any key to exit...
pause > nul
