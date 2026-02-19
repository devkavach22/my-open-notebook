# 🚀 Complete Setup & Run Guide

This guide will help you run Open Notebook on your Windows machine.

---

## 📋 Prerequisites (Install These First)

### 1. Docker Desktop (REQUIRED)
**Download**: https://www.docker.com/products/docker-desktop/

**Installation**:
1. Download Docker Desktop for Windows
2. Run the installer
3. Restart your computer
4. Open Docker Desktop
5. Wait for it to start (you'll see a green icon in system tray)

**Verify Installation**:
```cmd
docker --version
docker compose version
```

You should see version numbers.

---

### 2. Node.js (For Development Only)
**Download**: https://nodejs.org/ (LTS version)

**Installation**:
1. Download the Windows installer
2. Run installer (keep default settings)
3. Restart terminal

**Verify Installation**:
```cmd
node --version
npm --version
```

---

### 3. Python 3.11 (For Development Only)
**Download**: https://www.python.org/downloads/

**Installation**:
1. Download Python 3.11.x
2. ✅ CHECK "Add Python to PATH"
3. Run installer
4. Restart terminal

**Verify Installation**:
```cmd
python --version
```

---

## 🎯 Option 1: Quick Start with Docker (RECOMMENDED)

### This is the EASIEST way to run the project!

### Step 1: Check Your Files

You already have these files:
- ✅ `docker-compose.yml`
- ✅ `.env.example`

### Step 2: Create .env File

```cmd
copy .env.example .env
```

### Step 3: Edit .env File

Open `.env` in notepad and change this line:
```
OPEN_NOTEBOOK_ENCRYPTION_KEY=change-me-to-a-secret-string
```

To something like:
```
OPEN_NOTEBOOK_ENCRYPTION_KEY=my-super-secret-key-12345
```

**Important**: This key encrypts your API keys in the database. Keep it secret!

### Step 4: Start Docker Services

```cmd
docker compose up -d
```

**What this does**:
- Downloads Docker images (first time only, ~2GB)
- Starts SurrealDB database
- Starts Open Notebook application
- Takes 2-3 minutes first time

**Wait for it to finish**, then check if running:
```cmd
docker compose ps
```

You should see:
```
NAME                    STATUS
open-notebook-surrealdb-1       running
open-notebook-open_notebook-1   running
```

### Step 5: Open the Application

**Frontend (Web UI)**: http://localhost:8502
**Backend API**: http://localhost:5055
**API Docs**: http://localhost:5055/docs

### Step 6: Configure AI Provider

1. Open http://localhost:8502
2. Go to **Settings** → **API Keys**
3. Click **Add Credential**
4. Choose provider (OpenAI, Anthropic, etc.)
5. Paste your API key
6. Click **Test Connection**
7. Click **Discover Models**
8. Click **Register Models**

**Get API Keys**:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Groq (FREE): https://console.groq.com/

### Step 7: Create Your First Notebook!

1. Click **Notebooks** in sidebar
2. Click **+ New Notebook**
3. Enter name and description
4. Start adding sources!

---

## 🛑 Stop the Application

```cmd
docker compose down
```

---

## 🔄 Restart the Application

```cmd
docker compose up -d
```

---

## 📊 View Logs

```cmd
# All logs
docker compose logs -f

# Just backend
docker compose logs -f open_notebook

# Just database
docker compose logs -f surrealdb
```

---

## 🎯 Option 2: Run from Source (For Development)

### This is for developers who want to modify the code.

### Step 1: Install Dependencies

#### Backend (Python)
```cmd
# Install uv (Python package manager)
pip install uv

# Install Python dependencies
uv sync
```

#### Frontend (Node.js)
```cmd
cd frontend
npm install
cd ..
```

### Step 2: Start Database

```cmd
docker compose up -d surrealdb
```

### Step 3: Create .env File

```cmd
copy .env.example .env
```

Edit `.env` and change:
```
OPEN_NOTEBOOK_ENCRYPTION_KEY=my-secret-key-123
SURREAL_URL=ws://localhost:8000/rpc
```

### Step 4: Start Backend

Open a NEW terminal:
```cmd
# Activate virtual environment
.venv\Scripts\activate

# Run backend
python run_api.py
```

Backend will start on: http://localhost:5055

### Step 5: Start Frontend

Open ANOTHER NEW terminal:
```cmd
cd frontend
npm run dev
```

Frontend will start on: http://localhost:3000

### Step 6: Open Application

**Frontend**: http://localhost:3000
**Backend API**: http://localhost:5055
**API Docs**: http://localhost:5055/docs

---

## 🔧 Development Workflow

### Backend Development

1. Make changes to Python files in:
   - `api/` - API endpoints
   - `open_notebook/` - Core logic
   - `prompts/` - AI prompts

2. Backend auto-reloads on file changes

3. View logs in terminal

### Frontend Development

1. Make changes to TypeScript files in:
   - `frontend/src/app/` - Pages
   - `frontend/src/components/` - Components
   - `frontend/src/lib/` - Utilities

2. Frontend auto-reloads on file changes

3. View in browser at http://localhost:3000

---

## 📁 Project Structure

```
open-notebook/
├── api/                      # Backend API
│   ├── routers/             # API endpoints
│   └── main.py              # FastAPI app
│
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # Pages
│   │   ├── components/     # React components
│   │   └── lib/            # Utilities
│   └── package.json
│
├── open_notebook/           # Core Python package
│   ├── ai/                 # AI integrations
│   ├── database/           # Database layer
│   ├── graphs/             # LangGraph workflows
│   └── utils/              # Utilities
│
├── prompts/                 # AI prompt templates
├── docs/                    # Documentation
├── docker-compose.yml       # Docker setup
├── .env                     # Configuration
└── pyproject.toml          # Python dependencies
```

---

## 🐛 Troubleshooting

### Problem: Docker not starting

**Solution**:
1. Open Docker Desktop
2. Wait for it to fully start
3. Check system tray for green icon
4. Try again

### Problem: Port already in use

**Error**: `port is already allocated`

**Solution**:
```cmd
# Stop all containers
docker compose down

# Check what's using the port
netstat -ano | findstr :8502
netstat -ano | findstr :5055

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Start again
docker compose up -d
```

### Problem: Database connection error

**Solution**:
```cmd
# Restart database
docker compose restart surrealdb

# Wait 10 seconds
timeout /t 10

# Restart app
docker compose restart open_notebook
```

### Problem: Frontend not loading

**Solution**:
1. Check if backend is running: http://localhost:5055/docs
2. Check Docker logs: `docker compose logs -f open_notebook`
3. Restart: `docker compose restart open_notebook`

### Problem: "Module not found" errors

**Solution**:
```cmd
# Backend
uv sync

# Frontend
cd frontend
npm install
```

---

## 🔑 Getting API Keys

### OpenAI (Paid)
1. Go to https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add to Open Notebook

**Cost**: ~$0.002 per 1000 tokens (very cheap)

### Anthropic Claude (Paid)
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Go to API Keys
4. Create key
5. Copy and add to Open Notebook

**Cost**: Similar to OpenAI

### Groq (FREE!)
1. Go to https://console.groq.com/
2. Sign up (free)
3. Get API key
4. Add to Open Notebook

**Cost**: FREE with rate limits

### Ollama (FREE, Local)
1. Download Ollama: https://ollama.com/
2. Install it
3. Run: `ollama pull llama2`
4. In Open Notebook, use endpoint: `http://host.docker.internal:11434`

**Cost**: FREE, runs on your computer

---

## 📊 System Requirements

### Minimum
- Windows 10/11
- 8GB RAM
- 10GB free disk space
- Internet connection

### Recommended
- Windows 11
- 16GB RAM
- 20GB free disk space
- Fast internet

---

## 🎓 Next Steps

After running the project:

1. ✅ Read **START_HERE.md** for learning path
2. ✅ Read **ALL_APIS_EXPLAINED.md** to understand APIs
3. ✅ Read **LLM_FLOW_EXAMPLE.md** to see how AI works
4. ✅ Make your first notebook
5. ✅ Upload a PDF and chat with it
6. ✅ Generate a podcast!

---

## 🆘 Need Help?

### Documentation
- **Quick Start**: `docs/0-START-HERE/index.md`
- **User Guide**: `docs/3-USER-GUIDE/index.md`
- **Troubleshooting**: `docs/6-TROUBLESHOOTING/quick-fixes.md`

### Community
- **Discord**: https://discord.gg/37XJPXfz2w
- **GitHub Issues**: https://github.com/lfnovo/open-notebook/issues

---

## 🎉 You're Ready!

Choose your path:
- **Just want to use it?** → Use Docker (Option 1)
- **Want to develop?** → Run from source (Option 2)

Happy researching! 🚀
