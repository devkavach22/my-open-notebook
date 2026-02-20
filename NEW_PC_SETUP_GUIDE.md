# Open Notebook - New PC Setup Guide

Complete guide to set up the Open Notebook project on a new computer.

## Prerequisites

Before you start, install these on your new PC:

### 1. Git
- Download: https://git-scm.com/downloads
- Install with default settings

### 2. Docker Desktop
- Download: https://www.docker.com/products/docker-desktop/
- Install and start Docker Desktop
- Make sure it's running (check system tray)

### 3. Python 3.12+
- Download: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation
- Verify: Open CMD and type `python --version`

### 4. Node.js 20.x LTS
- Download: https://nodejs.org/ (LTS version)
- Install with default settings
- Verify: Open CMD and type `node --version` and `npm --version`

### 5. uv (Python Package Manager)
- Install: `pip install uv`
- Or follow: https://docs.astral.sh/uv/getting-started/installation/

## Step-by-Step Setup

### Step 1: Clone the Repository

```bash
# Open Command Prompt or PowerShell
cd C:\Users\YourUsername\Desktop

# Clone the repository
git clone https://github.com/YOUR_USERNAME/open-notebook.git

# Navigate into the project
cd open-notebook
```

### Step 2: Set Up Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` file (use Notepad or any text editor):
```
OPEN_NOTEBOOK_ENCRYPTION_KEY=your-secret-key-here-change-this

SURREAL_URL=ws://localhost:8000/rpc
SURREAL_USER=root
SURREAL_PASSWORD=root
SURREAL_NAMESPACE=open_notebook
SURREAL_DATABASE=open_notebook
```

**Important**: Change `OPEN_NOTEBOOK_ENCRYPTION_KEY` to any random string (at least 16 characters)

### Step 3: Install Backend Dependencies

```bash
# Install Python dependencies using uv
uv sync
```

This creates a virtual environment in `.venv` folder and installs all Python packages.

### Step 4: Install Frontend Dependencies

```bash
# Navigate to frontend folder
cd frontend

# Install Node.js dependencies
npm install

# Go back to root
cd ..
```

### Step 5: Start the Database

```bash
# Start SurrealDB in Docker
docker-compose up -d surrealdb
```

Wait 5-10 seconds for the database to start.

### Step 6: Run Database Migrations

The migrations will run automatically when you start the backend, but you can check:

```bash
# Check current migration version
python check-migrations.py
```

### Step 7: Start the Application

**Option A: Use Batch Files (Easiest)**

Double-click: `start-all-local.bat`

This opens 3 windows:
- Database (Docker)
- Backend API (Python)
- Frontend (Next.js)

**Option B: Manual Start (3 separate terminals)**

Terminal 1 - Database:
```bash
docker-compose up surrealdb
```

Terminal 2 - Backend:
```bash
.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

### Step 8: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5055
- **API Docs**: http://localhost:5055/docs

### Step 9: Create Your First User

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Fill in the form:
   - Username: your_username
   - Email: your@email.com
   - Password: YourPassword123!
4. Click "Create Account"
5. You'll be logged in automatically

## Verification Checklist

✅ Docker Desktop is running
✅ Database container is running: `docker ps` (should see surrealdb)
✅ Backend is running on port 5055: http://localhost:5055/health
✅ Frontend is running on port 3000: http://localhost:3000
✅ You can sign up and log in
✅ You can create a notebook

## Common Issues & Solutions

### Issue 1: "Docker is not running"
**Solution**: Start Docker Desktop and wait for it to fully start

### Issue 2: "Port 5055 already in use"
**Solution**: 
```bash
# Find what's using the port
netstat -ano | findstr :5055

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Issue 3: "Module not found" errors
**Solution**: 
```bash
# Reinstall backend dependencies
uv sync --reinstall

# Reinstall frontend dependencies
cd frontend
npm install
cd ..
```

### Issue 4: "Database connection failed"
**Solution**:
```bash
# Restart database
docker-compose restart surrealdb

# Check if it's running
docker ps
```

### Issue 5: Frontend won't start
**Solution**:
```bash
cd frontend
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Project Structure

```
open-notebook/
├── api/                    # Backend API routes
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/          # Pages and routes
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities and hooks
│   └── package.json
├── open_notebook/         # Core Python package
│   ├── ai/               # AI/LLM integration
│   ├── database/         # Database and migrations
│   ├── domain/           # Domain models
│   ├── graphs/           # LangGraph workflows
│   └── utils/            # Utilities
├── .env                   # Environment variables (create this)
├── docker-compose.yml     # Docker configuration
├── pyproject.toml        # Python dependencies
└── start-all-local.bat   # Quick start script
```

## Useful Commands

### Database
```bash
# Start database
docker-compose up -d surrealdb

# Stop database
docker-compose stop surrealdb

# View database logs
docker logs open-notebook-surrealdb-1

# Access database CLI
docker exec -it open-notebook-surrealdb-1 /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
```

### Backend
```bash
# Start backend
.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload

# Check migrations
python check-migrations.py

# Run tests
pytest
```

### Frontend
```bash
cd frontend

# Development
npm run dev

# Build for production
npm run build

# Run production build
npm start

# Run tests
npm test
```

## Configuration Files

### `.env` - Environment Variables
Contains database connection, API keys, and secrets.

### `docker-compose.yml` - Docker Configuration
Defines database and application containers.

### `pyproject.toml` - Python Dependencies
Lists all Python packages needed.

### `frontend/package.json` - Node.js Dependencies
Lists all frontend packages needed.

## Development Workflow

1. **Start the application**: `start-all-local.bat`
2. **Make changes** to code
3. **Backend auto-reloads** (thanks to `--reload` flag)
4. **Frontend auto-reloads** (Next.js hot reload)
5. **Test your changes** in the browser
6. **Commit changes**: 
   ```bash
   git add .
   git commit -m "Your message"
   git push
   ```

## Stopping the Application

### Stop All Services
```bash
# Stop Docker containers
docker-compose down

# Close the terminal windows for backend and frontend
# Or press Ctrl+C in each terminal
```

### Or use batch file
Double-click: `stop-local.bat`

## Updating the Project

When you pull new changes from Git:

```bash
# Pull latest changes
git pull

# Update backend dependencies
uv sync

# Update frontend dependencies
cd frontend
npm install
cd ..

# Restart everything
# Stop all services, then start again
```

## Getting Help

### Check Logs
- Backend: Look at the terminal where backend is running
- Frontend: Look at the terminal where frontend is running
- Database: `docker logs open-notebook-surrealdb-1`

### Diagnostic Tool
```bash
# Run diagnostic
diagnose-project.bat
```

This checks:
- Is Docker running?
- Is database running?
- Is backend running?
- Is frontend running?
- Can backend connect to database?

## Summary

**Minimum steps to get started:**

1. Install: Git, Docker, Python, Node.js, uv
2. Clone repository
3. Copy `.env.example` to `.env` and edit
4. Run `uv sync` (backend dependencies)
5. Run `cd frontend && npm install` (frontend dependencies)
6. Double-click `start-all-local.bat`
7. Open http://localhost:3000
8. Sign up and start using!

**That's it! You're ready to develop! 🚀**
