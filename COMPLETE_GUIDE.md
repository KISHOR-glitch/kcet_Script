# KCET Cutoff & PYQ System - Complete Setup & Usage Guide

## ✅ Application Successfully Created!

Your KCET Cutoff & PYQ Management System is ready to use. This document provides complete setup and usage instructions.

---

## 🚀 Quick Start (30 seconds)

### Option 1: Using Setup Script (Recommended)
```bash
cd c:\Users\kisho\OneDrive\Desktop\kcet_Script
python setup.py
```

### Option 2: Manual Setup
```bash
cd c:\Users\kisho\OneDrive\Desktop\kcet_Script

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate
python manage.py populate_data

# Create admin user
python manage.py createsuperuser

# Run server
python manage.py runserver
```

After running, visit: **http://127.0.0.1:8000/**

---

## 📚 Application Structure

```
kcet_Script/
├── kcet_project/              # Main Django project settings
├── cutoff/                    # Main Django app
│   ├── models.py              # Database models (7 models)
│   ├── views.py               # View functions (10 views)
│   ├── urls.py                # URL routing
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Django admin configuration
│   ├── utils/
│   │   └── pdf_parser.py      # PDF extraction logic
│   └── management/
│       └── commands/
│           └── populate_data.py
├── templates/                 # HTML templates (6 templates)
│   ├── base.html              # Base template with navbar
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard
│   ├── cutoff_search.html     # Cutoff search with filters
│   ├── pyq_list.html          # PYQ browsing
│   ├── upload_pdf.html        # PDF upload (admin)
│   └── upload_pyq.html        # PYQ upload (admin)
├── static/                    # Static files (CSS, JS)
├── media/                     # User uploads
├── manage.py                  # Django management
├── db.sqlite3                 # SQLite database
├── requirements.txt           # Python dependencies
├── README.md                  # Full documentation
├── QUICKSTART.md              # Quick start guide
└── setup.py                   # Setup script
```

---

## 🎯 Key URLs

| URL | Purpose | Access |
|-----|---------|--------|
| `/` | Index (redirects to login or dashboard) | Public |
| `/login/` | Login page | Public |
| `/dashboard/` | Dashboard | Authenticated users |
| `/cutoff-search/` | Search cutoffs | Authenticated users |
| `/upload-pdf/` | Upload cutoff PDF | Staff only |
| `/upload-pyq/` | Upload PYQ papers | Staff only |
| `/pyqs/` | Browse/download PYQs | Authenticated users |
| `/api/get-branches/` | API for dynamic filters | Authenticated users |
| `/api/get-categories/` | API for dynamic filters | Authenticated users |
| `/admin/` | Django admin panel | Staff only |

---

## 🗄️ Database Models

### 1. **College**
```
- name (unique string)
- city (string)
- created_at, updated_at (timestamps)
```

### 2. **Branch**
```
- name (unique string)
- code (optional string)
- created_at, updated_at (timestamps)
```

### 3. **Category**
```
- code (unique string) e.g., "1G", "2AG"
- description (string)
- created_at, updated_at (timestamps)
```

### 4. **Year**
```
- year (unique integer)
- created_at, updated_at (timestamps)
```

### 5. **Round**
```
- name (unique string)
- round_number (optional integer)
- created_at, updated_at (timestamps)
```

### 6. **Cutoff** (Main Model)
```
- college (FK to College)
- branch (FK to Branch)
- category (FK to Category)
- year (FK to Year)
- round (FK to Round)
- cutoff_rank (string, nullable)
- created_at, updated_at (timestamps)
- Unique constraint: college + branch + category + year + round
```

### 7. **PYQ**
```
- subject (string)
- year (FK to Year)
- pdf_file (file upload)
- created_at, updated_at (timestamps)
- Unique constraint: subject + year
```

### 8. **CutoffUploadLog** (Tracking)
```
- uploaded_file (file)
- status (success/partial/failed)
- total_rows (integer)
- inserted_count (integer)
- updated_count (integer)
- error_message (text)
- uploaded_by (FK to User)
- created_at (timestamp)
```

---

## 👥 User Roles

### **Student/User**
- ✅ Login/Logout
- ✅ View Dashboard
- ✅ Search Cutoffs with filters
- ✅ Browse and download PYQs
- ❌ Cannot upload files

### **Staff/Admin**
- ✅ All student features +
- ✅ Upload and process cutoff PDFs
- ✅ Upload PYQ papers
- ✅ Access Django admin panel
- ✅ Manage all data
- ✅ View upload logs

---

## 📊 Features

### Student Features
1. **Cutoff Search**
   - Filter by College, Branch, Category, Year, Round
   - Dynamic dropdown loading
   - Real-time result display
   - Clean table view of ranks

2. **PYQ Management**
   - Browse papers by year and subject
   - Search functionality
   - One-click download
   - Organized file structure

### Admin Features
1. **PDF Processing**
   - Upload cutoff PDFs
   - Automatic table extraction (pdfplumber)
   - Automatic data parsing and validation
   - Database insertion/update
   - Real-time feedback
   - Upload history tracking

2. **PYQ Upload**
   - Upload previous year papers
   - Organize by subject and year
   - Manage uploaded files

3. **Data Management**
   - Django admin interface
   - Edit/delete records
   - Bulk operations
   - Search and filtering

---

## 📄 PDF Upload Format

### Expected PDF Structure:

