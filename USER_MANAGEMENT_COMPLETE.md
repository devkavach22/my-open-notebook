# User Management System - Complete Implementation Guide

## 🎯 Overview

I've created a complete user management system with:
- ✅ User Registration (Signup)
- ✅ User Login with JWT tokens
- ✅ Forgot Password
- ✅ Reset Password
- ✅ Change Password
- ✅ Email Verification
- ✅ User Profile Management

## 📁 Files Created

### Backend Files:
1. `open_notebook/domain/user.py` - User model and schemas
2. `open_notebook/utils/auth_utils.py` - Password hashing, JWT tokens
3. `api/user_service.py` - User business logic
4. `api/routers/auth.py` - Authentication API endpoints
5. `open_notebook/database/migrations/14.surrealql` - Database schema
6. `open_notebook/database/migrations/14_down.surrealql` - Rollback migration

### Frontend Files (Need to create):
7. `frontend/src/components/auth/SignupForm.tsx` - Signup UI
8. `frontend/src/components/auth/ForgotPasswordForm.tsx` - Forgot password UI
9. `frontend/src/components/auth/ResetPasswordForm.tsx` - Reset password UI
10. `frontend/src/app/(auth)/signup/page.tsx` - Signup page
11. `frontend/src/app/(auth)/forgot-password/page.tsx` - Forgot password page
12. `frontend/src/app/(auth)/reset-password/page.tsx` - Reset password page

## 🔧 Setup Instructions

### Step 1: Install Dependencies

```bash
# Backend dependencies
pip install bcrypt pyjwt

# Or add to pyproject.toml:
# bcrypt = "^4.0.1"
# pyjwt = "^2.8.0"
```

### Step 2: Run Database Migration

```bash
# Run migration to create user table
python -m open_notebook.database.migrate
```

### Step 3: Register Auth Router

Add to `api/main.py`:

```python
from api.routers import auth

# Add this line with other router includes
app.include_router(auth.router, tags=["auth"])
```

### Step 4: Update Environment Variables

Add to `.env`:

```env
# JWT Secret Key (change this in production!)
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production-use-openssl-rand-hex-32

# JWT Token Expiration (in minutes)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days
```

## 📡 API Endpoints

### 1. Signup
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePassword123!",
  "full_name": "John Doe"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "user:abc123",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-02-19T10:30:00",
    "last_login": null
  }
}
```

### 2. Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": { ... }
}
```

### 3. Get Current User
```http
GET /auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response:
{
  "id": "user:abc123",
  "email": "user@example.com",
  "username": "johndoe",
  ...
}
```

### 4. Forgot Password
```http
POST /auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}

Response:
{
  "message": "If the email exists, a password reset link has been sent",
  "token": "reset_token_here"  // Remove in production!
}
```

### 5. Reset Password
```http
POST /auth/reset-password
Content-Type: application/json

{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePassword123!"
}

Response:
{
  "message": "Password reset successful"
}
```

### 6. Change Password
```http
POST /auth/change-password
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
Content-Type: application/json

{
  "current_password": "OldPassword123!",
  "new_password": "NewPassword123!"
}

Response:
{
  "message": "Password changed successfully"
}
```

### 7. Verify Email
```http
POST /auth/verify-email/{token}

Response:
{
  "message": "Email verified successfully"
}
```

### 8. Logout
```http
POST /auth/logout
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

Response:
{
  "message": "Logged out successfully"
}
```

## 🎨 Frontend Integration

### Using the Auth System

```typescript
// Login
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
})

const data = await response.json()
// Store token in localStorage or cookie
localStorage.setItem('access_token', data.access_token)

// Make authenticated requests
const response = await fetch('/api/notebooks', {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
```

## 🔐 Security Features

1. **Password Hashing**: Uses bcrypt with salt
2. **JWT Tokens**: Secure token-based authentication
3. **Token Expiration**: Tokens expire after 7 days (configurable)
4. **Password Reset**: Secure token-based password reset
5. **Email Verification**: Optional email verification
6. **Account Status**: Can disable/enable user accounts

## 📝 Database Schema

```sql
-- User table structure
user {
  id: record<user>,
  email: string (unique, validated),
  username: string (unique),
  hashed_password: string,
  full_name: string?,
  is_active: bool (default: true),
  is_verified: bool (default: false),
  created_at: datetime,
  updated_at: datetime,
  last_login: datetime?,
  reset_token: string?,
  reset_token_expires: datetime?,
  verification_token: string?
}
```

## 🚀 Next Steps

### 1. Create Frontend Components

I can create these for you:
- Signup form with validation
- Forgot password form
- Reset password form
- User profile page
- Settings page

### 2. Add Email Service

For production, integrate email service:
- SendGrid
- AWS SES
- Mailgun
- SMTP

### 3. Add Social Login (Optional)

- Google OAuth
- GitHub OAuth
- Microsoft OAuth

### 4. Add Two-Factor Authentication (Optional)

- TOTP (Google Authenticator)
- SMS verification

## 🧪 Testing

### Test Signup
```bash
curl -X POST http://localhost:5055/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "Test123!",
    "full_name": "Test User"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:5055/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET http://localhost:5055/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📊 User Flow Diagrams

### Signup Flow
```
User fills form → Validate input → Check if email/username exists
→ Hash password → Create user → Generate JWT → Return token + user data
```

### Login Flow
```
User enters credentials → Validate email → Check password hash
→ Update last_login → Generate JWT → Return token + user data
```

### Forgot Password Flow
```
User enters email → Check if user exists → Generate reset token
→ Save token with expiry → Send email (or return token for testing)
→ User clicks link → Enters new password → Verify token → Update password
```

## 🔄 Migration from Old Auth

If you want to keep the old password-based auth alongside the new system:

1. Keep `api/auth.py` (old system)
2. Use `api/routers/auth.py` (new system)
3. Gradually migrate users
4. Eventually remove old system

## ⚠️ Important Notes

1. **Change SECRET_KEY**: Update `JWT_SECRET_KEY` in production
2. **Remove Token from Response**: In `forgot_password`, remove the token from response in production
3. **Add Email Service**: Integrate proper email service for password reset
4. **HTTPS Only**: Use HTTPS in production
5. **Rate Limiting**: Add rate limiting to prevent brute force attacks
6. **Input Validation**: Frontend should validate inputs before sending

## 🎯 Ready to Use!

The backend is complete and ready. Would you like me to:
1. Create the frontend components (Signup, Forgot Password, etc.)?
2. Update the existing LoginForm to use the new system?
3. Add email service integration?
4. Add social login?

Just let me know what you'd like next!
