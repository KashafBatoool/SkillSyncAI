@echo off
REM SkillSync AI Resume Analyzer - Windows Launcher
REM This script installs dependencies and starts the Streamlit app

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  SkillSync AI Resume Analyzer - Launcher               ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo ❌ ERROR: Virtual environment not found (.venv)
    echo.
    echo Please create it first:
    echo   python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo 📦 Checking and installing dependencies...
echo.

REM Install packages
.\.venv\Scripts\pip.exe install streamlit pandas numpy scikit-learn requests fuzzywuzzy python-Levenshtein PyPDF2 python-docx PyMuPDF --no-cache-dir --quiet

if %ERRORLEVEL% neq 0 (
    echo ❌ Package installation failed
    pause
    exit /b 1
)

echo ✅ Packages installed successfully!
echo.
echo 🚀 Launching SkillSync app...
echo.
echo The app will open at: http://localhost:8501
echo.
echo Press Ctrl+C in the terminal to stop the app.
echo.

REM Launch Streamlit
.\.venv\Scripts\python.exe -m streamlit run app/main.py

pause
