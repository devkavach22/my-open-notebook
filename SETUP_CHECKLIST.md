# ✅ Setup Checklist

Use this checklist to set up Open Notebook step by step.

---

## 🎯 Pre-Setup

- [x] Docker Desktop installed
- [x] Project downloaded
- [x] Docker services running
- [x] Can access http://localhost:8502

---

## 🔑 Step 1: Get API Key (5 minutes)

Choose ONE provider to start:

### Option A: Groq (FREE, Recommended)
- [ ] Go to https://console.groq.com/
- [ ] Sign up (free account)
- [ ] Click "API Keys"
- [ ] Click "Create API Key"
- [ ] Copy key (starts with `gsk_`)
- [ ] Save key somewhere safe

### Option B: OpenAI (Paid)
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Sign up / Log in
- [ ] Click "Create new secret key"
- [ ] Copy key (starts with `sk-`)
- [ ] Save key somewhere safe

### Option C: Anthropic (Paid)
- [ ] Go to https://console.anthropic.com/
- [ ] Sign up / Log in
- [ ] Go to "API Keys"
- [ ] Create key
- [ ] Copy key
- [ ] Save key somewhere safe

---

## 🤖 Step 2: Configure in Open Notebook (5 minutes)

### Add Credential
- [ ] Open http://localhost:8502
- [ ] Click **Settings** in left sidebar
- [ ] Click **API Keys** tab
- [ ] Click **+ Add Credential** button
- [ ] Select your provider (Groq/OpenAI/Anthropic)
- [ ] Paste your API key
- [ ] Give it a name (e.g., "My Groq Key")
- [ ] Click **Save**

### Test Connection
- [ ] Click **Test Connection** button
- [ ] Wait for test to complete
- [ ] Verify: ✅ "Connection successful"

### Discover Models
- [ ] Click **Discover Models** button
- [ ] Wait for discovery (10-30 seconds)
- [ ] Verify: You see a list of models

### Register Models
- [ ] Click **Register Models** button
- [ ] Wait for registration
- [ ] Verify: ✅ "Models registered successfully"

---

## ⚙️ Step 3: Set Default Models (2 minutes)

- [ ] Click **Settings** in left sidebar
- [ ] Click **Models** tab
- [ ] Set default models:
  - [ ] **Default Chat Model**: Choose a model (e.g., llama-3.1-70b-versatile)
  - [ ] **Default Strategy Model**: Same as chat model
  - [ ] **Default Answer Model**: Same as chat model
  - [ ] **Default Final Answer Model**: Same as chat model
  - [ ] **Default Embedding Model**: Leave empty if not available
- [ ] Click **Save Defaults**
- [ ] Verify: ✅ "Defaults saved successfully"

---

## 🎉 Step 4: Verify Setup (1 minute)

- [ ] Go to **Notebooks** page
- [ ] Verify: Warning message is GONE
- [ ] You should see: "Create your first notebook"

---

## 📚 Step 5: Create First Notebook (5 minutes)

### Create Notebook
- [ ] Click **+ New Notebook** button
- [ ] Enter name: "My First Notebook"
- [ ] Enter description: "Testing Open Notebook"
- [ ] Click **Create**

### Add Source
- [ ] Click **+ Add Source** button
- [ ] Choose source type:
  - [ ] **Upload File** (PDF, DOCX, TXT)
  - [ ] **Web URL** (article, blog)
  - [ ] **Text** (paste content)
- [ ] Upload/paste your content
- [ ] Wait for processing (30-60 seconds)
- [ ] Verify: Source appears in list

### Test Chat
- [ ] Click **Chat** tab
- [ ] Type a question: "What is this about?"
- [ ] Press Enter
- [ ] Verify: AI responds!

---

## 🎊 Congratulations!

If you checked all boxes above, you're ready to use Open Notebook!

---

## 🐛 Troubleshooting

### ❌ Test Connection Failed
**Problem**: API key invalid or no internet

**Fix**:
- [ ] Double-check API key (copy-paste again)
- [ ] Check internet connection
- [ ] Try different provider
- [ ] Check provider status page

---

### ❌ No Models Discovered
**Problem**: Provider has no models or API key lacks permissions

**Fix**:
- [ ] Check provider documentation
- [ ] Verify API key permissions
- [ ] Try different provider
- [ ] Check logs: `docker compose logs`

---

### ❌ Warning Still Shows After Setup
**Problem**: Default models not set

**Fix**:
- [ ] Go to Settings → Models
- [ ] Set ALL default models
- [ ] Click Save Defaults
- [ ] Refresh page (F5)

---

### ❌ Chat Not Working
**Problem**: Models not configured or no sources

**Fix**:
- [ ] Verify models are set (Settings → Models)
- [ ] Add at least one source to notebook
- [ ] Check logs: `docker compose logs -f`
- [ ] Restart: `docker compose restart`

---

## 📖 Next Steps

After completing setup:

- [ ] Read **START_HERE.md** for learning path
- [ ] Read **ALL_APIS_EXPLAINED.md** to understand APIs
- [ ] Read **LLM_FLOW_EXAMPLE.md** to see how AI works
- [ ] Explore other features (Search, Podcasts, Transformations)
- [ ] Join Discord: https://discord.gg/37XJPXfz2w

---

## 🎯 Quick Reference

### URLs
- Frontend: http://localhost:8502
- API: http://localhost:5055
- API Docs: http://localhost:5055/docs

### Commands
```cmd
# Check status
docker compose ps

# View logs
docker compose logs -f

# Restart
docker compose restart

# Stop
docker compose down

# Start
docker compose up -d
```

### Files
- **CONFIGURE_MODELS_GUIDE.md** - Detailed model setup
- **QUICK_START.md** - Quick reference
- **SETUP_AND_RUN_GUIDE.md** - Complete setup guide

---

## ✅ Setup Complete!

You're now ready to use Open Notebook!

**What you can do**:
- ✅ Create notebooks
- ✅ Upload documents
- ✅ Chat with AI
- ✅ Search content
- ✅ Generate podcasts
- ✅ Create transformations

Happy researching! 🚀