```
┌─────────────────────────────────────────────────────────┐
│ College: Sri Chaitanya College of Engineering           │
└─────────────────────────────────────────────────────────┘

┌──────────────────────┬─────┬─────┬─────┬────────┬──────┐
│ Course Name          │ 1G  │ 1K  │ 1R  │ 2AG    │ 2AK  │
├──────────────────────┼─────┼─────┼─────┼────────┼──────┤
│ B.Sc Hons Commerce   │1234 │ --  │5678 │  890   │ --   │
│ B.Sc Hons Science    │2345 │3456 │4567 │ 1234   │ 2345 │
│ B.A Hons             │3456 │4567 │ --  │ 2345   │ 3456 │
└──────────────────────┴─────┴─────┴─────┴────────┴──────┘
```

### Requirements:
- PDF must have "College: Name" in header
- First column: Course/Branch names
- Header row: Category codes (1G, 1K, 1R, 2AG, 2AK, 2AR, 3BG, etc.)
- Data cells: Ranks as numbers
- Use "--" for N/A values
- One PDF per college, year, round combination

### Supported Categories:
```
1G, 1K, 1R     - 1st Round (General, Kannada, Reserved)
2AG, 2AK, 2AR  - 2nd Round OBC (General, Kannada, Reserved)
3BG, 3BK, 3BR  - 3rd Round SC (General, Kannada, Reserved)
4G, 4K, 4R     - 4th Round ST (General, Kannada, Reserved)
STG, STK, STR  - Special Categories (General, Kannada, Reserved)
GM             - General Merit
```

---

## 🔐 Security Features

- ✅ Django authentication with username/password
- ✅ Login required for all features
- ✅ Staff-only access for admin functions
- ✅ CSRF protection on all forms
- ✅ File upload validation (PDF only, max 50MB)
- ✅ SQL injection prevention (ORM queries)
- ✅ XSS protection (template auto-escaping)
- ✅ Session management
- ✅ User permission checking on every request

---

## 🛠️ Useful Commands

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Populate initial data
python manage.py populate_data

# Collect static files
python manage.py collectstatic

# Database backup
python manage.py dumpdata > backup.json

# Database restore
python manage.py loaddata backup.json

# Run tests
python manage.py test

# Clear database (WARNING!)
python manage.py flush
```

---

## 🐛 Troubleshooting

### Problem: "No reverse match" error
**Solution:** Make sure URL names use the app namespace `cutoff:url_name`

### Problem: PDF upload fails
**Solution:** 
1. Verify PDF has "College:" header
2. Check table has course names and category codes
3. Ensure proper table formatting

### Problem: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

### Problem: Database locked
**Solution:** Restart Django server (Ctrl+C, then `python manage.py runserver`)

### Problem: Can't login
**Solution:**
```bash
python manage.py createsuperuser
```

### Problem: Port 8000 already in use
**Solution:**
```bash
python manage.py runserver 8001
```

---

## 📈 Performance Tips

1. **Database**: SQLite is fine for small-to-medium deployments
2. **PDF Processing**: Upload PDFs during off-peak hours
3. **Search**: Use filters to reduce query results
4. **Static Files**: Browser caching enabled for CSS/JS
5. **Cleanup**: Periodically delete old upload logs

---

## 🚢 Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Generate new `SECRET_KEY`
4. Use PostgreSQL instead of SQLite
5. Configure environment variables
6. Enable HTTPS
7. Set up static file serving (Nginx/AWS S3)
8. Configure email backend for notifications
9. Run security check:
   ```bash
   python manage.py check --deploy
   ```

---

## 📞 Support & FAQ

**Q: How do I add more admin users?**
A: Via Django shell or admin panel. New users can't access admin until `is_staff=True`.

**Q: Can students change their passwords?**
A: Currently no. Admin must create/reset via admin panel.

**Q: How often should I update cutoff data?**
A: After each counseling round (typically every 1-2 weeks during admission season).

**Q: Can I edit cutoff data manually?**
A: Yes, via Django admin panel at `/admin/`.

**Q: How do I backup the database?**
A: Copy `db.sqlite3` or use: `python manage.py dumpdata > backup.json`

**Q: Can multiple PDFs be uploaded at once?**
A: Currently no, upload one at a time. Multiple uploads are queued.

---

## 📊 Sample Test Data

The system includes pre-populated:
- ✅ 16 Categories (1G, 1K, 1R, 2AG, etc.)
- ✅ 4 Rounds (Round 1, Round 2, Round 3, Spot Admission)
- ✅ 10 Years (2025 back to 2016)

You can add colleges and branches via:
1. Django admin (`/admin/`)
2. Direct PDF upload (auto-creates colleges)
3. Management shell

---

## 🎓 Next Steps

1. ✅ Create admin user
2. ✅ Run server: `python manage.py runserver`
3. ✅ Login at http://127.0.0.1:8000/login/
4. ✅ Upload sample PDF to test
5. ✅ Create student test account
6. ✅ Test cutoff search
7. ✅ Upload PYQ papers

---

## 📝 Version Info

- **Django**: 4.2.7
- **Python**: 3.8+
- **Database**: SQLite (default)
- **Frontend**: Bootstrap 5
- **Created**: November 2024

---

## ✨ Features Implemented

- ✅ Complete Django app structure
- ✅ 7 database models with relationships
- ✅ User authentication & authorization
- ✅ PDF parsing with pdfplumber
- ✅ Dynamic dropdown filters (AJAX)
- ✅ Responsive Bootstrap UI
- ✅ Admin panel with file upload
- ✅ PYQ management
- ✅ Upload logging & tracking
- ✅ Comprehensive error handling
- ✅ Complete documentation

---

**Ready to use! Happy cutoff hunting! 🎉**
