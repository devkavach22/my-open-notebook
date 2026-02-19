# 🔍 View Database Data & API Logs

## Database: SurrealDB

This project uses **SurrealDB** (not SQL or MongoDB). It's a modern multi-model database.

---

## 📊 Option 1: View Database via Surrealist (GUI - Recommended)

### Step 1: Install Surrealist
Download from: https://surrealdb.com/surrealist

**Windows**: Download the `.exe` installer

### Step 2: Connect to Database
1. Open Surrealist
2. Click **New Connection**
3. Enter connection details:
   - **Name**: Open Notebook
   - **Protocol**: HTTP
   - **Host**: localhost
   - **Port**: 8000
   - **Namespace**: open_notebook
   - **Database**: open_notebook
   - **Username**: root
   - **Password**: root
4. Click **Connect**

### Step 3: Browse Data
- Click **Explorer** tab
- See all tables: notebook, source, note, chat_session, etc.
- Click any table to view data
- Run queries in **Query** tab

---

## 📊 Option 2: View Database via Command Line

### Connect to SurrealDB CLI
```cmd
docker compose exec surrealdb /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
```

### Common Queries

#### List All Tables
```sql
INFO FOR DB;
```

#### View All Notebooks
```sql
SELECT * FROM notebook;
```

#### View All Sources
```sql
SELECT * FROM source;
```

#### View All Notes
```sql
SELECT * FROM note;
```

#### View All Chat Sessions
```sql
SELECT * FROM chat_session;
```

#### Count Records
```sql
SELECT count() FROM notebook GROUP ALL;
SELECT count() FROM source GROUP ALL;
SELECT count() FROM note GROUP ALL;
```

#### View Specific Notebook
```sql
SELECT * FROM notebook WHERE id = "notebook:abc123";
```

#### View Notebook with Sources
```sql
SELECT *, 
  (SELECT * FROM source WHERE id IN ->reference.in) AS sources 
FROM notebook;
```

---

## 📊 Option 3: View Database Files Directly

### Database Location
```
C:\Users\hemanshi.l\Desktop\open-notebook\surreal_data\mydatabase.db\
```

This is a RocksDB database (binary format). You can't open it with a text editor.

**To browse**: Use Surrealist (Option 1) or CLI (Option 2)

---

## 📝 View API Logs

### Option 1: View Live Logs (Recommended)

#### Using Batch File
Double-click: **logs.bat**

#### Using Command Line
```cmd
cd C:\Users\hemanshi.l\Desktop\open-notebook
docker compose logs -f open_notebook
```

Press `Ctrl+C` to stop viewing.

### Option 2: View Last 100 Lines
```cmd
docker compose logs --tail=100 open_notebook
```

### Option 3: View Logs for Specific Service

#### Backend API Logs
```cmd
docker compose logs -f open_notebook
```

#### Database Logs
```cmd
docker compose logs -f surrealdb
```

#### All Services
```cmd
docker compose logs -f
```

### Option 4: Save Logs to File
```cmd
docker compose logs open_notebook > api_logs.txt
```

Then open `api_logs.txt` in notepad.

---

## 📊 Database Structure

### Main Tables

#### notebook
- id (e.g., notebook:abc123)
- name
- description
- created
- updated
- archived

#### source
- id (e.g., source:xyz789)
- title
- content
- source_type (file, url, text)
- created
- updated

#### note
- id (e.g., note:def456)
- title
- content
- note_type
- created
- updated

#### chat_session
- id (e.g., chat_session:ghi789)
- title
- model_override
- created
- updated

#### source_insight
- id
- source_id
- insight_type (summary, key_points, etc.)
- content
- created

### Relationships

#### reference (notebook ↔ source)
```
source -> reference -> notebook
```

#### artifact (notebook ↔ note)
```
note -> artifact -> notebook
```

#### refers_to (chat_session ↔ notebook/source)
```
chat_session -> refers_to -> notebook
chat_session -> refers_to -> source
```

---

## 🔍 Useful Database Queries

### Get Notebook with All Related Data
```sql
SELECT *,
  (SELECT * FROM source WHERE id IN ->reference.in) AS sources,
  (SELECT * FROM note WHERE id IN ->artifact.in) AS notes,
  (SELECT * FROM chat_session WHERE out = $parent.id) AS chat_sessions
FROM notebook:abc123;
```

### Get All Notebooks with Counts
```sql
SELECT *,
  count(<-reference.in) as source_count,
  count(<-artifact.in) as note_count
FROM notebook;
```

### Search Sources by Content
```sql
SELECT * FROM source WHERE content CONTAINS "machine learning";
```

### Get Recent Chat Sessions
```sql
SELECT * FROM chat_session ORDER BY updated DESC LIMIT 10;
```

### Get Sources Without Notebooks
```sql
SELECT * FROM source WHERE count(->reference) = 0;
```

