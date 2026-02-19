# 🚀 Start Local Development - Quick Guide

## ✅ What You Need

You need to run 3 services in 3 separate terminals:

1. **SurrealDB** (Database) - Port 8000
2. **Backend API** (Python) - Port 5055  
3. **Frontend** (Next.js) - Port 3000

---

## 🎯 Quick Start (3 Terminals)

### Terminal 1: Start SurrealDB

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook

surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
```

**Keep this terminal open!**

---

### Terminal 2: Start Backend API

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook

.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

**Or double-click**: `start-backend.bat`

**Keep this terminal open!**

---

### Terminal 3: Start Frontend

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook\frontend

npm run dev
```

**Keep this terminal open!**

---

## 🌐 Access URLs

Once all 3 services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5055
- **API Docs**: http://localhost:5055/docs
- **Database**: http://localhost:8000

---

## ✅ What We Fixed

### Problem: `uvicorn: command not found`

**Solution**: Use the virtual environment Python:
```cmd
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

### Problem: `ModuleNotFoundError: No module named 'surreal_commands'`

**Solution**: Install all dependencies with `uv`:
```cmd
python -m uv sync
```

This created a virtual environment (`.venv`) with all required packages.

---

## 📝 Batch Files Created

### start-backend.bat
Double-click this file to start the backend automatically!

It will:
1. Activate the virtual environment
2. Start uvicorn with auto-reload
3. Keep the terminal open

---

## 🔧 Troubleshooting

### Backend won't start?

**Check if virtual environment exists**:
```cmd
dir .venv
```

**If not, install dependencies**:
```cmd
python -m uv sync
```

**Then start backend**:
```cmd
.\.venv\Scripts\python.exe -m uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

---

### Port already in use?

**Find and kill the process**:
```cmd
# For port 5055 (backend)
netstat -ano | findstr :5055
taskkill /PID <PID> /F

# For port 3000 (frontend)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# For port 8000 (database)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### SurrealDB not installed?

**Download from**: https://surrealdb.com/install

**Or use Chocolatey**:
```cmd
choco install surrealdb
```

---

## 🎯 Development Workflow

### 1. Start Services (Once per day)
- Terminal 1: Start SurrealDB
- Terminal 2: Start Backend
- Terminal 3: Start Frontend

### 2. Make Changes
- Edit files in `frontend/src/` or `api/` or `open_notebook/`
- Save files
- Services auto-reload

### 3. Test Changes
- Open http://localhost:3000
- See your changes immediately

### 4. Stop Services (End of day)
- Press `Ctrl+C` in each terminal

---

## 📊 Service Status

### Check if Backend is running:
```cmd
curl http://localhost:5055/
```

**Expected**: `{"message":"Open Notebook API is running"}`

### Check if Frontend is running:
```cmd
curl http://localhost:3000/
```

**Expected**: HTML page

### Check if Database is running:
```cmd
curl http://localhost:8000/health
```

**Expected**: Health status

---

## 🎨 Your Studio Changes

All your Studio UI changes are ready! Once the frontend starts, you'll see:

- ✅ Sources | Chat | Studio layout
- ✅ Studio with 9 feature cards
- ✅ All features clickable
- ✅ Audio Overview fully working
- ✅ NotebookLM-style design

---

## 🚀 Next Steps

1. **Start all 3 services** (see above)
2. **Open http://localhost:3000**
3. **Create a notebook**
4. **See your new Studio UI!**

---

## 💡 Pro Tips

### Use Batch Files
- Double-click `start-backend.bat` instead of typing commands
- Easier and faster!

### Keep Terminals Organized
- Label each terminal window
- Terminal 1: "Database"
- Terminal 2: "Backend"
- Terminal 3: "Frontend"

### Watch the Logs
- All terminals show real-time logs
- See errors immediately
- Debug faster

---

## ✅ Summary

**To run locally without Docker**:

1. Install dependencies: `python -m uv sync` ✅ (Done!)
2. Start SurrealDB: `surreal start ...`
3. Start Backend: `.\.venv\Scripts\python.exe -m uvicorn ...`
4. Start Frontend: `cd frontend && npm run dev`

**Access**: http://localhost:3000

Happy coding! 🚀

