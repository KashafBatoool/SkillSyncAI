@echo off
REM SkillSync - Health Check Script
REM Verifies all dependencies and configurations before starting the app

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  SkillSync - System Health Check                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    goto error
) else (
    echo ✅ Python is installed
)

REM Check virtual environment
echo [2/5] Checking virtual environment...
if not exist ".venv" (
    echo ⚠️  Virtual environment not found, creating...
    py -3 -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        goto error
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

REM Check Streamlit
echo [3/5] Checking Streamlit...
.\.venv\Scripts\python.exe -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Streamlit not found, installing...
    .\.venv\Scripts\pip.exe install streamlit -q
    if errorlevel 1 (
        echo ❌ Failed to install Streamlit
        goto error
    )
    echo ✅ Streamlit installed
) else (
    echo ✅ Streamlit is installed
)

REM Check main app file
echo [4/5] Checking app files...
if not exist "app\main.py" (
    echo ❌ app\main.py not found
    goto error
) else (
    echo ✅ App files exist
)

REM Check port availability
echo [5/5] Checking port 8501...
netstat -ano | findstr :8501 >nul 2>&1
if not errorlevel 1 (
    echo ⚠️  Port 8501 is already in use
    echo    Attempting to use port 8502 instead...
    set PORT=8502
) else (
    echo ✅ Port 8501 is available
    set PORT=8501
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  ✅ All checks passed! Starting app...                ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Clear cache
rmdir /s /q .streamlit 2>nul
rmdir /s /q __pycache__ 2>nul
rmdir /s /q app\__pycache__ 2>nul
rmdir /s /q modules\__pycache__ 2>nul

REM Start the app
.\.venv\Scripts\python.exe -m streamlit run app/main.py --server.port=!PORT!
exit /b 0

:error
echo.
echo ❌ Health check failed!
echo Please fix the issues above and try again.
echo.
pause
exit /b 1
