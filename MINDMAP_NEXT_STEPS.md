# Mind Map - Next Steps

## Current Status
❌ Backend endpoint has corrupted/duplicate code
❌ Need to clean up and rewrite
✅ Data is available (`full_text` field has content)
✅ Frontend UI component exists

## What Needs to Be Done

### Step 1: Clean Up Backend File
The `api/routers/notebooks.py` file has duplicate code starting around line 450. Need to:
1. Remove all duplicate/old mindmap code
2. Keep only the clean version (lines 350-450)
3. Test the endpoint

### Step 2: Enable Mind Map in Frontend
In `frontend/src/app/(dashboard)/notebooks/components/StudioColumn.tsx`:
- Change Mind Map button from "coming soon" alert back to opening the dialog
- Import and use MindMapDialog component

### Step 3: Test Basic Functionality
1. Click Mind Map button
2. Verify it fetches data from backend
3. Check if incidents are detected and displayed

### Step 4: Enhance Parsing
Add better content parsing for criminal cases:
- Extract FIR numbers
- Extract dates
- Extract locations
- Extract people names
- Group by incident type

### Step 5: Make Nodes Clickable
Add click handlers to expand/collapse nodes dynamically

## Quick Fix Commands

To clean up the backend file, you can manually:
1. Open `api/routers/notebooks.py`
2. Find line ~450 where duplicate code starts
3. Delete everything from there until line ~537
4. Keep only the `MindMapNode.model_rebuild()` line at the end

Or restart from scratch with a clean implementation.

## Recommendation

Due to the corrupted file and token limits, I recommend:
1. **Start a fresh conversation** focused only on Mind Map
2. I'll provide a clean, working implementation
3. We'll test it step by step
4. Then enhance with AI-powered parsing

This will be much cleaner than trying to fix the corrupted file in this conversation.
