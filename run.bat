@echo off
REM KCET Cutoff System - Quick Start Batch Script
REM This file starts the Django development server

echo.
echo ====================================================
echo  KCET Cutoff ^& PYQ Management System
echo  Starting Development Server...
echo ====================================================
echo.

REM Navigate to project directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if migrations need to be run
if not exist "db.sqlite3" (
    echo Database not found. Running migrations...
    python manage.py migrate
    python manage.py populate_data
)

REM Start the server
echo.
echo Starting Django development server...
echo.
echo ====================================================
echo  Server Details:
echo  - Application:  http://127.0.0.1:8000/
echo  - Login:        http://127.0.0.1:8000/login/
echo  - Django Admin: http://127.0.0.1:8000/admin/
echo  
echo  Press Ctrl+C to stop the server
echo ====================================================
echo.

python manage.py runserver

pause
