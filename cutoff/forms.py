from django import forms
from .models import PYQ


class PDFUploadForm(forms.Form):
    """Form for uploading PDF files with cutoff data"""
    pdf_file = forms.FileField(
        label='Upload Cutoff PDF',
        widget=forms.FileInput(attrs={
            'accept': 'application/pdf',
            'class': 'form-control',
            'required': 'required'
        })
    )

    def clean_pdf_file(self):
        file = self.cleaned_data['pdf_file']
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        if file.size > 50 * 1024 * 1024:  # 50MB limit
            raise forms.ValidationError("File size exceeds 50MB limit.")
        return file


class PYQUploadForm(forms.ModelForm):
    """Form for uploading PYQ (Previous Year Question) papers"""
    
    class Meta:
        model = PYQ
        fields = ['subject', 'year', 'pdf_file']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject name'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control'
            }),
            'pdf_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf'
            })
        }
