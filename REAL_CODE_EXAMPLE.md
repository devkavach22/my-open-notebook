# Real Code Example: Notebooks Feature

This shows the ACTUAL code from your project, explaining how frontend and backend work together.

---

## Feature: Viewing Notebooks List

### 🎨 FRONTEND - Step by Step

#### Step 1: The Page Component
**File**: `frontend/src/app/(dashboard)/notebooks/page.tsx`

```typescript
export default function NotebooksPage() {
  // 1️⃣ Get translation function for multi-language support
  const { t } = useTranslation()
  
  // 2️⃣ Local state for UI
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  
  // 3️⃣ FETCH DATA FROM BACKEND
  // This is where the magic happens!
  const { data: notebooks, isLoading, refetch } = useNotebooks(false)  // false = not archived
  const { data: archivedNotebooks } = useNotebooks(true)  // true = archived
  
  // 4️⃣ Filter notebooks based on search
  const filteredActive = useMemo(() => {
    if (!notebooks) return undefined
    if (!searchTerm) return notebooks
    
    // Search by name
    return notebooks.filter((notebook) =>
      notebook.name.toLowerCase().includes(searchTerm.toLowerCase())
    )
  }, [notebooks, searchTerm])
  
  // 5️⃣ RENDER THE UI
  return (
    <AppShell>  {/* Includes sidebar */}
      <div className="p-6">
        {/* Header with title and buttons */}
        <div className="flex items-center justify-between">
          <h1>{t.notebooks.title}</h1>
          
          {/* Refresh button */}
          <Button onClick={() => refetch()}>
            <RefreshCw />
          </Button>
          
          {/* Search input */}
          <Input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search notebooks..."
          />
          
          {/* Create button */}
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus /> New Notebook
          </Button>
        </div>
        
        {/* List of notebooks */}
        <NotebookList 
          notebooks={filteredActive}
          isLoading={isLoading}
        />
        
        {/* Archived notebooks (if any) */}
        {archivedNotebooks?.length > 0 && (
          <NotebookList 
            notebooks={archivedNotebooks}
            title="Archived"
          />
        )}
      </div>
      
      {/* Create dialog (popup) */}
      <CreateNotebookDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
      />
    </AppShell>
  )
}
```

**What this does:**
- ✅ Calls `useNotebooks()` to fetch data
- ✅ Shows loading spinner while fetching
- ✅ Filters notebooks by search term
- ✅ Displays notebooks in a list
- ✅ Has buttons to create/refresh

---

#### Step 2: The Hook (Data Fetching)
**File**: `frontend/src/lib/hooks/use-notebooks.ts`

```typescript
export function useNotebooks(archived?: boolean) {
  // This uses React Query to fetch data
  return useQuery({
    // 1️⃣ Cache key - unique identifier
    queryKey: [...QUERY_KEYS.notebooks, { archived }],
    // Example: ['notebooks', { archived: false }]
    
    // 2️⃣ Function that fetches the data
    queryFn: () => notebooksApi.list({ 
      archived, 
      order_by: 'updated desc'  // Sort by most recently updated
    }),
  })
}
```

**What React Query does automatically:**
- ✅ Caches the data
- ✅ Returns `{ data, isLoading, error }`
- ✅ Refetches when needed
- ✅ Handles loading/error states

---

#### Step 3: The API Client
**File**: `frontend/src/lib/api/notebooks.ts`

