@echo off
echo ========================================
echo   Connecting to SurrealDB
echo ========================================
echo.
echo Connection Details:
echo   Host: localhost:8000
echo   Namespace: open_notebook
echo   Database: open_notebook
echo   Username: root
echo.
echo Type 'exit' or press Ctrl+C to quit
echo.

REM Navigate to project directory
cd /d "%~dp0"

docker compose exec surrealdb /surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook
