# nirmaan_policy/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, UserData



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

# User Data Form
class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['text_input', 'voice_input', 'video_input']
        widgets = {
            'text_input': forms.Textarea(attrs={'rows': 4}),
        }
