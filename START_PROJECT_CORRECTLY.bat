@echo off
echo ========================================
echo Starting Open Notebook Project
echo ========================================
echo.

echo Step 1: Stopping Docker backend (keeping database)...
docker stop open-notebook-open_notebook-1
echo ✓ Docker backend stopped
echo.

echo Step 2: Starting local backend with your auth code...
echo Opening new terminal for backend...
start "Backend API" cmd /k ".venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload"
echo ✓ Backend starting on port 5055
echo.

timeout /t 3 /nobreak >nul

echo Step 3: Starting frontend...
echo Opening new terminal for frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"
echo ✓ Frontend starting on port 3000
echo.

echo ========================================
echo Project Started!
echo ========================================
echo.
echo Services:
echo - Database: http://localhost:8000 (Docker)
echo - Backend:  http://localhost:5055 (Local with auth)
echo - Frontend: http://localhost:3000 (Local)
echo.
echo Wait 10 seconds, then open: http://localhost:3000
echo.
echo To stop:
echo - Close the terminal windows
echo - Or press Ctrl+C in each terminal
echo.
pause
