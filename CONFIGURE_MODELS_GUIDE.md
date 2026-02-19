# 🤖 Configure AI Models - Step by Step

You're seeing this message because you need to configure AI models before using the app.

**Message**: "You are missing some default models and the app will not work as expected. Please, select them on the Models page."

This is NORMAL for a fresh installation! Let's fix it in 5 minutes.

---

## 🎯 Quick Fix (5 Minutes)

### Step 1: Get an API Key

You need an API key from one of these providers:

#### Option A: Groq (FREE, Recommended for Testing)
1. Go to https://console.groq.com/
2. Sign up (free account)
3. Click "API Keys" in sidebar
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

#### Option B: OpenAI (Paid, Best Quality)
1. Go to https://platform.openai.com/api-keys
2. Sign up / Log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

#### Option C: Anthropic Claude (Paid)
1. Go to https://console.anthropic.com/
2. Sign up / Log in
3. Go to "API Keys"
4. Create key
5. Copy it

---

### Step 2: Add API Key to Open Notebook

1. In Open Notebook, click **Settings** in the left sidebar
2. Click **API Keys** tab
3. Click **+ Add Credential** button
4. Fill in the form:
   - **Provider**: Choose your provider (Groq, OpenAI, Anthropic, etc.)
   - **API Key**: Paste your key
   - **Name**: Give it a name (e.g., "My Groq Key")
5. Click **Save**

---

### Step 3: Test Connection

1. After saving, you'll see your credential in the list
2. Click **Test Connection** button
3. Wait for the test to complete
4. You should see: ✅ "Connection successful"

---

### Step 4: Discover Models

1. Click **Discover Models** button
2. The app will query the provider for available models
3. You'll see a list of models (e.g., llama-3.1-70b, gpt-4, claude-3-opus)
4. Wait for discovery to complete

---

### Step 5: Register Models

1. Click **Register Models** button
2. This adds the discovered models to your database
3. Wait for registration to complete
4. You should see: ✅ "Models registered successfully"

---

### Step 6: Set Default Models

1. Go to **Settings** → **Models** tab
2. You'll see all registered models
3. Set default models for different purposes:
   - **Default Chat Model**: For conversations
   - **Default Embedding Model**: For search (if available)
   - **Default Strategy Model**: For Ask feature
   - **Default Answer Model**: For Ask feature
   - **Default Final Answer Model**: For Ask feature

4. Click **Save Defaults**

---

### Step 7: Verify Setup

1. Go back to **Notebooks** page
2. The warning should be gone!
3. Create a notebook and test chat

---

## 📊 Visual Guide

```
Settings → API Keys → + Add Credential
    ↓
Enter Provider & API Key
    ↓
Save
    ↓
Test Connection ✅
    ↓
Discover Models
    ↓
Register Models ✅
    ↓
Settings → Models → Set Defaults
    ↓
Save Defaults ✅
    ↓
Ready to use! 🎉
```

---

## 🔑 Recommended Providers

### For Testing (FREE)
**Groq**
- ✅ FREE with rate limits
- ✅ Very fast
- ✅ Good quality
- ✅ Models: Llama 3.1, Mixtral
- 🔗 https://console.groq.com/

### For Production (Paid)
**OpenAI**
- ✅ Best quality
- ✅ Most features
- ✅ Models: GPT-4, GPT-3.5
- 💰 ~$0.002 per 1000 tokens
- 🔗 https://platform.openai.com/

**Anthropic Claude**
- ✅ Great quality
- ✅ Long context
- ✅ Models: Claude 3 Opus, Sonnet
- 💰 Similar to OpenAI
- 🔗 https://console.anthropic.com/

### For Local (FREE)
**Ollama**
- ✅ Completely free
- ✅ Runs on your computer
- ✅ No API key needed
- ✅ Models: Llama 2, Mistral
- 🔗 https://ollama.com/

---

## 🐛 Troubleshooting

### Problem: "Connection failed"

**Possible causes**:
1. Invalid API key
2. No internet connection
3. Provider service down

**Solutions**:
1. Double-check your API key (copy-paste again)
2. Check internet connection
3. Try a different provider
4. Check provider status page

