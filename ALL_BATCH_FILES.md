# 📁 All Batch Files - Complete Reference

## 🚀 Startup & Control

### start.bat ⭐
**Purpose**: Start Open Notebook  
**What it does**:
- Starts Docker services
- Waits 30 seconds
- Opens browser to http://localhost:8502

**Usage**: Double-click or run `start.bat`

---

### stop.bat
**Purpose**: Stop Open Notebook  
**What it does**:
- Stops all Docker services
- Cleans up containers

**Usage**: Double-click or run `stop.bat`

---

### restart.bat
**Purpose**: Restart Open Notebook  
**What it does**:
- Stops services
- Starts services
- Opens browser

**Usage**: Double-click or run `restart.bat`

---

## 📊 Monitoring & Status

### status.bat
**Purpose**: Check if services are running  
**What it does**:
- Shows Docker container status
- Displays access URLs

**Usage**: Double-click or run `status.bat`

---

### logs.bat
**Purpose**: View live API logs  
**What it does**:
- Shows real-time logs from backend
- Press Ctrl+C to stop

**Usage**: Double-click or run `logs.bat`

---

### view-logs.bat
**Purpose**: View live API logs (same as logs.bat)  
**What it does**:
- Shows real-time logs from backend
- Press Ctrl+C to stop

**Usage**: Double-click or run `view-logs.bat`

---

### export-logs.bat
**Purpose**: Save logs to file  
**What it does**:
- Exports logs to `api_logs.txt`
- Opens file in Notepad

**Usage**: Double-click or run `export-logs.bat`

---

## 🗄️ Database

### view-db-cli.bat
**Purpose**: Open database CLI  
**What it does**:
- Connects to SurrealDB
- Opens SQL command line
- Type queries to view data

**Usage**: Double-click or run `view-db-cli.bat`

**Example queries**:
```sql
SELECT * FROM notebook;
SELECT * FROM source;
SELECT * FROM note;
```

---

### backup-database.bat
**Purpose**: Backup database  
**What it does**:
- Creates backup file with timestamp
- Saves as `backup_YYYYMMDD_HHMMSS.surql`

**Usage**: Double-click or run `backup-database.bat`

---

## 📋 Complete List

| File | Purpose | When to Use |
|------|---------|-------------|
| **start.bat** | Start app | Every time you want to use it |
| **stop.bat** | Stop app | When you're done working |
| **restart.bat** | Restart app | After config changes |
| **status.bat** | Check status | To see if it's running |
| **logs.bat** | View logs | To debug issues |
| **view-logs.bat** | View logs | Same as logs.bat |
| **export-logs.bat** | Save logs | To analyze or share logs |
| **view-db-cli.bat** | Database CLI | To query database |
| **backup-database.bat** | Backup DB | Before major changes |

---

## 🎯 Common Workflows

### Daily Startup
1. Double-click **start.bat**
2. Wait for browser to open
3. Start working!

### Daily Shutdown
1. Double-click **stop.bat**
2. Done!

### Debugging Issues
1. Double-click **logs.bat**
2. Watch for errors
3. Press Ctrl+C when done

### View Database
1. Double-click **view-db-cli.bat**
2. Type: `SELECT * FROM notebook;`
3. Type: `exit` to quit

### Backup Before Changes
1. Double-click **backup-database.bat**
2. Save the backup file
3. Make your changes

### Export Logs for Help
1. Double-click **export-logs.bat**
2. Share `api_logs.txt` with support

---

## 🔧 Technical Details

### start.bat
```batch
- Navigates to project directory
- Runs: docker compose up -d
- Waits 30 seconds
- Opens: http://localhost:8502
```

### stop.bat
```batch
- Navigates to project directory
- Runs: docker compose down
```

### logs.bat
```batch
- Navigates to project directory
- Runs: docker compose logs -f open_notebook
```

### view-db-cli.bat
```batch
- Navigates to project directory
- Runs: docker compose exec surrealdb /surreal sql ...
- Connects to: localhost:8000
- Database: open_notebook
```

---

## 💡 Pro Tips

1. **Create shortcuts** on desktop for frequently used files
2. **Pin to taskbar** for quick access
3. **Use start.bat** every morning
4. **Use stop.bat** every evening
5. **Use logs.bat** when debugging
6. **Use backup-database.bat** before major changes

---

## 🎨 Customize Batch Files

You can edit any batch file in Notepad:

1. Right-click the file
2. Choose "Edit"
3. Make changes
4. Save

Example: Change wait time in start.bat:
```batch
REM Change this line:
timeout /t 30 /nobreak > nul

REM To wait 60 seconds:
timeout /t 60 /nobreak > nul
```

---

## 📚 Related Guides

- **COMMANDS_QUICK_REFERENCE.md** - All commands
- **DATABASE_QUICK_GUIDE.md** - Database guide
- **VIEW_DATABASE_AND_LOGS.md** - Detailed guide
- **START_COMMANDS.md** - Startup commands

---

## ✅ Summary

**9 batch files** created for you:

**Essential** (Use daily):
- start.bat
- stop.bat

**Monitoring**:
- status.bat
- logs.bat
- view-logs.bat
- export-logs.bat

**Database**:
- view-db-cli.bat
- backup-database.bat

**Utility**:
- restart.bat

Just double-click and go! 🚀
