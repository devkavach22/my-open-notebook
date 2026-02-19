# 🔍 Database & Logs - Quick Guide

## 📊 Database: SurrealDB

This project uses **SurrealDB** (not MySQL/MongoDB/PostgreSQL).

---

## 🎯 Quick Access

### View Database (GUI - Easiest!)

1. **Download Surrealist**: https://surrealdb.com/surrealist
2. **Install and Open**
3. **Create Connection**:
   - Host: `localhost`
   - Port: `8000`
   - Namespace: `open_notebook`
   - Database: `open_notebook`
   - Username: `root`
   - Password: `root`
4. **Click Connect**
5. **Browse tables**: notebook, source, note, chat_session, etc.

### View Database (CLI)

Double-click: **view-db-cli.bat**

Or run:
```cmd
docker compose exec surrealdb /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
```

---

## 📝 View Logs

### Option 1: Batch File (Easiest!)
Double-click: **view-logs.bat**

### Option 2: Command Line
```cmd
docker compose logs -f open_notebook
```

### Option 3: Export to File
Double-click: **export-logs.bat**

This creates `api_logs.txt` that you can open in Notepad.

---

## 📊 Database Tables

### Main Tables

| Table | What It Stores |
|-------|---------------|
| **notebook** | Your notebooks |
| **source** | Uploaded files, URLs, text |
| **note** | Your notes |
| **chat_session** | Chat conversations |
| **source_insight** | AI-generated insights |
| **credential** | API keys (encrypted) |
| **model** | AI model configurations |

### Relationships

| Relationship | Connects |
|-------------|----------|
| **reference** | source ↔ notebook |
| **artifact** | note ↔ notebook |
| **refers_to** | chat_session ↔ notebook/source |

---

## 🔍 Common Database Queries

### View All Notebooks
```sql
SELECT * FROM notebook;
```

### View All Sources
```sql
SELECT * FROM source;
```

### View Notebook with Sources
```sql
SELECT *,
  (SELECT * FROM source WHERE id IN ->reference.in) AS sources
FROM notebook;
```

### Count Records
```sql
SELECT count() FROM notebook GROUP ALL;
SELECT count() FROM source GROUP ALL;
SELECT count() FROM note GROUP ALL;
```

### Search Sources
```sql
SELECT * FROM source WHERE content CONTAINS "AI";
```

---

## 📝 Understanding Logs

### Log Format
```
INFO:     172.18.0.1:12345 - "GET /api/notebooks HTTP/1.1" 200 OK
```

- **INFO**: Log level
- **172.18.0.1**: Client IP
- **GET**: HTTP method
- **/api/notebooks**: Endpoint
- **200**: Status code (200 = success)

### Log Levels

| Level | Meaning |
|-------|---------|
| **INFO** | Normal operations |
| **DEBUG** | Detailed information |
| **WARNING** | Potential issues |
| **ERROR** | Errors occurred |
| **CRITICAL** | Critical failures |

---

## 🛠️ Batch Files Created

| File | What It Does |
|------|-------------|
| **view-logs.bat** | View live API logs |
| **view-db-cli.bat** | Open database CLI |
| **export-logs.bat** | Save logs to file |
| **backup-database.bat** | Backup database |

---

## 📁 Database File Location

```
C:\Users\hemanshi.l\Desktop\open-notebook\surreal_data\mydatabase.db\
```

**Note**: This is a binary format (RocksDB). You can't open it with a text editor.

**To view data**: Use Surrealist (GUI) or CLI.

---

## 🔧 Connection Details

| Setting | Value |
|---------|-------|
| **Protocol** | HTTP |
| **Host** | localhost |
| **Port** | 8000 |
| **Namespace** | open_notebook |
| **Database** | open_notebook |
| **Username** | root |
| **Password** | root |

---

## 💾 Backup & Restore

### Backup Database
Double-click: **backup-database.bat**

Or run:
```cmd
docker compose exec surrealdb /surreal export --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook > backup.surql
```

### Restore Database
```cmd
docker compose exec surrealdb /surreal import --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook < backup.surql
```

---

## 🎯 Quick Tasks

### Task: View All Notebooks
1. Double-click **view-db-cli.bat**
2. Type: `SELECT * FROM notebook;`
3. Press Enter

### Task: View API Logs
1. Double-click **view-logs.bat**
2. Watch logs in real-time
3. Press Ctrl+C to stop

### Task: Export Logs for Analysis
1. Double-click **export-logs.bat**
2. Opens `api_logs.txt` in Notepad
3. Search, analyze, or share

### Task: Backup Database
1. Double-click **backup-database.bat**
2. Creates `backup_YYYYMMDD_HHMMSS.surql`
3. Save this file somewhere safe

---

## 🔍 Monitoring Tips

### Watch for Errors
```cmd
docker compose logs -f open_notebook | findstr "ERROR"
```

### Watch Specific Endpoint
```cmd
docker compose logs -f open_notebook | findstr "/api/notebooks"
```

### View Last 50 Lines
```cmd
docker compose logs --tail=50 open_notebook
```

---

## 📊 Database Schema

### notebook Table
```
id: notebook:abc123
name: "My Research"
description: "AI research notes"
created: "2024-02-17T10:30:00Z"
updated: "2024-02-17T15:45:00Z"
archived: false
```

### source Table
```
id: source:xyz789
title: "AI Paper"
content: "Full text content..."
source_type: "file"
file_path: "/uploads/paper.pdf"
created: "2024-02-17T10:30:00Z"
```

### note Table
```
id: note:def456
title: "Key Points"
content: "Important findings..."
note_type: "manual"
created: "2024-02-17T11:00:00Z"
```

---

## 🆘 Troubleshooting

### Can't Connect to Database
```cmd
# Check if running
docker compose ps

# Restart database
docker compose restart surrealdb
```

### No Logs Showing
```cmd
# Check container status
docker compose ps

# View all logs
docker compose logs
```

### Database Locked
```cmd
# Stop everything
docker compose down

# Start fresh
docker compose up -d
```

---

## 📚 More Information

- **Full Guide**: VIEW_DATABASE_AND_LOGS.md
- **SurrealDB Docs**: https://surrealdb.com/docs
- **Surrealist**: https://surrealdb.com/surrealist

---

## ✅ Summary

**View Database**:
- GUI: Install Surrealist
- CLI: Double-click `view-db-cli.bat`

**View Logs**:
- Live: Double-click `view-logs.bat`
- File: Double-click `export-logs.bat`

**Backup**:
- Double-click `backup-database.bat`

**Location**:
- Database: `surreal_data/mydatabase.db/`
- Logs: Run `docker compose logs`

Happy exploring! 🔍
