"""Test signup to see detailed error."""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from api.user_service import create_user
from open_notebook.domain.user import UserCreate

async def test_signup():
    try:
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="Test123!",
            full_name="Test User"
        )
        user = await create_user(user_data)
        print(f"✅ User created successfully: {user.email}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_signup())
