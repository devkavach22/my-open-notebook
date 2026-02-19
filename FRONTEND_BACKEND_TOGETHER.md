# Frontend ↔️ Backend - Understanding Together

This guide shows you how frontend and backend work together for the same features.

---

## Example 1: Viewing Notebooks List

### 🎨 FRONTEND Side

#### File: `frontend/src/app/(dashboard)/notebooks/page.tsx`
```typescript
'use client'

export default function NotebooksPage() {
  // 1️⃣ Call custom hook to get notebooks
  const { data: notebooks, isLoading } = useNotebooks()
  
  // 2️⃣ Show loading spinner while fetching
  if (isLoading) {
    return <LoadingSpinner />
  }
  
  // 3️⃣ Render the notebooks
  return (
    <AppShell>
      <div className="container">
        <h1>My Notebooks</h1>
        
        {/* 4️⃣ Loop through notebooks and show cards */}
        {notebooks?.map(notebook => (
          <NotebookCard 
            key={notebook.id} 
            notebook={notebook} 
          />
        ))}
      </div>
    </AppShell>
  )
}
```

**What happens here:**
- Component loads → calls `useNotebooks()`
- Shows loading spinner while waiting
- When data arrives → displays notebook cards

---

#### File: `frontend/src/lib/hooks/use-notebooks.ts`
```typescript
import { useQuery } from '@tanstack/react-query'
import { notebooksApi } from '@/lib/api/notebooks'

export function useNotebooks() {
  return useQuery({
    // 1️⃣ Unique key for caching
    queryKey: ['notebooks'],
    
    // 2️⃣ Function that fetches data
    queryFn: async () => {
      const response = await notebooksApi.getAll()
      return response
    },
    
    // 3️⃣ Refetch every 30 seconds
    refetchInterval: 30000,
  })
}
```

**What happens here:**
- React Query checks cache first
- If no cache → calls `notebooksApi.getAll()`
- Automatically handles loading, error states
- Caches result for future use

---

#### File: `frontend/src/lib/api/notebooks.ts`
```typescript
import { apiClient } from './client'

export const notebooksApi = {
  // 1️⃣ GET all notebooks
  getAll: async () => {
    const response = await apiClient.get('/api/notebooks')
    return response.data
  },
  
  // 2️⃣ GET single notebook
  getById: async (id: string) => {
    const response = await apiClient.get(`/api/notebooks/${id}`)
    return response.data
  },
  
  // 3️⃣ CREATE notebook
  create: async (data: NotebookCreate) => {
    const response = await apiClient.post('/api/notebooks', data)
    return response.data
  },
}
```

**What happens here:**
- Makes HTTP request to backend
- URL: `http://localhost:8000/api/notebooks`
- Method: GET
- Returns JSON data

---

### 🔧 BACKEND Side

#### File: `api/routers/notebooks.py`
```python
from fastapi import APIRouter, HTTPException
from api.notebook_service import NotebookService

router = APIRouter()
service = NotebookService()

# 1️⃣ GET /api/notebooks - List all notebooks
@router.get("/notebooks")
async def get_notebooks():
    """
    Get all notebooks for the current user
    """
    # Call service to get notebooks
    notebooks = await service.get_all_notebooks()
    
    # Return as JSON
    return notebooks


# 2️⃣ GET /api/notebooks/{id} - Get single notebook
@router.get("/notebooks/{id}")
async def get_notebook(id: str):
    """
    Get a specific notebook by ID
    """
    notebook = await service.get_notebook(id)
    
    # If not found, return 404 error
    if not notebook:
        raise HTTPException(status_code=404, detail="Notebook not found")
    
    return notebook


# 3️⃣ POST /api/notebooks - Create new notebook
@router.post("/notebooks")
async def create_notebook(data: NotebookCreate):
    """
    Create a new notebook
    """
    # Data is automatically validated by Pydantic
    notebook = await service.create_notebook(data)
    return notebook
```

**What happens here:**
- FastAPI receives HTTP request
- Routes to correct function based on URL + method
- Calls service layer for business logic
- Returns JSON response

---

