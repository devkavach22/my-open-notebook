# 📁 Batch Files Summary - Easy Start Guide

## 🎯 All Batch Files Created

### For Local Development (Without Docker):

| File | Command | What It Does |
|------|---------|-------------|
| **start-all-local.bat** | Double-click | 🚀 Starts everything (Database + Backend + Frontend) |
| **start-database.bat** | Double-click | 🗄️ Starts SurrealDB only |
| **start-backend.bat** | Double-click | 🐍 Starts Python Backend API only |
| **start-frontend.bat** | Double-click | ⚛️ Starts Next.js Frontend only |

### For Docker (Production):

| File | Command | What It Does |
|------|---------|-------------|
| **start.bat** | Double-click | 🐳 Starts Docker containers |
| **stop.bat** | Double-click | 🛑 Stops Docker containers |
| **restart.bat** | Double-click | 🔄 Restarts Docker containers |
| **status.bat** | Double-click | 📊 Shows Docker status |
| **logs.bat** | Double-click | 📝 Shows Docker logs |

### Utilities:

| File | Command | What It Does |
|------|---------|-------------|
| **view-logs.bat** | Double-click | 👀 View API logs |
| **view-db-cli.bat** | Double-click | 💾 Open database CLI |
| **export-logs.bat** | Double-click | 📤 Export logs to file |
| **backup-database.bat** | Double-click | 💾 Backup database |

---

## 🚀 Quick Start Guide

### For Local Development:

**One Command** (Recommended):
```cmd
start-all-local.bat
```

**Or Individual Services**:
```cmd
start-database.bat    # Terminal 1
start-backend.bat     # Terminal 2
start-frontend.bat    # Terminal 3
```

### For Docker:

**One Command**:
```cmd
start.bat
```

---

## 📊 Comparison: Local vs Docker

| Feature | Local Development | Docker |
|---------|------------------|--------|
| **Start Command** | `start-all-local.bat` | `start.bat` |
| **Terminals Needed** | 3 | 0 |
| **Hot Reload** | ✅ Yes | ✅ Yes |
| **Easy Debugging** | ✅ Yes | ⚠️ Harder |
| **Setup Time** | 5 min | 2 min |
| **Resource Usage** | Lower | Higher |
| **Best For** | Development | Production/Testing |

---

## 🎯 When to Use What

### Use Local Development When:
- ✅ Actively developing/coding
- ✅ Need to debug backend/frontend
- ✅ Want faster hot reload
- ✅ Need to see detailed logs
- ✅ Testing new features

### Use Docker When:
- ✅ Just using the app
- ✅ Don't need to modify code
- ✅ Want easy setup
- ✅ Testing production build
- ✅ Sharing with others

---

## 📝 File Locations

All batch files are in the project root:
```
C:\Users\hemanshi.l\Desktop\open-notebook\
├── start-all-local.bat    ← Start everything (local)
├── start-database.bat     ← Start database only
├── start-backend.bat      ← Start backend only
├── start-frontend.bat     ← Start frontend only
├── start.bat              ← Start Docker
├── stop.bat               ← Stop Docker
├── restart.bat            ← Restart Docker
├── status.bat             ← Docker status
├── logs.bat               ← Docker logs
├── view-logs.bat          ← View API logs
├── view-db-cli.bat        ← Database CLI
├── export-logs.bat        ← Export logs
└── backup-database.bat    ← Backup database
```

---

## 🌐 Ports Used

| Service | Local Port | Docker Port |
|---------|-----------|-------------|
| **Frontend** | 3000 | 8502 |
| **Backend API** | 5055 | 5055 |
| **Database** | 8000 | 8000 |

---

## ✅ Quick Reference

### Start Local Development:
```cmd
# Option 1: Everything at once
start-all-local.bat

# Option 2: Individual services
start-database.bat
start-backend.bat
start-frontend.bat
```

### Start Docker:
```cmd
start.bat
```

### Stop Everything:
```cmd
# Local: Close terminal windows or Ctrl+C
# Docker: stop.bat
```

### View Logs:
```cmd
# Local: Check terminal windows
# Docker: logs.bat or view-logs.bat
```

### Access Database:
```cmd
view-db-cli.bat
```

---

## 💡 Pro Tips

### Tip 1: Bookmark These Commands
- Pin batch files to taskbar
- Create desktop shortcuts
- Add to Start menu

### Tip 2: Use start-all-local.bat
- Easiest way to start local dev
- Opens everything automatically
- Opens browser when ready

### Tip 3: Keep Docker for Quick Testing
- Use Docker when you just want to use the app
- Use local dev when coding

### Tip 4: Check Logs When Debugging
- Local: Look at terminal windows
- Docker: Run `logs.bat`

---

## 🎉 Summary

**For Development** (Coding):
```cmd
start-all-local.bat
```
Access: http://localhost:3000

**For Production** (Using):
```cmd
start.bat
```
Access: http://localhost:8502

**That's it!** Choose what works best for you! 🚀

