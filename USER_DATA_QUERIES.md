# User-Specific Data Queries

After applying Migration 15, all data is now user-specific. Here's how to query data for specific users.

---

## Get User ID

First, you need the user's ID:

```sql
-- Get user by email
SELECT id FROM user WHERE email = "user@example.com";

-- Get user by username
SELECT id FROM user WHERE username = "johndoe";

-- Example result: user:abc123
```

---

## Query User's Data

### Notebooks

```sql
-- Get all notebooks for a specific user
SELECT * FROM notebook WHERE user_id = user:abc123;

-- Count user's notebooks
SELECT count() FROM notebook WHERE user_id = user:abc123 GROUP ALL;

-- Get user's recent notebooks
SELECT * FROM notebook 
WHERE user_id = user:abc123 
ORDER BY created DESC 
LIMIT 10;
```

### Sources

```sql
-- Get all sources for a specific user
SELECT * FROM source WHERE user_id = user:abc123;

-- Count user's sources
SELECT count() FROM source WHERE user_id = user:abc123 GROUP ALL;

-- Get user's sources by type
SELECT source_type, count() FROM source 
WHERE user_id = user:abc123 
GROUP BY source_type;
```

### Notes

```sql
-- Get all notes for a specific user
SELECT * FROM note WHERE user_id = user:abc123;

-- Count user's notes
SELECT count() FROM note WHERE user_id = user:abc123 GROUP ALL;

-- Get user's recent notes
SELECT * FROM note 
WHERE user_id = user:abc123 
ORDER BY created DESC 
LIMIT 10;
```

### Chat Sessions

```sql
-- Get all chat sessions for a specific user
SELECT * FROM chat_session WHERE user_id = user:abc123;

-- Count user's chat sessions
SELECT count() FROM chat_session WHERE user_id = user:abc123 GROUP ALL;
```

### Podcasts

```sql
-- Get all episodes for a specific user
SELECT * FROM episode WHERE user_id = user:abc123;

-- Count user's episodes
SELECT count() FROM episode WHERE user_id = user:abc123 GROUP ALL;
```

---

## User Statistics

### Complete User Dashboard

```sql
-- Get complete stats for a user
LET $user_id = user:abc123;

SELECT 
  (SELECT count() FROM notebook WHERE user_id = $user_id GROUP ALL)[0].count AS notebooks,
  (SELECT count() FROM source WHERE user_id = $user_id GROUP ALL)[0].count AS sources,
  (SELECT count() FROM note WHERE user_id = $user_id GROUP ALL)[0].count AS notes,
  (SELECT count() FROM chat_session WHERE user_id = $user_id GROUP ALL)[0].count AS chats,
  (SELECT count() FROM episode WHERE user_id = $user_id GROUP ALL)[0].count AS episodes
FROM user WHERE id = $user_id;
```

### User Activity

```sql
-- Get user's recent activity
LET $user_id = user:abc123;

(SELECT 'notebook' AS type, title, created FROM notebook WHERE user_id = $user_id ORDER BY created DESC LIMIT 5)
UNION
(SELECT 'source' AS type, title, created FROM source WHERE user_id = $user_id ORDER BY created DESC LIMIT 5)
UNION
(SELECT 'note' AS type, title, created FROM note WHERE user_id = $user_id ORDER BY created DESC LIMIT 5)
ORDER BY created DESC;
```

---

## Multi-User Queries

### All Users with Their Data Counts

```sql
SELECT 
  id,
  email,
  username,
  (SELECT count() FROM notebook WHERE user_id = $parent.id GROUP ALL)[0].count AS notebooks,
  (SELECT count() FROM source WHERE user_id = $parent.id GROUP ALL)[0].count AS sources,
  (SELECT count() FROM note WHERE user_id = $parent.id GROUP ALL)[0].count AS notes
FROM user;
```

### Find Users with Most Content