#### File: `api/notebook_service.py`
```python
from open_notebook.database.repository import Repository

class NotebookService:
    def __init__(self):
        self.repo = Repository()
    
    async def get_all_notebooks(self):
        """
        Business logic for getting notebooks
        """
        # 1️⃣ Get notebooks from database
        notebooks = await self.repo.get_all_notebooks()
        
        # 2️⃣ Add extra data (e.g., count sources)
        for notebook in notebooks:
            notebook['source_count'] = await self.repo.count_sources(notebook['id'])
        
        # 3️⃣ Return processed data
        return notebooks
    
    async def create_notebook(self, data):
        """
        Business logic for creating notebook
        """
        # 1️⃣ Validate business rules
        if len(data.title) < 3:
            raise ValueError("Title too short")
        
        # 2️⃣ Create in database
        notebook = await self.repo.create_notebook(data)
        
        # 3️⃣ Do additional setup (create default note, etc.)
        await self.repo.create_default_note(notebook['id'])
        
        return notebook
```

**What happens here:**
- Contains business logic
- Validates rules
- Calls repository for database operations
- Processes and enriches data

---

#### File: `open_notebook/database/repository.py`
```python
from surrealdb import Surreal

class Repository:
    def __init__(self):
        self.db = Surreal()
    
    async def get_all_notebooks(self):
        """
        Query database for all notebooks
        """
        # 1️⃣ Write SQL query
        query = """
            SELECT 
                id,
                title,
                description,
                created_at,
                updated_at
            FROM notebook
            ORDER BY updated_at DESC
        """
        
        # 2️⃣ Execute query
        result = await self.db.query(query)
        
        # 3️⃣ Return results
        return result[0]['result']
    
    async def create_notebook(self, data):
        """
        Insert new notebook into database
        """
        # 1️⃣ Write INSERT query
        query = """
            CREATE notebook CONTENT {
                title: $title,
                description: $description,
                created_at: time::now(),
                updated_at: time::now()
            }
        """
        
        # 2️⃣ Execute with parameters
        result = await self.db.query(query, {
            'title': data.title,
            'description': data.description
        })
        
        # 3️⃣ Return created notebook
        return result[0]['result'][0]
```

**What happens here:**
- Direct database operations
- Writes SQL queries
- Executes queries
- Returns raw data

---

## 📊 Complete Flow Diagram

```
USER CLICKS "Notebooks" in sidebar
         ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 1. NotebooksPage component loads      │
│    File: notebooks/page.tsx            │
│         ↓                              │
│ 2. Calls useNotebooks() hook           │
│    File: hooks/use-notebooks.ts        │
│         ↓                              │
│ 3. React Query checks cache            │
│    - Cache hit? Return cached data     │
│    - Cache miss? Make API call         │
│         ↓                              │
│ 4. API client makes HTTP request       │
│    File: api/notebooks.ts              │
│    GET http://localhost:8000/api/notebooks
└────────────────┬───────────────────────┘
                 │ HTTP Request
                 │ (over network)
                 ↓
┌────────────────────────────────────────┐
│ BACKEND                                │
├────────────────────────────────────────┤
│ 5. FastAPI receives request            │
│    File: api/main.py                   │
│         ↓                              │
│ 6. Middleware checks authentication    │
│    - Valid? Continue                   │
│    - Invalid? Return 401 error         │
│         ↓                              │
│ 7. Router handles request              │
│    File: api/routers/notebooks.py      │
│    @router.get("/notebooks")           │
│         ↓                              │
│ 8. Service processes business logic    │
│    File: api/notebook_service.py       │
│         ↓                              │
│ 9. Repository queries database         │
│    File: open_notebook/database/repository.py
│    SELECT * FROM notebook              │
│         ↓                              │
│ 10. SurrealDB returns data             │
└────────────────┬───────────────────────┘
                 │ HTTP Response
                 │ (JSON data)
                 ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 11. API client receives response       │
│         ↓                              │
│ 12. React Query caches data            │
│         ↓                              │
│ 13. Hook returns data to component     │
│         ↓                              │
│ 14. Component re-renders with data     │
│         ↓                              │
│ 15. User sees notebooks on screen! ✅  │
└────────────────────────────────────────┘
```

---

## Example 2: Creating a New Notebook

### 🎨 FRONTEND Side

