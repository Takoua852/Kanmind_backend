@echo off
git pull
git add .
git commit -m "%*"
git push

echo.
echo --------------------------------------------------
echo Deployment gestartet!
echo Deine Seite: https://kanmind-backend-rtam.onrender.com
echo --------------------------------------------------
echo.
pause