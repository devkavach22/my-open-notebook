# Open Notebook - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                     http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    NEXT.JS FRONTEND                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  App Router (frontend/src/app/)                          │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │  /login    │  │ /notebooks │  │  /sources  │  ...   │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Components (frontend/src/components/)                   │  │
│  │  - AppSidebar, NotebookCard, ChatPanel, etc.            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Hooks & State (frontend/src/lib/)                       │  │
│  │  - useNotebooks() → React Query                          │  │
│  │  - useSidebarStore() → Zustand                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  API Client (frontend/src/lib/api/)                      │  │
│  │  - fetch('/api/notebooks')                               │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Requests
                             │ (JSON)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                               │
│                  http://localhost:8000/api                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  main.py - FastAPI App                                   │  │
│  │  - CORS Middleware                                        │  │
│  │  - Auth Middleware                                        │  │
│  │  - Route Registration                                     │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Routers (api/routers/)                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │notebooks │  │ sources  │  │   chat   │  ...        │  │
│  │  │  .py     │  │   .py    │  │   .py    │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Services (api/*_service.py)                             │  │
│  │  - Business logic                                         │  │
│  │  - Data processing                                        │  │
│  └──────────────────────────┬───────────────────────────────┘  │
│                             │                                    │
│  ┌──────────────────────────▼──────────────────────────────┐  │
│  │  Core Package (open_notebook/)                           │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐        │  │
│  │  │ database/  │  │   graphs/  │  │    ai/     │        │  │
│  │  │repository  │  │  LangGraph │  │  providers │        │  │
│  │  └────────────┘  └────────────┘  └────────────┘        │  │
│  └──────────────────────────┬───────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SURREALDB DATABASE                          │
│                   http://localhost:8080                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Tables:                                                  │  │
│  │  - notebook                                               │  │
│  │  - source                                                 │  │
│  │  - note                                                   │  │
│  │  - chat_message                                           │  │
│  │  - embedding                                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL AI SERVICES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   OpenAI     │  │  Anthropic   │  │    Ollama    │         │
│  │     API      │  │     API      │  │   (Local)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Request Flow Example: Creating a Notebook

```
1. USER CLICKS "Create Notebook" BUTTON
   ↓
2. Component calls: openNotebookDialog()
   File: frontend/src/lib/hooks/use-create-dialogs.tsx
   ↓
3. Dialog opens, user fills form
   File: frontend/src/components/notebooks/CreateNotebookDialog.tsx
   ↓
4. User clicks "Create" → calls mutation
   const { mutate } = useCreateNotebook()
   File: frontend/src/lib/hooks/use-notebooks.ts
   ↓
5. Mutation calls API client
   await apiClient.post('/api/notebooks', data)
   File: frontend/src/lib/api/notebooks.ts
   ↓
6. HTTP POST → Backend receives request
   @router.post("/notebooks")
   File: api/routers/notebooks.py
   ↓
7. Router calls service
   await notebook_service.create_notebook(data)
   File: api/notebook_service.py
   ↓
8. Service calls repository
   await repository.create_notebook(data)
   File: open_notebook/database/repository.py
   ↓
9. Repository executes SQL
   CREATE notebook CONTENT {...}
   Database: SurrealDB
   ↓
10. Response flows back up the chain
    Database → Repository → Service → Router → API Response
    ↓
11. Frontend receives response
    React Query updates cache
    ↓
12. UI automatically re-renders
    New notebook appears in list
```

---

## Data Flow Patterns

### Pattern 1: Fetching Data (GET)
```
Component
  ↓ calls
Hook (useNotebooks)
  ↓ uses
React Query (useQuery)
  ↓ calls
API Client (fetch)
  ↓ HTTP GET
Backend Router
  ↓ calls
Service
  ↓ calls
Repository
  ↓ queries
Database
  ↓ returns
Data flows back up
  ↓ cached by
React Query
  ↓ renders in
Component
```

### Pattern 2: Modifying Data (POST/PUT/DELETE)
```
Component
  ↓ user action
Hook (useCreateNotebook)
  ↓ uses
React Query (useMutation)
  ↓ calls
API Client (fetch)
  ↓ HTTP POST
Backend Router
  ↓ validates
Pydantic Model
  ↓ calls
Service
  ↓ calls
Repository
  ↓ inserts
Database
  ↓ returns
Success response
  ↓ triggers
onSuccess callback
  ↓ invalidates
React Query cache
  ↓ refetches
Fresh data
  ↓ updates
Component
```

### Pattern 3: Real-time Updates (Streaming)
```
Component
  ↓ initiates
Chat message
  ↓ calls
API with streaming
  ↓ HTTP POST (stream)
Backend Router
  ↓ calls
LangGraph workflow
  ↓ calls
AI Provider (OpenAI/Anthropic)
  ↓ streams back
Token by token
  ↓ yields
Server-Sent Events
  ↓ received by
Frontend EventSource
  ↓ updates
Component state
  ↓ renders
Streaming text
```

---

## File Organization

### Frontend Structure
```
frontend/src/
├── app/                    # Pages (Next.js App Router)
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── (auth)/            # Auth pages (login)
│   └── (dashboard)/       # Protected pages
│       ├── layout.tsx     # Dashboard layout
│       ├── notebooks/     # Notebooks pages
│       ├── sources/       # Sources pages
│       └── ...
│
├── components/            # React components
│   ├── layout/           # Layout components (Sidebar, Shell)
│   ├── common/           # Shared components (Button, Dialog)
│   ├── notebooks/        # Notebook-specific components
│   ├── sources/          # Source-specific components
│   └── ui/               # Base UI components (shadcn)
│
└── lib/                  # Utilities & logic
    ├── api/             # API client functions
    ├── hooks/           # Custom React hooks
    ├── stores/          # Zustand state stores
    ├── types/           # TypeScript types
    └── utils/           # Helper functions
```

### Backend Structure
```
api/
├── main.py              # FastAPI app entry
├── routers/             # API endpoints
│   ├── notebooks.py
│   ├── sources.py
│   └── ...
├── *_service.py         # Business logic
└── models.py            # Pydantic models

open_notebook/
├── ai/                  # AI integrations
├── database/            # Database layer
│   ├── repository.py   # Database queries
│   └── migrations/     # Schema changes
├── domain/              # Domain models
├── graphs/              # LangGraph workflows
└── utils/               # Utilities
```

---

## Key Technologies Explained

### Frontend Technologies

**Next.js App Router**
- File-based routing
- Server & client components
- Built-in optimization

**React Query (TanStack Query)**
- Automatic caching
- Background refetching
- Optimistic updates

**Zustand**
- Simple state management
- No boilerplate
- TypeScript support

**Shadcn/ui**
- Copy-paste components
- Built on Radix UI
- Fully customizable

**TailwindCSS**
- Utility-first CSS
- No custom CSS files
- Responsive design

### Backend Technologies

**FastAPI**
- Fast Python web framework
- Automatic API docs
- Type validation

**SurrealDB**
- Multi-model database
- Graph + Document + SQL
- Real-time subscriptions

**LangGraph**
- AI workflow orchestration
- State management
- Tool calling

**Pydantic**
- Data validation
- Type checking
- Serialization

---

## Common Patterns

### 1. Component Pattern
```typescript
// Every component follows this structure
export function MyComponent({ prop1, prop2 }: Props) {
  // 1. Hooks at the top
  const [state, setState] = useState()
  const { data } = useQuery()
  
  // 2. Event handlers
  const handleClick = () => { }
  
  // 3. Effects
  useEffect(() => { }, [])
  
  // 4. Render
  return <div>...</div>
}
```

### 2. API Hook Pattern
```typescript
// Custom hook for API calls
export function useResource() {
  return useQuery({
    queryKey: ['resource'],
    queryFn: () => apiClient.get('/resource'),
  })
}

export function useCreateResource() {
  return useMutation({
    mutationFn: (data) => apiClient.post('/resource', data),
    onSuccess: () => queryClient.invalidateQueries(['resource']),
  })
}
```

### 3. Backend Route Pattern
```python
# Every route follows this structure
@router.post("/resource")
async def create_resource(data: ResourceCreate):
    # 1. Validate (automatic with Pydantic)
    # 2. Call service
    result = await service.create(data)
    # 3. Return response
    return result
```

---

## Where to Start?

### Beginner Path
1. ✅ Read this architecture guide
2. ✅ Read PROJECT_LEARNING_GUIDE.md
3. 📖 Study `frontend/src/app/layout.tsx`
4. 📖 Study `frontend/src/components/layout/AppSidebar.tsx`
5. 📖 Study `frontend/src/app/(dashboard)/notebooks/page.tsx`
6. 🔨 Make a small change (add a button, change text)
7. 🔨 Create a simple new page

### Intermediate Path
1. 📖 Study a complete feature (e.g., Notebooks)
2. 📖 Trace data flow from UI to database
3. 📖 Understand React Query caching
4. 🔨 Add a new field to an existing feature
5. 🔨 Create a new API endpoint

### Advanced Path
1. 📖 Study LangGraph workflows
2. 📖 Understand AI integrations
3. 📖 Study database migrations
4. 🔨 Build a complete new feature
5. 🔨 Optimize performance

---

## Questions to Guide Your Learning

As you read code, ask yourself:

1. **What does this file do?**
2. **What data does it need?**
3. **Where does the data come from?**
4. **What happens when the user interacts?**
5. **How does it connect to other parts?**

Happy learning! 🚀
