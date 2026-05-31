# SkillSync AI Resume Analyzer - PowerShell Launcher
# Run this script to install dependencies and launch the app

Clear-Host

Write-Host "`n" -ForegroundColor White
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  SkillSync AI Resume Analyzer - Launcher              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Check if .venv exists
if (-not (Test-Path ".\.venv")) {
    Write-Host "❌ ERROR: Virtual environment not found (.venv)" -ForegroundColor Red
    Write-Host "`nPlease create it first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv`n" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "📦 Checking and installing dependencies...`n" -ForegroundColor Cyan

# Install packages
& ".\.venv\Scripts\pip.exe" install streamlit pandas numpy scikit-learn requests fuzzywuzzy python-Levenshtein PyPDF2 python-docx PyMuPDF --no-cache-dir --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Package installation failed" -ForegroundColor Red
    Read-Host "`nPress Enter to exit"
    exit 1
}

Write-Host "✅ Packages installed successfully!`n" -ForegroundColor Green
Write-Host "🚀 Launching SkillSync app...`n" -ForegroundColor Green
Write-Host "The app will open at: http://localhost:8501" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in the terminal to stop the app.`n" -ForegroundColor White

# Launch Streamlit
& ".\.venv\Scripts\python.exe" -m streamlit run app/main.py

Read-Host "`nPress Enter when done"