```typescript
export const notebooksApi = {
  // GET all notebooks
  list: async (params?: { archived?: boolean; order_by?: string }) => {
    // 1️⃣ Make HTTP GET request
    const response = await apiClient.get<NotebookResponse[]>(
      '/notebooks',  // URL: /api/notebooks
      { params }     // Query params: ?archived=false&order_by=updated desc
    )
    
    // 2️⃣ Return the data
    return response.data
  },
  
  // GET single notebook
  get: async (id: string) => {
    const response = await apiClient.get<NotebookResponse>(
      `/notebooks/${id}`  // URL: /api/notebooks/notebook:abc123
    )
    return response.data
  },
  
  // POST create notebook
  create: async (data: CreateNotebookRequest) => {
    const response = await apiClient.post<NotebookResponse>(
      '/notebooks',
      data  // Body: { name: "My Notebook", description: "..." }
    )
    return response.data
  },
  
  // PUT update notebook
  update: async (id: string, data: UpdateNotebookRequest) => {
    const response = await apiClient.put<NotebookResponse>(
      `/notebooks/${id}`,
      data
    )
    return response.data
  },
  
  // DELETE notebook
  delete: async (id: string, deleteExclusiveSources: boolean = false) => {
    const response = await apiClient.delete<NotebookDeleteResponse>(
      `/notebooks/${id}`,
      { params: { delete_exclusive_sources: deleteExclusiveSources } }
    )
    return response.data
  },
}
```

**What this does:**
- ✅ Makes HTTP requests to backend
- ✅ Handles request/response
- ✅ TypeScript types for safety

---

### 🔧 BACKEND - Step by Step

#### Step 1: The Router (API Endpoints)
**File**: `api/routers/notebooks.py`

