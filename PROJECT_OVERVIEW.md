# KCET Cutoff Project - Complete Architecture & Workflow

## 🏗️ PROJECT ARCHITECTURE

### Technology Stack
- **Backend**: Django 4.2.7 (Python Web Framework)
- **Database**: SQLite (Django default)
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **PDF Processing**: pdfplumber (text extraction)
- **Authentication**: Django built-in auth system

---

## 📁 PROJECT STRUCTURE

```
kcet_Script/
├── manage.py                 # Django management script
├── db.sqlite3               # SQLite database
├── requirements.txt         # Python dependencies
│
├── kcet_project/            # Main Django project
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Root URL router
│   ├── wsgi.py              # WSGI app
│
├── cutoff/                  # Main app (cutoff management)
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── urls.py              # App URLs
│   ├── forms.py             # Forms for uploads
│   ├── admin.py             # Django admin config
│   ├── utils/
│   │   ├── pdf_parser.py    # PDF parsing logic
│   │
│   ├── migrations/          # Database migrations
│
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── login.html          # Login page
│   ├── dashboard.html      # Dashboard
│   ├── cutoff_search.html  # Search page
│   ├── upload_pdf.html     # PDF upload page
│   ├── upload_pyq.html     # PYQ upload page
│   ├── pyq_list.html       # PYQ list page
│
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User uploaded files
│   ├── uploads/           # PDF cutoff files
│   ├── pyqs/             # PYQ PDF files
```

---

## 🗄️ DATABASE SCHEMA

### Models & Relationships

```
College (1) ──────────────────────── (Many) Branch
   - id
   - name (unique)
   - city
   - created_at
   
       ↓
       
College ──────────────────────────── Cutoff ──────────────────────── Branch
Branch ──────────────────────────── Cutoff
   
Cutoff (many-to-many bridge)
   - id
   - college_id (FK → College)
   - branch_id (FK → Branch)
   - category_id (FK → Category)
   - year_id (FK → Year)
   - round_id (FK → Round)
   - cutoff_rank
   - created_at/updated_at
   
Category
   - id
   - code (e.g., '1G', '1K', '1R')
   - description
   
Year
   - id
   - year (e.g., 2023, 2024)
   
Round
   - id
   - name (e.g., 'Round 1', 'Round 2')
   - round_number

PYQ (Previous Year Question)
   - id
   - subject
   - year_id (FK → Year)
   - pdf_file
   - created_at/updated_at
   
CutoffUploadLog
   - id
   - uploaded_file
   - status (success/partial/failed)
   - total_rows/inserted_count/updated_count
   - error_message
   - uploaded_by (FK → User)
   - created_at
```

---

## 🔄 WORKFLOW DIAGRAM

### 1️⃣ PDF UPLOAD & PARSING FLOW

```
User uploads PDF
    ↓
View: upload_pdf()
    ↓
PDFParser.parse()
    ├─ Extract text from PDF pages
    ├─ Find college codes (E001, E002, etc.)
    ├─ Extract college names
    ├─ Parse branch data with ranks
    └─ Return structured data (3423 records for sample PDF)
    ↓
save_cutoff_data()
    ├─ Create/get College objects
    ├─ Create/get Branch objects (linked to College)
    ├─ Create/get Category objects
    ├─ Create/update Cutoff records
    └─ Log upload status
    ↓
Return success/failure to user
    ↓
Display in "Recent Uploads" section
```

### 2️⃣ CUTOFF SEARCH FLOW

```
User lands on /cutoff-search/
    ↓
Load initial page
    ├─ GET all colleges from DB
    ├─ GET all categories from DB
    ├─ GET all years from DB
    ├─ GET all rounds from DB
    ├─ Branch dropdown disabled (waiting for college selection)
    ↓
User selects College
    ↓
JavaScript triggered
    ├─ Fetch /api/get-branches/?college_id=X
    ├─ API queries: Branch.objects.filter(college_id=X)
    └─ Return JSON with branches for that college
    ↓
Populate Branch dropdown (enabled)
    ↓
User selects other filters (Category, Year, Round)
    ↓
User clicks "Search"
    ↓
View: cutoff_search()
    ├─ Filter Cutoff records by: college + branch + category + year + round
    ├─ Return matching records
    └─ Display in table
    ↓
Results shown to user
```

