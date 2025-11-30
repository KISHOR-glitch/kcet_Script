# 🏗️ SAHA Application Architecture Explained

## **What is SAHA?**
SAHA is a Django web application that helps students find KCET (Karnataka Entrance Test) college cutoff scores and access previous year question papers.

---

## **How It's Built - The Stack**

### **Backend (Server-Side)**
```
Python 3.13
├── Django 4.2.7 (Web Framework)
├── SQLite (Database)
└── pdfplumber (PDF Parser for cutoff extraction)
```

### **Frontend (User Interface)**
```
HTML/CSS/JavaScript
├── Bootstrap 5 (Responsive Design)
├── Font Awesome (Icons)
└── Apple.com Design Theme (Blue color scheme)
```

---

## **Database Structure (Models.py)**

Think of models as **tables in a spreadsheet**:

### **1. College Model**
```
College
├── name (e.g., "BMS Institute of Technology")
├── city (e.g., "Bangalore")
├── branches (List of branches offered)
└── cutoffs (All cutoff scores for this college)
```

### **2. Branch Model**
```
Branch
├── college (FK: Which college it belongs to)
├── name (e.g., "Computer Science")
├── code (e.g., "CS")
└── cutoffs (Cutoff scores for this branch)
```

### **3. Category Model**
```
Category
├── code (e.g., "1G" - General category)
├── description (e.g., "General Category Round 1")
└── cutoffs (Scores for this category)
```

### **4. Year Model**
```
Year
├── year (e.g., 2023)
└── cutoffs (All cutoffs from this year)
```

### **5. Round Model**
```
Round
├── name (e.g., "Round 1", "Round 2")
├── round_number (Integer for ordering)
└── cutoffs (Scores for this round)
```

### **6. Cutoff Model** (Main Data)
```
Cutoff
├── college (FK to College)
├── branch (FK to Branch)
├── category (FK to Category)
├── year (FK to Year)
├── round (FK to Round)
└── cutoff_rank (The actual score, e.g., "500")
```

**Example:** "BMS College → CS Branch → General (1G) → 2023 → Round 1 → Rank 500"

### **7. PYQ Model**
```
PYQ (Previous Year Questions)
├── subject (e.g., "Physics")
├── year (e.g., 2023)
├── pdf_file (PDF document)
└── uploaded_by (User who uploaded)
```

---

## **How Data Flows - The Journey**

### **Step 1: PDF Upload**
```
Admin uploads PDF file
    ↓
PDF Parser reads the file (pdfplumber library)
    ↓
Extracts college names, branches, cutoff scores
    ↓
Creates/Updates database records
    ↓
Data is now searchable!
```

### **Step 2: User Registration**
```
User goes to /register/
    ↓
Enters username & password
    ↓
Django's UserCreationForm validates
    ↓
Password is hashed (encrypted)
    ↓
User saved in database
    ↓
User can login now
```

### **Step 3: User Search**
```
User selects College → Branch → Category → Year → Round
    ↓
JavaScript sends request to server (AJAX)
    ↓
Server queries database: 
   "Give me cutoffs WHERE college=X AND branch=Y..."
    ↓
Database returns matching records
    ↓
Results display on page instantly (no page refresh)
```

---

## **File Structure Explanation**

### **Main Folders:**

```
kcet_Script/
├── kcet_project/          # Django project settings
│   ├── settings.py        # Database, apps, security config
│   ├── urls.py            # Main URL router
│   └── wsgi.py            # Web server interface
│
├── cutoff/                # Main app
│   ├── models.py          # Database tables (↑ explained above)
│   ├── views.py           # Logic for each page
│   ├── urls.py            # URL routes (/login, /register, etc.)
│   ├── forms.py           # Form validation
│   └── utils/
│       └── pdf_parser.py  # PDF extraction logic
│
├── templates/             # HTML pages
│   ├── base.html          # Main template (navbar, footer)
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Home page
│   └── ...
│
├── static/                # CSS, JavaScript, images
│   ├── css/
│   └── js/
│
├── db.sqlite3             # Database file (all data)
├── manage.py              # Django command tool
└── requirements.txt       # Python packages needed
```

---

## **How Views Work (views.py)**

Views are Python functions that handle requests:

```python
def login_view(request):
    # If user already logged in → go to dashboard
    if request.user.is_authenticated:
        return redirect('cutoff:dashboard')
    
    # If form submitted (POST)
    if request.method == 'POST':
        # Check username & password
        # If correct → login user
        # If wrong → show error
    
    # Show login page (GET)
    return render(request, 'login.html', {'form': form})
```

**Key Views in Your App:**
- `login_view()` - User login
- `register_view()` - User registration
- `dashboard()` - Home page with stats
- `cutoff_search()` - Search page
- `api_get_branches()` - Get branches for selected college (AJAX)
- `upload_pdf()` - Admin uploads cutoff PDF
- `pyq_list()` - List previous year questions

