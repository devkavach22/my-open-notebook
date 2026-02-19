@echo off
echo ========================================
echo Git Repository Setup
echo ========================================
echo.

echo Current remote:
git remote -v
echo.

echo ========================================
echo Instructions:
echo ========================================
echo.
echo 1. Create a new repository on GitHub
echo    Go to: https://github.com/new
echo    Name: open-notebook
echo.
echo 2. Run this command (replace YOUR_USERNAME):
echo    git remote set-url origin https://github.com/YOUR_USERNAME/open-notebook.git
echo.
echo 3. Add and commit your changes:
echo    git add .
echo    git commit -m "Add authentication system"
echo.
echo 4. Push to your repository:
echo    git push -u origin main
echo.
echo ========================================
echo Or use your existing username:
echo ========================================
echo.
echo git remote set-url origin https://github.com/devkavach22/open-notebook.git
echo git add .
echo git commit -m "Add authentication system with signup, login, password reset"
echo git push -u origin main
echo.
pause