#### File: `frontend/src/components/notebooks/CreateNotebookDialog.tsx`
```typescript
export function CreateNotebookDialog() {
  // 1️⃣ Get mutation hook
  const { mutate, isPending } = useCreateNotebook()
  
  // 2️⃣ Form state
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  
  // 3️⃣ Handle form submit
  const handleSubmit = () => {
    mutate({
      title,
      description
    }, {
      // 4️⃣ On success, close dialog and show toast
      onSuccess: () => {
        toast.success('Notebook created!')
        closeDialog()
      },
      // 5️⃣ On error, show error message
      onError: (error) => {
        toast.error(error.message)
      }
    })
  }
  
  return (
    <Dialog>
      <DialogContent>
        <h2>Create Notebook</h2>
        
        {/* 6️⃣ Form inputs */}
        <Input 
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Notebook title"
        />
        
        <Textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Description"
        />
        
        {/* 7️⃣ Submit button */}
        <Button 
          onClick={handleSubmit}
          disabled={isPending}
        >
          {isPending ? 'Creating...' : 'Create'}
        </Button>
      </DialogContent>
    </Dialog>
  )
}
```

---

#### File: `frontend/src/lib/hooks/use-notebooks.ts`
```typescript
export function useCreateNotebook() {
  const queryClient = useQueryClient()
  
  return useMutation({
    // 1️⃣ Function to call API
    mutationFn: async (data: NotebookCreate) => {
      return await notebooksApi.create(data)
    },
    
    // 2️⃣ On success, refresh notebooks list
    onSuccess: () => {
      // Invalidate cache to trigger refetch
      queryClient.invalidateQueries({ queryKey: ['notebooks'] })
    },
  })
}
```

---

#### File: `frontend/src/lib/api/notebooks.ts`
```typescript
export const notebooksApi = {
  create: async (data: NotebookCreate) => {
    // 1️⃣ POST request to backend
    const response = await apiClient.post('/api/notebooks', {
      title: data.title,
      description: data.description
    })
    
    // 2️⃣ Return created notebook
    return response.data
  },
}
```

---

### 🔧 BACKEND Side

#### File: `api/routers/notebooks.py`
```python
from pydantic import BaseModel

# 1️⃣ Define data model for validation
class NotebookCreate(BaseModel):
    title: str
    description: str | None = None

@router.post("/notebooks")
async def create_notebook(data: NotebookCreate):
    """
    Create a new notebook
    """
    # 2️⃣ Pydantic automatically validates:
    #    - title is required and must be string
    #    - description is optional
    
    # 3️⃣ Call service
    notebook = await service.create_notebook(data)
    
    # 4️⃣ Return created notebook (201 status)
    return notebook
```

---

#### File: `api/notebook_service.py`
```python
async def create_notebook(self, data: NotebookCreate):
    # 1️⃣ Validate business rules
    if len(data.title.strip()) < 3:
        raise ValueError("Title must be at least 3 characters")
    
    # 2️⃣ Create notebook in database
    notebook = await self.repo.create_notebook({
        'title': data.title.strip(),
        'description': data.description or '',
        'user_id': get_current_user_id()
    })
    
    # 3️⃣ Create default note for the notebook
    await self.repo.create_note({
        'notebook_id': notebook['id'],
        'title': 'Getting Started',
        'content': 'Welcome to your new notebook!'
    })
    
    # 4️⃣ Return the created notebook
    return notebook
```

---

#### File: `open_notebook/database/repository.py`
```python
async def create_notebook(self, data: dict):
    # 1️⃣ Generate unique ID
    notebook_id = f"notebook:{uuid.uuid4()}"
    
    # 2️⃣ Insert into database
    query = """
        CREATE $notebook_id CONTENT {
            title: $title,
            description: $description,
            user_id: $user_id,
            created_at: time::now(),
            updated_at: time::now()
        }
    """
    
    result = await self.db.query(query, {
        'notebook_id': notebook_id,
        'title': data['title'],
        'description': data['description'],
        'user_id': data['user_id']
    })
    
    # 3️⃣ Return created notebook
    return result[0]['result'][0]
```

---

## 📊 Create Notebook Flow

