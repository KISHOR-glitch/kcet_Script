# 🎓 KCET Cutoff & PYQ Management System

## Welcome! 👋

Your Django application for KCET cutoff and PYQ management is complete and ready to use.

---

## 📖 Documentation Index

### 🚀 Getting Started
1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick setup guide
2. **[COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)** - Comprehensive guide with all features
3. **[README.md](README.md)** - Full project documentation

### 🛠️ Running the Application

#### **Option 1: Windows Batch File (Easiest)**
```bash
Double-click: run.bat
```

#### **Option 2: PowerShell**
```powershell
.\run.ps1
```

#### **Option 3: Python Script**
```bash
python setup.py
```

#### **Option 4: Manual**
```bash
python manage.py migrate
python manage.py runserver
```

---

## ✨ What's Included

### Backend
- ✅ 7 Database Models (College, Branch, Category, Year, Round, Cutoff, PYQ)
- ✅ 10 Views/Functions (Login, Dashboard, Search, Upload, API)
- ✅ PDF Parser using pdfplumber
- ✅ Admin Dashboard with file upload
- ✅ User authentication & authorization
- ✅ Real-time error tracking

### Frontend
- ✅ 6 HTML Templates (Login, Dashboard, Search, PYQ, Upload)
- ✅ Bootstrap 5 Responsive Design
- ✅ Dynamic JavaScript for dropdown filters
- ✅ Clean, modern UI with animations
- ✅ Mobile-friendly interface

### Database
- ✅ SQLite (configurable to PostgreSQL)
- ✅ Pre-populated with categories, rounds, and years
- ✅ Unique constraints for data integrity
- ✅ Foreign key relationships

### Security
- ✅ Django authentication
- ✅ CSRF protection
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ File upload validation

---

## 🌐 Available URLs

| URL | Purpose | Who Can Access |
|-----|---------|----------------|
| `/` | Home (redirects to login/dashboard) | Anyone |
| `/login/` | User Login | Public |
| `/dashboard/` | Main Dashboard | Logged-in users |
| `/cutoff-search/` | Search Cutoffs | Logged-in users |
| `/upload-pdf/` | Upload Cutoff PDF | Staff/Admin only |
| `/upload-pyq/` | Upload PYQ Papers | Staff/Admin only |
| `/pyqs/` | Browse PYQs | Logged-in users |
| `/admin/` | Django Admin Panel | Staff/Admin only |

---

## 📋 File Structure

```
kcet_Script/
│
├── 📄 README.md                      ← Full documentation
├── 📄 QUICKSTART.md                  ← 5-minute setup guide
├── 📄 COMPLETE_GUIDE.md              ← Comprehensive guide
├── 📄 INDEX.md                       ← This file
│
├── 🚀 run.bat                        ← Windows batch startup
├── 🚀 run.ps1                        ← PowerShell startup
├── 🚀 setup.py                       ← Python setup script
├── 📦 requirements.txt               ← Python dependencies
├── 🧪 test_pdf_parser.py            ← PDF parser testing tool
│
├── 📁 kcet_project/                  ← Django project config
│   ├── settings.py                   ← Settings
│   ├── urls.py                       ← URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── 📁 cutoff/                        ← Main Django app
│   ├── models.py                     ← 7 Database models
│   ├── views.py                      ← 10 Views
│   ├── urls.py                       ← URL patterns
│   ├── forms.py                      ← Form definitions
│   ├── admin.py                      ← Django admin config
│   ├── apps.py
│   ├── tests.py
│   │
│   ├── 📁 utils/
│   │   ├── __init__.py
│   │   └── pdf_parser.py             ← PDF extraction logic
│   │
│   ├── 📁 management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_data.py      ← Initialize data
│   │
│   └── 📁 migrations/
│       └── 0001_initial.py
│
├── 📁 templates/                     ← HTML templates
│   ├── base.html                     ← Base template
│   ├── login.html                    ← Login page
│   ├── dashboard.html                ← Dashboard
│   ├── cutoff_search.html            ← Search page
│   ├── pyq_list.html                 ← PYQ list
│   ├── upload_pdf.html               ← PDF upload
│   └── upload_pyq.html               ← PYQ upload
│
├── 📁 static/                        ← CSS, JS, images
│
├── 📁 media/                         ← User uploads
│   ├── uploads/                      ← PDF uploads
│   └── pyqs/                         ← PYQ papers
│
├── manage.py                         ← Django management
└── db.sqlite3                        ← SQLite database (auto-created)
```

---

## 🎯 Quick Start (30 seconds)

### Step 1: Open Terminal
```bash
# Navigate to project
cd c:\Users\kisho\OneDrive\Desktop\kcet_Script
```

### Step 2: Start Application
**Windows:**
```bash
run.bat
```

**PowerShell:**
```powershell
.\run.ps1
```

**Manual:**
```bash
python manage.py runserver
```

### Step 3: Access Application
```
Login:    http://127.0.0.1:8000/login/
Admin:    http://127.0.0.1:8000/admin/
```

### Step 4: Create Admin Account (First Time Only)
```bash
python manage.py createsuperuser
```

---

## 🔑 Pre-Configured Credentials

The system comes pre-configured with:
- **Categories**: 1G, 1K, 1R, 2AG, 2AK, 2AR, 3BG, 3BK, 3BR, 4G, 4K, 4R, STG, STK, STR, GM
- **Rounds**: Round 1, Round 2, Round 3, Spot Admission
- **Years**: 2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016

No additional setup needed for these!

---

## 📊 Database Models

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **College** | Store colleges | name, city |
| **Branch** | Store branches | name, code |
| **Category** | Store cutoff categories | code, description |
| **Year** | Store academic years | year |
| **Round** | Store counseling rounds | name, round_number |
| **Cutoff** | Main data model | college, branch, category, year, round, cutoff_rank |
| **PYQ** | Store question papers | subject, year, pdf_file |
| **CutoffUploadLog** | Track uploads | status, inserted, updated, errors |

---

## 👤 User Roles

### **Student**
- View cutoffs
- Search with filters
- Download PYQs
- No upload access

### **Admin**
- All student features
- Upload & process PDFs
- Upload PYQs
- Manage all data via admin panel
- View upload logs

---

## 🧪 Testing the System

### 1. Create Admin User
```bash
python manage.py createsuperuser
# username: admin
# password: (your choice)
```

### 2. Create Test Data (via Django Shell)
```bash
python manage.py shell
```

```python
from cutoff.models import *

# Create college
college = College.objects.create(name="Test College", city="Bangalore")

# Create branch
branch = Branch.objects.create(name="Computer Science")

# Create cutoff
year = Year.objects.get(year=2024)
round_obj = Round.objects.get(name="Round 1")
category = Category.objects.get(code="1G")

Cutoff.objects.create(
    college=college,
    branch=branch,
    category=category,
    year=year,
    round=round_obj,
    cutoff_rank="1234"
)

print("✓ Test data created!")
exit()
```

### 3. Test in Browser
1. Login at http://127.0.0.1:8000/login/
2. Go to "Search Cutoffs"
3. Select filters
4. Verify results show "1234" for Test College

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'django'"
```bash
pip install -r requirements.txt
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8001
```

### "Database locked"
```
Restart the server (Ctrl+C, then run again)
```

### "No reverse match" error
```
All URLs should use: {% url 'cutoff:url_name' %}
```

### "Static files not found"
```bash
python manage.py collectstatic --noinput
```

---

## 📚 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [pdfplumber Documentation](https://github.com/jsvine/pdfplumber)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🚀 Next Steps

1. ✅ Run the application
2. ✅ Create admin account
3. ✅ Login and explore
4. ✅ Create test data
5. ✅ Upload a sample PDF
6. ✅ Test cutoff search
7. ✅ Upload PYQ papers
8. ✅ Create student accounts
9. ✅ Test as student user
10. ✅ Review Django admin panel

---

## 💾 Database Backup

```bash
# Export to JSON
python manage.py dumpdata > backup.json

# Import from JSON
python manage.py loaddata backup.json
```

---

## 🔐 Important Security Notes

1. **Change SECRET_KEY** in `settings.py` for production
2. **Set DEBUG = False** in production
3. **Update ALLOWED_HOSTS** with your domain
4. **Use a production database** (PostgreSQL recommended)
5. **Enable HTTPS** for production
6. **Store sensitive data** in environment variables

---

## 📞 Common Questions

**Q: How do I add more colleges?**
A: Via Django admin `/admin/` or by uploading a PDF (auto-creates)

**Q: How do I modify categories?**
A: Via Django admin. The 16 categories are pre-loaded.

**Q: Can I use PostgreSQL instead of SQLite?**
A: Yes, update `DATABASES` in `settings.py`

**Q: How do I reset the database?**
A: Delete `db.sqlite3` and run migrations again

**Q: Where are uploaded files stored?**
A: In the `media/` directory

---

## 📝 Version Information

- **Django Version**: 4.2.7
- **Python Version**: 3.8+
- **Created**: November 2024
- **Status**: Production Ready

---

## ✅ Checklist Before First Use

- [ ] Python 3.8+ installed
- [ ] Requirements installed: `pip install -r requirements.txt`
- [ ] Database migrated: `python manage.py migrate`
- [ ] Initial data populated: `python manage.py populate_data`
- [ ] Superuser created: `python manage.py createsuperuser`
- [ ] Server running: `python manage.py runserver`
- [ ] Can access http://127.0.0.1:8000/login/
- [ ] Can login with admin account
- [ ] Django admin accessible at `/admin/`

---

## 🎉 Ready to Use!

Your KCET Cutoff & PYQ Management System is now complete and ready for deployment!

**Next: Read [QUICKSTART.md](QUICKSTART.md) or [COMPLETE_GUIDE.md](COMPLETE_GUIDE.md)**

---

**For support, refer to the documentation files or check Django documentation.**

Happy cutoff hunting! 🚀
