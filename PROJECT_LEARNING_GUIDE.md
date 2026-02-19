# Open Notebook Project - Learning Guide

## Step-by-Step Understanding Guide

This guide will help you understand the Open Notebook project line by line, starting from the basics and moving to advanced concepts.

---

## Phase 1: Project Overview & Architecture

### 1.1 What is this project?
- **Open Notebook** is a full-stack application for research and knowledge management
- **Frontend**: Next.js 14+ (React) with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: SurrealDB
- **Features**: Notebooks, Sources, AI Chat, Podcasts, Search

### 1.2 Technology Stack
```
Frontend:
- Next.js 14+ (App Router)
- React 18+
- TypeScript
- TailwindCSS
- Shadcn/ui components
- React Query (TanStack Query)
- Zustand (State Management)

Backend:
- FastAPI (Python)
- SurrealDB (Database)
- LangGraph (AI workflows)
- OpenAI/Anthropic APIs
```

### 1.3 Project Structure
```
open-notebook/
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── app/          # Next.js App Router pages
│   │   ├── components/   # React components
│   │   ├── lib/          # Utilities, hooks, stores
│   │   └── test/         # Test files
│   └── public/           # Static assets
│
├── api/                  # FastAPI backend
│   ├── routers/         # API route handlers
│   ├── main.py          # FastAPI app entry point
│   └── models.py        # Data models
│
├── open_notebook/       # Core Python package
│   ├── ai/             # AI provider integrations
│   ├── database/       # Database layer
│   ├── domain/         # Domain models
│   ├── graphs/         # LangGraph workflows
│   └── utils/          # Utility functions
│
├── docs/               # Documentation
├── tests/              # Backend tests
└── prompts/            # AI prompt templates
```

---

## Phase 2: Understanding the Frontend

### 2.1 Entry Points (Start Here!)

#### File: `frontend/src/app/layout.tsx`
**Purpose**: Root layout that wraps the entire application

```typescript
// This is the FIRST file that loads in your app
export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <ErrorBoundary>           // Catches errors
          <ThemeProvider>         // Dark/Light mode
            <QueryProvider>       // API data fetching
              <I18nProvider>      // Multi-language support
                <ConnectionGuard> // Checks API connection
                  {children}      // Your pages render here
                </ConnectionGuard>
              </I18nProvider>
            </QueryProvider>
          </ThemeProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}
```

**Key Concepts**:
- **Providers**: Wrap components to give them special powers (theme, data, etc.)
- **children**: Whatever page you're on gets rendered here
- **Order matters**: Outer providers wrap inner ones

---

#### File: `frontend/src/app/page.tsx`
**Purpose**: Landing page (root `/` route)

```typescript
// When user visits http://localhost:3000/
export default function HomePage() {
  // Redirects to /notebooks
  // This is just a landing page
}
```

---

#### File: `frontend/src/app/(dashboard)/layout.tsx`
**Purpose**: Layout for all authenticated pages

```typescript
export default function DashboardLayout({ children }) {
  const { isAuthenticated } = useAuth()  // Check if user logged in
  
  // If not logged in → redirect to /login
  if (!isAuthenticated) {
    router.push('/login')
    return null
  }
  
  // If logged in → show the page
  return (
    <>
      {children}              // The actual page content
      <ModalProvider />       // Handles popup dialogs
      <CommandPalette />      // Cmd+K quick actions
    </>
  )
}
```

