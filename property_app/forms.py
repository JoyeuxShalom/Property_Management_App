from django import forms
from .models import MaintenanceRequest
from django.contrib.auth.models import User

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['issue']
        widgets = {
            'issue': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the issue...'}),
        }

class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

