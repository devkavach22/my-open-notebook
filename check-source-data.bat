@echo off
cd /d "%~dp0"

echo ========================================
echo Checking Source Data in SurrealDB
echo ========================================
echo.

echo 1. Checking source table:
echo.
docker exec -it open-notebook-surrealdb-1 /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --pretty "SELECT id, title, asset, full_text FROM source;"

echo.
echo ========================================
echo 2. Checking source_embedding table:
echo.
docker exec -it open-notebook-surrealdb-1 /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --pretty "SELECT id, source, content FROM source_embedding LIMIT 5;"

echo.
echo ========================================
echo 3. Checking command status:
echo.
docker exec -it open-notebook-surrealdb-1 /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --pretty "SELECT id, status, error FROM command WHERE type = 'embedding';"

echo.
echo ========================================
pause
