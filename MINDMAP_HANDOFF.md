# Mind Map Feature - Implementation Handoff

## Context Summary

### Project: Open Notebook (NotebookLM-style app)
- **Location**: `C:\Users\hemanshi.l\Desktop\open-notebook`
- **Stack**: Python/FastAPI backend, Next.js frontend, SurrealDB database
- **User**: Hemanshi, Windows environment

### What We Accomplished
1. ✅ Redesigned notebook layout to Sources-Chat-Studio
2. ✅ Created Studio section with 9 feature cards
3. ✅ Set up local development environment (3 terminals)
4. ✅ Created batch files for easy startup
5. ✅ Verified data exists in `source.full_text` field

### Current Issue
- Mind Map button shows "coming soon" alert
- Backend endpoint exists but has corrupted/duplicate code
- Need clean implementation

## Data Available

### Source 1: "testing purpose"
- **ID**: `source:zvqk736988lpm8yzyhae`
- **Content**: 9,243 characters
- **Type**: Criminal case with 15 incidents
- **Structure**: Numbered incidents (1ST INCIDENT, 2ND INCIDENT, etc.)

### Source 2: "Rohit Moi.pdf"
- **ID**: `source:rt82v6ffy57ndz73ffxs`
- **Content**: 17,190 characters
- **Type**: Police dossier with sections
- **Structure**: Sections like "Personal Information", "Previous Cases", etc.

### Database Query Result
```sql
SELECT id, title, full_text FROM source;
```
Returns both sources with complete `full_text` content.

## Goal

Create an interactive mind map like this structure:
```
Notebook Root
├── Source 1: "testing purpose"
│   ├── 1st Incident (clickable)
│   │   ├── Date: Feb 18, 2012
│   │   ├── Location: Jagsi, Sonipat
│   │   ├── People: Ravi, Kapil
│   │   └── FIR: 34/2012
│   ├── 2nd Incident (clickable)
│   │   └── ...
│   └── ...
└── Source 2: "Rohit Moi.pdf"
    ├── Personal Information (clickable)
    ├── Previous Cases (clickable)
    └── ...
```

## Files to Work With

### Backend
- **File**: `api/routers/notebooks.py`
- **Endpoint**: `POST /api/notebooks/{notebook_id}/mindmap`
- **Models**: `MindMapNode`, `MindMapResponse` (already defined around line 335)
- **Issue**: Duplicate code starting around line 450 - needs cleanup

### Frontend
- **Dialog**: `frontend/src/components/notebooks/MindMapDialog.tsx` (exists, working)
- **Button**: `frontend/src/app/(dashboard)/notebooks/components/StudioColumn.tsx` (line ~75)
- **Current**: Shows alert("Mind Map feature coming soon!")
- **Need**: Change to `setMindMapOpen(true)` and re-enable dialog

## Implementation Steps

### Step 1: Clean Backend (Priority 1)
1. Open `api/routers/notebooks.py`
2. Find the mindmap function (starts line 350)
3. Remove duplicate code (lines ~450-537)
4. Keep only clean implementation:
   ```python
   @router.post("/notebooks/{notebook_id}/mindmap")
   async def generate_mindmap(notebook_id: str):
       # Get notebook
       # Get sources with full_text
       # Parse incidents using regex
       # Return hierarchical structure
   ```

### Step 2: Parse Criminal Case Content
Use regex to find incidents:
```python
import re
incident_pattern = r'(\d+(?:ST|ND|RD|TH)?\s*INCIDENT)'
matches = re.finditer(incident_pattern, text, re.IGNORECASE)
```

For each incident, extract:
- Date (regex: `\d{2}/\d{2}/\d{4}` or `\d{2}\.\d{2}\.\d{4}`)
- FIR number (regex: `FIR NO[.:]?\s*(\d+/\d+)`)
- Location (look for village/city names)
- People (capitalized names)

### Step 3: Enable Frontend
In `StudioColumn.tsx`, change:
```typescript
// FROM:
onClick: () => {
  alert('Mind Map feature coming soon!')
}

// TO:
onClick: () => {
  setMindMapOpen(true)
}
```

And add back:
```typescript
const [mindMapOpen, setMindMapOpen] = useState(false)
```

And at the end:
```typescript
<MindMapDialog
  open={mindMapOpen}
  onOpenChange={setMindMapOpen}
  notebookId={notebookId}
  notebookName={notebookName}
/>
```

### Step 4: Test
1. Start services (database, backend, frontend)
2. Navigate to notebook: `http://localhost:3000/notebooks/notebook:kuo7qmjwlrbllbpxw4lm`
3. Click "Mind Map" button in Studio section
4. Verify dialog opens and shows data

### Step 5: Enhance (Optional)
- Add more detail extraction (dates, locations, people)
- Add search/filter functionality
- Add export to image/PDF
- Add AI-powered summarization

## Key Code Snippets

### Backend: Simple Incident Parser
```python
def parse_incidents(text: str, source_id: str) -> List[MindMapNode]:
    incidents = []
    pattern = r'(\d+(?:ST|ND|RD|TH)?\s*INCIDENT)'
    matches = list(re.finditer(pattern, text, re.IGNORECASE))
    
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        incident_text = text[start:end].strip()
        
        # Extract first 100 chars as label
        label = incident_text[:100].replace('\n', ' ')
        
        incident_node = MindMapNode(
            id=f"incident_{source_id}_{i}",
            label=label,
            type="sub",
            children=[]
        )
        incidents.append(incident_node)
    
    return incidents
```

### Frontend: Node Click Handler
```typescript
const handleNodeClick = (nodeId: string) => {
  const newExpanded = new Set(expandedNodes)
  if (newExpanded.has(nodeId)) {
    newExpanded.delete(nodeId)
  } else {
    newExpanded.add(nodeId)
  }
  setExpandedNodes(newExpanded)
}
```

## Testing Data

### Test Notebook
- **ID**: `notebook:kuo7qmjwlrbllbpxw4lm`
- **Name**: "sss"
- **Sources**: 2 (both have full_text)

### Test API Call
```bash
curl -X POST http://localhost:5055/api/notebooks/notebook:kuo7qmjwlrbllbpxw4lm/mindmap
```

Expected response:
```json
{
  "notebook_id": "notebook:kuo7qmjwlrbllbpxw4lm",
  "notebook_name": "sss",
  "root": {
    "id": "root",
    "label": "sss",
    "type": "root",
    "children": [...]
  }
}
```

## Important Notes

1. **Data is ready**: `full_text` field has complete content
2. **UI exists**: MindMapDialog component is already built
3. **Main work**: Clean backend code and parse incidents intelligently
4. **User wants**: Clickable nodes that expand/collapse to show details
5. **Content type**: Criminal case documents with numbered incidents

## Success Criteria

✅ Mind Map button opens dialog
✅ Dialog shows notebook name as root
✅ Each source appears as main node
✅ Incidents are parsed and shown as sub-nodes
✅ Nodes are clickable (expand/collapse)
✅ Zoom in/out works
✅ No errors in console

## Next Session Goals

1. Clean up corrupted backend code (15 min)
2. Implement incident parsing (30 min)
3. Test with real data (15 min)
4. Add detail extraction (30 min)
5. Polish UI interactions (30 min)

**Total estimated time**: 2 hours

Good luck! The foundation is solid, just needs clean implementation.
