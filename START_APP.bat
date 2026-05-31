@echo off
REM SkillSync AI Resume Analyzer - Startup Script
REM This script reliably starts the Streamlit app and keeps it running

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  SkillSync - Starting Application                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Change to the project directory
cd /d "%~dp0"

REM Check if .venv exists
if not exist ".venv" (
    echo ❌ ERROR: Virtual environment not found
    echo Creating .venv...
    py -3 -m venv .venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment and start the app
echo 🚀 Starting SkillSync app...
echo.

REM Start in new window so it doesn't block
start cmd /k ".venv\Scripts\python.exe -m streamlit run app/main.py --server.port=8501"

timeout /t 3

REM Try to open browser (optional)
echo Opening browser...
start http://localhost:8501

echo.
echo ✅ App started successfully!
echo 📱 Browser should open automatically
echo 🔗 If not, visit: http://localhost:8501
echo.
echo Press any key to close this window...
pause >nul
