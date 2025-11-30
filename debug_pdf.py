#!/usr/bin/env python
"""Debug PDF parsing"""
import os
import sys
import django
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kcet_project.settings')
django.setup()

import pdfplumber

# Path to your PDF (adjust as needed)
pdf_path = 'media/uploads/KCET-Round-2-Cutoff.pdf'  # Change this to your actual PDF path

if not os.path.exists(pdf_path):
    print(f"PDF not found at {pdf_path}")
    print("Checking media directory...")
    import glob
    pdfs = glob.glob('media/**/*.pdf', recursive=True)
    print(f"Found PDFs: {pdfs}")
    sys.exit(1)

# Extract text from PDF
print("Reading PDF...")
with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    
    full_text = ""
    for page_num in range(min(3, len(pdf.pages))):
        print(f"\n--- PAGE {page_num + 1} ---")
        text = pdf.pages[page_num].extract_text() or ""
        print(text[:500])  # Print first 500 chars
        full_text += text + "\n"

# Try to find college codes and names
print("\n\n--- ANALYSIS ---")
import re
college_codes = re.findall(r'E\d{3}', full_text)
print(f"College codes found: {set(college_codes)}")

# Look for college name patterns
lines = full_text.split('\n')
print(f"\nTotal lines: {len(lines)}")

print("\nFirst 20 lines:")
for i, line in enumerate(lines[:20]):
    print(f"{i}: {line}")
