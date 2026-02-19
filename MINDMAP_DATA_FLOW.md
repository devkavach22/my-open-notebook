# Mind Map Data Flow - Complete Guide

## Where is the Content Stored?

When you upload a source file (PDF, text, etc.), the data flows through these tables:

### 1. `source` Table
- Stores metadata about the uploaded file
- Fields: `id`, `title`, `asset` (file info), `topics`, `command` (processing job)
- **Does NOT store the actual text content**

### 2. `source_embedding` Table  
- Stores the actual extracted text content in chunks
- Fields: `id`, `source` (link to source), `content` (text chunk), `embedding` (vector)
- **This is where the full text lives!**
- Each source is split into multiple chunks for better AI processing

### 3. `command` Table
- Tracks the background processing jobs
- Shows status: `new`, `running`, `completed`, `failed`

## Why "Content not yet processed"?

Your sources show this message because:

1. Files were uploaded to the `source` table
2. But the embedding generation process hasn't run yet
3. So the `source_embedding` table is empty for those sources

## How to Fix It

### Option 1: Use the Batch File (Easiest)
Double-click `regenerate-embeddings.bat` to trigger embedding generation for all sources.

### Option 2: Manual API Call
```bash
curl -X POST "http://localhost:5055/api/embedding/rebuild" \
  -H "Content-Type: application/json" \
  -d '{"mode": "all", "include_sources": true, "include_notes": false, "include_insights": false}'
```

### Option 3: Re-upload with Embed Enabled
When uploading new sources through the UI, make sure the "Generate Embeddings" option is checked.

## Check Database Directly

### Check if sources exist:
```sql
SELECT id, title, asset FROM source;
```

### Check if embeddings exist:
```sql
SELECT source, count() as chunks 
FROM source_embedding 
GROUP BY source;
```

### Check processing status:
```sql
SELECT id, type, status, error 
FROM command 
WHERE type = 'embedding' 
ORDER BY created DESC;
```

## Requirements for Embedding Generation

You MUST have an AI provider configured in Settings:
- OpenAI (recommended)
- Anthropic Claude
- Google Gemini
- Groq
- Or any OpenAI-compatible endpoint

Without an AI provider, embedding generation will fail!

## After Embeddings are Generated

Once the `source_embedding` table has data:
1. The Mind Map will automatically fetch content from embeddings
2. It will parse the full text hierarchically
3. Create unlimited depth structure based on content
4. Show interactive, expandable nodes

## Troubleshooting

### "Content not yet processed"
- Run `regenerate-embeddings.bat`
- Check backend logs for errors
- Verify AI provider is configured

### "Error loading content"
- Check backend logs for specific error
- Verify database connection
- Check if source_embedding table has data

### Empty Mind Map
- Verify sources are in the notebook
- Check if embeddings were generated
- Look at backend logs during mind map generation
