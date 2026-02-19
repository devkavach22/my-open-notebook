"""Middleware for authentication and user context."""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from open_notebook.utils.auth_utils import decode_access_token


class UserContextMiddleware(BaseHTTPMiddleware):
    """Middleware to extract user_id from JWT token and add to request state."""
    
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        public_paths = [
            "/api/auth/signup",
            "/api/auth/login",
            "/api/auth/forgot-password",
            "/api/auth/reset-password",
            "/api/auth/verify-email",
            "/api/auth/status",
            "/docs",
            "/redoc",
            "/openapi.json",
        ]
        
        # Check if path is public
        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
            # Decode token
            payload = decode_access_token(token)
            
            if payload:
                user_id = payload.get("sub")
                if user_id:
                    # Add user_id to request state
                    request.state.user_id = user_id
                    logger.debug(f"User {user_id} authenticated")
                else:
                    logger.warning("Token missing 'sub' claim")
            else:
                logger.warning("Invalid or expired token")
        
        # Continue with request
        response = await call_next(request)
        return response


def get_current_user_id(request: Request) -> str:
    """Get current user ID from request state."""
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user_id
