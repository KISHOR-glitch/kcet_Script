from django.db import models
from django.core.validators import FileExtensionValidator


class College(models.Model):
    name = models.CharField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Branch(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='branches', null=True, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['college', 'name']]
        ordering = ['name']

    def __str__(self):
        return f"{self.college} - {self.name}"


class Category(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.code} - {self.description}"


class Year(models.Model):
    year = models.IntegerField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year']

    def __str__(self):
        return str(self.year)


class Round(models.Model):
    name = models.CharField(max_length=100, unique=True)
    round_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['round_number']

    def __str__(self):
        return self.name


class Cutoff(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='cutoffs')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='cutoffs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cutoffs')
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='cutoffs')
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='cutoffs')
    cutoff_rank = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['college', 'branch', 'category', 'year', 'round'],
                name='unique_cutoff'
            )
        ]
        ordering = ['-year', 'college', 'branch']

    def __str__(self):
        return f"{self.college} - {self.branch} ({self.category}) - {self.year} - {self.round}"


class PYQ(models.Model):
    subject = models.CharField(max_length=255)
    year = models.ForeignKey(Year, on_delete=models.CASCADE, related_name='pyqs')
    pdf_file = models.FileField(
        upload_to='pyqs/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['subject', 'year']]
        ordering = ['-year', 'subject']

    def __str__(self):
        return f"{self.subject} - {self.year}"


class CutoffUploadLog(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('partial', 'Partial'),
        ('failed', 'Failed'),
    ]

    uploaded_file = models.FileField(upload_to='uploads/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    total_rows = models.IntegerField(default=0)
    inserted_count = models.IntegerField(default=0)
    updated_count = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Upload {self.id} - {self.status}"

