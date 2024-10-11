from django import forms
from .models import FyersCredentials 
 

class FyersCredentialsForm(forms.ModelForm):
    class Meta:
        model = FyersCredentials
        fields = ['client_id', 'secret_key', 'redirect_uri', 'response_type', 'state']
        widgets = {
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