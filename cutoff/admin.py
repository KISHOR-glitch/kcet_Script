from django.contrib import admin
from .models import College, Branch, Category, Year, Round, Cutoff, PYQ, CutoffUploadLog


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'created_at']
    search_fields = ['name', 'city']
    ordering = ['name']


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'created_at']
    search_fields = ['code', 'description']
    ordering = ['code']


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ['year', 'created_at']
    ordering = ['-year']


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['name', 'round_number', 'created_at']
    search_fields = ['name']
    ordering = ['round_number']


@admin.register(Cutoff)
class CutoffAdmin(admin.ModelAdmin):
    list_display = ['college', 'branch', 'category', 'year', 'round', 'cutoff_rank']
    list_filter = ['year', 'round', 'college', 'category']
    search_fields = ['college__name', 'branch__name', 'category__code']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-year', 'college', 'branch']


@admin.register(PYQ)
class PYQAdmin(admin.ModelAdmin):
    list_display = ['subject', 'year', 'created_at']
    list_filter = ['year']
    search_fields = ['subject']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-year', 'subject']


@admin.register(CutoffUploadLog)
class CutoffUploadLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'total_rows', 'inserted_count', 'updated_count', 'uploaded_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['uploaded_by__username']
    readonly_fields = ['uploaded_file', 'status', 'total_rows', 'inserted_count', 'updated_count', 'error_message', 'uploaded_by', 'created_at']
    ordering = ['-created_at']