---

## 📝 Understanding API Logs

### Log Levels

#### INFO
Normal operations
```
INFO:     127.0.0.1:12345 - "GET /api/notebooks HTTP/1.1" 200 OK
```

#### DEBUG
Detailed information
```
DEBUG    | pages.stream_app.utils:check_migration:121 - Running migration check
```

#### WARNING
Potential issues
```
WARNING  | Could not read version from pyproject.toml
```

#### ERROR
Errors that occurred
```
ERROR    | Error fetching notebooks: Connection refused
```

#### CRITICAL
Critical errors
```
CRITICAL | Database migration failed
```

### Common Log Patterns

#### API Request
```
INFO: 172.18.0.1:12345 - "GET /api/notebooks HTTP/1.1" 200 OK
```
- IP: 172.18.0.1
- Method: GET
- Endpoint: /api/notebooks
- Status: 200 (success)

#### Database Migration
```
INFO | Running migration 1
INFO | Migration successful. New version: 7
```

#### Model Discovery
```
INFO | Using API for models operations
INFO | GET /api/models/defaults HTTP/1.1" 200 OK
```

---

## 🛠️ Create Batch Files for Quick Access

### view-logs.bat
```batch
@echo off
echo Viewing API logs (Press Ctrl+C to stop)...
cd /d "%~dp0"
docker compose logs -f open_notebook
```

### view-db-cli.bat
```batch
@echo off
echo Connecting to SurrealDB...
cd /d "%~dp0"
docker compose exec surrealdb /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
```

### export-logs.bat
```batch
@echo off
echo Exporting logs to api_logs.txt...
cd /d "%~dp0"
docker compose logs open_notebook > api_logs.txt
echo Done! Check api_logs.txt
pause
```

---

## 📊 Database Backup & Export

### Backup Database
```cmd
docker compose exec surrealdb /surreal export --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook backup.surql
```

### Restore Database
```cmd
docker compose exec surrealdb /surreal import --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook backup.surql
```

### Export to JSON
```cmd
docker compose exec surrealdb /surreal export --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --format json backup.json
```

---

## 🔍 Monitor in Real-Time

### Watch API Logs
```cmd
docker compose logs -f open_notebook | findstr "ERROR"
```

### Watch Database Logs
```cmd
docker compose logs -f surrealdb
```

### Watch All Logs
```cmd
docker compose logs -f
```

---

## 📊 Database GUI Tools

### Surrealist (Official - Recommended)
- **Download**: https://surrealdb.com/surrealist
- **Features**: 
  - Visual table browser
  - Query editor
  - Data visualization
  - Export/import

### SurrealDB Studio (Web-based)
```cmd
docker run -p 8080:8080 surrealdb/studio
```
Then open: http://localhost:8080

---

## 🎯 Quick Reference

### View Database
```cmd
# Install Surrealist (GUI)
https://surrealdb.com/surrealist

# Or use CLI
docker compose exec surrealdb /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
```

### View Logs
```cmd
# Live logs
docker compose logs -f open_notebook

# Last 100 lines
docker compose logs --tail=100 open_notebook

# Save to file
docker compose logs open_notebook > logs.txt
```

### Database Location
```
C:\Users\hemanshi.l\Desktop\open-notebook\surreal_data\mydatabase.db\
```

### Connection Details
- **Host**: localhost
- **Port**: 8000
- **Namespace**: open_notebook
- **Database**: open_notebook
- **Username**: root
- **Password**: root

---

## 💡 Pro Tips

1. **Use Surrealist** for visual database browsing
2. **Use logs.bat** for quick log viewing
3. **Save logs to file** for analysis
4. **Backup database** before major changes
5. **Monitor logs** when debugging issues

---

## 🆘 Troubleshooting

### Can't Connect to Database
```cmd
# Check if database is running
docker compose ps

# Restart database
docker compose restart surrealdb
```

### No Logs Showing
```cmd
# Check if container is running
docker compose ps

# View all logs
docker compose logs
```

### Database File Locked
```cmd
# Stop services
docker compose down

# Start again
docker compose up -d
```

---

## 📚 More Information

- **SurrealDB Docs**: https://surrealdb.com/docs
- **Surrealist Guide**: https://surrealdb.com/docs/surrealist
- **SurrealQL Reference**: https://surrealdb.com/docs/surrealql

---

## ✅ Summary

**View Database**:
1. Install Surrealist (GUI): https://surrealdb.com/surrealist
2. Connect to localhost:8000
3. Browse tables and data

**View Logs**:
1. Double-click `logs.bat`
2. Or run: `docker compose logs -f open_notebook`

**Database Location**:
- Files: `surreal_data/mydatabase.db/`
- Access: Use Surrealist or CLI

Happy exploring! 🔍