```
USER FILLS FORM & CLICKS "Create"
         ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 1. CreateNotebookDialog                │
│    - User enters: title, description   │
│    - Clicks "Create" button            │
│         ↓                              │
│ 2. Calls mutate() from hook            │
│    useCreateNotebook()                 │
│         ↓                              │
│ 3. React Query mutation                │
│    - Shows loading state               │
│    - Disables button                   │
│         ↓                              │
│ 4. API client POST request             │
│    POST /api/notebooks                 │
│    Body: { title, description }        │
└────────────────┬───────────────────────┘
                 │ HTTP POST
                 ↓
┌────────────────────────────────────────┐
│ BACKEND                                │
├────────────────────────────────────────┤
│ 5. FastAPI receives POST               │
│         ↓                              │
│ 6. Pydantic validates data             │
│    - title: required string ✓          │
│    - description: optional string ✓    │
│         ↓                              │
│ 7. Router calls service                │
│    create_notebook(data)               │
│         ↓                              │
│ 8. Service validates business rules    │
│    - Title length >= 3? ✓              │
│    - User authenticated? ✓             │
│         ↓                              │
│ 9. Repository inserts to database      │
│    CREATE notebook CONTENT {...}       │
│         ↓                              │
│ 10. Database returns created record    │
│         ↓                              │
│ 11. Service creates default note       │
│         ↓                              │
│ 12. Return notebook as JSON            │
└────────────────┬───────────────────────┘
                 │ HTTP Response
                 │ Status: 200
                 │ Body: { id, title, ... }
                 ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 13. Mutation onSuccess callback        │
│         ↓                              │
│ 14. Invalidate notebooks cache         │
│         ↓                              │
│ 15. React Query refetches notebooks    │
│         ↓                              │
│ 16. Notebooks list updates             │
│         ↓                              │
│ 17. Show success toast                 │
│         ↓                              │
│ 18. Close dialog                       │
│         ↓                              │
│ 19. User sees new notebook! ✅         │
└────────────────────────────────────────┘
```

---

## Example 3: Real-time Chat with AI

### 🎨 FRONTEND Side

#### File: `frontend/src/components/notebooks/ChatColumn.tsx`
```typescript
export function ChatColumn({ notebookId }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  
  const handleSend = async () => {
    // 1️⃣ Add user message to UI immediately
    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsStreaming(true)
    
    // 2️⃣ Create placeholder for AI response
    const aiMessage = { role: 'assistant', content: '' }
    setMessages(prev => [...prev, aiMessage])
    
    try {
      // 3️⃣ Call streaming API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          notebook_id: notebookId,
          message: input,
          stream: true
        })
      })
      
      // 4️⃣ Read stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        
        // 5️⃣ Decode chunk
        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))
            
            // 6️⃣ Update AI message with new token
            setMessages(prev => {
              const updated = [...prev]
              updated[updated.length - 1].content += data.token
              return updated
            })
          }
        }
      }
    } finally {
      setIsStreaming(false)
    }
  }
  
  return (
    <div>
      {/* 7️⃣ Display messages */}
      {messages.map((msg, i) => (
        <div key={i} className={msg.role}>
          {msg.content}
        </div>
      ))}
      
      {/* 8️⃣ Input box */}
      <Input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
        disabled={isStreaming}
      />
      
      <Button onClick={handleSend} disabled={isStreaming}>
        {isStreaming ? 'Thinking...' : 'Send'}
      </Button>
    </div>
  )
}
```

---

### 🔧 BACKEND Side

#### File: `api/routers/chat.py`
```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from api.chat_service import ChatService

router = APIRouter()
service = ChatService()

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat with AI - supports streaming
    """
    # 1️⃣ If streaming requested
    if request.stream:
        # Return streaming response
        return StreamingResponse(
            service.chat_stream(
                notebook_id=request.notebook_id,
                message=request.message
            ),
            media_type="text/event-stream"
        )
    
    # 2️⃣ Otherwise, return complete response
    else:
        response = await service.chat(
            notebook_id=request.notebook_id,
            message=request.message
        )
        return response
```

---

#### File: `api/chat_service.py`
```python
from open_notebook.graphs.chat import ChatGraph

class ChatService:
    async def chat_stream(self, notebook_id: str, message: str):
        """
        Stream AI response token by token
        """
        # 1️⃣ Get notebook context
        context = await self.get_notebook_context(notebook_id)
        
        # 2️⃣ Initialize LangGraph
        graph = ChatGraph()
        
        # 3️⃣ Stream response
        async for event in graph.stream({
            'message': message,
            'context': context
        }):
            # 4️⃣ Extract token from event
            if 'token' in event:
                token = event['token']
                
                # 5️⃣ Yield as Server-Sent Event
                yield f"data: {json.dumps({'token': token})}\n\n"
        
        # 6️⃣ Save conversation to database
        await self.save_message(notebook_id, message, response)
```

---

