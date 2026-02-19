"""Authentication API routes."""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger

from api.user_service import (
    create_user,
    authenticate_user,
    initiate_password_reset,
    reset_password,
    change_password,
    verify_email,
    get_user_by_id,
    user_to_response,
)
from open_notebook.domain.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    PasswordReset,
    PasswordResetConfirm,
    ChangePassword,
)
from open_notebook.utils.auth_utils import create_access_token, decode_access_token

router = APIRouter()
security = HTTPBearer()


@router.get("/auth/status")
async def auth_status():
    """Check authentication status and configuration."""
    return {
        "auth_enabled": True,
        "auth_required": True,
        "signup_enabled": True,
        "password_reset_enabled": True,
        "email_verification_enabled": False,  # Not implemented yet
        "oauth_providers": [],  # None configured yet
    }


# Dependency to get current user from token
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user from JWT token."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


@router.post("/auth/signup", response_model=dict)
async def signup(user_data: UserCreate):
    """Register a new user."""
    try:
        user = await create_user(user_data)
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_to_response(user),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Error creating user")


@router.post("/auth/login", response_model=dict)
async def login(credentials: UserLogin):
    """Login with email/username and password."""
    try:
        user = await authenticate_user(credentials.email_or_username, credentials.password)
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email/username or password")
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_to_response(user),
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Error during login")


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current user information."""
    return user_to_response(current_user)


@router.post("/auth/forgot-password")
async def forgot_password(data: PasswordReset):
    """Request password reset."""
    try:
        reset_token = await initiate_password_reset(data.email)
        
        # In production, send email with reset link
        # For now, return token (remove this in production!)
        if reset_token:
            logger.info(f"Password reset token: {reset_token}")
            return {
                "message": "If the email exists, a password reset link has been sent",
                "token": reset_token  # Remove this in production!
            }
        
        return {"message": "If the email exists, a password reset link has been sent"}
    except Exception as e:
        logger.error(f"Error during password reset request: {e}")
        raise HTTPException(status_code=500, detail="Error processing request")


@router.post("/auth/reset-password")
async def reset_password_confirm(data: PasswordResetConfirm):
    """Reset password with token."""
    try:
        await reset_password(data.token, data.new_password)
        return {"message": "Password reset successful"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during password reset: {e}")
        raise HTTPException(status_code=500, detail="Error resetting password")


@router.post("/auth/change-password")
async def change_user_password(
    data: ChangePassword,
    current_user = Depends(get_current_user)
):
    """Change password for authenticated user."""
    try:
        await change_password(str(current_user.id), data.current_password, data.new_password)
        return {"message": "Password changed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(status_code=500, detail="Error changing password")


@router.post("/auth/verify-email/{token}")
async def verify_user_email(token: str):
    """Verify user email with token."""
    try:
        await verify_email(token)
        return {"message": "Email verified successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error verifying email: {e}")
        raise HTTPException(status_code=500, detail="Error verifying email")


@router.post("/auth/logout")
async def logout(current_user = Depends(get_current_user)):
    """Logout user (client should delete token)."""
    return {"message": "Logged out successfully"}