---

## **How URLs Work (urls.py)**

```python
urlpatterns = [
    path('login/', views.login_view, name='login'),
    # When user visits: http://localhost:8000/login/
    # Django calls: views.login_view()
    
    path('register/', views.register_view, name='register'),
    # When user visits: http://localhost:8000/register/
    # Django calls: views.register_view()
    
    path('cutoff-search/', views.cutoff_search, name='cutoff_search'),
    # When user visits: http://localhost:8000/cutoff-search/
    # Django calls: views.cutoff_search()
]
```

---

## **Database Queries Example**

### **Python Code:**
```python
# Find all colleges
colleges = College.objects.all()

# Find cutoffs for a specific college
cutoffs = Cutoff.objects.filter(college__name="BMS College")

# Find cutoffs for CS branch in 2023
cs_cutoffs = Cutoff.objects.filter(
    branch__name="Computer Science",
    year__year=2023
)
```

### **What Happens:**
```
Your Python code
    ↓
Django converts to SQL query
    ↓
SQLite database executes
    ↓
Results returned as Python objects
    ↓
You can display in template
```

---

## **PDF Parser Flow (pdf_parser.py)**

```python
# 1. Open PDF file
pdf = pdfplumber.open('cutoffs.pdf')

# 2. Read all 45 pages
for page in pdf.pages:
    text = page.extract_text()
    
    # 3. Extract college name
    college_name = extract_college_name(text)
    
    # 4. Extract branches
    branches = extract_branches(text)
    
    # 5. Extract cutoff ranks
    ranks = extract_ranks(text)

# 6. Save to database
College.objects.create(name=college_name, ...)
Branch.objects.create(name=branch_name, ...)
Cutoff.objects.create(college=..., branch=..., rank=...)
```

---

## **Frontend - How Pages Work**

### **base.html** (Master Template)
- Contains navbar, footer, CSS styling
- All other templates **extend** this
- Changes here affect all pages

### **login.html** (Login Page)
```html
{% extends "base.html" %}
<form method="post">
    <input type="text" name="username">
    <input type="password" name="password">
    <button>Login</button>
</form>
```
- User enters credentials
- Form POSTs to `login_view()`
- Server validates & logs in user

### **dashboard.html** (Home Page)
- Shows stats: 308 colleges, branches, cutoffs
- Quick action buttons
- Dynamic content from database

### **cutoff_search.html** (Search Page)
```javascript
// When user selects college:
$('#college').change(function() {
    college_id = $(this).val()
    
    // AJAX request to server
    $.get('/api/get-branches/?college_id=' + college_id)
    .done(function(data) {
        // Fill branch dropdown
        $('#branch').html(data)
    })
})
```

---

## **Authentication Flow**

```
User visits /login/
    ↓
User enters username & password
    ↓
Server checks against User table
    ↓
If match:
    ├── Create session (stored in browser cookie)
    ├── User is now "authenticated"
    └── Can access protected pages
    
If no match:
    └── Show error message
```

---

## **Deployment Concept**

Right now: Running on **localhost:8000** (your computer)

To deploy online:
```
Your code + Database
    ↓
Upload to cloud server (PythonAnywhere, Heroku, etc.)
    ↓
Server runs: python manage.py runserver
    ↓
People access: saha-app.com
    ↓
Same code, accessible to everyone!
```

---

## **Key Technologies Explained**

| Technology | What it does | Example |
|------------|-------------|---------|
| **Django** | Web framework | Handles requests/responses |
| **SQLite** | Database | Stores all data |
| **pdfplumber** | PDF parsing | Extracts text from PDFs |
| **Bootstrap** | CSS framework | Makes it responsive & pretty |
| **JavaScript** | Frontend logic | Dynamic interactions (dropdowns) |
| **Git** | Version control | Tracks code changes |

---

## **Summary**

Your SAHA app follows the **Model-View-Template (MVT)** pattern:

```
Model (Database)
    ↓
    ← Data
    ↓
View (Python Logic)
    ↓
    ← HTML to display
    ↓
Template (HTML/CSS)
    ↓
Browser shows to user
    ↓
User interacts → Back to View → Loop!
```

**Simple Formula:**
```
User clicks → URL routes to View → View queries Model → 
Model returns data → View renders Template → 
Browser displays → User sees result
```

---

## **Want to Learn More?**

- **Models:** Define data structure
- **Views:** Handle business logic
- **Templates:** Display to users
- **URLs:** Route requests
- **Forms:** Validate user input
- **Middleware:** Process requests/responses

This is the Django framework! Once you understand these 6 concepts, you can build any web app! 🚀