```python
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

router = APIRouter()

# 1️⃣ GET /api/notebooks - List all notebooks
@router.get("/notebooks", response_model=List[NotebookResponse])
async def get_notebooks(
    archived: Optional[bool] = Query(None, description="Filter by archived status"),
    order_by: str = Query("updated desc", description="Order by field and direction"),
):
    """
    Get all notebooks with optional filtering and ordering.
    
    Example URLs:
    - GET /api/notebooks
    - GET /api/notebooks?archived=false
    - GET /api/notebooks?archived=true&order_by=created desc
    """
    try:
        # 2️⃣ Build SQL query with counts
        query = f"""
            SELECT *,
            count(<-reference.in) as source_count,
            count(<-artifact.in) as note_count
            FROM notebook
            ORDER BY {order_by}
        """
        
        # 3️⃣ Execute query
        result = await repo_query(query)
        
        # 4️⃣ Filter by archived status if specified
        if archived is not None:
            result = [nb for nb in result if nb.get("archived") == archived]
        
        # 5️⃣ Convert to response format
        return [
            NotebookResponse(
                id=str(nb.get("id", "")),
                name=nb.get("name", ""),
                description=nb.get("description", ""),
                archived=nb.get("archived", False),
                created=str(nb.get("created", "")),
                updated=str(nb.get("updated", "")),
                source_count=nb.get("source_count", 0),
                note_count=nb.get("note_count", 0),
            )
            for nb in result
        ]
    except Exception as e:
        logger.error(f"Error fetching notebooks: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Error fetching notebooks: {str(e)}"
        )


# 2️⃣ GET /api/notebooks/{id} - Get single notebook
@router.get("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def get_notebook(notebook_id: str):
    """
    Get a specific notebook by ID.
    
    Example: GET /api/notebooks/notebook:abc123
    """
    try:
        # Query with counts for single notebook
        query = """
            SELECT *,
            count(<-reference.in) as source_count,
            count(<-artifact.in) as note_count
            FROM $notebook_id
        """
        result = await repo_query(query, {"notebook_id": ensure_record_id(notebook_id)})
        
        if not result:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        nb = result[0]
        return NotebookResponse(
            id=str(nb.get("id", "")),
            name=nb.get("name", ""),
            description=nb.get("description", ""),
            archived=nb.get("archived", False),
            created=str(nb.get("created", "")),
            updated=str(nb.get("updated", "")),
            source_count=nb.get("source_count", 0),
            note_count=nb.get("note_count", 0),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching notebook {notebook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching notebook: {str(e)}")


# 3️⃣ POST /api/notebooks - Create new notebook
@router.post("/notebooks", response_model=NotebookResponse)
async def create_notebook(notebook: NotebookCreate):
    """
    Create a new notebook.
    
    Request body:
    {
        "name": "My Research",
        "description": "Notes about AI"
    }
    """
    try:
        # 1️⃣ Create notebook object
        new_notebook = Notebook(
            name=notebook.name,
            description=notebook.description,
        )
        
        # 2️⃣ Save to database
        await new_notebook.save()
        
        # 3️⃣ Return created notebook
        return NotebookResponse(
            id=new_notebook.id or "",
            name=new_notebook.name,
            description=new_notebook.description,
            archived=new_notebook.archived or False,
            created=str(new_notebook.created),
            updated=str(new_notebook.updated),
            source_count=0,  # New notebook has no sources
            note_count=0,    # New notebook has no notes
        )
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating notebook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating notebook: {str(e)}")


# 4️⃣ PUT /api/notebooks/{id} - Update notebook
@router.put("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(notebook_id: str, notebook_update: NotebookUpdate):
    """
    Update a notebook.
    
    Request body (all fields optional):
    {
        "name": "Updated Name",
        "description": "Updated description",
        "archived": true
    }
    """
    try:
        # 1️⃣ Get existing notebook
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        # 2️⃣ Update only provided fields
        if notebook_update.name is not None:
            notebook.name = notebook_update.name
        if notebook_update.description is not None:
            notebook.description = notebook_update.description
        if notebook_update.archived is not None:
            notebook.archived = notebook_update.archived
        
        # 3️⃣ Save changes
        await notebook.save()
        
        # 4️⃣ Query with counts after update
        query = """
            SELECT *,
            count(<-reference.in) as source_count,
            count(<-artifact.in) as note_count
            FROM $notebook_id
        """
        result = await repo_query(query, {"notebook_id": ensure_record_id(notebook_id)})
        
        if result:
            nb = result[0]
            return NotebookResponse(
                id=str(nb.get("id", "")),
                name=nb.get("name", ""),
                description=nb.get("description", ""),
                archived=nb.get("archived", False),
                created=str(nb.get("created", "")),
                updated=str(nb.get("updated", "")),
                source_count=nb.get("source_count", 0),
                note_count=nb.get("note_count", 0),
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating notebook {notebook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating notebook: {str(e)}")


# 5️⃣ DELETE /api/notebooks/{id} - Delete notebook
@router.delete("/notebooks/{notebook_id}", response_model=NotebookDeleteResponse)
async def delete_notebook(
    notebook_id: str,
    delete_exclusive_sources: bool = Query(
        False,
        description="Whether to delete sources that belong only to this notebook",
    ),
):
    """
    Delete a notebook with cascade deletion.
    
    Always deletes all notes associated with the notebook.
    If delete_exclusive_sources is True, also deletes sources that belong only
    to this notebook (not linked to any other notebooks).
    """
    try:
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        result = await notebook.delete(delete_exclusive_sources=delete_exclusive_sources)
        
        return NotebookDeleteResponse(
            message="Notebook deleted successfully",
            deleted_notes=result["deleted_notes"],
            deleted_sources=result["deleted_sources"],
            unlinked_sources=result["unlinked_sources"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting notebook {notebook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting notebook: {str(e)}")
```

**What this does:**
- ✅ Defines API endpoints (GET, POST, PUT, DELETE)
- ✅ Validates input with Pydantic models
- ✅ Queries database
- ✅ Returns JSON responses
- ✅ Handles errors

---

## 📊 Complete Flow: Viewing Notebooks

