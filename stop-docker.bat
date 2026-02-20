@echo off
echo Stopping Open Notebook Docker containers...
echo.

docker-compose down

echo.
echo ✓ Docker containers stopped!
echo.
pause