---

### Problem: "No models discovered"

**Possible causes**:
1. Provider has no models available
2. API key doesn't have permissions

**Solutions**:
1. Check provider documentation
2. Verify API key permissions
3. Try a different provider

---

### Problem: "Models registered but still showing warning"

**Solution**:
1. Go to Settings → Models
2. Set default models
3. Click Save Defaults
4. Refresh the page

---

### Problem: "Can't find Settings menu"

**Solution**:
1. Look in the left sidebar
2. Scroll down if needed
3. Click the gear icon ⚙️
4. Or click "Settings" text

---

## 📝 Example: Setting Up Groq (FREE)

### Step-by-Step with Screenshots

**1. Get Groq API Key**
```
1. Visit: https://console.groq.com/
2. Sign up (free)
3. Click "API Keys"
4. Click "Create API Key"
5. Copy: gsk_xxxxxxxxxxxxxxxxxxxxx
```

**2. Add to Open Notebook**
```
1. Open: http://localhost:8502
2. Click: Settings (left sidebar)
3. Click: API Keys tab
4. Click: + Add Credential
5. Select: Groq
6. Paste: gsk_xxxxxxxxxxxxxxxxxxxxx
7. Name: My Groq Key
8. Click: Save
```

**3. Test & Register**
```
1. Click: Test Connection
   → ✅ Connection successful
2. Click: Discover Models
   → Found: llama-3.1-70b-versatile, mixtral-8x7b, etc.
3. Click: Register Models
   → ✅ Models registered
```

**4. Set Defaults**
```
1. Click: Settings → Models
2. Set:
   - Chat Model: llama-3.1-70b-versatile
   - Embedding: (none for Groq)
   - Strategy: llama-3.1-70b-versatile
   - Answer: llama-3.1-70b-versatile
   - Final Answer: llama-3.1-70b-versatile
3. Click: Save Defaults
```

**5. Done!**
```
Go to Notebooks → Warning gone! 🎉
```

---

## 🎓 Understanding Models

### What are these models?

**Chat Model**
- Used for: Conversations in notebooks
- Example: GPT-4, Claude 3, Llama 3.1
- Purpose: Answer questions, discuss topics

**Embedding Model**
- Used for: Vector search
- Example: text-embedding-ada-002
- Purpose: Find similar content

**Strategy Model**
- Used for: Ask feature (step 1)
- Purpose: Decide what to search for

**Answer Model**
- Used for: Ask feature (step 2)
- Purpose: Answer from each source

**Final Answer Model**
- Used for: Ask feature (step 3)
- Purpose: Synthesize final answer

---

## 💡 Tips

### Tip 1: Start with One Provider
Don't add multiple providers at once. Start with one (Groq is easiest).

### Tip 2: Use Same Model for All
For simplicity, use the same model for all purposes initially.

### Tip 3: Test Before Using
Always test connection before registering models.

### Tip 4: Check Rate Limits
Free providers have rate limits. Upgrade if needed.

### Tip 5: Local Models for Privacy
Use Ollama if you want complete privacy (no API calls).

---

## 🆘 Still Having Issues?

### Check Logs
```cmd
docker compose logs -f open_notebook
```

### Restart Application
```cmd
docker compose restart
```

### Check API Key
- Make sure you copied the entire key
- No extra spaces
- Key is active (not revoked)

### Try Different Provider
If one doesn't work, try another:
1. Groq (easiest)
2. OpenAI (most reliable)
3. Anthropic (good alternative)

---

## 📚 Next Steps

After configuring models:

1. ✅ Create your first notebook
2. ✅ Upload a PDF or paste text
3. ✅ Chat with AI
4. ✅ Try search feature
5. ✅ Generate a podcast!

---

## 🎉 You're Almost There!

Just follow the steps above and you'll be up and running in 5 minutes!

**Quick Summary**:
1. Get API key from Groq/OpenAI/Anthropic
2. Add to Settings → API Keys
3. Test Connection
4. Discover Models
5. Register Models
6. Set Defaults
7. Done! 🚀

Need help? Check **SETUP_AND_RUN_GUIDE.md** or ask on Discord!
