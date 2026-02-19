# 🔍 Database Queries Guide - View Your Data

## 📊 Quick Access

**Open Database CLI**: Double-click `view-db-cli.bat`

**Or use Surrealist GUI**: https://surrealdb.com/surrealist

---

## 🎯 Common Queries

### View All Uploaded Files

```sql
USE NS open_notebook;
USE DB open_notebook;

SELECT * FROM source WHERE source_type = 'file';
```

---

## 📝 Source Table Queries

### 1. View All Sources (Files, URLs, Text)
```sql
SELECT * FROM source;
```

### 2. View Only Uploaded Files
```sql
SELECT * FROM source WHERE source_type = 'file';
```

### 3. View File Details (Title, Path, Status)
```sql
SELECT id, title, file_path, file_type, status, created 
FROM source 
WHERE source_type = 'file';
```

### 4. View Recent Uploads (Last 10)
```sql
SELECT * FROM source 
WHERE source_type = 'file' 
ORDER BY created DESC 
LIMIT 10;
```

### 5. Count Total Files Uploaded
```sql
SELECT count() FROM source 
WHERE source_type = 'file' 
GROUP ALL;
```

### 6. View Failed Uploads
```sql
SELECT id, title, status, error 
FROM source 
WHERE status = 'failed';
```

### 7. View Processing Status
```sql
SELECT id, title, status 
FROM source 
WHERE status IN ['pending', 'processing'];
```

### 8. Search Files by Name
```sql
SELECT * FROM source 
WHERE title CONTAINS 'your-search-term';
```

---

## 📚 Notebook Table Queries

### 1. View All Notebooks
```sql
SELECT * FROM notebook;
```

### 2. View Notebook with Source Count
```sql
SELECT *, 
  (SELECT count() FROM source WHERE id IN ->reference.out) AS source_count 
FROM notebook;
```

### 3. View Specific Notebook Details
```sql
SELECT * FROM notebook:your-notebook-id;
```

---

## 📝 Notes Table Queries

### 1. View All Notes
```sql
SELECT * FROM note;
```

### 2. View Notes by Type (AI vs Manual)
```sql
-- AI-generated notes
SELECT * FROM note WHERE note_type = 'ai';

-- Manual notes
SELECT * FROM note WHERE note_type = 'manual';
```

### 3. View Recent Notes
```sql
SELECT * FROM note 
ORDER BY created DESC 
LIMIT 10;
```

---

## 💬 Chat Sessions Queries

### 1. View All Chat Sessions
```sql
SELECT * FROM chat_session;
```

### 2. View Chat Messages
```sql
SELECT * FROM chat_session 
WHERE id = 'chat_session:your-session-id';
```

### 3. Count Chat Sessions per Notebook
```sql
SELECT notebook_id, count() AS session_count 
FROM chat_session 
GROUP BY notebook_id;
```

---

## 🔗 Relationship Queries

### 1. View Sources in a Notebook
```sql
-- Replace 'notebook:abc123' with your notebook ID
SELECT * FROM source 
WHERE id IN (
  SELECT ->reference.out 
  FROM notebook:abc123
);
```

### 2. View Which Notebook a Source Belongs To
```sql
-- Replace 'source:xyz789' with your source ID
SELECT <-reference<-notebook AS notebooks 
FROM source:xyz789;
```

### 3. View Notes in a Notebook
```sql
-- Replace 'notebook:abc123' with your notebook ID
SELECT * FROM note 
WHERE id IN (
  SELECT ->artifact.out 
  FROM notebook:abc123
);
```

---

## 🔍 Advanced Queries

### 1. Full Notebook with All Related Data
```sql
SELECT *,
  (SELECT * FROM source WHERE id IN ->reference.out) AS sources,
  (SELECT * FROM note WHERE id IN ->artifact.out) AS notes,
  (SELECT * FROM chat_session WHERE notebook_id = $parent.id) AS chat_sessions
FROM notebook:your-notebook-id;
```

### 2. Search Across All Content
```sql
SELECT * FROM source 
WHERE content CONTAINS 'your-search-term' 
OR title CONTAINS 'your-search-term';
```

### 3. Statistics Dashboard
```sql
-- Count everything
SELECT 
  (SELECT count() FROM notebook GROUP ALL) AS total_notebooks,
  (SELECT count() FROM source GROUP ALL) AS total_sources,
  (SELECT count() FROM note GROUP ALL) AS total_notes,
  (SELECT count() FROM chat_session GROUP ALL) AS total_chats;
```

---

## 📊 File Upload Flow

### What Happens When You Upload a File:

1. **Frontend** sends file to `/api/sources` endpoint
2. **Backend** saves file to `notebook_data/uploads/`
3. **Backend** extracts text content from file
4. **Backend** creates record in `source` table:
   ```json
   {
     "id": "source:xyz123",
     "title": "your-file.pdf",
     "content": "extracted text...",
     "source_type": "file",
     "file_path": "/uploads/your-file.pdf",
     "status": "completed"
   }
   ```
5. **Backend** links source to notebook via `reference` relationship

### View the Complete Flow:
```sql
-- 1. View the source
SELECT * FROM source:xyz123;

-- 2. View the file path
SELECT file_path FROM source:xyz123;

-- 3. View which notebook it belongs to
SELECT <-reference<-notebook FROM source:xyz123;
```

---

## 🎯 Quick Reference

| What You Want | Query |
|---------------|-------|
| **All files** | `SELECT * FROM source WHERE source_type = 'file';` |
| **Recent files** | `SELECT * FROM source WHERE source_type = 'file' ORDER BY created DESC LIMIT 10;` |
| **Failed uploads** | `SELECT * FROM source WHERE status = 'failed';` |
| **File count** | `SELECT count() FROM source WHERE source_type = 'file' GROUP ALL;` |
| **Search files** | `SELECT * FROM source WHERE title CONTAINS 'search-term';` |

---

## 📁 File Storage Locations

### Database Records:
- **Table**: `source`
- **Location**: SurrealDB at `surreal_data/mydatabase.db/`

### Actual Files:
- **Folder**: `notebook_data/uploads/`
- **Example**: `notebook_data/uploads/your-file.pdf`

---

## 🔧 Troubleshooting

### Can't see uploaded files?
```sql
-- Check if any sources exist
SELECT count() FROM source GROUP ALL;

-- Check source types
SELECT source_type, count() FROM source GROUP BY source_type;

-- Check status
SELECT status, count() FROM source GROUP BY status;
```

### File upload failed?
```sql
-- View error messages
SELECT id, title, status, error 
FROM source 
WHERE status = 'failed';
```

---

## 🎉 Summary

**To view uploaded files**:
1. Open `view-db-cli.bat`
2. Run: `SELECT * FROM source WHERE source_type = 'file';`
3. See all your uploaded files!

**Files are stored in**:
- Database: `source` table
- Disk: `notebook_data/uploads/` folder

Happy querying! 🔍

