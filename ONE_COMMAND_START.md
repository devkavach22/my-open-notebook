# 🚀 One Command Start - Local Development

## ✅ Super Easy Start

### Option 1: Start Everything at Once (Recommended!)

**Double-click**: `start-all-local.bat`

This will:
1. Open 3 terminal windows automatically
2. Start Database, Backend, and Frontend
3. Wait 30 seconds
4. Open browser to http://localhost:3000

**That's it!** 🎉

---

### Option 2: Start Services Individually

If you prefer to start each service separately:

**Terminal 1 - Database**:
```cmd
start-database.bat
```
Or double-click: `start-database.bat`

**Terminal 2 - Backend**:
```cmd
start-backend.bat
```
Or double-click: `start-backend.bat`

**Terminal 3 - Frontend**:
```cmd
start-frontend.bat
```
Or double-click: `start-frontend.bat`

---

## 📝 Batch Files Created

| File | What It Does | Port |
|------|-------------|------|
| **start-all-local.bat** | Starts everything automatically | All |
| **start-database.bat** | Starts SurrealDB only | 8000 |
| **start-backend.bat** | Starts Backend API only | 5055 |
| **start-frontend.bat** | Starts Frontend only | 3000 |

---

## 🎯 Quick Commands

### Start Everything:
```cmd
start-all-local.bat
```

### Start Backend Only:
```cmd
start-backend.bat
```

### Start Database Only:
```cmd
start-database.bat
```

### Start Frontend Only:
```cmd
start-frontend.bat
```

---

## 🌐 Access URLs

Once services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5055
- **API Docs**: http://localhost:5055/docs
- **Database**: http://localhost:8000

---

## 🛑 Stop Services

### Stop All:
Close all 3 terminal windows

### Stop Individual Service:
Press `Ctrl+C` in the terminal window

---

## 💡 Pro Tips

### Tip 1: Use start-all-local.bat
- Easiest way to start everything
- Opens all terminals automatically
- Opens browser when ready

### Tip 2: Keep Terminals Open
- Don't close the terminal windows
- They show real-time logs
- Useful for debugging

### Tip 3: Restart Individual Services
- If one service crashes, just restart that one
- No need to restart everything

---

## 🔧 Troubleshooting

### Problem: "surreal: command not found"
**Solution**: Install SurrealDB from https://surrealdb.com/install

### Problem: Port already in use
**Solution**: 
```cmd
# Find and kill the process
netstat -ano | findstr :5055
taskkill /PID <PID> /F
```

### Problem: Backend won't start
**Solution**: Make sure dependencies are installed:
```cmd
python -m uv sync
```

### Problem: Frontend won't start
**Solution**: Install npm dependencies:
```cmd
cd frontend
npm install
```

---

## 📊 What Each Service Does

### Database (Port 8000)
- Stores all data
- Notebooks, sources, notes, etc.
- File-based storage

### Backend API (Port 5055)
- Python FastAPI application
- Business logic
- REST API endpoints

### Frontend (Port 3000)
- Next.js React application
- User interface
- Calls backend API

---

## ✅ Daily Workflow

### Morning (Start Work):
1. Double-click `start-all-local.bat`
2. Wait 30 seconds
3. Browser opens automatically
4. Start coding!

### During Day (Making Changes):
- Edit files
- Save
- Services auto-reload
- See changes immediately

### Evening (End Work):
1. Close all 3 terminal windows
2. Done!

---

## 🎨 Your Studio Changes

All your Studio UI changes are ready:
- ✅ Sources | Chat | Studio layout
- ✅ 9 feature cards
- ✅ All clickable
- ✅ NotebookLM-style design

---

## 🚀 Summary

**Easiest way to start**:
```cmd
start-all-local.bat
```

**Or start individually**:
```cmd
start-database.bat
start-backend.bat
start-frontend.bat
```

**Access**: http://localhost:3000

That's it! One command and you're ready to code! 🎉

