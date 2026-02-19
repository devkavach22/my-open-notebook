# How to Run Open Notebook Project

## Simple 3-Terminal Setup

### Terminal 1: Database (SurrealDB)
```bash
docker compose up surrealdb
```
- Runs on: `http://localhost:8000`
- This must be running first before backend

### Terminal 2: Backend (Python/FastAPI)
```bash
cd C:\Users\hemanshi.l\Desktop\open-notebook
.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```
- Runs on: `http://localhost:5055`
- Auto-reloads when code changes

### Terminal 3: Frontend (Next.js)
```bash
cd C:\Users\hemanshi.l\Desktop\open-notebook\frontend
npm run dev
```
- Runs on: `http://localhost:3000`
- Open this URL in your browser

## Quick Start Batch Files

### Option 1: Start Database Only
Double-click: `start-database.bat`

### Option 2: Start Backend Only
Double-click: `start-backend.bat`

### Option 3: Start Frontend Only
Double-click: `start-frontend.bat`

### Option 4: Start Everything
Double-click: `start-all-local.bat`

## Verify Everything is Running

Check ports:
```bash
netstat -ano | findstr "8000 5055 3000"
```

You should see:
- Port 8000: SurrealDB
- Port 5055: Backend API
- Port 3000: Frontend

## Access the Application

Open browser: `http://localhost:3000`

## Stop Everything

Press `CTRL+C` in each terminal window

Or use: `stop.bat`

## Project Structure

```
open-notebook/
├── api/                    # Backend (Python/FastAPI)
├── frontend/               # Frontend (Next.js/React)
├── open_notebook/          # Core Python package
├── .env                    # Backend configuration
├── frontend/.env.local     # Frontend configuration
└── docker-compose.yml      # Database configuration
```

## Important Configuration Files

### Backend: `.env`
```
SURREAL_URL=ws://localhost:8000/rpc
SURREAL_USER=root
SURREAL_PASSWORD=root
SURREAL_NAMESPACE=open_notebook
SURREAL_DATABASE=open_notebook
```

### Frontend: `frontend/.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:5055
```

## Troubleshooting

### Database won't start
- Make sure Docker Desktop is running
- Check if port 8000 is already in use

### Backend errors
- Make sure database is running first
- Check `.env` file has correct settings
- Verify virtual environment is activated

### Frontend errors
- Make sure backend is running
- Check `frontend/.env.local` has correct API URL
- Try `npm install` if dependencies are missing

## Development Workflow

1. Start database (Terminal 1)
2. Wait 5 seconds for database to be ready
3. Start backend (Terminal 2)
4. Wait for "Uvicorn running" message
5. Start frontend (Terminal 3)
6. Open browser to http://localhost:3000

That's it! Your project is now running locally.
