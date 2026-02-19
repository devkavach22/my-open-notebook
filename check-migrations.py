"""Check migration status."""
import asyncio
from surrealdb import AsyncSurreal

async def check_migrations():
    try:
        db = AsyncSurreal("ws://localhost:8000/rpc")
        await db.signin({"username": "root", "password": "root"})
        await db.use("open_notebook", "open_notebook")
        
        # Check migrations table
        result = await db.query("SELECT * FROM _sbl_migrations ORDER BY version;")
        print("Current migrations:")
        print(f"Result: {result}")
        if result and len(result) > 0:
            for migration in result[0]:
                print(f"  Version {migration.get('version', 'N/A')}: {migration.get('name', 'N/A')}")
        
        # Check if user table exists
        result = await db.query("INFO FOR TABLE user;")
        print(f"\nUser table info: {result}")
        
        await db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_migrations())
