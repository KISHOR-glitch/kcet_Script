#!/usr/bin/env python
"""Clear all data from College, Branch, and Cutoff models"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kcet_project.settings')
django.setup()

from cutoff.models import College, Branch, Cutoff

# Delete all data
Cutoff.objects.all().delete()
Branch.objects.all().delete()
College.objects.all().delete()

print('✓ Database cleared successfully')
print(f'  Colleges: {College.objects.count()}')
print(f'  Branches: {Branch.objects.count()}')
print(f'  Cutoffs: {Cutoff.objects.count()}')
