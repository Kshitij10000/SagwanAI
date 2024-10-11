# nirmaan_policy/forms.py

from django import forms
from .models import Profile
from PaperTrade.models import Order



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



