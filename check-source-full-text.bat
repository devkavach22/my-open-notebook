@echo off
cd /d "%~dp0"

echo Checking source full_text in database...
echo.

docker exec -i open-notebook-surrealdb-1 /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook < check-query.sql

pause
