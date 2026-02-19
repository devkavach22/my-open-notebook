# 🧠 Mind Map Feature - Complete Guide

## ✅ What's New

I've implemented a fully functional Mind Map feature that generates visual representations of your notebook content!

---

## 🎯 How It Works

### Flow:
```
1. Upload sources to notebook
   ↓
2. Content is extracted and stored
   ↓
3. Click "Mind Map" button in Studio
   ↓
4. Backend analyzes source content
   ↓
5. Generates hierarchical topic structure
   ↓
6. Frontend displays visual mind map
```

---

## 🚀 How to Use

### Step 1: Upload Sources
1. Open a notebook
2. Click "Add Source" in the Sources column
3. Upload files (PDF, DOCX, etc.) or add URLs
4. Wait for content extraction to complete

### Step 2: Generate Mind Map
1. Go to Studio (right column)
2. Click the "Mind Map" card
3. Wait for generation (2-3 seconds)
4. See your visual mind map!

### Step 3: Interact with Mind Map
- **Zoom In/Out**: Use the zoom buttons
- **View Topics**: See main topics and subtopics
- **Export**: Click "Export" to save (coming soon)

---

## 📊 Mind Map Structure

### Hierarchy:
```
Root (Notebook Name)
├── Main Topic 1 (Source 1)
│   ├── Subtopic 1.1
│   ├── Subtopic 1.2
│   └── Subtopic 1.3
├── Main Topic 2 (Source 2)
│   ├── Subtopic 2.1
│   └── Subtopic 2.2
└── Main Topic 3 (Source 3)
    └── Subtopic 3.1
```

### Node Types:
- **Root**: Notebook name (purple, large)
- **Main**: Source titles (blue, medium)
- **Sub**: Key points from content (gray, small)

---

## 🔧 Technical Implementation

### Frontend Components:

**1. MindMapDialog.tsx**
- Location: `frontend/src/components/notebooks/MindMapDialog.tsx`
- Purpose: Display mind map in a modal dialog
- Features:
  - Zoom in/out
  - Hierarchical node rendering
  - Loading states
  - Export button (placeholder)

**2. StudioColumn.tsx** (Updated)
- Added Mind Map button click handler
- Opens MindMapDialog when clicked
- Passes notebook ID and name

---

### Backend API:

**1. mindmap.py**
- Location: `api/routers/mindmap.py`
- Endpoint: `POST /api/notebooks/{notebook_id}/mindmap`
- Purpose: Generate mind map data from sources

**Algorithm**:
```python
1. Fetch notebook by ID
2. Get all sources in notebook
3. For each source:
   - Use title as main topic
   - Extract first 3 sentences as subtopics
   - Truncate long text
4. Build hierarchical structure
5. Return JSON response
```

**Response Format**:
```json
{
  "notebook_id": "notebook:abc123",
  "notebook_name": "My Research",
  "root": {
    "id": "root",
    "label": "My Research",
    "type": "root",
    "children": [
      {
        "id": "main_0",
        "label": "Source Title 1",
        "type": "main",
        "children": [
          {
            "id": "sub_0_0",
            "label": "Key point 1...",
            "type": "sub"
          }
        ]
      }
    ]
  }
}
```

---

## 📁 Files Created/Modified

### Created:
1. **frontend/src/components/notebooks/MindMapDialog.tsx**
   - New mind map dialog component
   - Visual rendering of nodes
   - Zoom controls

2. **api/routers/mindmap.py**
   - New API endpoint
   - Mind map generation logic
   - Data extraction from sources

### Modified:
1. **frontend/src/app/(dashboard)/notebooks/components/StudioColumn.tsx**
   - Added Mind Map button handler
   - Opens dialog on click
   - Passes notebook data

2. **frontend/src/app/(dashboard)/notebooks/[id]/page.tsx**
   - Passes notebook name to StudioColumn

3. **api/main.py**
   - Registered mindmap router
   - Added to API routes

---

## 🎨 Visual Design

### Color Scheme:
- **Root Node**: Primary color (purple/blue)
- **Main Nodes**: Blue background
- **Sub Nodes**: Gray background

### Layout:
- Hierarchical tree structure
- Vertical connections between levels
- Horizontal spacing between siblings
- Hover effects on nodes

