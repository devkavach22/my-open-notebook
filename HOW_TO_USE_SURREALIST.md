# How to Use Surrealist (SurrealDB GUI)

## The Problem

When you click "Run Query" in Surrealist, you get "Failed to fetch" error.

## Why This Happens

Surrealist needs to be connected to the database with the correct:
- Namespace
- Database name
- Credentials

## Solution: Connect Properly

### Step 1: Open Connection Settings

In Surrealist, look for the connection settings (usually top-left or a connection icon).

### Step 2: Enter These Settings

```
Protocol: HTTP or WebSocket
Host: localhost
Port: 8000
Username: root
Password: root
Namespace: open_notebook
Database: open_notebook
```

**Full URL Options:**
- HTTP: `http://localhost:8000`
- WebSocket: `ws://localhost:8000`

### Step 3: Click "Connect"

Once connected, you should see a green indicator or "Connected" status.

### Step 4: Run Your Query

Now you can run queries like:
```sql
SELECT * FROM user;
SELECT * FROM notebook;
SELECT * FROM source;
```

## Common Queries

### View All Users
```sql
SELECT * FROM user;
```

### View All Notebooks
```sql
SELECT * FROM notebook;
```

### View All Sources
```sql
SELECT * FROM source;
```

### View Specific User by Email
```sql
SELECT * FROM user WHERE email = "hemanshiladola221@gmail.com";
```

### Count Records
```sql
SELECT count() FROM user GROUP ALL;
SELECT count() FROM notebook GROUP ALL;
```

## Alternative: Use Command Line

If Surrealist doesn't work, you can query from command line:

### Windows (PowerShell)
```powershell
docker exec -it open-notebook-surrealdb-1 surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --pretty
```

Then run queries:
```sql
SELECT * FROM user;
```

Type `exit` to quit.

## Alternative: Use Batch File

I'll create a batch file for you to easily access the database CLI.

## Troubleshooting

### "Failed to fetch"
- Check connection settings (namespace and database must be `open_notebook`)
- Make sure database is running: `docker ps`
- Try reconnecting in Surrealist

### "Authentication failed"
- Username: `root`
- Password: `root`

### "Namespace or database not found"
- Namespace: `open_notebook`
- Database: `open_notebook`
- Both are case-sensitive!

## Summary

**Connection Details:**
- URL: `http://localhost:8000`
- User: `root`
- Pass: `root`
- Namespace: `open_notebook`
- Database: `open_notebook`

Once connected with these settings, your queries will work!