### 3️⃣ PYQ MANAGEMENT FLOW

```
Admin: /upload-pyq/
    ├─ Enter subject name
    ├─ Select year
    ├─ Upload PDF file
    └─ Submit
    ↓
create_pyq()
    ├─ Create PYQ object in DB
    ├─ Save file to media/pyqs/
    └─ Redirect to success page
    ↓
Student: /pyqs/
    ├─ View all PYQ papers
    ├─ Download by clicking link
    └─ File served from media/pyqs/
```

---

## 🔐 AUTHENTICATION FLOW

```
Anonymous User
    ↓
Try to access protected page
    ↓
Redirect to /login/
    ↓
Enter username + password
    ↓
Django auth.authenticate()
    ├─ Verify credentials
    ├─ Create session
    └─ Redirect to dashboard
    ↓
Authenticated User
    ├─ Can view cutoff search
    ├─ Can download PYQs
    ├─ If staff: can upload PDFs
    └─ If superuser: can access /admin/
```

---

## 🔧 KEY COMPONENTS EXPLAINED

### 1. PDF PARSER (cutoff/utils/pdf_parser.py)

**What it does:**
- Reads PDF file using pdfplumber
- Extracts text from pages
- Parses college codes and names
- Identifies branch data lines
- Extracts ranks for 21 categories
- Handles multi-line branch names

**Example:**
```
Input PDF Line: "AI Artificial 10087 18087 -- 6918..."
                "Intelligence"

Output:
{
    'college_code': 'E001',
    'college_name': 'University of Visvesvaraya College of Engineering Bangalore',
    'branch_name': 'Artificial Intelligence',
    'category_code': '1G',
    'cutoff_rank': '10087'
}
```

### 2. VIEWS (cutoff/views.py)

**Main Views:**

| View | URL | Purpose |
|------|-----|---------|
| `index_view()` | `/` | Redirect to dashboard/login |
| `login_view()` | `/login/` | User login |
| `logout_view()` | `/logout/` | User logout |
| `dashboard()` | `/dashboard/` | Show statistics |
| `upload_pdf()` | `/upload-pdf/` | Admin: upload cutoff PDF |
| `cutoff_search()` | `/cutoff-search/` | Student: search cutoffs |
| `api_get_branches()` | `/api/get-branches/` | AJAX: get branches for college |
| `api_get_categories()` | `/api/get-categories/` | AJAX: get categories for filters |
| `pyq_list()` | `/pyqs/` | Student: browse PYQ papers |
| `pyq_download()` | `/pyqs/<id>/download/` | Student: download PYQ |

### 3. MODELS (cutoff/models.py)

**Key Relationships:**

1. **College → Branch** (One-to-Many)
   - Each college has multiple branches
   - Branch now has `college` ForeignKey (fixed in latest update)

2. **Branch → Cutoff** (One-to-Many)
   - Each branch can have multiple cutoffs (different categories/years/rounds)

3. **Cutoff** (Many-to-Many Hub)
   - Links: College + Branch + Category + Year + Round
   - Stores the actual cutoff rank
   - Unique constraint ensures no duplicates

---

## 📊 DATA FLOW EXAMPLE

**Scenario: Student searches for cutoff**

```
1. Student selects:
   - College: "University of Visvesvaraya College of Engineering Bangalore"
   - Branch: "Computer Science"
   - Category: "General (1G)"
   - Year: 2023
   - Round: 2

2. Database Query:
   SELECT cutoff_rank 
   FROM cutoff_Cutoff
   WHERE college_id = 1 
     AND branch_id = 3
     AND category_id = 1
     AND year_id = 2023
     AND round_id = 2

3. Result: 
   Cutoff rank = 5809

4. Display in UI:
   "Your cutoff rank for this combination is 5809"
```

---

