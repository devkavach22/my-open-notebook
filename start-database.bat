@echo off
cd /d "%~dp0"

echo ========================================
echo   Starting SurrealDB Database (Docker)
echo ========================================
echo.
echo Database will run on: http://localhost:8000
echo Username: root
echo Password: root
echo.
echo Starting database container...
echo ========================================
echo.

docker-compose up surrealdb

echo.
echo Database stopped. Press any key to exit...
pause > nul
