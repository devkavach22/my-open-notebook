# Testing Multi-User System

## Complete Testing Guide

Follow these steps to test the multi-user system with isolated data.

---

## Prerequisites

Make sure all services are running:

```bash
# Check services
check-services.bat

# Or manually:
# 1. SurrealDB: docker ps (should see surrealdb container)
# 2. Backend: http://localhost:5055/api/auth/status
# 3. Frontend: http://localhost:3000
```

---

## Test Scenario: Two Users with Separate Data

### Step 1: Create First User (Alice)

1. Open browser: `http://localhost:3000/signup`
2. Fill in the form:
   - Email: `alice@test.com`
   - Username: `alice`
   - Password: `Alice123!`
   - Full Name: `Alice Smith`
3. Click "Create Account"
4. You should be logged in and redirected to notebooks

### Step 2: Create Data for Alice

1. **Create a Notebook:**
   - Click "New Notebook"
   - Title: "Alice's Research"
   - Click "Create"

2. **Add a Source:**
   - Click "Add Source"
   - Title: "Alice's Document"
   - Content: "This is Alice's private document"
   - Click "Save"

3. **Add a Note:**
   - Open the notebook
   - Click "New Note"
   - Title: "Alice's Note"
   - Content: "This is Alice's private note"
   - Click "Save"

4. **Remember what you created:**
   - 1 Notebook: "Alice's Research"
   - 1 Source: "Alice's Document"
   - 1 Note: "Alice's Note"

### Step 3: Logout Alice

1. Click on user menu (top right)
2. Click "Logout"
3. You should be redirected to login page

### Step 4: Create Second User (Bob)

1. On login page, click "Sign up"
2. Fill in the form:
   - Email: `bob@test.com`
   - Username: `bob`
   - Password: `Bob123!`
   - Full Name: `Bob Johnson`
3. Click "Create Account"
4. You should be logged in and redirected to notebooks

### Step 5: Verify Bob Sees Empty Dashboard

✅ **Expected Result:**
- Bob should see NO notebooks
- Bob should see NO sources
- Bob should see NO notes
- Bob should NOT see Alice's data

❌ **If you see Alice's data, the multi-user system is NOT working**

### Step 6: Create Data for Bob

1. **Create a Notebook:**
   - Click "New Notebook"
   - Title: "Bob's Project"
   - Click "Create"

2. **Add a Source:**
   - Click "Add Source"
   - Title: "Bob's File"
   - Content: "This is Bob's private file"
   - Click "Save"

3. **Add a Note:**
   - Open the notebook
   - Click "New Note"
   - Title: "Bob's Note"
   - Content: "This is Bob's private note"
   - Click "Save"

4. **Verify Bob's data:**
   - 1 Notebook: "Bob's Project" (NOT "Alice's Research")
   - 1 Source: "Bob's File" (NOT "Alice's Document")
   - 1 Note: "Bob's Note" (NOT "Alice's Note")

### Step 7: Switch Back to Alice

1. Logout Bob
2. Login as Alice:
   - Email/Username: `alice@test.com` or `alice`
   - Password: `Alice123!`
3. Click "Sign In"

### Step 8: Verify Alice Still Sees Her Data

✅ **Expected Result:**
- Alice should see her notebook: "Alice's Research"
- Alice should see her source: "Alice's Document"
- Alice should see her note: "Alice's Note"
- Alice should NOT see Bob's data

---

## Verify in Database

### Check Users

```bash
.venv\Scripts\python.exe view-users.py
```

You should see:
```
Total users: 2

User #1
----------------------------------------
Email: alice@test.com
Username: alice
Full Name: Alice Smith

User #2
----------------------------------------
Email: bob@test.com
Username: bob
Full Name: Bob Johnson
```

### Check Data Isolation

Open Surrealist or run queries:

```sql
-- Get Alice's user ID
SELECT id FROM user WHERE email = "alice@test.com";
-- Result: user:abc123

-- Get Bob's user ID
SELECT id FROM user WHERE email = "bob@test.com";
-- Result: user:xyz789

-- Check Alice's notebooks
SELECT * FROM notebook WHERE user_id = user:abc123;
-- Should show: "Alice's Research"

-- Check Bob's notebooks
SELECT * FROM notebook WHERE user_id = user:xyz789;
-- Should show: "Bob's Project"

-- Verify isolation (should return 0)
SELECT * FROM notebook WHERE user_id = user:abc123 AND title = "Bob's Project";
-- Should return: []

SELECT * FROM notebook WHERE user_id = user:xyz789 AND title = "Alice's Research";
-- Should return: []
```

---

## Test Checklist

Use this checklist to verify everything works:

### User Management
- [ ] Can create new user (signup)
- [ ] Can login with email
- [ ] Can login with username
- [ ] Can logout
- [ ] JWT token is stored in localStorage
- [ ] Token is sent with API requests

### Data Isolation
- [ ] User A cannot see User B's notebooks
- [ ] User A cannot see User B's sources
- [ ] User A cannot see User B's notes
- [ ] User A cannot see User B's chat sessions
- [ ] Each user sees only their own data

### Data Creation
- [ ] New notebooks are assigned to current user
- [ ] New sources are assigned to current user
- [ ] New notes are assigned to current user
- [ ] user_id is automatically set

### Data Operations
- [ ] Can view own notebooks
- [ ] Can edit own notebooks
- [ ] Can delete own notebooks
- [ ] Cannot access other users' data via URL manipulation

### Authentication
- [ ] Unauthenticated users redirected to login
- [ ] Invalid token redirects to login
- [ ] Expired token redirects to login
- [ ] Token refresh works (if implemented)

---

## Troubleshooting

### Issue: Both users see the same data

**Possible Causes:**
1. JWT token not being sent with requests
2. Backend not extracting user_id from token
3. Queries not filtering by user_id

**Debug Steps:**
```bash
# 1. Check if token is in localStorage
# Open browser console (F12) and run:
localStorage.getItem('auth_token')

# 2. Check if token is being sent
# Open Network tab in DevTools
# Make a request (e.g., load notebooks)
# Check request headers for: Authorization: Bearer <token>

# 3. Check backend logs
# Look for: "User {user_id} authenticated"

# 4. Check database
# Run query to see if user_id is set:
SELECT id, title, user_id FROM notebook;
```

### Issue: "Authentication required" error

**Solution:**
1. Make sure you're logged in
2. Check if token exists: `localStorage.getItem('auth_token')`
3. Try logging out and logging back in
4. Clear browser cache and cookies

### Issue: user_id is NULL in database

**Solution:**
Backend needs to be updated to set user_id when creating data.

Example fix for notebooks:
```python
@router.post("/api/notebooks")
async def create_notebook(request: Request, data: NotebookCreate):
    user_id = get_current_user_id(request)
    
    notebook = Notebook(
        title=data.title,
        user_id=user_id,  # Add this line
        ...
    )
    
    await notebook.save()
    return notebook
```

---

## Advanced Testing

### Test with 3+ Users

Create multiple users and verify complete isolation:

```python
# test_multiple_users.py
users = [
    {"email": "user1@test.com", "username": "user1", "password": "User1!"},
    {"email": "user2@test.com", "username": "user2", "password": "User2!"},
    {"email": "user3@test.com", "username": "user3", "password": "User3!"},
]

# Create users and data
# Verify each user only sees their own data
```

### Test Edge Cases

1. **User with no data:**
   - Create user
   - Don't create any data
   - Verify empty state is shown

2. **User with lots of data:**
   - Create 100+ notebooks
   - Verify pagination works
   - Verify performance is good

3. **Concurrent users:**
   - Login as User A in Chrome
   - Login as User B in Firefox
   - Create data simultaneously
   - Verify no conflicts

---

## Performance Testing

### Check Query Performance

```sql
-- Should use index (fast)
EXPLAIN SELECT * FROM notebook WHERE user_id = user:abc123;

-- Check index usage
INFO FOR TABLE notebook;
-- Look for: notebook_user_idx
```

### Benchmark

```python
import time
import asyncio
from surrealdb import AsyncSurreal

async def benchmark():
    db = AsyncSurreal("ws://localhost:8000/rpc")
    await db.signin({"username": "root", "password": "root"})
    await db.use("open_notebook", "open_notebook")
    
    # Test query speed
    start = time.time()
    result = await db.query("SELECT * FROM notebook WHERE user_id = user:abc123;")
    end = time.time()
    
    print(f"Query took: {(end - start) * 1000:.2f}ms")
    
    await db.close()

asyncio.run(benchmark())
```

---

## Success Criteria

✅ **Multi-user system is working if:**

1. Two users can signup and login independently
2. Each user sees only their own data
3. Data created by User A is NOT visible to User B
4. JWT tokens are properly sent with requests
5. Backend correctly filters data by user_id
6. Database has user_id set for all records
7. No errors in browser console or backend logs

---

## Next Steps After Testing

Once multi-user is confirmed working:

1. **Update all API endpoints** to set user_id
2. **Add user profile page** to view/edit account
3. **Add admin panel** to manage users
4. **Add sharing features** (optional)
5. **Add usage quotas** (optional)
6. **Add audit logging** (optional)

---

*Last Updated: February 19, 2026*