## 🚀 HOW BRANCH DROPDOWN NOW WORKS (AFTER FIX)

**Before Fix:**
- Branch dropdown showed ALL branches from database
- Filtered by checking if branch had cutoffs for selected college
- Slow and confusing

**After Fix:**
- Branch model has direct `ForeignKey` to College
- Branch dropdown loads only branches belonging to selected college
- Faster query: `Branch.objects.filter(college_id=X)`
- Clean and efficient

```
HTML Load:
<select id="branch">
    <option>Select College First</option>  <!-- Disabled -->
</select>

User selects College:
↓
JavaScript triggers:
fetch('/api/get-branches/?college_id=1')

API Response:
{
    "branches": [
        {"id": 1, "name": "Computer Science"},
        {"id": 2, "name": "Electronics"},
        {"id": 3, "name": "Mechanical"}
    ]
}

Update HTML:
<select id="branch">  <!-- Now enabled -->
    <option>Select Branch</option>
    <option value="1">Computer Science</option>
    <option value="2">Electronics</option>
    <option value="3">Mechanical</option>
</select>
```

---

## 📝 CATEGORY CODES EXPLAINED

The system uses 21 category codes based on:
- **1st/2nd/3rd/4th** = Different category levels
- **A/B** = Subcategories  
- **G/K/R** = Language/Region groups

```
1G  = General (1st) - Kannada + General
1K  = Kannada speakers
1R  = Reserved
2AG = OBC (2nd category A) - General
2AK = OBC (2nd category A) - Kannada
2AR = OBC (2nd category A) - Reserved
... and so on
STG = Special Category - General
STK = Special Category - Kannada
STR = Special Category - Reserved
```

---

## 🔍 HOW TO EXTEND THE PROJECT

### Add New Feature: Export to Excel
```python
# In views.py
from openpyxl import Workbook

def export_cutoffs(request):
    cutoffs = Cutoff.objects.filter(...)
    # Create Excel file
    # Return as download
```

### Add New Model: Admission Results
```python
# In models.py
class AdmissionResult(models.Model):
    college = models.ForeignKey(College, ...)
    student_name = models.CharField(...)
    rank = models.IntegerField()
    allocated_branch = models.ForeignKey(Branch, ...)
    result_date = models.DateField()
```

### Add Notification System
```python
# Email notifications when new cutoffs are uploaded
from django.core.mail import send_mail
```

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| "No cutoff data found" | Check PDF format matches expected structure |
| Branch dropdown empty | Make sure college is selected first; check API endpoint |
| 404 errors on URLs | Check `urls.py` and template URL tags use correct names |
| File upload fails | Check `media/` folder exists and has write permissions |
| Login not working | Run `python manage.py createsuperuser` |
| Static files not loading | Run `python manage.py collectstatic` |

---

## 📚 QUICK REFERENCE

**Management Commands:**
```bash
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply migrations
python manage.py createsuperuser # Create admin account
python manage.py runserver       # Start dev server
python manage.py shell           # Interactive Python shell
python manage.py collectstatic   # Collect static files (production)
```

**Common URLs:**
```
/                    → Home (redirects)
/login/              → Login page
/logout/             → Logout
/dashboard/          → Dashboard
/cutoff-search/      → Search cutoffs
/upload-pdf/         → Upload cutoff PDF (admin)
/upload-pyq/         → Upload PYQ (admin)
/pyqs/               → Browse PYQs
/api/get-branches/   → API endpoint
/api/get-categories/ → API endpoint
/admin/              → Django admin
```

---

## ✅ PROJECT STATUS

- ✅ PDF parsing works correctly
- ✅ College/Branch/Category models properly structured
- ✅ Search functionality working
- ✅ Dynamic branch loading by college
- ✅ Authentication and authorization working
- ✅ PYQ upload and download working
- ✅ Upload logging working

**Next improvements:**
- [ ] Export search results to Excel
- [ ] Advanced filters (city, rank range, etc.)
- [ ] Comparison tool (compare cutoffs across years)
- [ ] Analytics dashboard
- [ ] Email notifications
