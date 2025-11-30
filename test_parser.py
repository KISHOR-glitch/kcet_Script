#!/usr/bin/env python
"""Test the updated PDF parser"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kcet_project.settings')
django.setup()

from cutoff.utils.pdf_parser import PDFParser

pdf_path = 'media/uploads/KCET-Round-2-Cutoff.pdf'

print("Testing PDF Parser...")
parser = PDFParser(pdf_path)
success, result = parser.parse()

print(f"\nSuccess: {success}")
print(f"Total rows extracted: {result['total_rows']}")
print(f"Colleges found: {result['colleges_found']}")
print(f"Errors: {result['errors']}")

if result['extracted_data']:
    print(f"\nFirst 5 records:")
    for row in result['extracted_data'][:5]:
        print(f"  {row['college_name']} - {row['branch_name']} ({row['category_code']}): {row['cutoff_rank']}")
    
    print(f"\nUnique colleges:")
    colleges = set((row['college_code'], row['college_name']) for row in result['extracted_data'])
    for code, name in sorted(colleges):
        print(f"  {code}: {name}")
    
    print(f"\nSample branches for first college:")
    first_college = result['extracted_data'][0]['college_code']
    branches = set(row['branch_name'] for row in result['extracted_data'] if row['college_code'] == first_college)
    for branch in sorted(branches):
        print(f"  - {branch}")
