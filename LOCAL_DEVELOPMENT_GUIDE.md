# 🛠️ Local Development Guide (Without Docker)

## What You Need to Run

To run Open Notebook locally without Docker, you need to start 3 things:

1. **SurrealDB** (Database)
2. **Backend API** (Python/FastAPI)
3. **Frontend** (Next.js/React)

---

## 📋 Prerequisites

### Required Software:
- **Python 3.11+** (for backend)
- **Node.js 18+** (for frontend)
- **SurrealDB** (database)
- **uv** or **pip** (Python package manager)

---

## 🚀 Step-by-Step Setup

### Step 1: Install SurrealDB

**Windows**:
```cmd
# Download from https://surrealdb.com/install
# Or use Chocolatey:
choco install surrealdb

# Or use Scoop:
scoop install surrealdb
```

**Verify installation**:
```cmd
surreal version
```

---

### Step 2: Start SurrealDB

Open **Terminal 1** (keep it running):

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook

surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
```

**What this does**:
- Starts SurrealDB on port 8000
- Uses file-based storage (surreal_data folder)
- Username: root, Password: root

**Keep this terminal open!**

---

### Step 3: Install Backend Dependencies

Open **Terminal 2**:

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook

# Install uv (if not installed)
pip install uv

# Install dependencies
uv sync
```

Or with pip:
```cmd
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables

Create `.env` file in project root:

```env
# Database
SURREAL_URL=ws://localhost:8000/rpc
SURREAL_USER=root
SURREAL_PASSWORD=root
SURREAL_NAMESPACE=open_notebook
SURREAL_DATABASE=open_notebook

# Encryption (change this!)
OPEN_NOTEBOOK_ENCRYPTION_KEY=your-secret-key-here

# Optional: AI Provider API Keys
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GROQ_API_KEY=your-groq-key
```

---

### Step 5: Run Database Migrations

In **Terminal 2**:

```cmd
# Run migrations
python -m open_notebook.database.migrate
```

**What this does**:
- Creates all database tables
- Sets up indexes and functions
- Prepares database for use

---

### Step 6: Start Backend API

In **Terminal 2** (keep it running):

```cmd
# Using uvicorn directly
uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload

# Or using the run script
python run_api.py
```

**What this does**:
- Starts FastAPI backend on port 5055
- Auto-reloads on code changes
- Serves API endpoints

**Keep this terminal open!**

---

### Step 7: Install Frontend Dependencies

Open **Terminal 3**:

```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook\frontend

# Install dependencies
npm install
```

---

### Step 8: Configure Frontend Environment

Create `frontend/.env.local`:

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:5055
```

---

### Step 9: Start Frontend

In **Terminal 3** (keep it running):

```cmd
cd frontend

npm run dev
```

**What this does**:
- Starts Next.js dev server on port 3000
- Auto-reloads on code changes
- Serves frontend UI

**Keep this terminal open!**

---

## ✅ Summary: 3 Terminals Running

### Terminal 1: SurrealDB
```cmd
surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
```
**Port**: 8000

### Terminal 2: Backend API
```cmd
uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```
**Port**: 5055

### Terminal 3: Frontend
```cmd
cd frontend
npm run dev
```
**Port**: 3000

---

## 🌐 Access URLs

| Service | URL | Purpose |
|---------|-----|---------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:5055 | REST API |
| **API Docs** | http://localhost:5055/docs | Swagger UI |
| **Database** | http://localhost:8000 | SurrealDB |

---

## 🔧 Quick Start Commands

### Start Everything (3 separate terminals):

**Terminal 1 - Database**:
```cmd
surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
```

**Terminal 2 - Backend**:
```cmd
uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

**Terminal 3 - Frontend**:
```cmd
cd frontend && npm run dev
```

---

## 🛑 Stop Everything

Press `Ctrl+C` in each terminal to stop the services.

---

## 🐛 Troubleshooting

### Problem: "surreal: command not found"
**Solution**: Install SurrealDB from https://surrealdb.com/install

### Problem: "Port 8000 already in use"
**Solution**: 
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /PID <PID> /F
```

