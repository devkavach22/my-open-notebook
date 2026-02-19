# ⚡ Quick Start - Your Project is Running!

## ✅ Status: RUNNING

Your Open Notebook is already running on your machine!

---

## 🌐 Access URLs

### Frontend (Web UI)
**URL**: http://localhost:8502
**What**: Main application interface
**Use**: Create notebooks, chat with AI, manage sources

### Backend API
**URL**: http://localhost:5055
**What**: REST API server
**Use**: API calls from frontend

### API Documentation
**URL**: http://localhost:5055/docs
**What**: Interactive API documentation (Swagger)
**Use**: Test API endpoints, see request/response formats

### Database
**URL**: http://localhost:8000
**What**: SurrealDB database
**Use**: Data storage (internal)

---

## 🎯 What to Do Next

### 1. Open the Application
Click here: http://localhost:8502

### 2. Configure AI Provider (REQUIRED) ⚠️

**You'll see a warning**: "You are missing some default models..."
**This is NORMAL!** Follow these steps:

**Quick Setup (5 minutes)**:
1. Get a FREE API key from Groq: https://console.groq.com/
2. In Open Notebook, go to **Settings** → **API Keys**
3. Click **+ Add Credential**
4. Choose **Groq** as provider
5. Paste your API key
6. Click **Save**
7. Click **Test Connection** ✅
8. Click **Discover Models** 
9. Click **Register Models** ✅
10. Go to **Settings** → **Models**
11. Set default models (use llama-3.1-70b for all)
12. Click **Save Defaults** ✅
13. Done! Warning will disappear 🎉

**Detailed Guide**: See **CONFIGURE_MODELS_GUIDE.md**

**Other Providers**:
- OpenAI: https://platform.openai.com/api-keys (Paid, Best)
- Anthropic: https://console.anthropic.com/ (Paid)
- Ollama: https://ollama.com/ (FREE, Local)

### 3. Create Your First Notebook

1. Click **Notebooks** in the sidebar
2. Click **+ New Notebook**
3. Enter:
   - Name: "My First Notebook"
   - Description: "Testing Open Notebook"
4. Click **Create**

### 4. Add a Source

1. Open your notebook
2. Click **+ Add Source**
3. Choose type:
   - **Upload File** (PDF, DOCX, TXT)
   - **Web URL** (article, blog post)
   - **Text** (paste content)
4. Upload/paste content
5. Wait for processing

### 5. Chat with AI

1. In your notebook, go to **Chat** tab
2. Type a question about your sources
3. Press Enter
4. Watch AI respond in real-time!

### 6. Try Other Features

- **Search**: Find information across all sources
- **Notes**: Create manual notes
- **Insights**: View AI-generated summaries
- **Podcasts**: Generate audio conversations!

---

## 🛠️ Common Commands

### View Status
```cmd
docker compose ps
```

### View Logs
```cmd
# All logs
docker compose logs -f

# Just app logs
docker compose logs -f open_notebook

# Last 50 lines
docker compose logs --tail=50
```

### Restart Application
```cmd
docker compose restart
```

### Stop Application
```cmd
docker compose down
```

### Start Application
```cmd
docker compose up -d
```

### Update to Latest Version
```cmd
docker compose pull
docker compose up -d
```

---

## 📊 Check if Running

### Quick Check
```cmd
docker compose ps
```

Should show:
```
NAME                            STATUS
open-notebook-open_notebook-1   Up X minutes
open-notebook-surrealdb-1       Up X minutes
```

### Test URLs
- Frontend: http://localhost:8502 (should load web page)
- API: http://localhost:5055/docs (should show API docs)
- Health: http://localhost:5055/health (should show `{"status":"healthy"}`)

---

## 🐛 Troubleshooting

### Problem: Can't access http://localhost:8502

**Solution 1**: Check if running
```cmd
docker compose ps
```

**Solution 2**: Restart
```cmd
docker compose restart
```

**Solution 3**: Check logs
```cmd
docker compose logs open_notebook
```

### Problem: "Connection refused" error

**Solution**: Wait 30 seconds after starting, then try again
```cmd
docker compose up -d
timeout /t 30
```

### Problem: Database errors

**Solution**: Restart database
```cmd
docker compose restart surrealdb
timeout /t 10
docker compose restart open_notebook
```

### Problem: Port already in use

**Solution**: Stop and restart
```cmd
docker compose down
docker compose up -d
```

---

## 📁 Important Files

### Configuration
- `.env` - Environment variables (API keys, settings)
- `docker-compose.yml` - Docker configuration

### Data Storage
- `notebook_data/` - Uploaded files, database
- `surreal_data/` - SurrealDB data

### Logs
```cmd
docker compose logs
```

---

## 🔑 Environment Variables

Edit `.env` file to configure:

```env
# REQUIRED: Encryption key for API keys
OPEN_NOTEBOOK_ENCRYPTION_KEY=your-secret-key

# Database (default values work)
SURREAL_URL=ws://surrealdb:8000/rpc
SURREAL_USER=root
SURREAL_PASSWORD=root

# Optional: AI Provider API Keys
# (Better to configure in UI)
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
```

After editing `.env`:
```cmd
docker compose down
docker compose up -d
```

---

## 📚 Learning Resources

### In This Project
1. **START_HERE.md** - Complete learning guide
2. **SETUP_AND_RUN_GUIDE.md** - Detailed setup instructions
3. **ALL_APIS_EXPLAINED.md** - All API endpoints explained
4. **LLM_FLOW_EXAMPLE.md** - How AI integration works
5. **REAL_CODE_EXAMPLE.md** - Real code walkthrough

### Official Documentation
- **Quick Start**: `docs/0-START-HERE/index.md`
- **User Guide**: `docs/3-USER-GUIDE/index.md`
- **API Reference**: `docs/7-DEVELOPMENT/api-reference.md`

---

## 🎉 You're All Set!

Your Open Notebook is running and ready to use!

**Next Steps**:
1. ✅ Open http://localhost:8502
2. ✅ Configure AI provider
3. ✅ Create a notebook
4. ✅ Upload a document
5. ✅ Chat with AI!

**Need Help?**
- Read **SETUP_AND_RUN_GUIDE.md** for detailed instructions
- Check `docs/6-TROUBLESHOOTING/quick-fixes.md`
- Join Discord: https://discord.gg/37XJPXfz2w

Happy researching! 🚀
