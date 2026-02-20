@echo off
echo Stopping local backend and frontend...
echo.

echo Killing processes on port 5055 (backend)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5055') do taskkill /F /PID %%a 2>nul

echo Killing processes on port 3000 (frontend)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do taskkill /F /PID %%a 2>nul

echo.
echo ✓ Local services stopped
echo.

echo Starting Docker backend again...
docker start open-notebook-open_notebook-1
echo ✓ Docker backend started
echo.
pause
