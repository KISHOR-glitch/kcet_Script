# KCET Cutoff System - PowerShell Startup Script

Write-Host ""
Write-Host "===================================================="
Write-Host "  KCET Cutoff & PYQ Management System"
Write-Host "  Starting Development Server..."
Write-Host "===================================================="
Write-Host ""

# Set location to script directory
Set-Location -Path $PSScriptRoot

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion"
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH"
    Write-Host "Please install Python 3.8 or higher"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if database exists
if (-not (Test-Path "db.sqlite3")) {
    Write-Host ""
    Write-Host "Database not found. Running initial setup..."
    Write-Host ""
    
    Write-Host "Running migrations..."
    python manage.py migrate
    
    Write-Host ""
    Write-Host "Populating initial data..."
    python manage.py populate_data
}

Write-Host ""
Write-Host "Starting Django development server..."
Write-Host ""
Write-Host "===================================================="
Write-Host "  Server Details:"
Write-Host "  - Application:  http://127.0.0.1:8000/"
Write-Host "  - Login:        http://127.0.0.1:8000/login/"
Write-Host "  - Django Admin: http://127.0.0.1:8000/admin/"
Write-Host "  "
Write-Host "  Press Ctrl+C to stop the server"
Write-Host "===================================================="
Write-Host ""

python manage.py runserver

Read-Host "Press Enter to exit"
