from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from loguru import logger

from api.models import (
    NotebookCreate,
    NotebookDeletePreview,
    NotebookDeleteResponse,
    NotebookResponse,
    NotebookUpdate,
)
from open_notebook.database.repository import ensure_record_id, repo_query
from open_notebook.domain.notebook import Notebook, Source
from open_notebook.exceptions import InvalidInputError

router = APIRouter()


@router.get("/notebooks", response_model=List[NotebookResponse])
async def get_notebooks(
    archived: Optional[bool] = Query(None, description="Filter by archived status"),
    order_by: str = Query("updated desc", description="Order by field and direction"),
):
    """Get all notebooks with optional filtering and ordering."""
    try:
        # Build the query with counts
        query = f"""
            SELECT *,
            count(<-reference.in) as source_count,
            count(<-artifact.in) as note_count
            FROM notebook
            ORDER BY {order_by}
        """

        result = await repo_query(query)

        # Filter by archived status if specified
        if archived is not None:
            result = [nb for nb in result if nb.get("archived") == archived]

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
            status_code=500, detail=f"Error fetching notebooks: {str(e)}"
        )


@router.post("/notebooks", response_model=NotebookResponse)
async def create_notebook(notebook: NotebookCreate):
    """Create a new notebook."""
    try:
        new_notebook = Notebook(
            name=notebook.name,
            description=notebook.description,
        )
        await new_notebook.save()

        return NotebookResponse(
            id=new_notebook.id or "",
            name=new_notebook.name,
            description=new_notebook.description,
            archived=new_notebook.archived or False,
            created=str(new_notebook.created),
            updated=str(new_notebook.updated),
            source_count=0,  # New notebook has no sources
            note_count=0,  # New notebook has no notes
        )
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating notebook: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error creating notebook: {str(e)}"
        )


