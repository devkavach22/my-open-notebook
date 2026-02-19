"""Helper functions for filtering data by user."""

from typing import List, Dict, Any, Optional
from fastapi import Request
from loguru import logger

from api.middleware import get_current_user_id


def add_user_filter(request: Request, query: str) -> str:
    """
    Add user_id filter to a SurrealDB query.
    
    Args:
        request: FastAPI request object
        query: Original SurrealDB query
        
    Returns:
        Modified query with user_id filter
    """
    try:
        user_id = get_current_user_id(request)
        
        # If query already has WHERE clause, add AND condition
        if "WHERE" in query.upper():
            query = query.replace("WHERE", f"WHERE user_id = {user_id} AND", 1)
        # If query has ORDER BY, add WHERE before it
        elif "ORDER BY" in query.upper():
            query = query.replace("ORDER BY", f"WHERE user_id = {user_id} ORDER BY", 1)
        # If query has LIMIT, add WHERE before it
        elif "LIMIT" in query.upper():
            query = query.replace("LIMIT", f"WHERE user_id = {user_id} LIMIT", 1)
        # Otherwise, add WHERE at the end
        else:
            # Remove semicolon if present
            query = query.rstrip(';')
            query = f"{query} WHERE user_id = {user_id};"
        
        logger.debug(f"Added user filter to query: {query}")
        return query
        
    except Exception as e:
        logger.warning(f"Could not add user filter: {e}")
        return query


def get_user_id_from_request(request: Request) -> Optional[str]:
    """
    Get user_id from request, returns None if not authenticated.
    
    Args:
        request: FastAPI request object
        
    Returns:
        User ID or None
    """
    try:
        return get_current_user_id(request)
    except:
        return None


def filter_by_user(request: Request, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Filter a list of items by user_id.
    
    Args:
        request: FastAPI request object
        items: List of items to filter
        
    Returns:
        Filtered list
    """
    try:
        user_id = get_current_user_id(request)
        return [item for item in items if item.get('user_id') == user_id]
    except:
        # If no user_id, return all items (backwards compatibility)
        return items
