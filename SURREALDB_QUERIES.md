# SurrealDB Queries for User Management

## Connection Details
- **URL:** `http://localhost:8000`
- **Namespace:** `open_notebook`
- **Database:** `open_notebook`
- **Username:** `root`
- **Password:** `root`

---

## Basic Queries

### 1. View All Users
```sql
SELECT * FROM user;
```

### 2. View Specific User by Email
```sql
SELECT * FROM user WHERE email = "user@example.com";
```

### 3. View Specific User by Username
```sql
SELECT * FROM user WHERE username = "johndoe";
```

### 4. View User by ID
```sql
SELECT * FROM user:abc123;
```

### 5. Count Total Users
```sql
SELECT count() FROM user GROUP ALL;
```

### 6. View Only Active Users
```sql
SELECT * FROM user WHERE is_active = true;
```

### 7. View Only Verified Users
```sql
SELECT * FROM user WHERE is_verified = true;
```

### 8. View Users Created Today
```sql
SELECT * FROM user WHERE created_at >= time::now() - 1d;
```

### 9. View Users with Recent Login
```sql
SELECT * FROM user WHERE last_login != NONE ORDER BY last_login DESC;
```

### 10. View User Without Sensitive Data
```sql
SELECT id, email, username, full_name, is_active, is_verified, created_at, last_login 
FROM user;
```

---

## Advanced Queries

### 11. Search Users by Email Pattern
```sql
SELECT * FROM user WHERE email ~ "gmail.com";
```

### 12. Search Users by Username Pattern
```sql
SELECT * FROM user WHERE username ~ "john";
```

### 13. View Users with Pending Password Reset
```sql
SELECT * FROM user WHERE reset_token != NONE AND reset_token_expires > time::now();
```

### 14. View Users with Expired Reset Tokens
```sql
SELECT * FROM user WHERE reset_token != NONE AND reset_token_expires < time::now();
```

### 15. View Unverified Users
```sql
SELECT * FROM user WHERE is_verified = false AND verification_token != NONE;
```

---

## Update Queries

### 16. Verify a User's Email
```sql
UPDATE user SET is_verified = true, verification_token = NONE 
WHERE email = "user@example.com";
```

### 17. Activate/Deactivate User
```sql
-- Activate
UPDATE user SET is_active = true WHERE email = "user@example.com";

-- Deactivate
UPDATE user SET is_active = false WHERE email = "user@example.com";
```

### 18. Clear Reset Token
```sql
UPDATE user SET reset_token = NONE, reset_token_expires = NONE 
WHERE email = "user@example.com";
```

### 19. Update User's Full Name
```sql
UPDATE user SET full_name = "John Doe" WHERE email = "user@example.com";
```

### 20. Update Last Login
```sql
UPDATE user SET last_login = time::now() WHERE email = "user@example.com";
```

---

## Delete Queries

### 21. Delete User by Email
```sql
DELETE user WHERE email = "user@example.com";
```

### 22. Delete User by ID
```sql
DELETE user:abc123;
```

### 23. Delete All Unverified Users (CAREFUL!)
```sql
DELETE user WHERE is_verified = false;
```

### 24. Delete Inactive Users (CAREFUL!)
```sql
DELETE user WHERE is_active = false;
```

---

## Table Information Queries

### 25. View Table Schema
```sql
INFO FOR TABLE user;
```

### 26. View All Indexes
```sql
INFO FOR TABLE user;
-- Look at the "indexes" section
```

### 27. View All Fields
```sql
INFO FOR TABLE user;
-- Look at the "fields" section
```

### 28. Check if Table Exists
```sql
INFO FOR DB;
-- Look for "user" in the "tables" section
```

---

## Aggregation Queries

### 29. Count Users by Verification Status
```sql
SELECT is_verified, count() FROM user GROUP BY is_verified;
```

### 30. Count Users by Active Status
```sql
SELECT is_active, count() FROM user GROUP BY is_active;
```

### 31. Get User Registration Stats by Date
```sql
SELECT 
  time::day(created_at) AS date, 
  count() AS registrations 
FROM user 
GROUP BY date 
ORDER BY date DESC;
```

### 32. Get Average Users per Day
```sql
SELECT 
  count() / time::day(time::now() - min(created_at)) AS avg_users_per_day 
FROM user;
```

---

## Security Queries

### 33. Find Users with Same Email (Should be 0 due to unique index)
```sql
SELECT email, count() FROM user GROUP BY email HAVING count() > 1;
```

### 34. Find Users with Same Username (Should be 0 due to unique index)
```sql
SELECT username, count() FROM user GROUP BY username HAVING count() > 1;
```

### 35. View Users Without Password (Should be 0)
```sql
SELECT * FROM user WHERE hashed_password = NONE OR hashed_password = "";
```

---

## Testing Queries

### 36. Create Test User
```sql
CREATE user CONTENT {
  email: "test@example.com",
  username: "testuser",
  hashed_password: "$2b$12$abcdefghijklmnopqrstuvwxyz",
  full_name: "Test User",
  is_active: true,
  is_verified: false,
  created_at: time::now(),
  updated_at: time::now(),
  verification_token: "test-token-123"
};
```

### 37. Update Test User
```sql
UPDATE user SET 
  full_name = "Updated Test User",
  is_verified = true,
  updated_at = time::now()
WHERE email = "test@example.com";
```

### 38. Delete Test User
```sql
DELETE user WHERE email = "test@example.com";
```

---

## Maintenance Queries

### 39. Clean Up Expired Reset Tokens
```sql
UPDATE user SET 
  reset_token = NONE, 
  reset_token_expires = NONE 
WHERE reset_token_expires < time::now();
```

### 40. Find Inactive Users (No login in 30 days)
```sql
SELECT * FROM user 
WHERE last_login < time::now() - 30d 
OR last_login = NONE;
```

---

## How to Use These Queries

### Using Surrealist GUI:
1. Download Surrealist from https://surrealdb.com/surrealist
2. Connect with the details above
3. Paste any query in the query editor
4. Click "Run" or press Ctrl+Enter

### Using Docker CLI:
```bash
docker exec -it open-notebook-surrealdb-1 /bin/sh
surreal sql --conn http://localhost:8000 --user root --pass root --ns open_notebook --db open_notebook
# Then paste your query
```

### Using Python Script:
```python
from surrealdb import AsyncSurreal

db = AsyncSurreal("ws://localhost:8000/rpc")
await db.signin({"username": "root", "password": "root"})
await db.use("open_notebook", "open_notebook")
result = await db.query("SELECT * FROM user;")
print(result)
```

---

## Quick Reference

| Action | Query |
|--------|-------|
| View all users | `SELECT * FROM user;` |
| Count users | `SELECT count() FROM user GROUP ALL;` |
| Find by email | `SELECT * FROM user WHERE email = "...";` |
| Find by username | `SELECT * FROM user WHERE username = "...";` |
| Verify user | `UPDATE user SET is_verified = true WHERE email = "...";` |
| Delete user | `DELETE user WHERE email = "...";` |
| View table info | `INFO FOR TABLE user;` |

---

*Last Updated: February 19, 2026*
