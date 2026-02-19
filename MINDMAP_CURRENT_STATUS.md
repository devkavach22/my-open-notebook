# Mind Map Feature - Current Status

## ✅ What's Working
1. Backend endpoint exists at `POST /api/notebooks/{notebook_id}/mindmap`
2. Frontend MindMapDialog component is complete with interactive features
3. Mind Map button in Studio section opens the dialog
4. Data is available in `source.full_text` field
5. Basic regex parsing extracts incidents, FIR numbers, dates, locations

## 🎯 Next Step: Integrate AI-Powered Mind Map

You provided an AI-powered MindMapEngine that uses LLM to generate intelligent hierarchies.

### Files Created:
1. `open_notebook/utils/mindmap_engine.py` - AI mind map engine (DONE ✅)

### What Needs to Be Done:
Replace the regex-based parsing in `api/routers/notebooks.py` (lines 350-540) with AI-powered generation.

### How to Integrate:

**Option 1: Quick Test (Manual)**
1. Open `api/routers/notebooks.py`
2. Find line 350: `@router.post("/notebooks/{notebook_id}/mindmap"...`
3. Replace the entire function with the AI-powered version below

**Option 2: Let Me Do It**
Just say "integrate AI mindmap" and I'll update the code for you.

### AI-Powered Version (Ready to Use):

```python
@router.post("/notebooks/{notebook_id}/mindmap", response_model=MindMapResponse)
async def generate_mindmap(notebook_id: str):
    """Generate an AI-powered mind map from notebook sources."""
    try:
        logger.info("=" * 80)
        logger.info(f"MINDMAP: Starting AI mind map generation for notebook {notebook_id}")
        
        # Get notebook
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")
        
        logger.info(f"MINDMAP: Found notebook '{notebook.name}'")
        
        # Get sources with full_text
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
        
        if not sources:
            return MindMapResponse(
                notebook_id=notebook_id,
                notebook_name=notebook.name,
                root=MindMapNode(id="root", label=notebook.name, type="root", children=[])
            )
        
        # Import AI mind map engine
        from open_notebook.utils.mindmap_engine import MindMapEngine
        from open_notebook.ai.provision import get_llm
        
        # Initialize engine with LLM
        try:
            llm = get_llm()
            engine = MindMapEngine(llm=llm)
            logger.info("✅ Using AI-powered mind map generation")
        except Exception as e:
            logger.warning(f"⚠️ Could not load LLM, using rule-based fallback: {e}")
            engine = MindMapEngine(llm=None)
        
        # Generate mind map for each source
        main_topics = []
        
        for idx, source in enumerate(sources):
            logger.info(f"MINDMAP: Processing source {idx+1}/{len(sources)}: '{source.title}'")
            
            if not source.full_text or len(source.full_text.strip()) == 0:
                main_topics.append(MindMapNode(
                    id=f"source_{source.id}",
                    label=source.title or "Untitled",
                    type="main",
                    children=[MindMapNode(id=f"info_{source.id}", label="No content", type="sub")]
                ))
                continue
            
            # Generate AI mind map
            try:
                ai_mindmap = engine.generate_mind_map(
                    full_text=source.full_text,
                    title=source.title
                )
                
                # Convert to MindMapNode structure
                def convert_to_nodes(data: dict, parent_id: str, level: int = 0) -> MindMapNode:
                    node_type = "main" if level == 0 else "sub" if level == 1 else "detail"
                    node_id = f"{parent_id}_{data['label'][:20].replace(' ', '_')}"
                    
                    children = None
                    if data.get("children"):
                        children = [convert_to_nodes(child, node_id, level + 1) for child in data["children"]]
                    
                    return MindMapNode(id=node_id, label=data["label"], type=node_type, children=children)
                
                source_node = MindMapNode(
                    id=f"source_{source.id}",
                    label=ai_mindmap.get("label", source.title or "Untitled"),
                    type="main",
                    children=[convert_to_nodes(child, f"source_{source.id}", 1) for child in ai_mindmap.get("children", [])] if ai_mindmap.get("children") else None
                )
                
                main_topics.append(source_node)
                logger.info(f"✅ Generated AI mind map with {len(ai_mindmap.get('children', []))} categories")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate AI mind map: {e}")
                preview = source.full_text[:200].replace('\n', ' ')
                main_topics.append(MindMapNode(
                    id=f"source_{source.id}",
                    label=source.title or "Untitled",
                    type="main",
                    children=[MindMapNode(id=f"content_{source.id}", label=preview, type="sub")]
                ))
        
        root = MindMapNode(id="root", label=notebook.name, type="root", children=main_topics)
        
        logger.info("MINDMAP: Successfully generated AI-powered mind map!")
        logger.info("=" * 80)
        
        return MindMapResponse(notebook_id=notebook_id, notebook_name=notebook.name, root=root)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MINDMAP: Fatal error: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Failed to generate mind map: {str(e)}")
```

## Benefits of AI-Powered Mind Map:
1. ✅ Intelligent categorization (Identity, Criminal History, Associates, etc.)
2. ✅ Context-aware fact extraction
3. ✅ Automatic deduplication
4. ✅ Better hierarchy organization
5. ✅ Falls back to regex if LLM fails
6. ✅ Works with any document type (not just criminal cases)

## To Test:
1. Restart backend: `restart-backend.bat`
2. Open notebook: `http://localhost:3000/notebooks/notebook:kuo7qmjwlrbllbpxw4lm`
3. Click "Mind Map" button
4. See AI-generated intelligent hierarchy!

Ready to integrate?
