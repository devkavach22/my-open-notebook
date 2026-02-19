"""User service for authentication and user management."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from loguru import logger

from open_notebook.database.repository import repo_query, ensure_record_id
from open_notebook.domain.user import User, UserCreate, UserResponse
from open_notebook.utils.auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    generate_reset_token,
    generate_verification_token,
)


async def create_user(user_data: UserCreate) -> User:
    """Create a new user."""
    # Check if user already exists
    existing_user = await repo_query(
        "SELECT * FROM user WHERE email = $email OR username = $username",
        {"email": user_data.email, "username": user_data.username}
    )
    
    if existing_user:
        if existing_user[0].get("email") == user_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            raise HTTPException(status_code=400, detail="Username already taken")
    
    # Hash password
    hashed_password = hash_password(user_data.password)
    
    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        verification_token=generate_verification_token(),
    )
    
    await user.save()
    logger.info(f"Created new user: {user.email}")
    
    return user


async def authenticate_user(email_or_username: str, password: str) -> Optional[User]:
    """Authenticate a user with email/username and password."""
    # Try to find user by email or username
    result = await repo_query(
        "SELECT * FROM user WHERE email = $identifier OR username = $identifier",
        {"identifier": email_or_username}
    )
    
    if not result:
        return None
    
    user_data = result[0]
    user = User(**user_data)
    
    if not verify_password(password, user.hashed_password):
        return None
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is disabled")
    
    # Update last login
    user.last_login = datetime.utcnow()
    await user.save()
    
    return user


async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    result = await repo_query(
        "SELECT * FROM user WHERE email = $email",
        {"email": email}
    )
    
    if not result:
        return None
    
    return User(**result[0])


async def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID."""
    user = await User.get(user_id)
    return user


async def initiate_password_reset(email: str) -> Optional[str]:
    """Initiate password reset process."""
    user = await get_user_by_email(email)
    
    if not user:
        # Don't reveal if email exists
        logger.warning(f"Password reset requested for non-existent email: {email}")
        return None
    
    # Generate reset token
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
    await user.save()
    
    logger.info(f"Password reset initiated for user: {email}")
    return reset_token


async def reset_password(token: str, new_password: str) -> bool:
    """Reset password using token."""
    result = await repo_query(
        "SELECT * FROM user WHERE reset_token = $token",
        {"token": token}
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user = User(**result[0])
    
    # Check if token is expired
    if user.reset_token_expires and user.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Reset token has expired")
    
    # Update password
    user.hashed_password = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    await user.save()
    
    logger.info(f"Password reset completed for user: {user.email}")
    return True


async def change_password(user_id: str, current_password: str, new_password: str) -> bool:
    """Change user password."""
    user = await get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify current password
    if not verify_password(current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    user.hashed_password = hash_password(new_password)
    user.updated_at = datetime.utcnow()
    await user.save()
    
    logger.info(f"Password changed for user: {user.email}")
    return True


async def verify_email(token: str) -> bool:
    """Verify user email with token."""
    result = await repo_query(
        "SELECT * FROM user WHERE verification_token = $token",
        {"token": token}
    )
    
    if not result:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user = User(**result[0])
    user.is_verified = True
    user.verification_token = None
    await user.save()
    
    logger.info(f"Email verified for user: {user.email}")
    return True


def user_to_response(user: User) -> UserResponse:
    """Convert User model to UserResponse."""
    return UserResponse(
        id=str(user.id),
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=str(user.created_at),
        last_login=str(user.last_login) if user.last_login else None,
    )
