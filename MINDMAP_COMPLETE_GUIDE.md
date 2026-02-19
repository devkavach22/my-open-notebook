# Mind Map Feature - Complete Guide (Frontend to Backend)

## 📋 Table of Contents
1. [Overview](#overview)
2. [User Journey](#user-journey)
3. [Frontend Flow](#frontend-flow)
4. [Backend Flow](#backend-flow)
5. [AI Engine](#ai-engine)
6. [Data Structure](#data-structure)
7. [Code Walkthrough](#code-walkthrough)

---

## Overview

The Mind Map feature generates an AI-powered visual hierarchy from notebook sources, allowing users to explore content interactively.

**Tech Stack:**
- Frontend: React/Next.js + TypeScript
- Backend: Python/FastAPI
- AI: LangChain + LLM (OpenAI/Anthropic/etc.)
- Database: SurrealDB

---

## User Journey

```
User clicks "Mind Map" button
    ↓
Dialog opens with loading spinner
    ↓
Frontend calls API: POST /api/notebooks/{id}/mindmap
    ↓
Backend fetches sources from database
    ↓
AI analyzes content and generates hierarchy
    ↓
Backend returns JSON tree structure
    ↓
Frontend renders interactive nodes
    ↓
User clicks nodes to expand/collapse
```

---

## Frontend Flow

### 1. Entry Point: Studio Column Button

**File:** `frontend/src/app/(dashboard)/notebooks/components/StudioColumn.tsx`

```typescript
// Line ~75
{
  id: 'mindmap',
  icon: Brain,
  label: 'Mind Map',
  description: 'Visualize connections',
  available: true,
  onClick: () => {
    setMindMapOpen(true)  // Opens the dialog
  }
}
```

**What happens:**
- User clicks "Mind Map" card in Studio section
- `setMindMapOpen(true)` triggers dialog to open
- Dialog component mounts and starts loading

---

### 2. Dialog Component: MindMapDialog

**File:** `frontend/src/components/notebooks/MindMapDialog.tsx`

#### A. Component State (Lines 25-30)

```typescript
const [loading, setLoading] = useState(false)           // Loading indicator
const [mindMapData, setMindMapData] = useState<MindMapNode | null>(null)  // Tree data
const [zoom, setZoom] = useState(1)                     // Zoom level (0.5 - 2.0)
const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set(['root']))  // Which nodes are open
const [fullscreen, setFullscreen] = useState(false)     // Fullscreen mode
```

#### B. Auto-fetch on Open (Lines 32-36)

```typescript
useEffect(() => {
  if (open && !mindMapData) {
    generateMindMap()  // Fetch data when dialog opens
  }
}, [open])
```

#### C. API Call Function (Lines 38-67)

```typescript
const generateMindMap = async () => {
  setLoading(true)
  try {
    // 1. Call backend API
    const response = await fetch(`/api/notebooks/${notebookId}/mindmap`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    })

    // 2. Handle errors
    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to generate mind map')
    }

    // 3. Parse response
    const data = await response.json()
    // Response format: { notebook_id, notebook_name, root: {...} }
    
    // 4. Set data and auto-expand first level
    setMindMapData(data.root)
    const newExpanded = new Set<string>(['root'])
    if (data.root.children) {
      data.root.children.forEach((child: MindMapNode) => {
        newExpanded.add(child.id)
      })
    }
    setExpandedNodes(newExpanded)
  } catch (error) {
    alert(`Failed to generate mind map: ${error}`)
  } finally {
    setLoading(false)
  }
}
```

**What happens:**
1. Makes POST request to `/api/notebooks/{notebookId}/mindmap`
2. Waits for backend to process (can take 5-30 seconds with AI)
3. Receives JSON tree structure
4. Auto-expands root and first-level nodes
5. Renders the tree

#### D. Node Interaction (Lines 69-85)

```typescript
// Toggle single node
const toggleNode = (nodeId: string) => {
  const newExpanded = new Set(expandedNodes)
  if (newExpanded.has(nodeId)) {
    newExpanded.delete(nodeId)  // Collapse
  } else {
    newExpanded.add(nodeId)     // Expand
  }
  setExpandedNodes(newExpanded)
}

// Expand all nodes recursively
const expandAll = () => {
  const allIds = new Set<string>()
  const collectIds = (node: MindMapNode) => {
    allIds.add(node.id)
    node.children?.forEach(collectIds)
  }
  if (mindMapData) collectIds(mindMapData)
  setExpandedNodes(allIds)
}

// Collapse to root only
const collapseAll = () => {
  setExpandedNodes(new Set(['root']))
}
```

#### E. Rendering Nodes (Lines 87-150)

```typescript
const renderNode = (node: MindMapNode, level: number = 0) => {
  const isExpanded = expandedNodes.has(node.id)
  const hasChildren = node.children && node.children.length > 0

  return (
    <div className="flex flex-row items-center gap-4">
      {/* Node Box */}
      <div
        className={`rounded-xl border-2 ${colors[node.type]} ...`}
        onClick={() => hasChildren && toggleNode(node.id)}
      >
        {/* Chevron icon */}
        {hasChildren && (
          isExpanded ? <ChevronDown /> : <ChevronRight />
        )}
        
        {/* Label */}
        <span>{node.label}</span>
        
        {/* Child count badge */}
        {hasChildren && <span>({node.children?.length})</span>}
      </div>

      {/* Children - Expand to the RIGHT */}
      {hasChildren && isExpanded && (
        <div className="flex flex-col gap-6">
          {node.children!.map((child) => (
            <div key={child.id} className="flex flex-row items-center gap-3">
              {/* Horizontal connection line */}
              <div className="w-8 h-0.5 bg-gradient-to-r ..." />
              {/* Recursive render */}
              {renderNode(child, level + 1)}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
```

**Visual Structure:**
```
[Root Node] ──── [Main 1] ──── [Sub 1.1] ──── [Detail 1.1.1]
            │                └── [Sub 1.2]
            │
            └─── [Main 2] ──── [Sub 2.1]
```

---

## Backend Flow

### 1. API Endpoint

**File:** `api/routers/notebooks.py` (Lines 350-450)

```python
@router.post("/notebooks/{notebook_id}/mindmap", response_model=MindMapResponse)
async def generate_mindmap(notebook_id: str):
    """Generate an AI-powered mind map from notebook sources."""
```

#### Step 1: Get Notebook (Lines 356-363)

```python
# Get notebook from database
notebook = await Notebook.get(notebook_id)
if not notebook:
    raise HTTPException(status_code=404, detail="Notebook not found")

logger.info(f"MINDMAP: Found notebook '{notebook.name}'")
```

**What happens:**
- Queries SurrealDB: `SELECT * FROM notebook WHERE id = $notebook_id`
- Returns notebook object with metadata

#### Step 2: Get Sources (Lines 365-380)

```python
# Get all sources linked to this notebook
sources = await notebook.get_sources()
logger.info(f"MINDMAP: Found {len(sources)} sources")

# Fetch full_text for each source
for source in sources:
    try:
        full_source = await Source.get(source.id)
        if full_source and full_source.full_text:
            source.full_text = full_source.full_text
            logger.info(f"MINDMAP: Source '{source.title}' has {len(full_source.full_text)} chars")
    except Exception as e:
        logger.error(f"MINDMAP: Error fetching full_text: {e}")
```

**What happens:**
- Queries SurrealDB: `SELECT * FROM source WHERE id IN (SELECT in FROM reference WHERE out = $notebook_id)`
- For each source, fetches the `full_text` field (contains complete document content)
- Example: Source 1 has 9,243 characters, Source 2 has 17,190 characters

#### Step 3: Initialize AI Engine (Lines 382-393)

```python
# Import AI mind map engine
from open_notebook.utils.mindmap_engine import MindMapEngine
from open_notebook.ai.provision import provision_langchain_model

# Initialize engine with LLM
try:
    llm = await provision_langchain_model(
        content="",
        model_id=None,
        default_type="chat"
    )
    engine = MindMapEngine(llm=llm)
    logger.info("✅ Using AI-powered mind map generation")
except Exception as e:
    logger.warning(f"⚠️ Could not load LLM, using rule-based fallback: {e}")
    engine = MindMapEngine(llm=None)
```

**What happens:**
- Loads configured LLM (OpenAI GPT-4, Claude, etc.)
- If LLM fails, falls back to regex-based parsing
- Engine is ready to process text

#### Step 4: Generate Mind Map for Each Source (Lines 395-440)

```python
main_topics = []

for idx, source in enumerate(sources):
    logger.info(f"MINDMAP: Processing source {idx+1}/{len(sources)}: '{source.title}'")
    
    # Generate AI mind map for this source
    try:
        ai_mindmap = engine.generate_mind_map(
            full_text=source.full_text,
            title=source.title
        )
        
        # Convert AI mind map to our node structure
        def convert_to_nodes(data: dict, parent_id: str, level: int = 0) -> MindMapNode:
            node_type = "main" if level == 0 else "sub" if level == 1 else "detail"
            node_id = f"{parent_id}_{data['label'][:20].replace(' ', '_')}"
            
            children = None
            if data.get("children"):
                children = [
                    convert_to_nodes(child, node_id, level + 1)
                    for child in data["children"]
                ]
            
            return MindMapNode(
                id=node_id,
                label=data["label"],
                type=node_type,
                children=children
            )
        
        # Create source node with AI-generated children
        source_node = MindMapNode(
            id=f"source_{source.id}",
            label=ai_mindmap.get("label", source.title),
            type="main",
            children=[
                convert_to_nodes(child, f"source_{source.id}", level=1)
                for child in ai_mindmap.get("children", [])
            ]
        )
        
        main_topics.append(source_node)
        logger.info(f"✅ Generated AI mind map with {len(ai_mindmap.get('children', []))} categories")
        
    except Exception as e:
        logger.error(f"❌ Failed to generate AI mind map: {e}")
        # Fallback to simple preview
```

**What happens:**
- For each source, calls AI engine with full text
- AI analyzes content and returns hierarchical structure
- Converts AI format to MindMapNode format
- Handles errors gracefully with fallback

#### Step 5: Return Response (Lines 442-455)

```python
root = MindMapNode(
    id="root",
    label=notebook.name,
    type="root",
    children=main_topics
)

logger.info("MINDMAP: Successfully generated AI-powered mind map!")

return MindMapResponse(
    notebook_id=notebook_id,
    notebook_name=notebook.name,
    root=root
)
```

**Response Format:**
```json
{
  "notebook_id": "notebook:kuo7qmjwlrbllbpxw4lm",
  "notebook_name": "sss",
  "root": {
    "id": "root",
    "label": "sss",
    "type": "root",
    "children": [
      {
        "id": "source_source:zvqk736988lpm8yzyhae",
        "label": "Ravi Jagit",
        "type": "main",
        "children": [
          {
            "id": "source_source:zvqk736988lpm8yzyhae_Identity_&_Backgrou",
            "label": "Identity & Background",
            "type": "sub",
            "children": [
              {
                "id": "...",
                "label": "Resident of Jagsi, Sonipat",
                "type": "detail",
                "children": null
              }
            ]
          }
        ]
      }
    ]
  }
}
```

---

## AI Engine

### File: `open_notebook/utils/mindmap_engine.py`

#### 1. Initialization (Lines 30-60)

```python
class MindMapEngine:
    def __init__(self, llm=None):
        self.llm = llm
        
        # LLM Prompt for intelligent categorization
        self.mindmap_prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are a professional intelligence analyst building a structured mind map.\n"
                "STRICT RULES:\n"
                "1. Root label MUST be the Subject Name.\n"
                "2. Create maximum 6 high-level categories.\n"
                "3. Categories: Identity, Criminal History, Associates, Legal Status, etc.\n"
                "4. Each child must be a complete factual statement.\n"
                "Return ONLY valid JSON: { \"label\": \"Name\", \"children\": [...] }"
            ),
            ("human", "Subject: {person}\nIntelligence Text:\n{context}")
        ])
        
        if self.llm:
            self.mindmap_chain = self.mindmap_prompt | self.llm | StrOutputParser()
```

#### 2. Main Generation Function (Lines 140-170)

```python
def generate_mind_map(self, full_text: str, title: Optional[str] = None) -> Dict:
    """Main API to generate mind map from text"""
    person = title or self.detect_main_person(full_text)

    # If no LLM configured, use fallback
    if not self.llm:
        return self.fallback_mindmap(person, full_text)

    try:
        # Call LLM with prompt
        raw = self.mindmap_chain.invoke({
            "person": person,
            "context": full_text[:12000]  # Limit to 12k chars
        })

        # Parse JSON response
        mind_map = self.safe_json_load(raw)
        
        # Remove duplicates
        mind_map = self.deduplicate_mindmap(mind_map)
        
        return mind_map

    except Exception as e:
        logger.warning(f"⚠️ LLM failed, using fallback: {e}")
        return self.fallback_mindmap(person, full_text)
```

#### 3. Fallback Rule-Based Parser (Lines 95-135)

```python
def fallback_mindmap(self, person: str, text: str) -> Dict:
    """Generate rule-based mind map when LLM fails"""
    
    # Extract incidents using regex
    incident_pattern = r'(\d+(?:ST|ND|RD|TH)?\s*INCIDENT)'
    incident_matches = list(re.finditer(incident_pattern, text, re.IGNORECASE))
    
    children = []
    
    if incident_matches:
        incidents = []
        for i, match in enumerate(incident_matches[:10]):
            start = match.start()
            end = incident_matches[i+1].start() if i+1 < len(incident_matches) else len(text)
            incident_text = text[start:end].strip()
            
            # Extract FIR, dates, etc.
            facts = []
            fir_match = re.search(r'FIR\s*NO[.:]?\s*(\d+/\d+)', incident_text)
            if fir_match:
                facts.append({"label": f"FIR: {fir_match.group(1)}"})
            
            incidents.append({"label": incident_title, "children": facts})
        
        children.append({"label": "Criminal Incidents", "children": incidents})
    
    return {"label": person, "children": children}
```

---

## Data Structure

### MindMapNode (Pydantic Model)

```python
class MindMapNode(BaseModel):
    id: str                              # Unique identifier
    label: str                           # Display text
    type: str                            # 'root', 'main', 'sub', 'detail'
    children: Optional[List['MindMapNode']] = None  # Nested nodes
```

### Example Tree Structure

```
Root (notebook name)
├── Main (source 1)
│   ├── Sub (category 1)
│   │   ├── Detail (fact 1)
│   │   └── Detail (fact 2)
│   └── Sub (category 2)
│       └── Detail (fact 3)
└── Main (source 2)
    └── Sub (category 1)
        └── Detail (fact 1)
```

### Node Types & Colors

| Type   | Level | Color Scheme | Example |
|--------|-------|--------------|---------|
| root   | 0     | Indigo/Purple gradient | Notebook name |
| main   | 1     | Blue/Cyan gradient | Source title |
| sub    | 2     | Purple/Pink gradient | Category (Identity, Criminal History) |
| detail | 3+    | White/Gray | Individual facts |

---

## Code Walkthrough

### Complete Flow Example

**User Action:** Clicks "Mind Map" button

**1. Frontend (StudioColumn.tsx)**
```typescript
onClick: () => setMindMapOpen(true)
```

**2. Frontend (MindMapDialog.tsx)**
```typescript
useEffect(() => {
  if (open && !mindMapData) {
    generateMindMap()  // Triggers API call
  }
}, [open])
```

**3. Frontend API Call**
```typescript
const response = await fetch(`/api/notebooks/${notebookId}/mindmap`, {
  method: 'POST',
})
```

**4. Backend (notebooks.py)**
```python
@router.post("/notebooks/{notebook_id}/mindmap")
async def generate_mindmap(notebook_id: str):
    # Get notebook
    notebook = await Notebook.get(notebook_id)
    
    # Get sources
    sources = await notebook.get_sources()
    
    # Initialize AI engine
    engine = MindMapEngine(llm=llm)
    
    # Generate mind map
    for source in sources:
        ai_mindmap = engine.generate_mind_map(source.full_text, source.title)
        # Convert and add to tree
    
    # Return response
    return MindMapResponse(root=root)
```

**5. AI Engine (mindmap_engine.py)**
```python
def generate_mind_map(self, full_text: str, title: str) -> Dict:
    # Call LLM
    raw = self.mindmap_chain.invoke({
        "person": title,
        "context": full_text[:12000]
    })
    
    # Parse JSON
    mind_map = self.safe_json_load(raw)
    
    # Return structure
    return mind_map
```

**6. Backend Response**
```json
{
  "notebook_id": "...",
  "notebook_name": "...",
  "root": {
    "id": "root",
    "label": "Notebook Name",
    "type": "root",
    "children": [...]
  }
}
```

**7. Frontend Rendering**
```typescript
setMindMapData(data.root)
// Renders tree with renderNode() function
```

**8. User Interaction**
```typescript
onClick={() => toggleNode(node.id)}
// Expands/collapses node
```

---

## Key Files Summary

| File | Purpose | Lines |
|------|---------|-------|
| `StudioColumn.tsx` | Mind Map button | ~75 |
| `MindMapDialog.tsx` | Dialog UI & API call | 1-250 |
| `api/routers/notebooks.py` | Backend endpoint | 350-455 |
| `open_notebook/utils/mindmap_engine.py` | AI engine | 1-200 |
| `open_notebook/ai/provision.py` | LLM loader | 1-60 |

---

## Testing the Feature

### 1. Check Backend Logs
```bash
# Look for these logs in backend terminal:
MINDMAP: Starting AI mind map generation for notebook ...
MINDMAP: Found notebook 'sss'
MINDMAP: Found 2 sources
MINDMAP: Source 'testing purpose' has 9243 chars
✅ Using AI-powered mind map generation
MINDMAP: Processing source 1/2: 'testing purpose'
✅ Generated AI mind map with 6 categories
MINDMAP: Successfully generated AI-powered mind map!
```

### 2. Check Network Tab
```
Request: POST http://localhost:5055/api/notebooks/notebook:kuo7qmjwlrbllbpxw4lm/mindmap
Response: 200 OK
Body: { "notebook_id": "...", "root": {...} }
```

### 3. Check Console
```javascript
// Should see in browser console:
Mind map data received: { notebook_id: "...", root: {...} }
```

---

## Troubleshooting

### Issue: "Failed to generate mind map"
**Solution:** Check backend logs for detailed error

### Issue: Empty mind map
**Solution:** Verify sources have `full_text` field populated

### Issue: LLM timeout
**Solution:** Reduce content size or use fallback mode

### Issue: Nodes not expanding
**Solution:** Check `expandedNodes` state in React DevTools

---

## Summary

The Mind Map feature is a complete AI-powered visualization system:

1. **Frontend** handles UI, user interaction, and API calls
2. **Backend** orchestrates data fetching and AI processing
3. **AI Engine** analyzes content and generates intelligent hierarchies
4. **Database** stores source content and relationships

The system is resilient with fallback mechanisms and provides a smooth user experience with loading states, animations, and interactive controls.
