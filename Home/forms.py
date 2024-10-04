# nirmaan_policy/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, FyersCredentials



# Profile Update Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,          # Limits the number of visible text lines
                'maxlength': 200,   # Sets a maximum number of characters
                'placeholder': 'Tell us about yourself (max 200 characters)...'
            }),
        }



# Fyers Credentials Form
class FyersCredentialsForm(forms.ModelForm):
    class Meta:
        model = FyersCredentials
        fields = ['ttop_key', 'client_id', 'secret_key', 'redirect_uri', 'response_type', 'state']
        widgets = {
            'ttop_key': forms.TextInput(attrs={'class': 'form-control'}),
            'client_id': forms.TextInput(attrs={'class': 'form-control'}),
            'secret_key': forms.PasswordInput(attrs={'class': 'form-control'}),
            'redirect_uri': forms.URLInput(attrs={'class': 'form-control'}),
            'response_type': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        # Add any additional validation if necessary
        return cleaned_data