```
1. USER OPENS /notebooks PAGE
   ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND                                                    │
├─────────────────────────────────────────────────────────────┤
│ File: frontend/src/app/(dashboard)/notebooks/page.tsx      │
│                                                             │
│ Component loads:                                            │
│   const { data, isLoading } = useNotebooks(false)          │
│         ↓                                                   │
│ File: frontend/src/lib/hooks/use-notebooks.ts              │
│                                                             │
│ Hook calls:                                                 │
│   useQuery({                                                │
│     queryKey: ['notebooks', { archived: false }],          │
│     queryFn: () => notebooksApi.list({ archived: false })  │
│   })                                                        │
│         ↓                                                   │
│ File: frontend/src/lib/api/notebooks.ts                    │
│                                                             │
│ API client makes request:                                   │
│   GET http://localhost:8000/api/notebooks?archived=false   │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP GET Request
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND                                                     │
├─────────────────────────────────────────────────────────────┤
│ File: api/main.py                                           │
│                                                             │
│ FastAPI receives request:                                   │
│   GET /api/notebooks?archived=false                         │
│         ↓                                                   │
│ Middleware checks authentication ✓                          │
│         ↓                                                   │
│ File: api/routers/notebooks.py                              │
│                                                             │
│ Router function:                                            │
│   @router.get("/notebooks")                                 │
│   async def get_notebooks(archived: Optional[bool]):        │
│         ↓                                                   │
│ Execute SQL query:                                          │
│   SELECT *,                                                 │
│   count(<-reference.in) as source_count,                    │
│   count(<-artifact.in) as note_count                        │
│   FROM notebook                                             │
│   ORDER BY updated desc                                     │
│         ↓                                                   │
│ SurrealDB returns results:                                  │
│   [                                                         │
│     {                                                       │
│       id: "notebook:abc123",                                │
│       name: "My Research",                                  │
│       description: "AI notes",                              │
│       source_count: 5,                                      │
│       note_count: 12,                                       │
│       created: "2024-01-15T10:30:00Z",                      │
│       updated: "2024-02-10T14:20:00Z"                       │
│     },                                                      │
│     ...                                                     │
│   ]                                                         │
│         ↓                                                   │
│ Filter by archived=false                                    │
│         ↓                                                   │
│ Convert to NotebookResponse format                          │
│         ↓                                                   │
│ Return JSON response                                        │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Response
                          │ Status: 200 OK
                          │ Body: [{ id, name, ... }]
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND                                                    │
├─────────────────────────────────────────────────────────────┤
│ API client receives response                                │
│         ↓                                                   │
│ React Query:                                                │
│   - Caches data with key ['notebooks', { archived: false }]│
│   - Sets isLoading = false                                  │
│   - Returns data to hook                                    │
│         ↓                                                   │
│ Hook returns data to component                              │
│         ↓                                                   │
│ Component re-renders:                                       │
│   {notebooks?.map(notebook => (                             │
│     <NotebookCard notebook={notebook} />                    │
│   ))}                                                       │
│         ↓                                                   │
│ USER SEES NOTEBOOKS ON SCREEN! ✅                           │
│                                                             │
│ Display:                                                    │
│   📓 My Research (5 sources, 12 notes)                      │
│   📓 Work Notes (3 sources, 8 notes)                        │
│   📓 Personal (1 source, 4 notes)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Complete Flow: Creating a Notebook

```
1. USER CLICKS "New Notebook" BUTTON
   ↓
2. Dialog opens, user fills form:
   - Name: "AI Research"
   - Description: "Notes about machine learning"
   ↓
3. USER CLICKS "Create"
   ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND                                                    │
