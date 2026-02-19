@echo off
REM View all users in the database

echo Connecting to SurrealDB...
echo.

docker exec -it open-notebook-surrealdb-1 /bin/sh -c "echo 'SELECT * FROM user;' | surreal sql --conn http://localhost:8000 --user root --pass root --ns open_notebook --db open_notebook --pretty"

echo.
pause
