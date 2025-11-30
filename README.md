# KCET Cutoff & PYQ Management System

A comprehensive Django application for managing KCET (Karnataka Examination Authority) cutoff data and Previous Year Question (PYQ) papers.

## Features

### 📋 Core Features
- **PDF-Based Cutoff Management**: Extract cutoff data from PDF files using pdfplumber
- **Dynamic Search Filters**: Search cutoffs by College, Branch, Category, Year, and Round
- **PYQ Management**: Upload and download previous year question papers
- **Responsive Design**: Bootstrap 5-based responsive UI
- **Admin Dashboard**: Comprehensive Django admin interface

### 👥 User Roles
- **Students**: Search cutoffs, download PYQs
- **Admin**: Upload and process cutoff PDFs, upload PYQs, manage all data

### 🔐 Security
- Django authentication with login/logout
- Staff-only access for admin features
- CSRF protection
- Secure file upload with validation

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual Environment (recommended)

### Step 1: Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### Step 2: Install Dependencies
```bash
pip install django pdfplumber pandas camelot-py openpyxl
```

### Step 3: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py populate_data
```

### Step 4: Create Superuser
```bash
python manage.py createsuperuser
```
Follow prompts to create admin account.

### Step 5: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/login/`

## Usage

### For Students
1. **Login**: Use your username and password
2. **Dashboard**: View system statistics
3. **Search Cutoffs**:
   - Select College → Branch → Category → Year → Round
   - Click "Search" to see results
4. **Download PYQs**: Browse and download subject-wise papers

### For Admin
1. **Login** with admin account
2. **Dashboard**: Access admin panel from dropdown menu
3. **Upload Cutoff PDF**:
   - Select PDF file (see PDF Format below)
   - Choose Academic Year and Round
   - Click "Upload & Process"
   - System automatically extracts data and shows results
4. **Upload PYQ**:
   - Enter subject name
   - Select year
   - Upload PDF file
5. **Django Admin** (`/admin/`):
   - Manage all models directly
   - Edit/delete records
   - View upload logs

## PDF Format Specification

### Expected PDF Structure
```
PAGE 1 HEADER:
College: Sri Chaitanya College of Engineering

TABLE FORMAT:
┌─────────────────────┬──────┬──────┬──────┬────────┐
│ Course Name         │  1G  │  1K  │  1R  │  2AG   │
├─────────────────────┼──────┼──────┼──────┼────────┤
│ B.Sc Hons Commerce  │21266 │  --  │ 45891│ 18939  │
│ B.Sc Hons Science   │ 5234 │ 8934 │ 12345│  4521  │
│ B.A Hons            │ 3421 │ 5678 │  --  │  2890  │
└─────────────────────┴──────┴──────┴──────┴────────┘

Notes:
- First column: Course/Branch names
- Header row: Category codes (1G, 1K, 1R, 2AG, 2AK, etc.)
- Data cells: Cutoff ranks as numbers
- Use "--" for N/A values
- One PDF per college, per year, per round
```

### Supported Category Codes
- `1G`, `1K`, `1R` - 1st Round categories
- `2AG`, `2AK`, `2AR` - 2nd Round OBC categories
- `3BG`, `3BK`, `3BR` - 3rd Round SC categories
- `4G`, `4K`, `4R` - 4th Round ST categories
- `STG`, `STK`, `STR` - Special Categories
- `GM` - General Merit

## Project Structure

```
kcet_Script/
├── kcet_project/           # Main Django project
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── cutoff/                 # Django app
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   ├── admin.py            # Django admin config
│   ├── utils/
│   │   └── pdf_parser.py   # PDF extraction logic
│   └── management/
│       └── commands/
│           └── populate_data.py
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── cutoff_search.html
│   ├── pyq_list.html
│   ├── upload_pdf.html
│   └── upload_pyq.html
│
├── static/                 # CSS, JS, images
├── media/                  # User uploads
├── manage.py
└── db.sqlite3              # SQLite database
```

## Database Models

### College
- `name` (CharField, unique)
- `city` (CharField)

### Branch
- `name` (CharField, unique)
- `code` (CharField, blank)

### Category
- `code` (CharField, unique) - e.g., "1G", "2AG"
- `description` (CharField)

### Year
- `year` (IntegerField, unique)

### Round
- `name` (CharField, unique)
- `round_number` (IntegerField)

### Cutoff
- `college` (ForeignKey to College)
- `branch` (ForeignKey to Branch)
- `category` (ForeignKey to Category)
- `year` (ForeignKey to Year)
- `round` (ForeignKey to Round)
- `cutoff_rank` (CharField, nullable)

### PYQ
- `subject` (CharField)
- `year` (ForeignKey to Year)
- `pdf_file` (FileField)

### CutoffUploadLog
- `uploaded_file` (FileField)
- `status` (CharField: success/partial/failed)
- `total_rows` (IntegerField)
- `inserted_count` (IntegerField)
- `updated_count` (IntegerField)
- `error_message` (TextField)
- `uploaded_by` (ForeignKey to User)

## API Endpoints

### For Dynamic Filters
- `GET /api/get-branches/?college_id=<id>` - Get branches for a college
- `GET /api/get-categories/?college_id=<id>&branch_id=<id>` - Get categories

## Troubleshooting

### PDF Parsing Errors
- Ensure PDF has table data with course names and category codes
- Check that "College: Name" is present in header
- Verify category column headers match expected codes

### Database Issues
```bash
python manage.py migrate --fake-initial  # If schema conflicts
python manage.py migrate cutoff zero     # Reverse migrations
```

### File Upload Issues
- Check `MEDIA_ROOT` in settings.py
- Ensure media directory has write permissions
- Verify file size doesn't exceed 50MB limit

## Performance Tips

1. **Batch PDF Processing**: Upload PDFs during off-peak hours
2. **Database Indexing**: Ensure indexes on frequently searched fields
3. **Caching**: Consider caching cutoff search results
4. **Cleanup**: Remove old upload logs periodically

## Future Enhancements

- [ ] Email notifications for new cutoff data
- [ ] Export cutoff data to Excel
- [ ] Student comparison tool (multiple colleges)
- [ ] Cutoff trend analysis
- [ ] Mobile app integration
- [ ] REST API with authentication
- [ ] Bulk PDF processing

## Support & Contact

For issues or questions:
1. Check the FAQ section below
2. Review PDF format specification
3. Check Django admin for data accuracy

## FAQ

**Q: How often should I update cutoff data?**
A: Typically after each counseling round. Once per round is recommended.

**Q: Can I edit cutoff data manually?**
A: Yes, use Django admin (`/admin/`) to edit individual records.

**Q: What if PDF extraction fails?**
A: Check PDF format, ensure college header is present, and try re-uploading.

**Q: How do I backup the database?**
A: Copy `db.sqlite3` file to a safe location.

**Q: Can students modify their login passwords?**
A: Add password change functionality via Django's contrib.auth views.

## License

This project is provided as-is for KCET cutoff management purposes.

---

**Last Updated**: November 2024
**Version**: 1.0
**Author**: KCET Management System Team