```sql
-- Users with most notebooks
SELECT 
  user_id,
  count() AS notebook_count
FROM notebook 
GROUP BY user_id 
ORDER BY notebook_count DESC;

-- Users with most sources
SELECT 
  user_id,
  count() AS source_count
FROM source 
GROUP BY user_id 
ORDER BY source_count DESC;
```

---

## Assign Existing Data to User

If you have existing data without user_id, assign it to a user:

```sql
-- Assign all notebooks to a user
UPDATE notebook SET user_id = user:abc123 WHERE user_id = NONE;

-- Assign all sources to a user
UPDATE source SET user_id = user:abc123 WHERE user_id = NONE;

-- Assign all notes to a user
UPDATE note SET user_id = user:abc123 WHERE user_id = NONE;

-- Assign all chat sessions to a user
UPDATE chat_session SET user_id = user:abc123 WHERE user_id = NONE;
```

---

## Python Script to View User Data

```python
import asyncio
from surrealdb import AsyncSurreal

async def view_user_data(email: str):
    db = AsyncSurreal("ws://localhost:8000/rpc")
    await db.signin({"username": "root", "password": "root"})
    await db.use("open_notebook", "open_notebook")
    
    # Get user
    result = await db.query("SELECT * FROM user WHERE email = $email;", {"email": email})
    if not result or len(result[0]) == 0:
        print(f"User {email} not found")
        return
    
    user = result[0][0]
    user_id = user['id']
    
    print(f"\n{'='*60}")
    print(f"Data for: {user['email']} ({user['username']})")
    print(f"User ID: {user_id}")
    print(f"{'='*60}\n")
    
    # Get notebooks
    result = await db.query("SELECT * FROM notebook WHERE user_id = $user_id;", {"user_id": user_id})
    notebooks = result[0] if result else []
    print(f"Notebooks: {len(notebooks)}")
    for nb in notebooks:
        print(f"  - {nb.get('title', 'Untitled')}")
    
    # Get sources
    result = await db.query("SELECT * FROM source WHERE user_id = $user_id;", {"user_id": user_id})
    sources = result[0] if result else []
    print(f"\nSources: {len(sources)}")
    for src in sources:
        print(f"  - {src.get('title', 'Untitled')}")
    
    # Get notes
    result = await db.query("SELECT * FROM note WHERE user_id = $user_id;", {"user_id": user_id})
    notes = result[0] if result else []
    print(f"\nNotes: {len(notes)}")
    for note in notes:
        print(f"  - {note.get('title', 'Untitled')}")
    
    await db.close()

# Usage
asyncio.run(view_user_data("user@example.com"))
```

---

## API Integration

The backend now automatically filters data by user_id from the JWT token:

```python
# In your API endpoints
from fastapi import Request
from api.middleware import get_current_user_id

@router.get("/api/notebooks")
async def get_notebooks(request: Request):
    user_id = get_current_user_id(request)
    # Query will automatically filter by user_id
    result = await repo_query(
        "SELECT * FROM notebook WHERE user_id = $user_id",
        {"user_id": user_id}
    )
    return result
```

---

## Testing

### Create Test Data for Multiple Users

```sql
-- Create test users
CREATE user:user1 CONTENT {
  email: "user1@test.com",
  username: "user1",
  hashed_password: "$2b$12$test",
  is_active: true
};

CREATE user:user2 CONTENT {
  email: "user2@test.com",
  username: "user2",
  hashed_password: "$2b$12$test",
  is_active: true
};

-- Create notebooks for user1
CREATE notebook CONTENT {
  title: "User1 Notebook 1",
  user_id: user:user1,
  created: time::now()
};

-- Create notebooks for user2
CREATE notebook CONTENT {
  title: "User2 Notebook 1",
  user_id: user:user2,
  created: time::now()
};

-- Verify isolation
SELECT * FROM notebook WHERE user_id = user:user1;
SELECT * FROM notebook WHERE user_id = user:user2;
```

---

*Last Updated: February 19, 2026*
