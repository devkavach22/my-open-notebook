# ⚡ Commands Quick Reference

## 🎯 Easiest Way - Use Batch Files

I created these files for you. Just double-click them!

| File | What It Does |
|------|-------------|
| **start.bat** | Start Open Notebook |
| **stop.bat** | Stop Open Notebook |
| **restart.bat** | Restart Open Notebook |
| **status.bat** | Check if running |
| **logs.bat** | View logs |

---

## 🚀 Manual Commands

### Start Everything
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose up -d
timeout /t 30
start http://localhost:8502
```

### Stop Everything
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose down
```

### Check Status
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose ps
```

### View Logs
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose logs -f
```

### Restart
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose restart
```

---

## 📋 Daily Workflow

### Morning - Start Work
1. Double-click **start.bat**
2. Wait for browser to open
3. Configure AI models (first time only)
4. Start working!

### Evening - Stop Work
1. Double-click **stop.bat**
2. Done!

---

## 🔧 Common Tasks

### Check if Running
Double-click **status.bat**

### View Logs
Double-click **logs.bat**

### Restart After Changes
Double-click **restart.bat**

### Update to Latest Version
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose pull
docker compose up -d
```

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:8502 |
| **API** | http://localhost:5055 |
| **API Docs** | http://localhost:5055/docs |
| **Database** | http://localhost:8000 |

---

## 🐛 Troubleshooting

### Services Won't Start
```cmd
docker compose down
docker compose up -d
```

### Port Already in Use
```cmd
netstat -ano | findstr :8502
taskkill /PID <PID> /F
docker compose up -d
```

### Clear Everything
```cmd
docker compose down -v
docker compose up -d
```

---

## 💡 Pro Tips

1. **Always navigate to project folder first**
2. **Wait 30 seconds after starting**
3. **Use batch files for convenience**
4. **Check logs if something goes wrong**
5. **Restart if you change .env or docker-compose.yml**

---

## 📚 More Help

- **START_COMMANDS.md** - Detailed command reference
- **SETUP_AND_RUN_GUIDE.md** - Complete setup guide
- **QUICK_START.md** - Quick reference
- **README_FIRST.md** - Getting started

---

## ✅ Quick Checklist

When you enter the project:

- [ ] Navigate to project folder
- [ ] Run `docker compose up -d` (or double-click start.bat)
- [ ] Wait 30 seconds
- [ ] Open http://localhost:8502
- [ ] Start working!

When you're done:

- [ ] Run `docker compose down` (or double-click stop.bat)

That's it! 🎉
