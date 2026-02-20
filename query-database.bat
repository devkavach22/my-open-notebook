@echo off
echo ========================================
echo SurrealDB Query Interface
echo ========================================
echo.
echo Connection Details:
echo   Database: open_notebook
echo   Namespace: open_notebook
echo   User: root
echo.
echo Type your SQL queries and press Enter
echo Type 'exit' to quit
echo ========================================
echo.

docker exec -it open-notebook-surrealdb-1 surreal sql --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook --pretty

echo.
echo Disconnected from database.
pause
