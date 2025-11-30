#!/usr/bin/env python
"""
KCET Cutoff System - Setup & Run Script
This script helps set up and run the Django application
"""

import os
import sys
import subprocess
import platform


def run_command(cmd, description=""):
    """Run a shell command"""
    if description:
        print(f"\n{'='*70}")
        print(f"📌 {description}")
        print(f"{'='*70}")
    
    try:
        result = subprocess.run(cmd, shell=True, cwd=os.getcwd())
        if result.returncode != 0:
            print(f"❌ Command failed with exit code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Main setup function"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║  KCET Cutoff & PYQ Management System - Setup           ║
    ║  Version 1.0                                           ║
    ╚════════════════════════════════════════════════════════╝
    """)

    print("\n📋 Checking prerequisites...")
    
    # Check if Python is available
    try:
        py_version = subprocess.check_output("python --version", shell=True).decode().strip()
        print(f"✅ {py_version}")
    except:
        print("❌ Python not found. Please install Python 3.8+")
        return

    # Check if Django is installed
    try:
        subprocess.check_output("python -c \"import django\"", shell=True)
        print("✅ Django installed")
    except:
        print("❌ Django not installed. Running: pip install -r requirements.txt")
        run_command("pip install -r requirements.txt", "Installing dependencies")

    print("\n🔧 Setting up database...")
    run_command("python manage.py makemigrations", "Creating migrations")
    run_command("python manage.py migrate", "Applying migrations")
    run_command("python manage.py populate_data", "Populating initial data")

    print("\n👤 Creating superuser account...")
    try:
        from django.contrib.auth.models import User
        if User.objects.filter(username='admin').exists():
            print("✅ Admin user already exists")
        else:
            print("No admin user found. Creating superuser...")
            run_command("python manage.py createsuperuser", "Create superuser")
    except:
        run_command("python manage.py createsuperuser", "Create superuser")

    print("\n🚀 Starting development server...")
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║  Development Server Starting                           ║
    ║                                                        ║
    ║  📱 Application:  http://127.0.0.1:8000/              ║
    ║  🔑 Login:        http://127.0.0.1:8000/login/        ║
    ║  ⚙️  Admin:       http://127.0.0.1:8000/admin/        ║
    ║                                                        ║
    ║  Press Ctrl+C to stop the server                      ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    run_command("python manage.py runserver", "Running development server")


if __name__ == '__main__':
    main()
