@echo off
echo ========================================
echo   BXZ - Professional Build
echo ========================================

:: ساخت آیکون
python setup_icon.py

:: بیلد
pyinstaller --onefile --name bxz --console --icon=bxz.ico ^
    --add-data "web;web" ^
    --add-data "examples;examples" ^
    --add-data "polyglot;polyglot" ^
    --add-data "templates;templates" ^
    --add-data "api;api" ^
    --add-data "scripts;scripts" ^
    --hidden-import=json ^
    --hidden-import=re ^
    --hidden-import=subprocess ^
    --hidden-import=http.server ^
    --hidden-import=urllib.parse ^
    bxz.py

echo.
echo ✅ Done: dist\bxz.exe
dist\bxz.exe --version
pause