@router.get(
    "/notebooks/{notebook_id}/delete-preview", response_model=NotebookDeletePreview
)
async def get_notebook_delete_preview(notebook_id: str):
    """Get a preview of what will be deleted when this notebook is deleted."""
    try:
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        preview = await notebook.get_delete_preview()

        return NotebookDeletePreview(
            notebook_id=str(notebook.id),
            notebook_name=notebook.name,
            note_count=preview["note_count"],
            exclusive_source_count=preview["exclusive_source_count"],
            shared_source_count=preview["shared_source_count"],
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting delete preview for notebook {notebook_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching notebook deletion preview: {str(e)}",
        )


@router.get("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def get_notebook(notebook_id: str):
    """Get a specific notebook by ID."""
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
        raise HTTPException(
            status_code=500, detail=f"Error fetching notebook: {str(e)}"
        )


@router.put("/notebooks/{notebook_id}", response_model=NotebookResponse)
async def update_notebook(notebook_id: str, notebook_update: NotebookUpdate):
    """Update a notebook."""
    try:
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        # Update only provided fields
        if notebook_update.name is not None:
            notebook.name = notebook_update.name
        if notebook_update.description is not None:
            notebook.description = notebook_update.description
        if notebook_update.archived is not None:
            notebook.archived = notebook_update.archived

        await notebook.save()

        # Query with counts after update
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

        # Fallback if query fails
        return NotebookResponse(
            id=notebook.id or "",
            name=notebook.name,
            description=notebook.description,
            archived=notebook.archived or False,
            created=str(notebook.created),
            updated=str(notebook.updated),
            source_count=0,
            note_count=0,
        )
    except HTTPException:
        raise
    except InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating notebook {notebook_id}: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error updating notebook: {str(e)}"
        )


@router.post("/notebooks/{notebook_id}/sources/{source_id}")
async def add_source_to_notebook(notebook_id: str, source_id: str):
    """Add an existing source to a notebook (create the reference)."""
    try:
        # Check if notebook exists
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        # Check if source exists
        source = await Source.get(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")

        # Check if reference already exists (idempotency)
        existing_ref = await repo_query(
            "SELECT * FROM reference WHERE out = $source_id AND in = $notebook_id",
            {
                "notebook_id": ensure_record_id(notebook_id),
                "source_id": ensure_record_id(source_id),
            },
        )

        # If reference doesn't exist, create it
        if not existing_ref:
            await repo_query(
                "RELATE $source_id->reference->$notebook_id",
                {
                    "notebook_id": ensure_record_id(notebook_id),
                    "source_id": ensure_record_id(source_id),
                },
            )

        return {"message": "Source linked to notebook successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error linking source {source_id} to notebook {notebook_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"Error linking source to notebook: {str(e)}"
        )


@router.delete("/notebooks/{notebook_id}/sources/{source_id}")
async def remove_source_from_notebook(notebook_id: str, source_id: str):
    """Remove a source from a notebook (delete the reference)."""
    try:
        # Check if notebook exists
        notebook = await Notebook.get(notebook_id)
        if not notebook:
            raise HTTPException(status_code=404, detail="Notebook not found")

        # Delete the reference record linking source to notebook
        await repo_query(
            "DELETE FROM reference WHERE out = $notebook_id AND in = $source_id",
            {
                "notebook_id": ensure_record_id(notebook_id),
                "source_id": ensure_record_id(source_id),
            },
        )

        return {"message": "Source removed from notebook successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Error removing source {source_id} from notebook {notebook_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"Error removing source from notebook: {str(e)}"
        )


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
        raise HTTPException(
            status_code=500, detail=f"Error deleting notebook: {str(e)}"
        )


# Mind Map endpoint
from pydantic import BaseModel
from typing import List, Optional


class MindMapNode(BaseModel):
    """Mind map node structure."""
    id: str
    label: str
    type: str  # 'root', 'main', 'sub'
    children: Optional[List['MindMapNode']] = None


class MindMapResponse(BaseModel):
    """Mind map response."""
    notebook_id: str
    notebook_name: str
    root: MindMapNode


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
                else:
                    logger.warning(f"MINDMAP: Source '{source.title}' has no full_text")
            except Exception as e:
                logger.error(f"MINDMAP: Error fetching full_text for source {source.id}: {e}")
        
        if not sources:
            logger.info("MINDMAP: No sources found, returning empty mind map")
            return MindMapResponse(
                notebook_id=notebook_id,
                notebook_name=notebook.name,
                root=MindMapNode(id="root", label=notebook.name, type="root", children=[])
            )
        
        # Import AI mind map engine
        from open_notebook.utils.mindmap_engine import MindMapEngine
        from open_notebook.ai.provision import provision_langchain_model
        
        # Initialize engine with LLM
        try:
            llm = await provision_langchain_model(
                content="",  # Empty content for default model
                model_id=None,
                default_type="chat"
            )
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
                logger.warning(f"MINDMAP: No content for source '{source.title}'")
                main_topics.append(MindMapNode(
                    id=f"source_{source.id}",
                    label=source.title or "Untitled",
                    type="main",
                    children=[MindMapNode(
                        id=f"info_{source.id}",
                        label="No content available",
                        type="sub"
                    )]
                ))
                continue
            
            # Generate AI mind map for this source
            try:
                ai_mindmap = engine.generate_mind_map(
                    full_text=source.full_text,
                    title=source.title
                )
                
                # Convert AI mind map to our node structure
                def convert_to_nodes(data: dict, parent_id: str, level: int = 0) -> MindMapNode:
                    """Recursively convert AI mind map to MindMapNode structure"""
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
                    label=ai_mindmap.get("label", source.title or "Untitled"),
                    type="main",
                    children=[
                        convert_to_nodes(child, f"source_{source.id}", level=1)
                        for child in ai_mindmap.get("children", [])
                    ] if ai_mindmap.get("children") else None
                )
                
                main_topics.append(source_node)
                logger.info(f"✅ Generated AI mind map for '{source.title}' with {len(ai_mindmap.get('children', []))} categories")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate AI mind map for '{source.title}': {e}")
                logger.exception(e)
                # Fallback to simple preview
                preview = source.full_text[:200].replace('\n', ' ')
                main_topics.append(MindMapNode(
                    id=f"source_{source.id}",
                    label=source.title or "Untitled",
                    type="main",
                    children=[MindMapNode(
                        id=f"content_{source.id}",
                        label=preview,
                        type="sub"
                    )]
                ))
        
        root = MindMapNode(
            id="root",
            label=notebook.name,
            type="root",
            children=main_topics
        )
        
        logger.info("MINDMAP: Successfully generated AI-powered mind map!")
        logger.info("=" * 80)
        
        return MindMapResponse(
            notebook_id=notebook_id,
            notebook_name=notebook.name,
            root=root
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MINDMAP: Fatal error generating mind map: {e}")
        logger.exception(e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate mind map: {str(e)}"
        )


# Update forward refs for nested model
MindMapNode.model_rebuild()