#### File: `open_notebook/graphs/chat.py`
```python
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

class ChatGraph:
    def __init__(self):
        # 1️⃣ Initialize AI model
        self.llm = ChatOpenAI(
            model="gpt-4",
            streaming=True
        )
    
    async def stream(self, input_data):
        """
        Stream AI response
        """
        # 2️⃣ Build prompt with context
        prompt = f"""
        Context: {input_data['context']}
        
        User: {input_data['message']}
        
        Assistant:
        """
        
        # 3️⃣ Stream from AI
        async for chunk in self.llm.astream(prompt):
            # 4️⃣ Yield each token
            if chunk.content:
                yield {'token': chunk.content}
```

---

## 📊 Chat Streaming Flow

```
USER TYPES MESSAGE & HITS ENTER
         ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 1. Add user message to UI immediately  │
│    (Optimistic update)                 │
│         ↓                              │
│ 2. Create empty AI message placeholder │
│         ↓                              │
│ 3. Open streaming connection           │
│    POST /api/chat (stream=true)        │
└────────────────┬───────────────────────┘
                 │ HTTP POST (streaming)
                 ↓
┌────────────────────────────────────────┐
│ BACKEND                                │
├────────────────────────────────────────┤
│ 4. Router receives request             │
│         ↓                              │
│ 5. Service gets notebook context       │
│    - Fetch related sources             │
│    - Fetch previous messages           │
│         ↓                              │
│ 6. Initialize LangGraph                │
│         ↓                              │
│ 7. Build prompt with context           │
│         ↓                              │
│ 8. Call OpenAI API (streaming)         │
└────────────────┬───────────────────────┘
                 │
                 ↓
┌────────────────────────────────────────┐
│ OPENAI API                             │
├────────────────────────────────────────┤
│ 9. Generate response token by token    │
│    "Hello" → " there" → "!" → ...      │
└────────────────┬───────────────────────┘
                 │ Stream tokens back
                 ↓
┌────────────────────────────────────────┐
│ BACKEND                                │
├────────────────────────────────────────┤
│ 10. Receive each token                 │
│         ↓                              │
│ 11. Yield as Server-Sent Event         │
│     data: {"token": "Hello"}           │
│     data: {"token": " there"}          │
│     data: {"token": "!"}               │
└────────────────┬───────────────────────┘
                 │ Stream to frontend
                 ↓
┌────────────────────────────────────────┐
│ FRONTEND                               │
├────────────────────────────────────────┤
│ 12. Receive token stream               │
│         ↓                              │
│ 13. Parse each event                   │
│         ↓                              │
│ 14. Append token to AI message         │
│     "Hello" → "Hello there" → ...      │
│         ↓                              │
│ 15. Component re-renders               │
│         ↓                              │
│ 16. User sees text appearing! ✅       │
│     (Like ChatGPT typing effect)       │
└────────────────────────────────────────┘
```

---

## Key Concepts Summary

### Frontend Responsibilities
- ✅ Display UI
- ✅ Handle user interactions
- ✅ Make API calls
- ✅ Cache data (React Query)
- ✅ Manage local state (Zustand)
- ✅ Show loading/error states

### Backend Responsibilities
- ✅ Receive HTTP requests
- ✅ Validate data (Pydantic)
- ✅ Enforce business rules
- ✅ Query database
- ✅ Call external APIs (OpenAI)
- ✅ Return responses

### Communication
- ✅ HTTP/HTTPS protocol
- ✅ JSON data format
- ✅ REST API pattern
- ✅ Server-Sent Events (streaming)

---

## Practice Exercise

Try tracing these features yourself:

1. **Sources List**
   - Frontend: `frontend/src/app/(dashboard)/sources/page.tsx`
   - Backend: `api/routers/sources.py`

2. **Search**
   - Frontend: `frontend/src/app/(dashboard)/search/page.tsx`
   - Backend: `api/routers/search.py`

3. **Podcasts**
   - Frontend: `frontend/src/app/(dashboard)/podcasts/page.tsx`
   - Backend: `api/routers/podcasts.py`

For each feature, ask:
- What does the frontend display?
- What API call does it make?
- What does the backend do?
- What database query runs?
- How does data flow back?

---

## Next Steps

1. ✅ Pick ONE feature (e.g., Notebooks)
2. ✅ Open frontend file
3. ✅ Open corresponding backend file
4. ✅ Read them side by side
5. ✅ Trace the data flow
6. ✅ Make a small change
7. ✅ Test it!

Happy learning! 🚀
