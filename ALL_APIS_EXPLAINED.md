# Complete API Guide - All Endpoints Explained

This guide explains ALL 20 API routers in your project, with special focus on how data flows to LLM models.

---

## Table of Contents

1. [Authentication APIs](#1-authentication-apis)
2. [Configuration APIs](#2-configuration-apis)
3. [Notebooks APIs](#3-notebooks-apis)
4. [Search & Ask APIs](#4-search--ask-apis-llm)
5. [Chat APIs](#5-chat-apis-llm)
6. [Source Chat APIs](#6-source-chat-apis-llm)
7. [Sources APIs](#7-sources-apis)
8. [Notes APIs](#8-notes-apis)
9. [Insights APIs](#9-insights-apis-llm)
10. [Models APIs](#10-models-apis)
11. [Transformations APIs](#11-transformations-apis-llm)
12. [Podcasts APIs](#12-podcasts-apis-llm)
13. [Episode Profiles APIs](#13-episode-profiles-apis)
14. [Speaker Profiles APIs](#14-speaker-profiles-apis)
15. [Embedding APIs](#15-embedding-apis)
16. [Settings APIs](#16-settings-apis)
17. [Context APIs](#17-context-apis)
18. [Commands APIs](#18-commands-apis)
19. [Credentials APIs](#19-credentials-apis)

---

## 🤖 LLM Integration Overview

### How LLMs are Used in This Project

```
User Input
    ↓
API Endpoint (FastAPI)
    ↓
LangGraph Workflow (Orchestration)
    ↓
AI Provider (OpenAI/Anthropic/Ollama)
    ↓
Stream Response Back
    ↓
User Sees Result
```

### Key Components:
- **LangGraph**: Orchestrates AI workflows with state management
- **LangChain**: Provides LLM abstractions and tools
- **AI Providers**: OpenAI, Anthropic Claude, Ollama (local)
- **Streaming**: Real-time token-by-token responses

---

## 1. Authentication APIs

**Router**: `api/routers/auth.py`  
**Prefix**: `/api/auth`

### Endpoints:

#### GET `/api/auth/status`
**Purpose**: Check if authentication is required and if user is authenticated

```python
@router.get("/auth/status")
async def get_auth_status():
    """
    Returns:
    {
        "auth_required": true/false,
        "authenticated": true/false
    }
    """
```

**Flow**:
```
Frontend → GET /api/auth/status → Check env var → Return status
```

**No LLM involved** - Simple authentication check

---

## 2. Configuration APIs

**Router**: `api/routers/config.py`  
**Prefix**: `/api/config`

### Endpoints:

#### GET `/api/config`
**Purpose**: Get frontend configuration (API URL, features enabled, etc.)

```python
@router.get("/config")
async def get_config():
    """
    Returns configuration for frontend
    """
```

**No LLM involved** - Returns static configuration

---

## 3. Notebooks APIs

**Router**: `api/routers/notebooks.py`  
**Prefix**: `/api/notebooks`

### Endpoints:

#### GET `/api/notebooks`
List all notebooks

#### POST `/api/notebooks`
Create new notebook

#### GET `/api/notebooks/{id}`
Get single notebook

#### PUT `/api/notebooks/{id}`
Update notebook

#### DELETE `/api/notebooks/{id}`
Delete notebook

**No LLM involved** - Pure CRUD operations

---

## 4. Search & Ask APIs 🤖 (LLM)

**Router**: `api/routers/search.py`  
**Prefix**: `/api/search`

### This is where LLM magic happens!


### Endpoint 1: POST `/api/search`
**Purpose**: Search knowledge base (text or vector search)

```python
@router.post("/search")
async def search_knowledge_base(search_request: SearchRequest):
    # Request body:
    {
        "query": "machine learning",
        "type": "vector",  # or "text"
        "limit": 10,
        "search_sources": true,
        "search_notes": true,
        "minimum_score": 0.7
    }
```

**Flow**:
```
1. User types search query
   ↓
2. Frontend sends POST /api/search
   ↓
3. Backend checks search type:
   - Vector search: Uses embeddings (LLM)
   - Text search: Uses keyword matching
   ↓
4. Query database with embeddings
   ↓
5. Return ranked results
```

**LLM Usage**: 
- Converts query to embedding vector
- Finds similar content using cosine similarity

---

### Endpoint 2: POST `/api/search/ask` 🤖 (STREAMING)
**Purpose**: Ask AI a question about your knowledge base

**This is the MOST COMPLEX LLM endpoint!**

```python
@router.post("/search/ask")
async def ask_knowledge_base(ask_request: AskRequest):
    # Request body:
    {
        "question": "What are the main benefits of AI?",
        "strategy_model": "gpt-4",
        "answer_model": "gpt-4",
        "final_answer_model": "gpt-4"
    }
```

**Complete Flow**:
```
1. USER ASKS QUESTION
   "What are the main benefits of AI?"
   ↓
2. FRONTEND sends POST /api/search/ask
   ↓
3. BACKEND validates models exist
   ↓
4. LANGGRAPH WORKFLOW STARTS
   ↓
5. STEP 1: Strategy Agent (LLM #1)
   - Analyzes question
   - Decides what to search for
   - Creates search strategy
   
   LLM Prompt:
   """
   Question: What are the main benefits of AI?
   
   Create a search strategy. What should we search for?
   """
   
   LLM Response:
   {
       "reasoning": "Need to find sources about AI benefits",
       "searches": [
           {"term": "AI benefits", "instructions": "Find advantages"},
           {"term": "artificial intelligence advantages", "instructions": "..."}
       ]
   }
   ↓
6. STEP 2: Execute Searches
   - For each search term
   - Do vector search in database
   - Collect relevant sources
   ↓
7. STEP 3: Answer Agent (LLM #2)
   - Reads each source
   - Generates answer from each source
   
   LLM Prompt:
   """
   Source: [content about AI]
   Question: What are the main benefits of AI?
   
   Answer based on this source only.
   """
   
   LLM Response:
   "According to this source, AI benefits include..."
   ↓
8. STEP 4: Final Answer Agent (LLM #3)
   - Combines all answers
   - Creates comprehensive final answer
   
   LLM Prompt:
   """
   Question: What are the main benefits of AI?
   
   Answers from sources:
   1. [answer 1]
   2. [answer 2]
   3. [answer 3]
   
   Synthesize a final comprehensive answer.
   """
   
   LLM Response:
   "The main benefits of AI are: 1) Automation..."
   ↓
9. STREAM BACK TO FRONTEND
   - Strategy event
   - Answer events (one per source)
   - Final answer event
   ↓
10. USER SEES ANSWER APPEAR IN REAL-TIME
```

**LLM Models Used**: 3 different LLM calls!
1. Strategy model - decides what to search
2. Answer model - answers from each source
3. Final answer model - synthesizes final answer

**Code Location**: `open_notebook/graphs/ask.py`

---

### Endpoint 3: POST `/api/search/ask/simple`
**Purpose**: Same as `/ask` but returns complete response (no streaming)

---

## 5. Chat APIs 🤖 (LLM)

**Router**: `api/routers/chat.py`  
**Prefix**: `/api/chat`

### This handles conversational AI chat!


### Endpoint 1: GET `/api/chat/sessions?notebook_id=xxx`
**Purpose**: Get all chat sessions for a notebook

```python
@router.get("/chat/sessions")
async def get_sessions(notebook_id: str):
    # Returns list of chat sessions
    [
        {
            "id": "chat_session:abc123",
            "title": "Discussion about AI",
            "notebook_id": "notebook:xyz",
            "message_count": 15,
            "model_override": "gpt-4"
        }
    ]
```

**No LLM** - Just fetches session metadata

---

### Endpoint 2: POST `/api/chat/sessions`
**Purpose**: Create new chat session

```python
@router.post("/chat/sessions")
async def create_session(request: CreateSessionRequest):
    # Request:
    {
        "notebook_id": "notebook:xyz",
        "title": "My Chat",
        "model_override": "gpt-4"  # Optional
    }
```

**No LLM** - Just creates session record

---

### Endpoint 3: GET `/api/chat/sessions/{session_id}`
**Purpose**: Get session with all messages

```python
@router.get("/chat/sessions/{session_id}")
async def get_session(session_id: str):
    # Returns:
    {
        "id": "chat_session:abc123",
        "title": "My Chat",
        "messages": [
            {"type": "human", "content": "Hello"},
            {"type": "ai", "content": "Hi! How can I help?"}
        ]
    }
```

**No LLM** - Retrieves from LangGraph checkpoint

---

### Endpoint 4: POST `/api/chat/execute` 🤖 (LLM)
**Purpose**: Send message and get AI response

**This is where chat AI happens!**

```python
@router.post("/chat/execute")
async def execute_chat(request: ExecuteChatRequest):
    # Request:
    {
        "session_id": "chat_session:abc123",
        "message": "What is machine learning?",
        "context": {
            "sources": [...],  # Relevant sources
            "notes": [...]     # Relevant notes
        },
        "model_override": "gpt-4"  # Optional
    }
```

**Complete Flow**:
```
1. USER TYPES MESSAGE
   "What is machine learning?"
   ↓
2. FRONTEND builds context
   - Gets sources from notebook
   - Gets notes from notebook
   - Sends to API
   ↓
3. BACKEND receives request
   ↓
4. GET CURRENT CONVERSATION
   - Load previous messages from LangGraph
   - Messages: [
       {"type": "human", "content": "Hello"},
       {"type": "ai", "content": "Hi!"},
       {"type": "human", "content": "What is machine learning?"}
     ]
   ↓
5. BUILD SYSTEM PROMPT
   Template: prompts/chat/system.jinja
   
   """
   You are a helpful AI assistant.
   
   Context from notebook:
   
   Sources:
   - Source 1: [content]
   - Source 2: [content]
   
   Notes:
   - Note 1: [content]
   - Note 2: [content]
   
   Answer the user's questions based on this context.
   """
   ↓
6. CALL LLM
   Messages sent to LLM:
   [
       SystemMessage("You are a helpful AI assistant..."),
       HumanMessage("Hello"),
       AIMessage("Hi!"),
       HumanMessage("What is machine learning?")
   ]
   ↓
7. LLM GENERATES RESPONSE
   "Machine learning is a subset of AI that..."
   ↓
8. SAVE TO LANGGRAPH CHECKPOINT
   - Stores conversation state
   - Can resume later
   ↓
9. RETURN RESPONSE
   {
       "session_id": "chat_session:abc123",
       "messages": [
           ...,
           {"type": "ai", "content": "Machine learning is..."}
       ]
   }
   ↓
10. USER SEES RESPONSE
```

**LLM Usage**:
- Single LLM call with full conversation history
- Context-aware (uses sources and notes)
- Stateful (remembers conversation)

**Code Location**: `open_notebook/graphs/chat.py`

**Key Features**:
- ✅ Conversation memory
- ✅ Context from sources/notes
- ✅ Model override per session
- ✅ Thinking tags cleaned (<think>...</think>)

---

### Endpoint 5: POST `/api/chat/context`
**Purpose**: Build context for chat (get sources and notes)

```python
@router.post("/chat/context")
async def build_context(request: BuildContextRequest):
    # Request:
    {
        "notebook_id": "notebook:xyz",
        "context_config": {
            "sources": {
                "source:abc": "full content",
                "source:def": "insights only"
            },
            "notes": {
                "note:123": "full content"
            }
        }
    }
    
    # Response:
    {
        "context": {
            "sources": [...],
            "notes": [...]
        },
        "token_count": 5000,
        "char_count": 20000
    }
```

**No LLM** - Just gathers context data

---

## 6. Source Chat APIs 🤖 (LLM)

**Router**: `api/routers/source_chat.py`  
**Prefix**: `/api/sources/{source_id}/chat`

### Chat with a SPECIFIC source (like chatting with a PDF)


### Endpoint 1: POST `/api/sources/{source_id}/chat/sessions`
**Purpose**: Create chat session for a specific source

```python
@router.post("/sources/{source_id}/chat/sessions")
async def create_source_chat_session(request, source_id):
    # Request:
    {
        "source_id": "source:abc123",
        "title": "Chat about this PDF",
        "model_override": "gpt-4"
    }
```

---

### Endpoint 2: POST `/api/sources/{source_id}/chat/sessions/{session_id}/messages` 🤖 (STREAMING)
**Purpose**: Send message to source chat

**This is like ChatPDF - chat with a specific document!**

```python
@router.post("/sources/{source_id}/chat/sessions/{session_id}/messages")
async def send_message_to_source_chat(request, source_id, session_id):
    # Request:
    {
        "message": "What is the main conclusion?",
        "model_override": "gpt-4"
    }
```

**Complete Flow**:
```
1. USER UPLOADS PDF
   ↓
2. PDF BECOMES A SOURCE
   - Content extracted
   - Embeddings created
   - Insights generated
   ↓
3. USER CLICKS "Chat with this source"
   ↓
4. CREATE CHAT SESSION
   POST /api/sources/{source_id}/chat/sessions
   ↓
5. USER ASKS QUESTION
   "What is the main conclusion?"
   ↓
6. FRONTEND sends message
   POST /api/sources/{source_id}/chat/sessions/{session_id}/messages
   ↓
7. BACKEND LOADS SOURCE CONTENT
   - Get source full text
   - Get source insights
   - Get related notes
   ↓
8. BUILD CONTEXT
   """
   Source: [PDF title]
   Content: [full PDF text or relevant chunks]
   
   Insights:
   - Summary: [AI-generated summary]
   - Key points: [AI-generated key points]
   """
   ↓
9. GET CONVERSATION HISTORY
   Previous messages in this session
   ↓
10. CALL LLM
    System Prompt:
    """
    You are chatting about a specific source.
    
    Source: [title]
    Content: [text]
    
    Answer questions about this source only.
    """
    
    Messages:
    [
        SystemMessage("You are chatting about..."),
        HumanMessage("What is the main conclusion?")
    ]
    ↓
11. LLM GENERATES RESPONSE
    "The main conclusion of this document is..."
    ↓
12. STREAM BACK
    Server-Sent Events:
    data: {"type": "user_message", "content": "What is..."}
    data: {"type": "ai_message", "content": "The main..."}
    data: {"type": "context_indicators", "data": {...}}
    data: {"type": "complete"}
    ↓
13. USER SEES RESPONSE STREAMING
```

**LLM Usage**:
- Focused on single source
- Uses source content as context
- Streaming response
- Context indicators show what was used

**Code Location**: `open_notebook/graphs/source_chat.py`

---

## 7. Sources APIs

**Router**: `api/routers/sources.py`  
**Prefix**: `/api/sources`

### Endpoints:

#### GET `/api/sources`
List all sources

#### POST `/api/sources`
Create/upload new source (file, URL, text)

#### GET `/api/sources/{id}`
Get single source

#### PUT `/api/sources/{id}`
Update source

#### DELETE `/api/sources/{id}`
Delete source

**LLM Usage**: 
- When source is created, LLM generates insights
- Embeddings are created for vector search

---

## 8. Notes APIs

**Router**: `api/routers/notes.py`  
**Prefix**: `/api/notes`

### Endpoints:

#### GET `/api/notebooks/{notebook_id}/notes`
Get all notes in notebook

#### POST `/api/notebooks/{notebook_id}/notes`
Create new note

#### GET `/api/notes/{id}`
Get single note

#### PUT `/api/notes/{id}`
Update note

#### DELETE `/api/notes/{id}`
Delete note

**LLM Usage**:
- Notes can be created from AI-generated insights
- Embeddings created for search

---

## 9. Insights APIs 🤖 (LLM)

**Router**: `api/routers/insights.py`  
**Prefix**: `/api/insights`

### What are Insights?
When you upload a source (PDF, URL, text), AI automatically generates:
- Summary
- Key points
- Questions
- Tags

### Endpoints:

#### GET `/api/insights/{id}`
Get specific insight

#### DELETE `/api/insights/{id}`
Delete insight

#### POST `/api/insights/{id}/save-as-note`
Convert insight to note

**LLM Usage**:
- Insights are generated by LLM when source is created
- Uses prompts to extract key information

---

## 10. Models APIs

**Router**: `api/routers/models.py`  
**Prefix**: `/api/models`

### Endpoints:

#### GET `/api/models`
List all configured AI models

```python
@router.get("/models")
async def get_models():
    # Returns:
    [
        {
            "id": "gpt-4",
            "name": "GPT-4",
            "provider": "openai",
            "type": "chat",
            "enabled": true
        },
        {
            "id": "claude-3-opus",
            "name": "Claude 3 Opus",
            "provider": "anthropic",
            "type": "chat",
            "enabled": true
        }
    ]
```

#### POST `/api/models`
Add new model configuration

#### PUT `/api/models/{id}`
Update model

#### DELETE `/api/models/{id}`
Delete model

#### POST `/api/models/{id}/test`
Test if model works

**No LLM calls** - Just manages model configurations

---

## 11. Transformations APIs 🤖 (LLM)

**Router**: `api/routers/transformations.py`  
**Prefix**: `/api/transformations`

### What are Transformations?
AI-powered content transformations:
- Summarize
- Translate
- Rewrite
- Extract key points
- Generate questions


### Endpoints:

#### GET `/api/transformations`
List all transformation templates

#### POST `/api/transformations/execute` 🤖
Execute a transformation

```python
@router.post("/transformations/execute")
async def execute_transformation(request):
    # Request:
    {
        "transformation_id": "summarize",
        "content": "Long text to summarize...",
        "model_id": "gpt-4",
        "parameters": {
            "length": "short"
        }
    }
```

**Flow**:
```
1. USER SELECTS TEXT
   "Long article about AI..."
   ↓
2. USER CLICKS "Summarize"
   ↓
3. FRONTEND sends transformation request
   ↓
4. BACKEND loads transformation template
   Template: "Summarize the following text..."
   ↓
5. BUILD PROMPT
   """
   Summarize the following text in a short format:
   
   [Long article about AI...]
   """
   ↓
6. CALL LLM
   ↓
7. LLM GENERATES SUMMARY
   "This article discusses AI's impact on..."
   ↓
8. RETURN RESULT
   {
       "result": "This article discusses..."
   }
```

**LLM Usage**: Direct LLM call with transformation prompt

---

## 12. Podcasts APIs 🤖 (LLM)

**Router**: `api/routers/podcasts.py`  
**Prefix**: `/api/podcasts`

### What are Podcasts?
AI-generated audio conversations about your content!

### Endpoints:

#### POST `/api/podcasts/generate` 🤖 (STREAMING)
Generate podcast from sources

```python
@router.post("/podcasts/generate")
async def generate_podcast(request):
    # Request:
    {
        "notebook_id": "notebook:xyz",
        "source_ids": ["source:abc", "source:def"],
        "episode_profile_id": "profile:123",
        "speaker_profiles": ["speaker:1", "speaker:2"]
    }
```

**Complete Flow**:
```
1. USER SELECTS SOURCES
   - Research paper 1
   - Research paper 2
   - Blog post
   ↓
2. USER CLICKS "Generate Podcast"
   ↓
3. FRONTEND sends request
   ↓
4. BACKEND STEP 1: Generate Outline (LLM #1)
   
   LLM Prompt:
   """
   Create a podcast outline based on these sources:
   
   Source 1: [content]
   Source 2: [content]
   Source 3: [content]
   
   Create an engaging conversation outline.
   """
   
   LLM Response:
   {
       "title": "AI Revolution Discussion",
       "segments": [
           {"topic": "Introduction", "duration": "2 min"},
           {"topic": "Main benefits", "duration": "5 min"},
           {"topic": "Challenges", "duration": "5 min"}
       ]
   }
   ↓
5. BACKEND STEP 2: Generate Transcript (LLM #2)
   
   LLM Prompt:
   """
   Create a natural conversation between two speakers:
   
   Speaker 1: [profile - enthusiastic host]
   Speaker 2: [profile - expert analyst]
   
   Outline: [from step 1]
   Sources: [content]
   
   Generate engaging dialogue.
   """
   
   LLM Response:
   """
   Speaker 1: Welcome to today's episode! We're diving into AI.
   Speaker 2: Thanks for having me! This is fascinating stuff.
   Speaker 1: So what are the main benefits?
   Speaker 2: Well, according to our research...
   """
   ↓
6. BACKEND STEP 3: Generate Audio (TTS)
   - Split transcript by speaker
   - For each line:
     - Call Text-to-Speech API
     - Generate audio chunk
   - Combine all audio chunks
   ↓
7. SAVE PODCAST
   - Store transcript
   - Store audio file
   - Link to sources
   ↓
8. RETURN PODCAST
   {
       "id": "podcast:xyz",
       "title": "AI Revolution Discussion",
       "audio_url": "/uploads/podcast.mp3",
       "transcript": "..."
   }
```

**LLM Usage**: 2 LLM calls + TTS
1. Outline generation
2. Transcript generation
3. Text-to-Speech for audio

**Code Location**: `open_notebook/graphs/podcast.py`

---

## 13. Episode Profiles APIs

**Router**: `api/routers/episode_profiles.py`  
**Prefix**: `/api/episode-profiles`

### What are Episode Profiles?
Templates for podcast generation:
- Tone (casual, formal, educational)
- Length (short, medium, long)
- Style (interview, discussion, monologue)

### Endpoints:

#### GET `/api/episode-profiles`
List all profiles

#### POST `/api/episode-profiles`
Create profile

#### PUT `/api/episode-profiles/{id}`
Update profile

#### DELETE `/api/episode-profiles/{id}`
Delete profile

**No LLM** - Just manages templates

---

## 14. Speaker Profiles APIs

**Router**: `api/routers/speaker_profiles.py`  
**Prefix**: `/api/speaker-profiles`

### What are Speaker Profiles?
Voice characteristics for podcast speakers:
- Name
- Voice type
- Personality
- Speaking style

### Endpoints:

#### GET `/api/speaker-profiles`
List all speakers

#### POST `/api/speaker-profiles`
Create speaker

#### PUT `/api/speaker-profiles/{id}`
Update speaker

#### DELETE `/api/speaker-profiles/{id}`
Delete speaker

**No LLM** - Just manages speaker configs

---

## 15. Embedding APIs

**Router**: `api/routers/embedding.py`  
**Prefix**: `/api/embeddings`

### What are Embeddings?
Vector representations of text for semantic search

### Endpoints:

#### POST `/api/embeddings/rebuild`
Rebuild all embeddings

```python
@router.post("/embeddings/rebuild")
async def rebuild_embeddings():
    # Regenerates embeddings for all sources and notes
```

**Flow**:
```
1. USER CLICKS "Rebuild Embeddings"
   ↓
2. BACKEND gets all sources and notes
   ↓
3. FOR EACH source/note:
   - Get text content
   - Call embedding model
   - Store vector in database
   ↓
4. EMBEDDING MODEL (LLM)
   Text: "Machine learning is..."
   ↓
   Vector: [0.123, -0.456, 0.789, ...]  (1536 dimensions)
   ↓
5. SAVE TO DATABASE
```

**LLM Usage**: Embedding model (text-embedding-ada-002, etc.)

---

## 16. Settings APIs

**Router**: `api/routers/settings.py`  
**Prefix**: `/api/settings`

### Endpoints:

#### GET `/api/settings`
Get all settings

#### PUT `/api/settings`
Update settings

**No LLM** - Just manages app settings

---

## 17. Context APIs

**Router**: `api/routers/context.py`  
**Prefix**: `/api/context`

### Endpoints:

#### POST `/api/context/build`
Build context for AI operations

**No LLM** - Gathers context data

---

## 18. Commands APIs

**Router**: `api/routers/commands.py`  
**Prefix**: `/api/commands`

### Endpoints:

#### GET `/api/commands`
List available commands

#### POST `/api/commands/execute`
Execute a command

**No LLM** - System commands

---

## 19. Credentials APIs

**Router**: `api/routers/credentials.py`  
**Prefix**: `/api/credentials`

### Endpoints:

#### GET `/api/credentials`
List API credentials

#### POST `/api/credentials`
Add credential (OpenAI key, etc.)

#### PUT `/api/credentials/{id}`
Update credential

#### DELETE `/api/credentials/{id}`
Delete credential

**No LLM** - Manages API keys

---

## 🎯 Summary: Which APIs Use LLM?

### Heavy LLM Usage:
1. ✅ **Search/Ask** - 3 LLM calls (strategy, answer, final)
2. ✅ **Chat** - Conversational AI
3. ✅ **Source Chat** - Chat with documents
4. ✅ **Podcasts** - 2 LLM calls + TTS
5. ✅ **Transformations** - Content transformation
6. ✅ **Insights** - Auto-generated summaries

### Light LLM Usage:
7. ✅ **Embeddings** - Vector generation
8. ✅ **Sources** - Insight generation on upload

### No LLM:
- Authentication
- Configuration
- Notebooks (CRUD)
- Notes (CRUD)
- Models (management)
- Settings
- Credentials

---

## 🔥 Most Important LLM Flows

### 1. Ask Feature (Most Complex)
```
Question → Strategy LLM → Search → Answer LLM (per source) → Final LLM → Response
```

### 2. Chat Feature (Most Used)
```
Message + Context → LLM with history → Response
```

### 3. Source Chat (Most Focused)
```
Message + Source content → LLM → Response
```

### 4. Podcast Generation (Most Creative)
```
Sources → Outline LLM → Transcript LLM → TTS → Audio
```

---

## 📊 Data Flow to LLM

### General Pattern:
```
1. User Input
   ↓
2. API Endpoint
   ↓
3. Gather Context
   - Sources
   - Notes
   - History
   ↓
4. Build Prompt
   - System message
   - Context
   - User message
   ↓
5. Call LLM
   - OpenAI API
   - Anthropic API
   - Ollama (local)
   ↓
6. Process Response
   - Clean thinking tags
   - Format output
   ↓
7. Save State
   - LangGraph checkpoint
   - Database
   ↓
8. Return to User
   - Streaming or complete
```

---

## 🛠️ Key Technologies

### LangGraph
- State management for AI workflows
- Checkpointing (conversation memory)
- Multi-step workflows

### LangChain
- LLM abstractions
- Message types (Human, AI, System)
- Prompt templates

### AI Providers
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Ollama (local models)

### Streaming
- Server-Sent Events (SSE)
- Real-time token delivery
- Progress updates

---

## 🎓 Learning Path

1. Start with simple: **Notebooks API** (no LLM)
2. Then: **Search API** (basic LLM)
3. Then: **Chat API** (conversational LLM)
4. Advanced: **Ask API** (multi-step LLM)
5. Expert: **Podcast API** (complex workflow)

Happy learning! 🚀
