"""Test database connection."""
import asyncio
import os
from surrealdb import AsyncSurreal

async def test_connection():
    try:
        db = AsyncSurreal("ws://localhost:8000/rpc")
        
        # Try to sign in as root
        print("Signing in as root...")
        await db.signin({
            "username": "root",
            "password": "root"
        })
        print("✅ Signed in successfully")
        
        # Try to use namespace and database
        print("Using namespace and database...")
        await db.use("open_notebook", "open_notebook")
        print("✅ Using namespace/database successfully")
        
        # Try to query
        print("Testing query...")
        result = await db.query("INFO FOR DB;")
        print(f"✅ Query successful: {result}")
        
        await db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
