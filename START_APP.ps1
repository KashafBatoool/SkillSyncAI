# SkillSync AI Resume Analyzer - PowerShell Startup Script
# This script reliably starts the Streamlit app and keeps it running

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗"
Write-Host "║  SkillSync - Starting Application                     ║"
Write-Host "╚════════════════════════════════════════════════════════╝"
Write-Host ""

# Change to the project directory
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectPath

# Check if .venv exists
if (-not (Test-Path ".venv")) {
    Write-Host "❌ ERROR: Virtual environment not found"
    Write-Host "Creating .venv..."
    py -3 -m venv .venv
    Write-Host "✅ Virtual environment created"
}

# Clear old Streamlit cache to prevent errors
Write-Host "🧹 Clearing cache..."
if (Test-Path ".streamlit") {
    Remove-Item -Force -Recurse ".streamlit" -ErrorAction SilentlyContinue
}
if (Test-Path "__pycache__") {
    Remove-Item -Force -Recurse "__pycache__" -ErrorAction SilentlyContinue
}
if (Test-Path "app/__pycache__") {
    Remove-Item -Force -Recurse "app/__pycache__" -ErrorAction SilentlyContinue
}
if (Test-Path "modules/__pycache__") {
    Remove-Item -Force -Recurse "modules/__pycache__" -ErrorAction SilentlyContinue
}
Write-Host "✅ Cache cleared"

# Start the app
Write-Host "🚀 Starting SkillSync app..."
Write-Host ""

# Run in background
$process = Start-Process -FilePath ".\.venv\Scripts\python.exe" `
    -ArgumentList "-m streamlit run app/main.py --server.port=8501" `
    -PassThru

# Wait a moment for the server to start
Start-Sleep -Seconds 3

# Try to open browser
try {
    Start-Process "http://localhost:8501"
} catch {
    Write-Host "Could not open browser automatically"
}

Write-Host ""
Write-Host "✅ App started successfully!"
Write-Host "📱 Browser should open automatically at: http://localhost:8501"
Write-Host "🔗 If not, manually visit: http://localhost:8501"
Write-Host ""
Write-Host "💡 Tip: Keep this window open. Close it to stop the app."
Write-Host ""

# Keep the process alive
Wait-Process -Id $process.Id
