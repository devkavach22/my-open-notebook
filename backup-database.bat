@echo off
echo ========================================
echo   Backup SurrealDB Database
echo ========================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Create backup filename with timestamp
set timestamp=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
set filename=backup_%timestamp%.surql

echo Creating backup: %filename%
echo.

docker compose exec -T surrealdb /surreal export --endpoint http://localhost:8000 --username root --password root --namespace open_notebook --database open_notebook > %filename%

echo.
echo ========================================
echo   Backup completed!
echo ========================================
echo.
echo File: %filename%
echo Location: %cd%
echo.
pause