### Problem: "Port 5055 already in use"
**Solution**:
```cmd
# Find and kill process
netstat -ano | findstr :5055
taskkill /PID <PID> /F
```

### Problem: "Port 3000 already in use"
**Solution**:
```cmd
# Find and kill process
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problem: Backend won't start
**Solution**:
```cmd
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Check .env file exists
dir .env
```

### Problem: Frontend won't start
**Solution**:
```cmd
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
cd frontend
rmdir /s /q node_modules
rmdir /s /q .next
npm install
npm run dev
```

### Problem: Database connection failed
**Solution**:
```cmd
# Make sure SurrealDB is running
# Check the terminal where you started it

# Test connection
curl http://localhost:8000/health
```

---

## 📝 Development Workflow

### Making Changes:

**Frontend Changes**:
1. Edit files in `frontend/src/`
2. Save file
3. Browser auto-refreshes
4. See changes immediately

**Backend Changes**:
1. Edit files in `api/` or `open_notebook/`
2. Save file
3. Backend auto-reloads
4. Test in browser or API docs

**Database Changes**:
1. Create new migration file in `open_notebook/database/migrations/`
2. Run migrations: `python -m open_notebook.database.migrate`
3. Restart backend

---

## 🎯 What Each Component Does

### 1. SurrealDB (Terminal 1)
- Stores all data (notebooks, sources, notes, etc.)
- Runs on port 8000
- File-based storage in `surreal_data/`

### 2. Backend API (Terminal 2)
- Python FastAPI application
- Handles all business logic
- Communicates with database
- Provides REST API endpoints
- Runs on port 5055

### 3. Frontend (Terminal 3)
- Next.js React application
- User interface
- Calls backend API
- Runs on port 3000

---

## 🔄 Restart Services

### Restart Database:
```cmd
# In Terminal 1, press Ctrl+C
# Then run again:
surreal start --log info --user root --pass root file:surreal_data/mydatabase.db
```

### Restart Backend:
```cmd
# In Terminal 2, press Ctrl+C
# Then run again:
uvicorn api.main:app --host 0.0.0.0 --port 5055 --reload
```

### Restart Frontend:
```cmd
# In Terminal 3, press Ctrl+C
# Then run again:
npm run dev
```

---

## 📊 Monitoring

### View Backend Logs:
- Check Terminal 2 where backend is running
- See all API requests and errors

### View Frontend Logs:
- Check Terminal 3 where frontend is running
- See compilation and runtime errors

### View Database Logs:
- Check Terminal 1 where SurrealDB is running
- See database queries and operations

---

## � Hot Reload

All services support hot reload:
- **Frontend**: Auto-refreshes on file changes
- **Backend**: Auto-reloads on file changes
- **Database**: No reload needed (always running)

---

## 💾 Data Persistence

### Where Data is Stored:
- **Database**: `surreal_data/mydatabase.db/`
- **Uploads**: `notebook_data/uploads/`
- **Cache**: `notebook_data/tiktoken-cache/`

### Backup Data:
```cmd
# Backup database
surreal export --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook > backup.surql

# Backup uploads
xcopy notebook_data\uploads backup\uploads /E /I
```

---

## 🚀 Production Build

### Build Frontend:
```cmd
cd frontend
npm run build
npm start
```

### Run Backend in Production:
```cmd
uvicorn api.main:app --host 0.0.0.0 --port 5055 --workers 4
```

---

## ✅ Checklist

### Initial Setup:
- [ ] Install Python 3.11+
- [ ] Install Node.js 18+
- [ ] Install SurrealDB
- [ ] Clone/download project
- [ ] Create .env file
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Run database migrations

### Daily Development:
- [ ] Start SurrealDB (Terminal 1)
- [ ] Start Backend (Terminal 2)
- [ ] Start Frontend (Terminal 3)
- [ ] Open http://localhost:3000
- [ ] Make changes
- [ ] Test changes
- [ ] Stop all services (Ctrl+C)

---

## 🎉 You're Ready!

Now you can develop locally without Docker:
- ✅ Full control over each service
- ✅ Easy debugging
- ✅ Fast hot reload
- ✅ See all logs in real-time
- ✅ No Docker overhead

Open http://localhost:3000 and start coding! 🚀

