@echo off
cd /d "%~dp0"

echo ========================================
echo Regenerate Embeddings for All Sources
echo ========================================
echo.
echo This will trigger embedding generation for ALL sources
echo (including those without embeddings).
echo.
echo Make sure:
echo 1. Backend is running (port 5055)
echo 2. You have configured an AI provider in Settings
echo    (OpenAI, Anthropic, Google, etc.)
echo.
pause

echo.
echo Calling API to rebuild embeddings...
echo.

curl -X POST "http://localhost:5055/api/embedding/rebuild" ^
  -H "Content-Type: application/json" ^
  -d "{\"mode\": \"all\", \"include_sources\": true, \"include_notes\": false, \"include_insights\": false}"

echo.
echo.
echo ========================================
echo Done! Embedding generation started.
echo.
echo The process runs in the background.
echo Check backend logs for progress.
echo.
echo Once complete, try the Mind Map again!
echo ========================================
pause
