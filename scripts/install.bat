@echo off
echo ==========================================
echo 🚀 Installing BXZ Language
echo ==========================================

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.6+
    pause
    exit /b 1
)

:: Install via pip
echo 📦 Installing Python package...
python -m pip install -e .

:: Create batch file
echo 🔧 Creating bxz.bat...
echo @python "%~dp0bxz.py" %%* > bxz.bat

:: Add to PATH (temporarily)
set "PATH=%PATH%;%CD%"
echo ✅ Added to current session PATH

echo ==========================================
echo ✅ Installation complete!
echo.
echo Usage: bxz ^<file.bxz^>
echo        bxz -i
echo.
echo Note: Restart terminal for PATH changes
echo ==========================================
pause