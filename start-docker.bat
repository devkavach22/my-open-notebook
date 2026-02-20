@echo off
echo Starting Open Notebook with Docker...
echo.

docker-compose up -d

echo.
echo ✓ Docker containers started!
echo.
echo Services:
echo - Frontend: http://localhost:8502
echo - Backend:  http://localhost:5055
echo - Database: http://localhost:8000
echo.
echo Open: http://localhost:8502
echo.
pause
