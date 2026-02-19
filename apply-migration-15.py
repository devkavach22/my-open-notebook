"""Apply migration 15 - Add user_id to tables."""
import asyncio
from surrealdb import AsyncSurreal

async def apply_migration():
    try:
        db = AsyncSurreal("ws://localhost:8000/rpc")
        await db.signin({"username": "root", "password": "root"})
        await db.use("open_notebook", "open_notebook")
        
        # Read migration file
        with open("open_notebook/database/migrations/15.surrealql", "r") as f:
            migration_sql = f.read()
        
        print("Applying migration 15 (Add user_id to tables)...")
        print(f"SQL:\n{migration_sql}\n")
        
        # Execute migration
        result = await db.query(migration_sql)
        print(f"✅ Migration applied: {result}")
        
        # Record migration
        await db.query(
            "CREATE _sbl_migrations SET version = 15, applied_at = time::now();"
        )
        print("✅ Migration recorded")
        
        # Verify fields were added
        print("\n✅ Checking notebook table...")
        result = await db.query("INFO FOR TABLE notebook;")
        if 'user_id' in str(result):
            print("✅ user_id field added to notebook")
        
        print("\n✅ Checking source table...")
        result = await db.query("INFO FOR TABLE source;")
        if 'user_id' in str(result):
            print("✅ user_id field added to source")
        
        await db.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(apply_migration())
