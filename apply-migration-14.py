"""Apply migration 14 manually."""
import asyncio
from surrealdb import AsyncSurreal

async def apply_migration():
    try:
        db = AsyncSurreal("ws://localhost:8000/rpc")
        await db.signin({"username": "root", "password": "root"})
        await db.use("open_notebook", "open_notebook")
        
        # Read migration file
        with open("open_notebook/database/migrations/14.surrealql", "r") as f:
            migration_sql = f.read()
        
        print("Applying migration 14...")
        print(f"SQL:\n{migration_sql}\n")
        
        # Execute migration
        result = await db.query(migration_sql)
        print(f"✅ Migration applied: {result}")
        
        # Record migration
        await db.query(
            "CREATE _sbl_migrations SET version = 14, applied_at = time::now();"
        )
        print("✅ Migration recorded")
        
        # Verify user table exists
        result = await db.query("INFO FOR TABLE user;")
        print(f"\n✅ User table created: {result}")
        
        await db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(apply_migration())