├─────────────────────────────────────────────────────────────┤
│ File: frontend/src/components/notebooks/CreateNotebookDialog.tsx
│                                                             │
│ Form submit:                                                │
│   const { mutate } = useCreateNotebook()                    │
│   mutate({ name: "AI Research", description: "..." })       │
│         ↓                                                   │
│ File: frontend/src/lib/hooks/use-notebooks.ts              │
│                                                             │
│ Mutation hook:                                              │
│   useMutation({                                             │
│     mutationFn: (data) => notebooksApi.create(data)         │
│   })                                                        │
│         ↓                                                   │
│ File: frontend/src/lib/api/notebooks.ts                    │
│                                                             │
│ API client:                                                 │
│   POST http://localhost:8000/api/notebooks                  │
│   Body: { name: "AI Research", description: "..." }         │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP POST
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ BACKEND                                                     │
├─────────────────────────────────────────────────────────────┤
│ File: api/routers/notebooks.py                              │
│                                                             │
│ Router receives POST:                                       │
│   @router.post("/notebooks")                                │
│   async def create_notebook(notebook: NotebookCreate):      │
│         ↓                                                   │
│ Pydantic validates:                                         │
│   ✓ name is string                                          │
│   ✓ description is string or None                           │
│         ↓                                                   │
│ Create Notebook object:                                     │
│   new_notebook = Notebook(                                  │
│     name="AI Research",                                     │
│     description="Notes about machine learning"              │
│   )                                                         │
│         ↓                                                   │
│ Save to database:                                           │
│   await new_notebook.save()                                 │
│         ↓                                                   │
│ SurrealDB executes:                                         │
│   CREATE notebook:abc123 CONTENT {                          │
│     name: "AI Research",                                    │
│     description: "Notes about machine learning",            │
│     created: time::now(),                                   │
│     updated: time::now(),                                   │
│     archived: false                                         │
│   }                                                         │
│         ↓                                                   │
│ Return created notebook:                                    │
│   {                                                         │
│     id: "notebook:abc123",                                  │
│     name: "AI Research",                                    │
│     description: "Notes about machine learning",            │
│     source_count: 0,                                        │
│     note_count: 0,                                          │
│     created: "2024-02-11T15:30:00Z",                        │
│     updated: "2024-02-11T15:30:00Z"                         │
│   }                                                         │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP Response
                          │ Status: 200 OK
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ FRONTEND                                                    │
├─────────────────────────────────────────────────────────────┤
│ Mutation onSuccess callback:                                │
│   - Invalidate notebooks cache                              │
│   - Show success toast                                      │
│         ↓                                                   │
│ React Query refetches notebooks:                            │
│   GET /api/notebooks                                        │
│         ↓                                                   │
│ Notebooks list updates with new notebook                    │
│         ↓                                                   │
│ Dialog closes                                               │
│         ↓                                                   │
│ USER SEES NEW NOTEBOOK IN LIST! ✅                          │
│                                                             │
│ Display:                                                    │
│   📓 AI Research (0 sources, 0 notes) ← NEW!                │
│   📓 My Research (5 sources, 12 notes)                      │
│   📓 Work Notes (3 sources, 8 notes)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Takeaways

### Frontend Pattern
```typescript
Page Component
  ↓ uses
Custom Hook (useNotebooks)
  ↓ uses
React Query (useQuery/useMutation)
  ↓ calls
API Client (notebooksApi)
  ↓ makes
HTTP Request
```

### Backend Pattern
```python
FastAPI Router
  ↓ receives
HTTP Request
  ↓ validates
Pydantic Model
  ↓ creates/queries
Domain Model (Notebook)
  ↓ saves to
Database (SurrealDB)
  ↓ returns
JSON Response
```

### Data Types
```typescript
// Frontend TypeScript
interface NotebookResponse {
  id: string
  name: string
  description: string
  archived: boolean
  created: string
  updated: string
  source_count: number
  note_count: number
}
```

```python
# Backend Python
class NotebookResponse(BaseModel):
    id: str
    name: str
    description: str
    archived: bool
    created: str
    updated: str
    source_count: int
    note_count: int
```

---

## Practice Exercise

Now trace these features yourself:

1. **Sources** - How does the sources list work?
2. **Search** - How does search with AI work?
3. **Chat** - How does real-time chat work?

For each, find:
- Frontend page file
- Frontend hook file
- Frontend API file
- Backend router file
- Trace the complete flow!

Happy learning! 🚀