**Key Concepts**:
- **Authentication Guard**: Protects pages from unauthorized access
- **Nested Layouts**: Dashboard layout wraps all dashboard pages
- **Folder naming**: `(dashboard)` is a route group (doesn't affect URL)

---

### 2.2 Navigation & Sidebar

#### File: `frontend/src/components/layout/AppSidebar.tsx`
**Purpose**: The left sidebar menu you see in the app

**Line-by-line breakdown**:

```typescript
// 1. Define the menu structure
const getNavigation = (t: TranslationKeys) => [
  {
    title: t.navigation.collect,  // Section title
    items: [
      { 
        name: t.navigation.sources,  // Menu item name
        href: '/sources',            // Where it goes
        icon: FileText              // Icon to show
      },
    ],
  },
  // ... more sections
]

// 2. The sidebar component
export function AppSidebar() {
  const pathname = usePathname()  // Current URL path
  const { isCollapsed } = useSidebarStore()  // Is sidebar collapsed?
  
  // 3. Render the sidebar
  return (
    <div className={isCollapsed ? 'w-16' : 'w-64'}>
      {/* Logo and collapse button */}
      
      {/* Create button dropdown */}
      <DropdownMenu>
        <Button>Create</Button>
        <DropdownMenuContent>
          <DropdownMenuItem>Source</DropdownMenuItem>
          <DropdownMenuItem>Notebook</DropdownMenuItem>
          <DropdownMenuItem>Podcast</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      
      {/* Navigation menu items */}
      {navigation.map((section) => (
        <div key={section.title}>
          <h3>{section.title}</h3>
          {section.items.map((item) => (
            <Link href={item.href}>
              <Button variant={isActive ? 'secondary' : 'ghost'}>
                <item.icon />
                {item.name}
              </Button>
            </Link>
          ))}
        </div>
      ))}
      
      {/* Theme toggle, language, logout */}
    </div>
  )
}
```

**Key Concepts**:
- **usePathname()**: Gets current URL to highlight active menu
- **Conditional rendering**: Shows different UI based on collapsed state
- **Tooltip**: Shows text on hover when sidebar is collapsed
- **State management**: `useSidebarStore()` manages collapse state globally

---

### 2.3 Pages & Routing

#### Next.js App Router Routing Rules:
```
File Path                                    → URL
frontend/src/app/page.tsx                   → /
frontend/src/app/(dashboard)/page.tsx       → / (dashboard home)
frontend/src/app/(dashboard)/notebooks/page.tsx → /notebooks
frontend/src/app/(dashboard)/notebooks/[id]/page.tsx → /notebooks/123
frontend/src/app/(auth)/login/page.tsx      → /login
```

**Key Concepts**:
- **Folders = Routes**: Each folder becomes a URL segment
- **page.tsx**: The actual page component
- **layout.tsx**: Wraps all pages in that folder
- **[id]**: Dynamic route parameter (e.g., notebook ID)
- **(folder)**: Route group - doesn't affect URL

---

#### File: `frontend/src/app/(dashboard)/notebooks/page.tsx`
**Purpose**: List all notebooks

```typescript
export default function NotebooksPage() {
  // 1. Fetch data from API
  const { data: notebooks, isLoading } = useNotebooks()
  
  // 2. Show loading state
  if (isLoading) return <LoadingSpinner />
  
  // 3. Render the page
  return (
    <AppShell>  {/* Includes sidebar + main content area */}
      <div className="container">
        <h1>Notebooks</h1>
        
        {/* List of notebooks */}
        {notebooks.map(notebook => (
          <NotebookCard key={notebook.id} notebook={notebook} />
        ))}
      </div>
    </AppShell>
  )
}
```

---

#### File: `frontend/src/app/(dashboard)/notebooks/[id]/page.tsx`
**Purpose**: Single notebook detail page (3-column layout)

```typescript
export default function NotebookDetailPage({ params }) {
  const notebookId = params.id  // Get ID from URL
  
  // Fetch notebook data
  const { data: notebook } = useNotebook(notebookId)
  
  return (
    <AppShell>
      <div className="grid grid-cols-3">
        {/* Column 1: Sources */}
        <SourcesColumn notebookId={notebookId} />
        
        {/* Column 2: Chat */}
        <ChatColumn notebookId={notebookId} />
        
        {/* Column 3: Notes */}
        <NotesColumn notebookId={notebookId} />
      </div>
    </AppShell>
  )
}
```

---

## Phase 3: Understanding Data Flow

### 3.1 How Data Flows in the App

```
User Action → Component → Hook → API Call → Backend → Database
                ↓                    ↓
            Update UI ← React Query Cache ← Response
```

### 3.2 React Query (Data Fetching)

#### File: `frontend/src/lib/hooks/use-notebooks.ts`

```typescript
// Custom hook to fetch notebooks
export function useNotebooks() {
  return useQuery({
    queryKey: ['notebooks'],  // Unique cache key
    queryFn: async () => {
      // Call API
      const response = await fetch('/api/notebooks')
      return response.json()
    },
  })
}

// Hook to create a notebook
export function useCreateNotebook() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: async (data) => {
      // POST to API
      return await fetch('/api/notebooks', {
        method: 'POST',
        body: JSON.stringify(data),
      })
    },
    onSuccess: () => {
      // Refresh the notebooks list
      queryClient.invalidateQueries(['notebooks'])
    },
  })
}
```

**Key Concepts**:
- **useQuery**: Fetch data (GET requests)
- **useMutation**: Modify data (POST, PUT, DELETE)
- **queryKey**: Identifies cached data
- **invalidateQueries**: Refresh data after changes

---

### 3.3 State Management (Zustand)

#### File: `frontend/src/lib/stores/sidebar-store.ts`

```typescript
// Global state for sidebar
export const useSidebarStore = create<SidebarStore>((set) => ({
  // State
  isCollapsed: false,
  
  // Actions
  toggleCollapse: () => set((state) => ({ 
    isCollapsed: !state.isCollapsed 
  })),
  
  setCollapsed: (collapsed) => set({ isCollapsed: collapsed }),
}))

// Usage in components:
const { isCollapsed, toggleCollapse } = useSidebarStore()
```

**Key Concepts**:
- **Zustand**: Simple state management (lighter than Redux)
- **create()**: Creates a store
- **set()**: Updates state
- **Automatic re-renders**: Components using the store update automatically

---

## Phase 4: Understanding the Backend

### 4.1 Backend Entry Point

#### File: `api/main.py`

```python
# 1. Create FastAPI app
app = FastAPI(title="Open Notebook API")

# 2. Add middleware
app.add_middleware(CORSMiddleware)  # Allow frontend to call API
app.add_middleware(PasswordAuthMiddleware)  # Require authentication

# 3. Register routes
app.include_router(notebooks.router, prefix="/api")
app.include_router(sources.router, prefix="/api")
# ... more routers

# 4. Startup event
@asynccontextmanager
async def lifespan(app):
    # Run database migrations
    await migration_manager.run_migration_up()
    yield
    # Cleanup on shutdown
```

**Key Concepts**:
- **FastAPI**: Python web framework (like Express for Node.js)
- **Middleware**: Code that runs before every request
- **Routers**: Organize routes by feature
- **Lifespan**: Startup/shutdown logic

---

### 4.2 API Routes

#### File: `api/routers/notebooks.py`

```python
router = APIRouter()

# GET /api/notebooks - List all notebooks
@router.get("/notebooks")
async def get_notebooks():
    # 1. Query database
    notebooks = await repository.get_all_notebooks()
    
    # 2. Return JSON response
    return notebooks

# POST /api/notebooks - Create notebook
@router.post("/notebooks")
async def create_notebook(data: NotebookCreate):
    # 1. Validate data (automatic with Pydantic)
    # 2. Save to database
    notebook = await repository.create_notebook(data)
    
    # 3. Return created notebook
    return notebook

# GET /api/notebooks/{id} - Get single notebook
@router.get("/notebooks/{id}")
async def get_notebook(id: str):
    notebook = await repository.get_notebook(id)
    if not notebook:
        raise HTTPException(status_code=404)
    return notebook
```

**Key Concepts**:
- **@router.get/post/put/delete**: Define HTTP methods
- **Path parameters**: `{id}` in URL
- **Pydantic models**: Automatic validation
- **async/await**: Asynchronous operations

---

### 4.3 Database Layer

#### File: `open_notebook/database/repository.py`

```python
class Repository:
    async def get_all_notebooks(self):
        # Query SurrealDB
        query = "SELECT * FROM notebook"
        result = await self.db.query(query)
        return result
    
    async def create_notebook(self, data):
        # Insert into database
        query = """
            CREATE notebook CONTENT {
                title: $title,
                description: $description,
                created_at: time::now()
            }
        """
        result = await self.db.query(query, {
            'title': data.title,
            'description': data.description
        })
        return result
```

---

## Phase 5: Key Concepts to Master

### 5.1 React Concepts
1. **Components**: Reusable UI pieces
2. **Props**: Data passed to components
3. **State**: Data that changes over time
4. **Hooks**: Special functions (useState, useEffect, etc.)
5. **Context**: Share data without passing props

### 5.2 Next.js Concepts
1. **App Router**: File-based routing
2. **Server Components**: Render on server (default)
3. **Client Components**: Interactive ('use client')
4. **Layouts**: Shared UI across pages
5. **Dynamic Routes**: [id] for variable URLs

### 5.3 TypeScript Concepts
1. **Types**: Define data shapes
2. **Interfaces**: Object structure definitions
3. **Generics**: Reusable type definitions
4. **Type inference**: TS guesses types

### 5.4 API Concepts
1. **REST**: HTTP methods (GET, POST, PUT, DELETE)
2. **JSON**: Data format
3. **Authentication**: Verify user identity
4. **CORS**: Allow cross-origin requests

---

## Phase 6: Learning Path

### Week 1: Frontend Basics
1. Read `frontend/src/app/layout.tsx` - understand providers
2. Read `frontend/src/app/(dashboard)/layout.tsx` - auth guard
3. Read `frontend/src/components/layout/AppSidebar.tsx` - navigation
4. Read `frontend/src/app/(dashboard)/notebooks/page.tsx` - simple page

### Week 2: Data Flow
1. Read `frontend/src/lib/hooks/use-notebooks.ts` - data fetching
2. Read `frontend/src/lib/api/notebooks.ts` - API client
3. Read `frontend/src/lib/stores/sidebar-store.ts` - state management
4. Trace a full flow: Click button → API call → Update UI

### Week 3: Components
1. Read `frontend/src/components/notebooks/NotebookCard.tsx`
2. Read `frontend/src/components/ui/button.tsx` - UI components
3. Read `frontend/src/components/common/ConfirmDialog.tsx` - dialogs
4. Build a simple component yourself

### Week 4: Backend
1. Read `api/main.py` - app setup
2. Read `api/routers/notebooks.py` - API routes
3. Read `open_notebook/database/repository.py` - database
4. Test API with Postman or curl

---

## Next Steps

1. **Pick a feature** to study deeply (e.g., Notebooks)
2. **Trace the flow** from UI → API → Database
3. **Make small changes** to understand how things work
4. **Ask questions** about specific files or concepts

Would you like me to explain any specific file or concept in detail?
