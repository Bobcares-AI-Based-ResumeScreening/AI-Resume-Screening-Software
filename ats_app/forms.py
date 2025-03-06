from django import forms
from .models import ResumeUpload

class ResumeForm(forms.ModelForm):
    class Meta:
        model = ResumeUpload
        fields = ['resume']
