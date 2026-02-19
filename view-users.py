"""View all users in the database."""
import asyncio
from dotenv import load_dotenv
from surrealdb import AsyncSurreal

load_dotenv()

async def view_users():
    try:
        db = AsyncSurreal("ws://localhost:8000/rpc")
        await db.signin({"username": "root", "password": "root"})
        await db.use("open_notebook", "open_notebook")
        
        print("=" * 80)
        print("ALL USERS IN DATABASE")
        print("=" * 80)
        
        # Get all users
        result = await db.query("SELECT * FROM user;")
        
        if result and len(result) > 0:
            users = result[0]
            print(f"\nTotal users: {len(users)}\n")
            
            for i, user in enumerate(users, 1):
                print(f"User #{i}")
                print("-" * 40)
                print(f"ID: {user.get('id')}")
                print(f"Email: {user.get('email')}")
                print(f"Username: {user.get('username')}")
                print(f"Full Name: {user.get('full_name')}")
                print(f"Active: {user.get('is_active')}")
                print(f"Verified: {user.get('is_verified')}")
                print(f"Created: {user.get('created_at')}")
                print(f"Last Login: {user.get('last_login')}")
                print(f"Reset Token: {user.get('reset_token')}")
                print(f"Verification Token: {user.get('verification_token')}")
                print()
        else:
            print("\n❌ No users found in database\n")
        
        await db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(view_users())
