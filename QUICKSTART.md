# Quick Start Guide - KCET Cutoff System

## ⚡ 5-Minute Setup

### 1. Navigate to Project
```bash
cd c:\Users\kisho\OneDrive\Desktop\kcet_Script
```

### 2. Create Superuser
```bash
python manage.py createsuperuser
```

Example:
```
Username: admin
Email: admin@example.com
Password: (enter password)
```

### 3. Run Server
```bash
python manage.py runserver
```

### 4. Access the Application
- **Application**: http://127.0.0.1:8000/login/
- **Django Admin**: http://127.0.0.1:8000/admin/

---

## 📝 First Time Usage Checklist

### As Admin:
1. ✅ Login with superuser credentials
2. ✅ Go to Dashboard
3. ✅ Click "Upload Cutoff PDF" (admin dropdown)
4. ✅ Select a test PDF file
5. ✅ Choose Year and Round
6. ✅ Click "Upload & Process"
7. ✅ Verify data appears in cutoff search

### As Student:
1. ✅ Create a student account (optional - create via admin)
2. ✅ Login with student credentials
3. ✅ Go to "Search Cutoffs"
4. ✅ Select filters and search
5. ✅ Go to "PYQs" to view papers

---

## 📚 Sample PDF Creation

### Step 1: Create a sample PDF
Use Microsoft Word or Google Docs to create:

```
College: Sri Chaitanya College of Engineering, Bangalore

Course Name             | 1G    | 1K   | 1R    | 2AG   | 2AK  | 2AR   | 3BG  | 3BK | 3BR | 4G   | 4K  | 4R  | STG | STK | STR
B.Sc(Hons) Computer Sc | 1234  | --   | 5678  | 890   | --   | 2341  | 3456 | --  | 4567| 5678 | --  | 6789| --  | 7890| 8901
B.Sc(Hons) Electronics | 2345  | 3456 | 4567  | 1234  | 2345 | 3456  | 4567 | 5678| 6789| 7890 | 8901| 9012| 1234| 2345| 3456
B.Sc(Hons) Mechanical  | 3456  | 4567 | 5678  | 2345  | 3456 | 4567  | 5678 | 6789| 7890| 8901 | 9012| 1234| 2345| 3456| 4567
```

Save as PDF.

### Step 2: Upload PDF
1. Login as admin
2. Dashboard → Upload Cutoff PDF
3. Select the PDF
4. Choose Year: 2024, Round: Round 1
5. Click Upload & Process

---

## 🔍 Testing the System

### Test Cutoff Search:
1. After PDF upload, cutoff search will show data
2. Try filtering by college, branch, category, year, round
3. Verify cutoff ranks appear correctly

### Test PYQ Upload:
1. Dashboard → Upload PYQ
2. Subject: "Physics"
3. Year: 2024
4. Upload any PDF file
5. Go to PYQs to verify download

---

## 🐛 Common Issues & Solutions

### Issue: "No PDF found after upload"
**Solution**: Check that:
- PDF has "College:" header
- Table has course names in first column
- Category codes are in header row (1G, 1K, 2AG, etc.)

### Issue: "Login not working"
**Solution**: 
- Verify superuser was created: `python manage.py shell`
- Then: `from django.contrib.auth.models import User; User.objects.all()`
- If empty, create again: `python manage.py createsuperuser`

### Issue: "Static files not loading"
**Solution**:
```bash
python manage.py collectstatic --noinput
```

### Issue: "Database locked"
**Solution**: Restart server
```bash
# Ctrl+C to stop server
python manage.py runserver
```

---

## 📊 Creating Test Data

### Via Django Shell:
```bash
python manage.py shell
```

Then:
```python
from cutoff.models import *

# Create college
college = College.objects.create(name="Test College", city="Bangalore")

# Create branch
branch = Branch.objects.create(name="Computer Science")

# Create year
year = Year.objects.create(year=2024)

# Create round
round = Round.objects.create(name="Round 1", round_number=1)

# Create category (already created by populate_data)
category = Category.objects.get(code="1G")

# Create cutoff
cutoff = Cutoff.objects.create(
    college=college,
    branch=branch,
    category=category,
    year=year,
    round=round,
    cutoff_rank="1234"
)

print("Test data created successfully!")
```

---

## 🚀 Production Deployment

### Before Going Live:
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set up environment variables for `SECRET_KEY`
5. Configure proper file storage (AWS S3 recommended)
6. Enable HTTPS
7. Run: `python manage.py check --deploy`

---

## 📞 Commands Reference

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
python manage.py collectstatic --noinput

# Run tests
python manage.py test

# Create backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

---

## 📧 Adding More Admin Users

```bash
python manage.py createsuperuser
```

Or via Django Shell:
```python
from django.contrib.auth.models import User

# Create staff user (not superuser)
user = User.objects.create_user(
    username='staff_user',
    email='staff@example.com',
    password='staffpassword'
)
user.is_staff = True
user.save()
```

---

## ✅ Verification Checklist

- [ ] Server running without errors
- [ ] Can login with admin credentials
- [ ] Dashboard loads with statistics
- [ ] Can upload test PDF
- [ ] Cutoff search shows results
- [ ] PYQ upload works
- [ ] Django admin accessible at /admin/

---

**Congratulations! Your KCET Cutoff System is ready to use! 🎉**

For more details, see README.md
