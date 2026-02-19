@echo off
cd /d "%~dp0"

echo ========================================
echo   Starting SurrealDB Database
echo ========================================
echo.
echo Database will run on: http://localhost:8000
echo Username: root
echo Password: root
echo.
echo Press Ctrl+C to stop the database
echo ========================================
echo.

surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
