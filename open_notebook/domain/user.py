"""User domain model for authentication and user management."""

from datetime import datetime
from typing import Optional, ClassVar
from pydantic import BaseModel, EmailStr, Field

from open_notebook.domain.base import ObjectModel


class User(ObjectModel):
    """User model for authentication."""
    
    table_name: ClassVar[str] = "user"
    
    email: EmailStr
    username: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None
    verification_token: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Schema for user login."""
    email_or_username: str
    password: str


class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)."""
    id: str
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: str
    last_login: Optional[str] = None


class PasswordReset(BaseModel):
    """Schema for password reset request."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset."""
    token: str
    new_password: str


class ChangePassword(BaseModel):
    """Schema for changing password."""
    current_password: str
    new_password: str
