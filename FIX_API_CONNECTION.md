# 🔧 Fix: Unable to Connect to API Server

## Problem
You see this error:
```
Unable to Connect to API Server
The Open Notebook API server could not be reached
```

## ✅ Solution Applied

I've fixed this issue by adding the `API_URL` environment variable to `docker-compose.yml`.

### What Was Wrong
The frontend (running in Docker) couldn't find the backend API because it was trying to connect to `localhost:5055` from inside the container, which doesn't work in Docker networking.

### What I Fixed
Added this line to `docker-compose.yml`:
```yaml
- API_URL=http://localhost:5055
```

This tells the frontend (in your browser) to connect to `http://localhost:5055` on your host machine.

---

## ✅ Verification Steps

### 1. Check Services Are Running
```cmd
docker compose ps
```

You should see:
```
NAME                            STATUS
open-notebook-open_notebook-1   Up
open-notebook-surrealdb-1       Up
```

### 2. Test Backend API
Open: http://localhost:5055/docs

You should see the API documentation (Swagger UI).

### 3. Test Frontend
Open: http://localhost:8502

You should see the Open Notebook interface WITHOUT the connection error.

---

## 🐛 If Still Not Working

### Step 1: Restart Services
```cmd
docker compose down
docker compose up -d
```

Wait 30 seconds, then try again.

### Step 2: Check Logs
```cmd
docker compose logs -f open_notebook
```

Look for errors.

### Step 3: Verify Environment Variable
```cmd
docker compose exec open_notebook env | findstr API_URL
```

Should show:
```
API_URL=http://localhost:5055
```

### Step 4: Check Ports
```cmd
netstat -ano | findstr :8502
netstat -ano | findstr :5055
```

Both ports should be listening.

---

## 🌐 For Different Deployment Scenarios

### Local Development (Current Setup)
```yaml
- API_URL=http://localhost:5055
```

### Remote Server (Public IP)
```yaml
- API_URL=http://YOUR_SERVER_IP:5055
```

### Behind Reverse Proxy (Domain)
```yaml
- API_URL=https://your-domain.com
```

### Custom Port
```yaml
- API_URL=http://localhost:CUSTOM_PORT
```

---

## 📝 Understanding the Fix

### The Problem
```
Browser → http://localhost:8502 (Frontend in Docker)
          ↓
Frontend tries to connect to API
          ↓
Uses localhost:5055 (WRONG - this is inside container)
          ↓
Connection fails ❌
```

### The Solution
```
Browser → http://localhost:8502 (Frontend in Docker)
          ↓
Frontend gets API_URL from environment
          ↓
Uses http://localhost:5055 (CORRECT - this is host machine)
          ↓
Connection succeeds ✅
```

---

## 🎯 Quick Fix Commands

If you ever see this error again:

```cmd
# Stop services
docker compose down

# Make sure API_URL is in docker-compose.yml
# (It should be there now)

# Start services
docker compose up -d

# Wait 30 seconds
timeout /t 30

# Open browser
start http://localhost:8502
```

---

## ✅ Current Status

- ✅ docker-compose.yml updated with API_URL
- ✅ Services restarted
- ✅ Should be working now!

Open http://localhost:8502 and verify the connection error is gone.

---

## 📚 Related Files

- **docker-compose.yml** - Contains the fix
- **frontend/src/lib/config.ts** - How frontend detects API URL
- **frontend/src/app/config/route.ts** - Runtime config endpoint

---

## 🆘 Still Having Issues?

1. Check **SETUP_AND_RUN_GUIDE.md** troubleshooting section
2. Check logs: `docker compose logs -f`
3. Restart: `docker compose restart`
4. Ask on Discord: https://discord.gg/37XJPXfz2w

---

## ✨ Next Steps

After fixing the connection:
1. Configure AI models (see **CONFIGURE_MODELS_GUIDE.md**)
2. Create your first notebook
3. Start using Open Notebook!

Happy researching! 🚀
