# 🚀 Start Commands - Quick Reference

## When You Enter the Project

### Option 1: Using Docker (Recommended - Easiest)

```cmd
# Navigate to project folder
cd C:\Users\hemanshi.l\Desktop\open-notebook

# Start everything
docker compose up -d

# Wait 30 seconds for services to start
timeout /t 30

# Open in browser
start http://localhost:8502
```

**That's it!** Everything starts automatically.

---

### Option 2: Check if Already Running

```cmd
# Check status
docker compose ps

# If running, just open browser
start http://localhost:8502
```

---

## Complete Startup Commands

### 1. Navigate to Project
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
```

### 2. Start Services
```cmd
docker compose up -d
```

### 3. Wait for Startup (30 seconds)
```cmd
timeout /t 30
```

### 4. Open Application
```cmd
start http://localhost:8502
```

### 5. (Optional) Open API Docs
```cmd
start http://localhost:5055/docs
```

---

## One-Line Startup

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook && docker compose up -d && timeout /t 30 && start http://localhost:8502
```

Copy and paste this entire line!

---

## Stop Commands

### Stop Everything
```cmd
docker compose down
```

### Stop but Keep Data
```cmd
docker compose stop
```

### Restart
```cmd
docker compose restart
```

---

## Check Status Commands

### Check if Running
```cmd
docker compose ps
```

### View Logs
```cmd
docker compose logs -f
```

### View Only App Logs
```cmd
docker compose logs -f open_notebook
```

### Check Health
```cmd
curl http://localhost:5055/health
```

---

## Development Mode (Run from Source)

If you want to modify code:

### Terminal 1: Start Database
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose up -d surrealdb
```

### Terminal 2: Start Backend
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
.venv\Scripts\activate
python run_api.py
```

### Terminal 3: Start Frontend
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook\frontend
npm run dev
```

Then open: http://localhost:3000

---

## Daily Workflow

### Morning (Start Work)
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose up -d
timeout /t 30
start http://localhost:8502
```

### Evening (Stop Work)
```cmd
docker compose down
```

---

## Troubleshooting Commands

### Services Won't Start
```cmd
# Stop everything
docker compose down

# Remove old containers
docker compose rm -f

# Start fresh
docker compose up -d
```

### Port Already in Use
```cmd
# Find what's using port 8502
netstat -ano | findstr :8502

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Start again
docker compose up -d
```

### Database Issues
```cmd
# Restart database
docker compose restart surrealdb

# Wait 10 seconds
timeout /t 10

# Restart app
docker compose restart open_notebook
```

### Clear Everything and Start Fresh
```cmd
# Stop services
docker compose down

# Remove volumes (WARNING: Deletes all data!)
docker compose down -v

# Start fresh
docker compose up -d
```

---

## Update to Latest Version

```cmd
# Pull latest images
docker compose pull

# Restart with new images
docker compose up -d
```

---

## Quick Reference Card

| Command | What It Does |
|---------|-------------|
| `docker compose up -d` | Start everything |
| `docker compose down` | Stop everything |
| `docker compose ps` | Check status |
| `docker compose logs -f` | View logs |
| `docker compose restart` | Restart services |
| `docker compose pull` | Update to latest |
| `start http://localhost:8502` | Open app |
| `start http://localhost:5055/docs` | Open API docs |

---

## Create a Startup Script

Create a file called `start.bat`:

```batch
@echo off
echo Starting Open Notebook...
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose up -d
echo Waiting for services to start...
timeout /t 30 /nobreak
echo Opening browser...
start http://localhost:8502
echo Done! Open Notebook is running.
pause
```

Then just double-click `start.bat` to start everything!

---

## Create a Stop Script

Create a file called `stop.bat`:

```batch
@echo off
echo Stopping Open Notebook...
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose down
echo Done! Open Notebook stopped.
pause
```

---

## Aliases (Optional)

Add to your PowerShell profile:

```powershell
# Open PowerShell profile
notepad $PROFILE

# Add these lines:
function Start-OpenNotebook {
    cd C:\Users\hemanshi.l\Desktop\open-notebook
    docker compose up -d
    timeout /t 30
    start http://localhost:8502
}

function Stop-OpenNotebook {
    cd C:\Users\hemanshi.l\Desktop\open-notebook
    docker compose down
}

# Save and restart PowerShell
# Then use:
# Start-OpenNotebook
# Stop-OpenNotebook
```

---

## Most Common Commands

### Start
```cmd
docker compose up -d
```

### Stop
```cmd
docker compose down
```

### Restart
```cmd
docker compose restart
```

### Check Status
```cmd
docker compose ps
```

### View Logs
```cmd
docker compose logs -f
```

---

## Remember

- **Always navigate to project folder first!**
- **Wait 30 seconds after starting**
- **Use `docker compose` (not `docker-compose`)**
- **Check status with `docker compose ps`**

---

## 🎯 Your Daily Routine

1. Open terminal
2. Run: `cd C:\Users\hemanshi.l\Desktop\open-notebook`
3. Run: `docker compose up -d`
4. Wait 30 seconds
5. Open: http://localhost:8502
6. Start working!

When done:
1. Run: `docker compose down`

That's it! 🚀