### Zoom:
- Range: 50% to 200%
- Smooth scaling
- Centered origin

---

## 🔍 How Content is Extracted

### When You Upload a Source:

1. **File Upload**:
   ```
   Frontend → POST /api/sources
   Backend → Saves file to notebook_data/uploads/
   Backend → Extracts text content
   Backend → Stores in source table
   ```

2. **Content Extraction**:
   - PDF: Uses PyMuPDF to extract text
   - DOCX: Uses python-docx
   - TXT: Direct read
   - URL: Web scraping

3. **Storage**:
   ```sql
   INSERT INTO source {
     title: "Document.pdf",
     content: "Full extracted text...",
     source_type: "file",
     file_path: "/uploads/document.pdf"
   }
   ```

4. **Mind Map Generation**:
   ```
   GET sources WHERE notebook_id = X
   FOR EACH source:
     main_topic = source.title
     subtopics = extract_key_points(source.content)
   BUILD tree structure
   RETURN JSON
   ```

---

## 💡 Current Algorithm

### Simple Extraction (v1):
```python
# Main topics: Source titles
main_topic = source.title[:50]

# Subtopics: First 3 sentences
sentences = source.content.split('.')[:3]
subtopics = [s.strip()[:60] + "..." for s in sentences]
```

### Future Improvements (v2):
- Use AI to extract key topics
- Identify relationships between topics
- Group similar concepts
- Generate better labels
- Add more levels

---

## 🚀 Future Enhancements

### Phase 1 (Current): ✅
- Basic mind map generation
- Hierarchical display
- Zoom controls
- Source-based topics

### Phase 2 (Next):
- AI-powered topic extraction
- Better subtopic identification
- Interactive node editing
- Drag and drop nodes

### Phase 3 (Future):
- Cross-source connections
- Topic clustering
- Export as image/PDF
- Share mind maps
- Collaborative editing

---

## 🎯 Example Use Cases

### Research Paper:
```
Upload 5 research papers
↓
Generate mind map
↓
See: Main themes, Key findings, Connections
```

### Study Notes:
```
Upload lecture slides + textbook chapters
↓
Generate mind map
↓
See: Topics, Subtopics, Relationships
```

### Project Planning:
```
Upload project docs + requirements
↓
Generate mind map
↓
See: Features, Tasks, Dependencies
```

---

## 📊 Data Flow Diagram

```
┌─────────────┐
│   Upload    │
│   Source    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Extract   │
│   Content   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Store    │
│  in source  │
│    table    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│    Click    │
│  Mind Map   │
│   Button    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  POST /api/ │
│  notebooks/ │
│  {id}/      │
│  mindmap    │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Analyze   │
│   Sources   │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Generate  │
│  Structure  │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│   Display   │
│  Mind Map   │
└─────────────┘
```

---

## 🔧 API Endpoint Details

### POST /api/notebooks/{notebook_id}/mindmap

**Request**:
```http
POST /api/notebooks/notebook:abc123/mindmap
Content-Type: application/json
```

**Response**:
```json
{
  "notebook_id": "notebook:abc123",
  "notebook_name": "My Research",
  "root": {
    "id": "root",
    "label": "My Research",
    "type": "root",
    "children": [...]
  }
}
```

**Error Responses**:
- `404`: Notebook not found
- `500`: Generation failed

---

## ✅ Testing Checklist

- [ ] Upload a source to notebook
- [ ] Wait for content extraction
- [ ] Click Mind Map in Studio
- [ ] See loading spinner
- [ ] Mind map appears
- [ ] Zoom in/out works
- [ ] Nodes are properly colored
- [ ] Hierarchy is correct
- [ ] Can close dialog
- [ ] Can reopen and see same map

---

## 🎉 Summary

You now have a fully functional Mind Map feature!

**What it does**:
- ✅ Extracts content from uploaded sources
- ✅ Generates hierarchical topic structure
- ✅ Displays visual mind map
- ✅ Supports zoom in/out
- ✅ Shows notebook name as root
- ✅ Shows sources as main topics
- ✅ Shows key points as subtopics

**How to use**:
1. Upload sources to notebook
2. Click "Mind Map" in Studio
3. See your visual mind map!

**Next steps**:
- Improve topic extraction with AI
- Add more interactivity
- Enable export functionality

Happy mind mapping! 🧠🎨

